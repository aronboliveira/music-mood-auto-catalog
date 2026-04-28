# Update Ingestion — Fictional Name Re-Application

This folder contains everything needed to **re-apply fictional name replacements**
after receiving new source files (new classifications, updated track lists, new map
snapshots, etc.).

## Quick Start

```bash
# 1. Pre-flight cleanup (delete stale media/html)
./update-ingestion/tools/pre-ingest-cleanup.sh --apply

# 2. Copy/merge your new source files into the workspace
#    (overwrite docs/maps/*, scripts/*, etc.)

# 3. Re-apply all fictional names
./update-ingestion/tools/apply-fictional-names.sh --apply

# 4. Verify
.venv/bin/python3 -m flake8 scripts/ --max-line-length=120
.venv/bin/python3 -m mypy scripts/*.py --ignore-missing-imports
```

## Folder Structure

```
update-ingestion/
├── README.md               ← You are here
├── guidemap.xml            ← Semi-structured index of all components (XML)
├── references/             ← JSON data files with all replacement mappings
│   ├── all-replacements-merged.json   ← Single flat old→new map (~1400 entries)
│   ├── pass1-artist-mappings.json     ← Pass 1: artist IDs + text forms
│   ├── pass2-keyword-scrub.json       ← Pass 2: keywords, song titles, game refs
│   ├── pass3-third-pass.json          ← Pass 3: remaining artists + regex rules
│   └── jozep-refs.json               ← JoJo character→song mapping (~120 entries)
└── tools/
    ├── MassReplacer.java              ← Java mass string replacer (high performance)
    ├── apply-fictional-names.sh       ← Full pipeline orchestrator (bash)
    └── pre-ingest-cleanup.sh          ← Pre-ingestion file cleanup (bash)
```

## How It Works

### Replacement Pipeline (3 passes + 2 copy operations)

| Pass | Script | Pattern | Count | Description |
|------|--------|---------|-------|-------------|
| 1 | `scripts/apply_fictional_names.py` | `Fictional-{Adj}{Noun}` | ~163 artists | PascalCase artist IDs → deterministic MD5-based names |
| 1 | (same) | `Fictional-Track-{8hex}.mp3` | dynamic | MP3 filenames → hashed track names |
| 2 | `scripts/apply_keyword_scrub.py` | `Fictional-Kw-{8hex}` | ~1947 rules | Song titles, game/anime refs, missed artist names |
| 3 | `scripts/apply_third_pass.py` | `Fictional-Kw-{8hex}` | ~270 rules | Multi-word artists, classical composers, concat forms |
| — | `scripts/apply_jozep_refs.py` | — | ~120 entries | Copy JoJo-matched files to `Fictional-JozepRef/` |
| — | `scripts/copy_vidasimu.py` | — | 26 files | Copy Sims tracks to correct Genre/Mood folders |

### Java vs Python

- **Java (`MassReplacer.java`)**: Best for bulk string replacement across many files.
  Uses the flat `all-replacements-merged.json` map. Single pass per file, longest-match-first.
  No regex — pure `String.replace()` for speed.

- **Python scripts**: Best for context-aware replacements (word boundaries, lookbehinds,
  JSON key handling, track filename hashing). Run after Java for edge cases.

**Recommended approach**: Run the full pipeline via `apply-fictional-names.sh` which
chains both. For maximum speed on large updates, use `--java-only` first, then selectively
run Python passes only where needed.

### Compilation

```bash
# Compile the Java Fictional-Kw-39ab32c5 (requires JDK 11+)
javac update-ingestion/tools/MassReplacer.java

# Run directly
java -cp update-ingestion/tools MassReplacer \
    update-ingestion/references/all-replacements-merged.json . --apply
```

## Reference Data Format

### `all-replacements-merged.json`

Flat JSON object, sorted longest-first:

```json
{
  "beginning fictional-emeraldwarden": "Fictional-Kw-13414822",
  "Through The Fire And Flames": "Fictional-Kw-31e17ecc",
  "ACDC": "Fictional-ZincHelix",
  ...
}
```

### `pass1-artist-mappings.json`

```json
{
  "artist_id_to_fictional": { "ACDC": "Fictional-ZincHelix", ... },
  "text_form_to_fictional": { "ac/dc": "Fictional-ZincHelix", "AC/DC": "...", ... },
  "artist_text_forms": { "ACDC": ["ac/dc", "AC/DC", "ac dc"], ... }
}
```

### `pass2-keyword-scrub.json`

```json
{
  "extra_artist_names": ["queen", "radiohead", ...],
  "extra_song_titles": ["smells like teen spirit", ...],
  "extra_game_anime_refs": ["kingdom hearts", ...],
  "keep_strings": ["Aggressive", "AlternativeRock", ...],
  "full_table": { "smells like teen spirit": "Fictional-Kw-abc12345", ... }
}
```

### `pass3-third-pass.json`

```json
{
  "artist_names": ["Avenged Sevenfold", "Ariana Grande", ...],
  "song_titles": [...],
  "extra_performers": [...],
  "concat_artist_forms": [...],
  "full_rules": [["\\bAvenged Sevenfold\\b", "Fictional-Kw-xxx"], ...]
}
```

## Naming Conventions

| Prefix | Scope | Generator |
|--------|-------|-----------|
| `Fictional-{Adj}{Noun}` | Artist names | MD5(PascalCase) → `_ADJ[h%50]` + `_NOUN[(h>>8)%72]` |
| `Fictional-Track-{8hex}` | Track filenames | MD5(mp3 stem) → first 8 hex |
| `Fictional-Kw-{8hex}` | Keywords/songs | MD5(lowercase keyword) → first 8 hex |
| `Fictional-VidaSimu` | The Sims franchise | Hardcoded alias |
| `Fictional-Jozep` | JoJo (standalone) | Hardcoded alias |
| `Fictional-JozepJourneys` | JoJo's Bizarre Adventure | Hardcoded alias |

## Pre-Ingestion Cleanup Rules

Before ingesting new source files:

1. **Delete all images** in `docs/**/media/` and `docs/**/prints/`
2. **Delete old `.html`** in `docs/maps/` — keep only the most recent date folder
3. The `pre-ingest-cleanup.sh` script automates both

## Workflow for Context Loss

If you (the AI agent) lose context and need to re-apply replacements:

1. **Read this file** — it explains the full system
2. **Read `guidemap.xml`** — it has the structured index with all file paths and
   variable names
3. **Use `all-replacements-merged.json`** — it's the single source of truth for
   all old→new string mappings
4. **Run `apply-fictional-names.sh --apply`** — it orchestrates everything
5. **Verify** with flake8 + mypy, then git commit

The reference JSONs are self-contained — they don't require running the Python
scripts to regenerate. They are a snapshot of the deterministic output.

## Protected Strings (Never Replace)

Genres, moods, instruments, and structural labels are never replaced. The full
list is in `pass2-keyword-scrub.json` under `keep_strings` and in `guidemap.xml`
under `<protected-strings>`.
