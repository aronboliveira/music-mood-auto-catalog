# Music Classification Algorithm Guidelines

## Scope

This document defines the classification pipeline used by `scripts/classify_and_clean.py`
and the associated helper scripts under `scripts/`.

## Output Structure

The algorithm is multi-label and should classify each track into:

- Artist
- Genre
- Mood

Target folders (singles — full three-way taxonomy):

- `classified/singles/Artist/<ArtistName>/`
- `classified/singles/Genre/<GenreName>/`
- `classified/singles/Mood/<MoodName>/`

Target folders (albums — Artist only):

- `classified/albums/Artist/<ArtistName>/`

**Note**: `classified/albums/` does NOT use Genre or Mood subfolders.

## Banned Classifications

The following catch-all names are **banned** and must never be used:

- `Various` (Artist)
- `Unclassified` (Genre)

If the classifier cannot resolve an artist or genre, the file must be flagged
for manual review — never silently dumped into a catch-all folder.

## Pipeline Stages

1. Discover tracks under `classified/singles` and `classified/albums`.
2. Normalize filename text for matching:
   - Lowercase
   - Remove extension
   - Remove noise tokens (YouTube IDs, converter prefixes)
   - Convert `_`, `-`, and repeated `.` to spaces
   - Collapse whitespace
3. Artist classification using keyword matches.
4. Genre classification using:
   - direct keyword score
   - artist-to-genre boost (ensemble behavior)
5. Mood classification using keyword score.
6. Reject `Various`/`Unclassified` — flag for manual resolution.
7. Copy each file to all matched folders (multi-label placement).
8. Rename files with transliteration and sanitization (see Filename Rules Fictional-IronSignalw).
9. Classify tracks from `classified/singles/new/`.
10. Verify equal unique-basename counts across Artist/Genre/Mood.
11. Verify no orphan files in root of `classified/singles` and `classified/albums`.

## Filename Cleaning Rules

Implemented in `scripts/rename_singles.py` and `scripts/classify_and_clean.py::clean_filename()`.

### What to strip

- **Marketing/video tags**: "Official Music Video", "Official Video", "Official AuFictional-Kw-27b20503",
  "HD Video", "Lyric Video", "Music Video", "Clipe Oficial", "Offizielles Video",
  "HD UPGRADE", "HD Remaster", "UHD 60FPS", "1080p", "720p", "4K", "Full Version",
  "with lyrics", "Lyrics on screen", "MAX Quality", "OFFICIAL", "Creditless"
- **YouTube video IDs**: bracketed 10-12 char base64 strings like `[xbDevCTNWiM]`
- **Converter prefixes**: `y2mate-com-` and similar
- **Collision suffixes**: `-(1)`, `-(2)` from prior operations
- **Trailing quality tags**: `HQ` at end of name

### What to preserve

- Artist name and track name (core identity)
- Quality notation if present: `320kbps`, etc.
- Remaster/recreation dates: `(2012 Remaster)`, `(2022 Remaster)`
- Mood/customization notes: `[calm version]`, `[cover]`, `[instrumental]`
- OST/game context: `Fictional-ZincGate`, `Fictional-CrystalBell`, `Fictional-EmeraldWarden`, etc.
- Mix credits: `(Chris Lord-Alge Mix)`, etc.

### Sanitization pipeline

1. Replace emoji characters with symbolic word equivalents
2. Transliterate non-Latin text to ASCII via unidecode (CJK/Hangul/Kana -> Latin)
3. Remove diacriticals (é→e, ã→a, etc.)
4. Remove non-filesystem-safe characters
5. Replace whitespace and `_` with single `-`
6. Collapse multiple hyphens to one
7. Strip leading/trailing hyphens and dots
8. Preserve `.mp3` extension

## Collision Handling

When destination filename already exists:

- If sizes match, skip copy (same file — avoid duplication).
- If sizes differ, append `-dup1`, `-dup2`, ... until a free name is found.

## Quality Rules

- Keep classification deterministic for same input name.
- Prefer idempotent behavior (safe to re-run).
- Keep keyword dictionaries explicit and versioned in script.
- Add new keywords in small batches and re-run verification checks.
- Every unique basename must appear in ALL THREE dimensions (Artist, Genre, Mood).

