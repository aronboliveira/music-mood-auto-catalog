#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────
# pre-ingest-cleanup.sh
#
# Run BEFORE ingesting new source files. Removes stale artifacts:
# - Images in docs/**/media/ and docs/**/prints/
# - Old .html files in docs/maps/ (keeps only the most recent date folder)
# - Logs media files
#
# Usage:
#   ./update-ingestion/tools/pre-ingest-cleanup.sh           # dry run
#   ./update-ingestion/tools/pre-ingest-cleanup.sh --apply   # delete
# ─────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

MODE="dry"
[ "${1:-}" = "--apply" ] && MODE="apply"

echo "=== Pre-Ingest Cleanup ($([ "$MODE" = "apply" ] && echo "APPLY" || echo "DRY RUN")) ==="
echo "Project: $PROJECT_ROOT"
echo

cd "$PROJECT_ROOT"

DELETED=0

# ── Media and prints directories ──────────────────────────────────
echo "── Images in docs/**/media/ and docs/**/prints/"
for f in $(find docs logs -type f \( -path '*/media/*' -o -path '*/prints/*' \) 2>/dev/null); do
    echo "  $([ "$MODE" = "apply" ] && echo "DELETE" || echo "WOULD DELETE"): $f"
    [ "$MODE" = "apply" ] && rm -f "$f" && DELETED=$((DELETED + 1))
done

# ── Old HTML in docs/maps/ ────────────────────────────────────────
echo
echo "── Old .html files in docs/maps/ (keeping most recent date folder)"
LATEST_MAP=$(ls -d docs/maps/*/ 2>/dev/null | sort | tail -1)
echo "   Most recent map folder: ${LATEST_MAP:-none}"

if [ -n "$LATEST_MAP" ]; then
    for html_file in $(find docs/maps -name '*.html' -type f 2>/dev/null | sort); do
        html_dir="$(dirname "$html_file")/"
        if [ "$html_dir" != "$LATEST_MAP" ]; then
            echo "  $([ "$MODE" = "apply" ] && echo "DELETE" || echo "WOULD DELETE"): $html_file"
            [ "$MODE" = "apply" ] && rm -f "$html_file" && DELETED=$((DELETED + 1))
        else
            echo "  KEEP: $html_file"
        fi
    done
fi

echo
echo "--- Summary ---"
if [ "$MODE" = "apply" ]; then
    echo "Deleted: $DELETED files"
else
    echo "This was a DRY RUN. Use --apply to execute."
fi
