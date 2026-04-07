#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────
# apply-fictional-names.sh
#
# Orchestrator: re-apply all fictional name replacements to the workspace
# after ingesting a new source update. Uses the Java MassReplacer for
# heavy string replacement and Python scripts for context-aware passes.
#
# Usage:
#   ./update-ingestion/tools/apply-fictional-names.sh              # dry run
#   ./update-ingestion/tools/apply-fictional-names.sh --apply      # apply
#   ./update-ingestion/tools/apply-fictional-names.sh --java-only  # only Java mass replace
#   ./update-ingestion/tools/apply-fictional-names.sh --py-only    # only Python passes
# ─────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
REFERENCES="$SCRIPT_DIR/../references"
TOOLS="$SCRIPT_DIR"

MODE="dry"
RUN_JAVA=true
RUN_PYTHON=true

for arg in "$@"; do
    case "$arg" in
        --apply)     MODE="apply" ;;
        --java-only) RUN_PYTHON=false ;;
        --py-only)   RUN_JAVA=false ;;
        --help|-h)
            echo "Usage: $0 [--apply] [--java-only] [--py-only]"
            echo "  --apply      Actually modify files (default: dry run)"
            echo "  --java-only  Only run Java mass replacer"
            echo "  --py-only    Only run Python context-aware passes"
            exit 0 ;;
        *) echo "Unknown arg: $arg"; exit 1 ;;
    esac
done

echo "════════════════════════════════════════════════════════"
echo "  Fictional Name Re-Application Pipeline"
echo "  Mode: $([ "$MODE" = "apply" ] && echo "APPLY" || echo "DRY RUN")"
echo "  Project: $PROJECT_ROOT"
echo "════════════════════════════════════════════════════════"
echo

cd "$PROJECT_ROOT"

# ── Step 0: Pre-flight cleanup ─────────────────────────────────────
echo "── Step 0: Pre-flight cleanup"
echo "   Deleting images in docs/**/media/ and docs/**/prints/ ..."
find docs -type d \( -name media -o -name prints \) -exec find {} -type f -delete \;
find logs -type d -name media -exec find {} -type f -delete \; 2>/dev/null || true

echo "   Deleting old .html in docs/maps/ (keeping most recent) ..."
LATEST_MAP=$(ls -d docs/maps/*/ 2>/dev/null | sort | tail -1)
if [ -n "$LATEST_MAP" ]; then
    for html_file in $(find docs/maps -name '*.html' -type f 2>/dev/null); do
        html_dir="$(dirname "$html_file")/"
        if [ "$html_dir" != "$LATEST_MAP" ]; then
            rm -f "$html_file"
            echo "     Deleted: $html_file"
        else
            echo "     Kept:    $html_file"
        fi
    done
fi
echo

# ── Step 1: Java mass replacement (fast, O(n) per file) ───────────
if [ "$RUN_JAVA" = true ]; then
    echo "── Step 1: Java mass replacement"
    REPLACEMENTS_JSON="$REFERENCES/all-replacements-merged.json"

    if [ ! -f "$REPLACEMENTS_JSON" ]; then
        echo "   ERROR: $REPLACEMENTS_JSON not found"
        exit 1
    fi

    # Compile if needed
    CLASS_FILE="$TOOLS/MassReplacer.class"
    JAVA_SRC="$TOOLS/MassReplacer.java"
    if [ ! -f "$CLASS_FILE" ] || [ "$JAVA_SRC" -nt "$CLASS_FILE" ]; then
        echo "   Compiling MassReplacer.java ..."
        javac "$JAVA_SRC"
    fi

    JAVA_ARGS=("$REPLACEMENTS_JSON" "$PROJECT_ROOT")
    [ "$MODE" = "apply" ] && JAVA_ARGS+=("--apply")

    echo "   Running MassReplacer ..."
    (cd "$TOOLS" && java MassReplacer "${JAVA_ARGS[@]}")
    echo
fi

# ── Step 2: Python context-aware passes ───────────────────────────
if [ "$RUN_PYTHON" = true ]; then
    PYTHON="${PROJECT_ROOT}/.venv/bin/python3"
    if [ ! -x "$PYTHON" ]; then
        PYTHON="python3"
    fi

    PY_ARGS=""
    [ "$MODE" = "apply" ] && PY_ARGS="--apply"

    echo "── Step 2a: Pass 1 — Artist ID + Track Filename replacement"
    $PYTHON scripts/apply_fictional_names.py $PY_ARGS 2>&1 | tail -5
    echo

    echo "── Step 2b: Pass 2 — Keyword Scrub (song titles, game/anime refs)"
    $PYTHON scripts/apply_keyword_scrub.py $PY_ARGS 2>&1 | tail -5
    echo

    echo "── Step 2c: Pass 3 — Remaining artist names + concat forms"
    $PYTHON scripts/apply_third_pass.py $PY_ARGS 2>&1 | tail -5
    echo
fi

# ── Step 3: Verification ──────────────────────────────────────────
echo "── Step 3: Verification"
echo "   Running flake8 ..."
"${PROJECT_ROOT}/.venv/bin/python3" -m flake8 scripts/ --max-line-length=120 --count 2>&1 || true
echo "   Running mypy ..."
"${PROJECT_ROOT}/.venv/bin/python3" -m mypy scripts/*.py --ignore-missing-imports 2>&1 || true
echo

echo "════════════════════════════════════════════════════════"
echo "  Pipeline complete."
if [ "$MODE" != "apply" ]; then
    echo "  This was a DRY RUN. Use --apply to execute."
fi
echo "════════════════════════════════════════════════════════"