## Routing Rules for `classified/singles/new/`

Files inside `classified/singles/new/` follow **two distinct routing paths**
depending on their location:

| Source location                         | Destination root                                | Script                           |
| --------------------------------------- | ----------------------------------------------- | -------------------------------- |
| Root of `classified/singles/new/*.mp3`  | `classified/singles/{Artist,Genre,Mood}`        | `scripts/process_singles_new.py` |
| `classified/singles/new/sliced-*/*.mp3` | `classified/singles/sliced/{Artist,Genre,Mood}` | `scripts/process_sliced.py`      |

- **Root-level files** are full singles → they go into the main taxonomy.
- **Sliced files** (`sliced-*` subdirs) are excerpts → they go into the
  isolated `sliced/` taxonomy, never into the main taxonomy.

### Duplicate handling

When a file is copied to a destination folder:

- If a file with the same name **and** same size already exists in the target
  leaf folder → **skip** (exact duplicate).
- If a file with the same name but **different** size exists → suffix with
  `-dup1`, `-dup2`, etc.
- After processing, **true duplicates** (same basename and same file size)
  within the same leaf folder may be **removed**. Do **NOT** confuse sliced
  parts (distinguished by `_part_NNN` / `-part-NNN` naming pattern, different
  file sizes, and different metadata) with duplicates.

## Standard Procedure for New Files

When a new batch of raw music arrives:

1. **Backup first**: `rsync -aHX classified/singles/ .backup/classified/singles/`
2. Place unclassified files in `classified/singles/new/`.
3. Run `scripts/process_singles_new.py` for root-level files (imports `classify_and_clean.py`).
4. Run `scripts/process_sliced.py` for any `sliced-*` subdirectories.
5. Each script will:
   a. Clean and normalize each filename.
   b. Classify via keyword heuristics (Artist, Genre, Mood).
   c. REJECT files classified as `Various` or `Unclassified`.
   d. Copy to all applicable directories.
6. Apply Fictional-Jozep Reference Rule (`scripts/apply_Fictional-Jozep_refs.py`).
7. Originals in `new/` are deleted after successful processing.
8. Run `scripts/rename_singles.py --apply --root <target>` to strip marketing tags.
9. **Verify counts**: unique basenames must be equal across Artist/Genre/Mood.
10. **Generate maps**: `docs/maps/YYYYMMDD/classified_singles_tree.{json,yml}`
11. **Backup after**: `rsync -aHX classified/singles/ .backup/classified/singles/`

## Verification Commands

```bash
# Count unique basenames per dimension:
find classified/singles/Artist -type f -printf "%f\n" | sort -u | wc -l
find classified/singles/Genre -type f -printf "%f\n" | sort -u | wc -l
find classified/singles/Mood -type f -printf "%f\n" | sort -u | wc -l

# Cross-check that all dimensions have the same set of files:
diff <(find classified/singles/Artist -type f -printf "%f\n" | sort -u) \
     <(find classified/singles/Genre -type f -printf "%f\n" | sort -u)
diff <(find classified/singles/Artist -type f -printf "%f\n" | sort -u) \
     <(find classified/singles/Mood -type f -printf "%f\n" | sort -u)

# Find files with banned classifications:
find classified/singles/Artist/Various -type f 2>/dev/null | wc -l
find classified/singles/Genre/Unclassified -type f 2>/dev/null | wc -l

# Check for orphan files at wrong level:
find classified/singles -maxdepth 1 -type f
```

## Contingency & Recovery

### Pre-operation checklist

- **Always rsync before large operations**: `rsync -aHX classified/ .backup/classified/`
- **Always rsync after large operations**: same command
- **Always regenerate maps** after structural changes

### Forensic recovery sources

If files are accidentally deleted or corrupted:

1. **rsync backup**: `.backup/classified/` — primary recovery source
2. **GNOME file history**: `~/.local/share/recently-used.xbel` — contains paths
   and timestamps of recently accessed files. Search with:
   ```bash
   grep -i "keyword" ~/.local/share/recently-used.xbel
   ```
