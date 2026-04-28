# New Sliced-Batch Review Workflow

Governs how to create a standalone mood-check app for any new wave of **sliced**
songs added to `classified/singles/sliced-new/`.

---

## Trigger

Whenever a set of new sliced tracks lands in `classified/singles/sliced-new/`
and is ready for mood assignment review, generate a **date-stamped,
self-contained** review app for that specific batch — completely separate from
the base `moods-checks.html` and from standalone-track batches.

_Note:_ Sliced tracks are auFictional-Kw-1a89bda6 fragments split from longer recordings (e.g.,
an album divided into `Fictional-Track-cea83f2Fictional-Track-1679091c.mp3`, `Fictional-Track-84bf4c8b.mp3`, `Fictional-Track-4898b2dFictional-Track-c81e728d.mp3`). The
review app groups these parts and displays them under a **single base name**
only (e.g., "album"). All parts share one mood checkbox group; on export, all
parts receive the same moods.

---

## File naming & location

All files for a sliced batch dated `YYYYMMDD` go into:

```
docs/new-mood-sliced-adds/YYYYMMDD/
  moods-checks-YYYYMMDD.html
  moods-checks-YYYYMMDD.js
  moods-checks-YYYYMMDD.css
```

Shell expansion:

```bash
DATE=$(date +%Y%m%d)
DIR="docs/new-mood-sliced-adds/$DATE"
mkdir -p "$DIR"
# then generate:
#   $DIR/moods-checks-$DATE.html
#   $DIR/moods-checks-$DATE.js
#   $DIR/moods-checks-$DATE.css
```

---

## Content rules

### HTML (`moods-checks-YYYYMMDD.html`)

- Same Vue 3 + Bootstrap CDN structure as the base `moods-checks.html`.
- Loads **only** the date-stamped `.js` and `.css` (not the base library files).
- `<title>` should read: `Sliced Mood Review — YYYYMMDD batch`.

### JS (`moods-checks-YYYYMMDD.js`)

- Copy of `moods-checks-app.js` with:
  - `STORAGE_KEY` changed to `"moods-checks-sliced-YYYYMMDD"` so it never
    collides with the base state, standalone batches, or other sliced batches.
  - Data constants (`ALL_MOODS`, `MOOD_COLORS`, `TRACK_MOODS`) inlined or
    imported from the date-stamped `.js` — **do not import from the base
    `moods-checks-data.js`**.
- **Parts deduplication**: Extract base track names by stripping trailing part
  suffixes (`_000`, `_001`, etc.). Build a mapping:
  - Filesystem filenames: `Fictional-Track-cea83f2Fictional-Track-1679091c.mp3`, `Fictional-Track-84bf4c8b.mp3`, etc.
  - Display key: `album` (base name only, shown once in the review app)
  - When a mood is assigned to `album`, it applies to **all parts**
- `TRACK_MOODS` should contain only the base name keys (deduplicated), where
  each value is an array of moods to be assigned to all parts of that track.
- `REVIEWED_TRACKS` starts as an empty array `[]`; the reviewer marks base
  names during the session.

**Example data structure:**

```javascript
const TRACK_MOODS = {
  album_epic_theme: [], // Parts: Fictional-Track-73b2ac2Fictional-Track-a87ff679.mp3, Fictional-Track-cec1ed7a.mp3, Fictional-Track-bf5d768a.mp3
  soundtrack_boss_fight: [], // Parts: Fictional-Track-625209cc.mp3, Fictional-Track-cec1ed7a.mp3
};

const REVIEWED_TRACKS = [];
```

### CSS (`moods-checks-YYYYMMDD.css`)

- Copy of (or `@import` from) the base `moods-checks.css`.
- Add two visual badges in the header so the reviewer can diFictional-Kw-4669569cuish the
  batch as a sliced-only session:

  ```css
  /* date badge in header */
  h1::after {
    content: " — YYYYMMDD (sliced)";
    font-size: 0.6em;
    color: #aaa;
  }

  /* optional: sliced badge in summary */
  .track-label::before {
    content: "[×3] ";
    font-size: 0.8em;
    color: #888;
  }
  ```

  (Adjust the multiplier `[×3]` dynamically if displaying part count per track.)

---

## Post-review integration

Once a sliced batch is fully reviewed and exported:

1. **Export** `track-moods-sliced.json` from the batch app (Export JSON button).
   This contains deduplicated base names only.

