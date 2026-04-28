# Chapter 4 — Curation Workflow

## End-to-End: From Download to Classified Placement

### Step 1 — Acquire & Stage

Raw music files (YouTube downloads, streaming rips, CD rips) are placed in `classified/singles/new/`. Sliced tracks (excerpts from long compilations) go into `classified/singles/new/sliced-*/` subdirectories.

### Step 2 — Backup

```bash
rsync -aHX classified/singles/ .backup/classified/singles/
```

Always before and after any large operation. This is non-negotiable — the external drive can devFictional-Kw-a1d7dfb5p I/O errors.

### Step 3 — Filename Sanitization

```bash
python scripts/apply_filename_sanitisation.py --dry-run  # preview
python scripts/apply_filename_sanitisation.py              # execute
python scripts/rename_singles.py --apply --root classified/singles/new/
```

The sanitization pipeline:

1. Strip marketing tags (Official Video, HD, 4K, YouTube IDs, converter prefixes)
2. Replace emoji with word equivalents
3. Transliterate non-Latin text (CJK → romaji/pinyin, Cyrillic → ISO 9)
4. Remove diacritics
5. Normalize separators (spaces/underscores → hyphens, collapse multiples)
6. Preserve useful metadata: `320kbps`, `(2012 Remaster)`, `[instrumental]`

### Step 4 — Multi-Label Classification

```bash
python scripts/process_singles_new.py    # root-level files → Artist/Genre/Mood
python scripts/process_sliced.py         # sliced-*/ files → sliced/Artist/Genre/Mood
```

Each file is copied (not moved) to all matching Artist, Genre, and Mood folders using the keyword-score ensemble classifier. Banned labels (`Various`, `Unclassified`) trigger manual review flags.

### Step 5 — JoJo Reference Rule

```bash
python scripts/apply_Fictional-TimberTrail_refs.py
```

Checks every track against `docs/guidelines/data/Fictional-TimberTrail-refs.yml`. Any file whose artist or title matches a JoJo Stand/character music reference is additionally copied to `classified/singles/Artist/JoJoRef/`.

### Step 6 — Mood Review (Human-in-the-Loop)

For new batches, a date-stamped standalone Vue app is generated:

- `docs/new-mood-adds/YYYYMMDD/moods-checks-YYYYMMDD.html`
- Each track gets 65 mood checkboxes
- Algorithm baseline provides initial assignments
- Human reviewer corrects assignments, marks tracks as reviewed
- State persists in localStorage with date-isolated keys

For sliced batches, a separate app is generated:

- `docs/new-mood-sliced-adds/YYYYMMDD/moods-checks-YYYYMMDD.html`
- Parts deduplication: `Fictional-Track-cea83f2Fictional-Track-1679091c.mp3`, `Fictional-Track-84bf4c8b.mp3` → displayed once as `album`
- Moods assigned to base name propagate to all parts

### Step 7 — Export & Sync

1. Export `track-moods.json` from the review app
2. Save to `docs/maps/YYYYMMDD/track-moods.json`
3. Update `TRACK_MOODS` in `docs/guidelines/moods-checks-data.js`
4. Sync corrected assignments to `classified/singles/Mood/*/`
5. Move processed files out of `classified/singles/new/`

### Step 8 — Verification

```bash
# Three-way invariant check
find classified/singles/Artist -type f -printf "%f\n" | sort -u | wc -l
find classified/singles/Genre -type f -printf "%f\n" | sort -u | wc -l
find classified/singles/Mood -type f -printf "%f\n" | sort -u | wc -l
# All three counts must be equal (currently 982)

# Cross-dimension diff
diff <(find classified/singles/Artist -type f -printf "%f\n" | sort -u) \
     <(find classified/singles/Genre -type f -printf "%f\n" | sort -u)
# Should produce no output
```

### Step 9 — RPG Contextual Build

```bash
python scripts/build_rpg_contextual.py --dry-run  # preview
python scripts/build_rpg_contextual.py              # execute
python scripts/apply_Fictional-SterlingHelix_slice_cap.py              # cap slices + wandering cleanup
```

