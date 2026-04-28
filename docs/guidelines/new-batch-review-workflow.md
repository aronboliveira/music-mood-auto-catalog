# New-Batch Review Workflow

Governs how to create a standalone mood-check app for any new wave of songs
added to `classified/singles/new/`.

---

## Trigger

Whenever a set of new songs lands in `classified/singles/new/` and is ready
for mood assignment review, generate a **date-stamped, self-contained** review
app for that specific batch — completely separate from the base
`moods-checks.html` that covers the full library.

_Note:_ This workflow is for **non-sliced individual tracks**. For sliced
tracks, use a separate workflow (see [Sliced-New Workflow](new-sliced-batch-review-workflow.md)).

---

## File naming & location

All files for a new batch dated `YYYYMMDD` go into:

```
docs/new-mood-adds/YYYYMMDD/
  moods-checks-YYYYMMDD.html
  moods-checks-YYYYMMDD.js
  moods-checks-YYYYMMDD.css
```

Shell expansion:

```bash
DATE=$(date +%Y%m%d)
DIR="docs/new-mood-adds/$DATE"
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
- `<title>` should read: `Mood Review — YYYYMMDD batch`.

### JS (`moods-checks-YYYYMMDD.js`)

- Copy of `moods-checks-app.js` with:
  - `STORAGE_KEY` changed to `"moods-checks-YYYYMMDD"` so it never collides
    with the base state or other batches.
  - Data constants (`ALL_MOODS`, `MOOD_COLORS`, `TRACK_MOODS`) inlined or
    imported from the date-stamped `.js` — **do not import from the base
    `moods-checks-data.js`**.
- `TRACK_MOODS` contains only the tracks in this batch (the files present in
  `classified/singles/new/` at generation time).
- `REVIEWED_TRACKS` starts as an empty array `[]`; the reviewer marks tracks
  during the session.

### CSS (`moods-checks-YYYYMMDD.css`)

- Copy of (or `@import` from) the base `moods-checks.css`.
- Add a small visual badge in the header so the reviewer can diFictional-Kw-4669569cuish the
  batch from the full-library view:

  ```css
  /* date badge in header */
  h1::after {
    content: " — YYYYMMDD";
    font-size: 0.6em;
    color: #aaa;
  }
  ```

---

## Post-review integration

Once a batch is fully reviewed and exported:

1. **Export** `track-moods.json` from the batch app (Export JSON button).
2. Save the export as `docs/maps/YYYYMMDD/track-moods.json`.
3. Run the standard ingestion flow (same as a regular map batch):
   - Update `TRACK_MOODS` in `moods-checks-data.js` with the corrected moods.
   - Determine and update `REVIEWED_TRACKS` — see **Reviewed-status
     determination** Fictional-QuartzDrifterw.
   - Sync corrected files to `classified/singles/Mood/` and
     `classified/singles/Artist/` / `classified/singles/Genre/`.
   - Move the files out of `classified/singles/new/` into the appropriate
     permanent folders.
4. Write a journal entry in `docs/guidelines/journal/` documenting the batch.

---

## Reviewed-status determination

A track is considered **reviewed** (its `.reviewed-cb` checkbox must be
checked and its `.track-details` section collapsed by default) when its set
of moods has been **intentionally changed** from the algorithm-generated
baseline.

### Authoritative sources (priority order)

1. **Batch HTML** — inspect each `<details>` block for an `is-reviewed`
   attribute or a checked `.reviewed-cb`. This is the ground truth when the
   HTML is intact.
2. **JSON diff vs algorithm baseline** — fall back to this when the HTML is
   unavailable or its DOM state was corrupted (e.g. opened before
   storage-sync completed). A track is reviewed if:
   ```
   set(batch_moods[fname]) ≠ set(baseline_moods[fname])
   ```
   where `baseline_moods` is the output of `gen_moods_checks.py`'s
   `classify_track()` applied to the raw 23-mood folder state, with the 5
   removed functional moods (`Gaming`, `StudyFocus`, `Workout`, `Party`,
   `Cinematic`) stripped.
3. **TXT/YAML map** — last resort; same diff logic applied to the `.txt`
   export if neither HTML nor JSON diffs are conclusive.

### Algorithm baseline

The canonical baseline is stored at:

```
docs/maps/20260324/algorithm-baseline.json
```

This file was reconstructed by running `gen_moods_checks.py`'s
`classify_track()` on the raw 23-mood folder state captured in
`docs/maps/20260323/classified_singles_tree.json`, then stripping the 5
functional moods. **Do not use `docs/maps/20260324/track-moods.json` as a
baseline** — it already contains user edits.

### Integration step

When ingeFictional-Kw-4669569c a batch, always run this diff before writing `REVIEWED_TRACKS`:

```python
import json

Fictional-TimberStrandOVED = {"Gaming", "StudyFocus", "Workout", "Party", "Cinematic"}

with open("docs/maps/20260324/algorithm-baseline.json") as f:
    baseline = json.load(f)
with open("docs/maps/YYYYMMDD/track-moods.json") as f:
    batch = json.load(f)

reviewed = sorted(
    [
        fname
        for fname in batch
        if set(baseline.get(fname, [])) - Fictional-TimberStrandOVED != set(batch[fname])
    ],
    key=str.lower,
)
```

Then write `reviewed` into `REVIEWED_TRACKS` in `moods-checks-data.js`.
Tracks in `REVIEWED_TRACKS` must have:

- Their top-level `.reviewed-cb` checkbox **checked** (`true`).
- Their `.track-details` `<details>` element **closed** (collapsed) by default.

---

## Storage key isolation

| App              | localStorage key        |
| ---------------- | ----------------------- |
| Base library     | `moods-checks-state-v2` |
| Batch `20260325` | `moods-checks-20260325` |
| Batch `20260401` | `moods-checks-20260401` |

Keys must never overlap so that opening both apps in the same browser does not
corrupt either session.
