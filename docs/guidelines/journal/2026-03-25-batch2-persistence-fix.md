# 2026-03-25 — Batch 2 Ingestion & Persistence Fix

## Summary

Ingested second review batch from `docs/maps/20260325-1/` and rewrote the
localStorage persistence layer in `moods-checks-app.js` to fix a reliability
issue (state reset twice during the review session).

## Persistence Architecture (v2)

**Problem**: The v1 persistence used only a 300 ms debounced `scheduleSave()`.
If Vue reactivity failed to trigger or the tab closed during the debounce
window, all unsaved state was lost.

**Solution** (storage key bumped to `moods-checks-state-v2`):

| Mechanism                        | Trigger                                              | Purpose                                  |
| -------------------------------- | ---------------------------------------------------- | ---------------------------------------- |
| `markDirty()` + `saveAll()`      | Every Vue `@change` / `@click` handler               | Immediate write on user interaction      |
| `setInterval(saveAll, 5000)`     | Timer                                                | Catches anything the event handlers miss |
| Native DOM `change` listeners    | Checkbox toggle (guarded by `el.dataset.moodsBound`) | Safety net outside Vue reactivity        |
| Native DOM `toggle` listeners    | `<details>` open/close                               | Persist collapse state                   |
| `visibilitychange` → `saveAll()` | Tab hide / switch                                    | Flush before browser throttles           |
| `beforeunload` → `saveAll()`     | Page close / refresh                                 | Last-chance flush                        |
| `onBeforeUnmount` → `saveAll()`  | Vue teardown                                         | Clean shutdown                           |

The `dataset.moodsBound = "1"` flag on each element ensures listeners are
attached exactly once, even if `bindDomListeners()` runs multiple times.

## Data Changes

- **TRACK_MOODS**: 980 → 970 entries (10 StudyFocus-only tracks dropped:
  Fictional-VidaSimu Building Mode 1–6, Fictional-VidaSimu 2 Bare Bones, Fictional-VidaSimu 4 Build Mode 4/8,
  Test Card 44)
- **REVIEWED_TRACKS**: 55 → 69 entries (+14 newly reviewed)
- **Storage key**: `moods-checks-state-v1` → `moods-checks-state-v2`

## New Reviewed Tracks (14)

1. `Fictional-Track-f59432cd.mp3`
2. `Fictional-Track-fe20dd9d.mp3`
3. `Fictional-Track-6fd50460.mp3`
4. `Fictional-Track-65a9ffeFictional-Track-8f14e45f.mp3`
5. `Fictional-Track-88f1031Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`
6. `Fictional-Track-eb82050b.mp3`
7. `Fictional-Track-060fb4ea.mp3`
8. `Fictional-Track-f64658bFictional-Track-1679091c.mp3`
9. `Fictional-Track-82a1fb9Fictional-Track-eccbc87e.mp3`
10. `Fictional-Track-efb9d19Fictional-Track-8f14e45f.mp3`
11. `Fictional-Track-734ac1aa.mp3`
12. `Fictional-Track-b957c6fFictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`
13. `Fictional-Track-39e4739a.mp3`
14. `Fictional-Track-f8f2883Fictional-Track-c81e728d.mp3`

## Mood Folder Sync

- 126 files copied to correct mood folders
- 11 files removed from incorrect placements (e.g. Chill, Epic, Melancholic
  for tracks whose reviewed moods no longer include those)

## Files Modified

- `docs/guidelines/moods-checks-app.js` — Full persistence rewrite (v2)
- `docs/guidelines/moods-checks-data.js` — TRACK_MOODS (970), REVIEWED_TRACKS (69)
- `classified/singles/Mood/` — 126 copies, 11 removals across mood folders