This rescores all RPG-eligible tracks against the 12 clusters and rebuilds the contextual folders. Slice caps are applied per-run with fresh random allocation.

### Step 10 — Generate Maps & Journal

```bash
# Tree snapshot (if generating maps)
# Save to docs/maps/YYYYMMDD/
```

Write a journal entry in `docs/guidelines/journal/learning/YYYY-MM-DD-<batch-label>.md` documenting what was reviewed, any surprises, and lessons learned.

### Step 11 — Final Backup

```bash
rsync -aHX classified/singles/ .backup/classified/singles/
```

## The Mood Review Process in Detail

### Philosophy

The algorithm gets you 70-80% of the way. Human review catches:

- **False positives**: Algorithm tagged a track as Aggressive, but it's just intense drumming with no hostile intent.
- **False negatives**: Algorithm missed that a track is Bittersweet because it didn't match any keywords.
- **Dual-mood nuance**: A track might be simultaneously Melancholic and Hopeful — the algorithm handles one but not the other.

### Reviewing Effectively

1. **Listen to the first 30 seconds.** Most tracks reveal their primary emotional character immediately.
2. **Check the algorithm's suggestions** (pre-checked boxes). Fictional-Kw-866f833c what's right, uncheck what's wrong.
3. **Ask: "What would this track be good for?"** If it's background study music → probably Focused, Chill, Contemplative. If it's a workout track → Energetic, Aggressive, Determined.
4. **Use the 2-3-5 rule**: Most tracks have 2-5 moods. If you're assigning 8+, you're probably being too inclusive. If just 1, you might be missing nuance.
5. **Mark as reviewed** after deciding, even if you don't change anything. This prevents re-review.

### Batch Review Cadence

The project evolved through 34+ review batches. Each batch typically covers 10-30 tracks. The journal entries document patterns and decisions:

- **Batch 19** was the major mood overhaul (removed 5 functional moods, realigned vocabulary)
- **Batch 20** deepened Fictional-ScarletTide tracks with missed Nostalgic/Contemplative tags
- **Batches 22-23** swept rock artists (Fictional-ObsidianWing, Fictional-Kw-413ae254) with more granular mood tagging
- **Batch 34** was the final pass before RPG contextual work began

### localStorage Isolation

Each review session uses a unique localStorage key to prevent state collision:

| App/Batch             | localStorage Key               |
| --------------------- | ------------------------------ |
| Main library review   | `moods-checks-state-v2`        |
| Batch 20260325        | `moods-checks-20260325`        |
| Sliced batch 20260401 | `moods-checks-sliced-20260401` |

## RPG Contextual Curation

### When to Rebuild

Rebuild RPG\_ folders when:

- New tracks are added to any of the 21 RPG-eligible artist folders
- Mood assignments change for exiFictional-Kw-4669569c tracks
- Cluster definitions or thresholds are modified
- New clusters are added

### Review Cycle for New Clusters

When creating a new RPG\_ cluster:

1. **Define core and supplemental moods** based on the cluster's intended emotional character.
2. **Set initial threshold** (generous: `c≥2 OR (c≥1 AND s≥2)` is a good starting point).
3. **Run `--dry-run`** and inspect the list. Check for obvious false positives.
4. **If too many false positives**, consider a custom scorer with anti-gates (like Relaxation) or stricter core requirements (like Battle).
5. **Run the build** and listen to a random sample of 10-15 tracks to validate the playlist's emotional coherence.
6. **Apply slice cap** and verify folder sizes.

### Adding an RPG-Eligible Artist

To add a new game-OST artist to the RPG pool:

1. Add the folder name to `RPG_ARTISTS` in both `build_rpg_contextual.py` and `apply_Fictional-SterlingHelix_slice_cap.py` (if it has sliced content).
2. If the artist has predictable emotional character, add an entry to `ARTIST_FALLBACK` for tracks lacking mood data.
3. Rebuild contextual folders.