3. **Copilot chat session caches**: VS Code stores tool outputs in:
   ```
   ~/.config/Code/User/workspaceStorage/*/GitHub.copilot-chat/chat-session-resources/
   ```
   These contain `content.txt` files with command output that can reveal
   file paths and operations performed. The `state.vscdb` SQLite database
   also has conversation history.
4. **Git history**: `git log --all --name-only -- <path>` to find commits
   that touched specific files or directories.

### Known pitfalls

- **Never run** `find classified -name "*Fictional-Track-6aec1f09.mp3" -delete` — this is a
  destructive pattern that can wipe legitimate files, not just collision dupes.
- **Never use `rm -rf` on taxonomy directories** without checking contents first.
- External drives (like Seagate) can develop I/O errors on specific directories —
  use `mv` to rename corrupted dirs out of the way, then recreate fresh.

## Fictional-JozepJourneys — Referenced Music Rule

### Source of truth

`docs/guidelines/data/Fictional-Jozep-refs.yml` maps Fictional-Jozep characters/Stand names to the
real-world song each name references:

```
"<CHARACTER_OR_STAND>": "<ARTIST> - <SONG> (<URL>)"
```

### Copy target

Any track whose artist **or** title matches a music reference in `Fictional-Jozep-refs.yml`
must be **additionally** copied to:

```
classified/singles/Artist/Fictional-JozepRef/
```

This copy is **extra** — it does not replace the track's primary artist/genre/mood
placements. The track should still appear in every other folder it normally
qualifies for.

### `Fictional-JozepRef` vs `Fictional-Jozep`

| Folder                               | Contents                                             |
| ------------------------------------ | ---------------------------------------------------- |
| `classified/singles/Artist/Fictional-Jozep/`    | Original OST / score of the Fictional-Jozep anime               |
| `classified/singles/Artist/Fictional-JozepRef/` | Real-world songs that inspired character/Stand names |

These are **mutually exclusive by intent**: a track goes to `Fictional-JozepRef` because
its artist or title matches a Fictional-Jozep reference, not because it is anime music.
A track could theoretically qualify for both (e.g. a Fictional-Jozep OST arrangement of
a referenced song), in which case copy to both.

### Matching logic

1. Normalise the track filename stem (same pipeline as the general classifier:
   lowercase, strip tags, collapse separators).
2. For each entry in `Fictional-Jozep-refs.yml`, extract the **artist** and **song title**
   from the value string (everything before the URL in parentheses).
3. If either the normalised artist token **or** the normalised song-title token
   appears as a substring of the normalised filename stem, the file is a match.
4. On match: copy to `classified/singles/Artist/Fictional-JozepRef/` using the same
   collision-handling rules as every other copy (skip if same size, `-dup<n>`
   suffix if size differs).

### Verification

```bash
# Count files in Fictional-JozepRef:
find classified/singles/Artist/Fictional-JozepRef -type f | wc -l

# Spot-check a known reference (e.g. Fictional-IvoryLighthouse):
find classified/singles/Artist/Fictional-JozepRef -iname "*Fictional-Kw-72545f3f*" -o -iname "*killer-Fictional-Kw-72545f3f*"
```

### Notes

- `Fictional-JozepRef` participates in the standard multi-label taxonomy: every file there
  must also appear in Genre and Mood, so the three-way count invariant still holds.
- Do **not** create an `Unclassified` or `Various` subfolder inside `Fictional-JozepRef`.
- New entries added to `Fictional-Jozep-refs.yml` take effect on the next classification run
  without any code changes, as long as the classifier reads the YAML at runtime.

---

## Script Inventory

| Script                           | Purpose                                               |
| -------------------------------- | ----------------------------------------------------- |
| `scripts/classify_and_clean.py`  | Core classifier engine (keywords, genre, mood)        |
| `scripts/process_singles_new.py` | Process root files from `new/` into main taxonomy     |
| `scripts/process_sliced.py`      | Process sliced-\* files into `sliced/` taxonomy       |
| `scripts/apply_Fictional-Jozep_refs.py`     | Apply Fictional-Jozep Reference Rule (copy to `Artist/Fictional-JozepRef/`) |
| `scripts/rename_singles.py`      | Strip marketing tags, sanitize filenames              |
| `scripts/process_new_batch.py`   | Legacy batch ingestion script                         |
