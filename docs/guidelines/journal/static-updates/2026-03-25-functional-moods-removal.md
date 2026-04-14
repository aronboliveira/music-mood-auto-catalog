# Functional Moods Removal — Static Updates — 2026-03-25

## Files Changed

### Taxonomy core

- `docs/guidelines/moods.txt` — removed StudyFocus (65 lines now)
- `docs/guidelines/moods-checks-data.js` — removed from ALL_MOODS, MOOD_COLORS, and stripped from all 980 TRACK_MOODS entries
- `docs/guidelines/moods-guide.json` — removed StudyFocus entry; updated Focused description to remove reference

### Filesystem

- Deleted `classified/singles/Mood/{Gaming, StudyFocus, Workout, Party, Cinematic}` (418 files across 5 folders; all tracks still present in Artist/ and Genre/)
- Mood folder count: 68 → 63

### Specifications

- `docs/specifications/mood-vectors.json` — removed StudyFocus; 66 → 65 vectors; date updated to 2026-03-25
- `docs/specifications/mood-clusters.json` — removed StudyFocus from cluster 14 (Determined/Focused); cluster now has 3 moods
- `docs/specifications/technical-overview.md` — updated counts (65 moods, 63 folders, 65×6 matrix); added v3 row to evolution table; removed StudyFocus from cluster list
- `docs/specifications/data-schemas.yml` — updated all "66" references to 65
- `docs/specifications/scripts-inventory.yml` — updated copy_sims.py outputs

### Scripts

- `scripts/_sort_moods.py` — removed StudyFocus from MOOD_VECTORS, removed from CLUSTERS[13]; updated assert from 66 to 65
- `scripts/classify_and_clean.py` — removed Gaming, Party, StudyFocus, Workout, Cinematic keyword dicts
- `scripts/gen_moods_checks.py` — removed Gaming/Workout/Party/Cinematic from OLD_TO_NEW migration map; removed StudyFocus keyword entry and color entry
- `scripts/copy_sims.py` — removed STUDYFOCUS path variable; remapped StudyFocus-bound Sims files to Upbeat