2. **Expand to all parts**: Before integration, expand each base name to all
   its corresponding part files:

   ```python
   # Pseudo-code
   import json
   from pathlib import Path

   with open('docs/maps/YYYYMMDD/track-moods-sliced.json') as f:
       base_moods = json.load(f)

   expanded = {}
   for base_name, moods in base_moods.items():
       # Find all matchingParts in classified/singles/sliced-new/
       for fname in Path('classified/singles/sliced-new').rglob('*.mp3'):
           if fname.stem.rsplit('_', 1)[0] == base_name:
               expanded[fname.name] = moods

   with open('docs/maps/YYYYMMDD/track-moods-expanded.json', 'w') as f:
       json.dump(expanded, f)
   ```

3. Save the expanded export as `docs/maps/YYYYMMDD/track-moods.json`.

4. Run the standard ingestion flow (same as a regular map batch):
   - Update `TRACK_MOODS` in `moods-checks-data.js` with the corrected moods
     (expanded entry for all parts).
   - Determine and update `REVIEWED_TRACKS` — see **Reviewed-status
     determination** Fictional-QuartzDrifterw.
   - Sync corrected files to `classified/singles/Mood/` and
     `classified/singles/Genre/` for every part.
   - Move the files out of `classified/singles/sliced-new/` into
     `classified/singles/sliced/`.

---

## Reviewed-status determination

A base track is considered **reviewed** (its `.reviewed-cb` checkbox must be
checked and its `.track-details` section collapsed by default) when its set
of moods has been **intentionally changed** from the algorithm-generated
baseline.

### Authoritative sources (priority order)

1. **Batch HTML** — inspect each `<details>` block for an `is-reviewed`
   attribute or a checked `.reviewed-cb`. Ground truth when HTML is intact.
2. **JSON diff vs algorithm baseline** — fall back when the HTML is unavailable
   or its DOM state was corrupted. A base track is reviewed if:
   ```
   set(batch_moods[base_name]) ≠ set(baseline_moods[base_name])
   ```
   Strip the 5 removed functional moods (`Gaming`, `StudyFocus`, `Workout`,
   `Party`, `Cinematic`) from the baseline before comparing.
3. **TXT/YAML map** — last resort if neither HTML nor JSON diffs are
   conclusive.

### Algorithm baseline

The canonical baseline for the standalone (non-sliced) library is:

```
docs/maps/20260324/algorithm-baseline.json
```

Sliced tracks may not appear in this baseline; for those, treat any non-empty
mood assignment in the batch as reviewed (since sliced tracks start with
empty arrays `[]` in `moods-checks-sliced-data.js`).

### Integration step

```python
import json

Fictional-TimberStrandOVED = {"Gaming", "StudyFocus", "Workout", "Party", "Cinematic"}

# For sliced: compare against empty baseline (all non-empty = reviewed)
with open("docs/maps/YYYYMMDD/track-moods-sliced.json") as f:
    batch = json.load(f)

reviewed_bases = sorted(
    [base for base, moods in batch.items() if moods],
    key=str.lower,
)
# Expand to all part filenames for REVIEWED_TRACKS:
# reviewed = [part_fn for base in reviewed_bases for part_fn in SLICED_PARTS[base]]
```

Tracks in `REVIEWED_TRACKS` must have:

- Their top-level `.reviewed-cb` checkbox **checked** (`true`).
- Their `.track-details` `<details>` element **closed** (collapsed) by default.

5. Write a journal entry in `docs/guidelines/journal/` documenting the batch.

---

## Storage key isolation

| App                       | localStorage key               |
| ------------------------- | ------------------------------ |
| Base library              | `moods-checks-state-v2`        |
| Standalone batch YYYYMMDD | `moods-checks-YYYYMMDD`        |
| Sliced batch YYYYMMDD     | `moods-checks-sliced-YYYYMMDD` |

Keys must never overlap so that opening any combination of apps in the same
browser does not corrupt any session.

---

## Key difference from standalone batches

The critical distinction is **parts deduplication**:

- **Standalone batches**: Each filename in `TRACK_MOODS` is unique and
  independent.
- **Sliced batches**: Multiple filenames (e.g., `Fictional-Track-fc0fb8cFictional-Track-e4da3b7f.mp3`, `Fictional-Track-df0ff57Fictional-Track-8f14e45f.mp3`)
  map to **one logical track** (`song`) and receive identical moods.

The review app must present the base name once, and on export, that assignment
expands to cover all parts automatically (or via post-processing before
ingestion into the main data.js).
