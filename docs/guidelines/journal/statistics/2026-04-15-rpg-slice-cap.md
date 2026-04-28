# RPG Contextual Folders — Slice Cap & Wandering Cleanup — 2026-04-15

## Operation Summary

| Step                             | Action                                                          |
| -------------------------------- | --------------------------------------------------------------- |
| 1. RPG_Wandering Fictional-Kw-287e9593 cleanup | Removed 44 non-slice tracks with incompatible primary character |
| 2. Fictional-SterlingHelix slice cap (5%)          | Removed 1882 old copies, placed 37 fresh random slices          |
| 3. MedievalAmbience slices (2%)  | First-time placement of 8 slices from a 22-file source pool     |

## RPG_Wandering Fictional-Kw-287e9593-Track Removal

| Trigger              | Threshold                                                                  | Tracks removed |
| -------------------- | -------------------------------------------------------------------------- | -------------- |
| Epic-dominant        | >= 3 of {Epic, Triumphant, Heroic, Awe-inspired}                           | 12             |
| Battle-dominant      | >= 2 of {Aggressive, Explosive, Frenzy, Chaotic, Furious}                  | 10             |
| Danceful-dominant    | >= 3 of {Danceful, Groovy, Ecstatic, Upbeat}                               | 15             |
| Melancholic-dominant | >= 3 of {Melancholic, Sad, Bittersweet, Anguished, Heartbreak, Depressive} | 7              |
| **Total**            |                                                                            | **44**         |

Notable removals: Angelica (RO-108, Battle), Invincible (WoW, Melancholic), Lament of the Highborne (WoW, Melancholic), Midna's Lament (Fictional-SterlingHelix, Melancholic), Legends of Azeroth (WoW, Epic).

Threshold was calibrated to avoid false positives — Prontera Theme (Epic:2), Goron Lullaby (Epic:2), Sims buy-mode tracks (Dance:2) all correctly retained.

## Fictional-SterlingHelix Slice Cap (5%)

| Metric                      | Value                                       |
| --------------------------- | ------------------------------------------- |
| Source pool                 | `sliced/Artist/Fictional-SterlingHelix/` — 404 files          |
| Cap formula                 | `max(1, round(N * 0.05 / 0.95))`            |
| Total cap slots (6 folders) | 37                                          |
| Unique slices placed        | 37 (9.2% of pool)                           |
| Coverage model              | Randomized per run; full coverage over time |

### Per-Folder Breakdown

| Folder          | Non-slice | Cap | Eligible | Placed | Fictional-SterlingHelix % |
| --------------- | --------- | --- | -------- | ------ | ------- |
| RPG_Ambient     | 115       | 6   | 404      | 6      | 4.9%    |
| RPG_Epic        | 126       | 7   | 50       | 7      | 5.3%    |
| RPG_Melancholic | 48        | 3   | 216      | 3      | 5.9%    |
| RPG_Mystical    | 117       | 6   | 404      | 6      | 4.9%    |
| RPG_Town        | 143       | 8   | 404      | 8      | 5.2%    |
| RPG_Wandering   | 140       | 7   | 404      | 7      | 4.7%    |

RPG_Battle, RPG_Danceful, RPG_Macabre, RPG_Tension: 0 eligible Fictional-SterlingHelix slices (no placement).

## MedievalAmbience Slices (2%)

| Metric                      | Value                                                                                                     |
| --------------------------- | --------------------------------------------------------------------------------------------------------- |
| Source pool                 | `sliced/Artist/MedievalAmbience/` — 22 files                                                              |
| Cap formula                 | `max(1, round(N * 0.02 / 0.98))`                                                                          |
| Mood profile (inherited)    | Chill, Contemplative, Cozy, Emotional, Focused, Optimistic, Peaceful, Relaxed, Reverent, Soaring, Wistful |
| Eligible clusters           | RPG_Ambient, RPG_Town, RPG_Wandering                                                                      |
| Total cap slots (3 folders) | 8                                                                                                         |
| Unique slices placed        | 8 (36.4% of pool)                                                                                         |

### Per-Folder Breakdown

| Folder        | Non-slice | Cap | Placed | Medieval % |
| ------------- | --------- | --- | ------ | ---------- |
| RPG_Ambient   | 115       | 2   | 2      | 1.6%       |
| RPG_Town      | 143       | 3   | 3      | 1.9%       |
| RPG_Wandering | 140       | 3   | 3      | 2.0%       |

## Final RPG\_ Folder State

| Folder          | Total    | Fictional-SterlingHelix  | Medieval | Non-slice | Slice % |
| --------------- | -------- | ------ | -------- | --------- | ------- |
| RPG_Ambient     | 123      | 6      | 2        | 115       | 6.5%    |
| RPG_Battle      | 79       | 0      | 0        | 79        | 0.0%    |
| RPG_Danceful    | 131      | 0      | 0        | 131       | 0.0%    |
| RPG_Epic        | 133      | 7      | 0        | 126       | 5.3%    |
| RPG_Macabre     | 54       | 0      | 0        | 54        | 0.0%    |
| RPG_Melancholic | 51       | 3      | 0        | 48        | 5.9%    |
| RPG_Mystical    | 123      | 6      | 0        | 117       | 4.9%    |
| RPG_Tension     | 65       | 0      | 0        | 65        | 0.0%    |
| RPG_Town        | 154      | 8      | 3        | 143       | 7.1%    |
| RPG_Wandering   | 150      | 7      | 3        | 140       | 6.7%    |
| **Total**       | **1063** | **37** | **8**    | **1018**  |         |

## Algorithm Design

- **Coverage-maximising allocation**: Phase 1 places each file in one random under-cap eligible folder (most constrained first); Phase 2 fills remaining cap space.
- **No duplicates**: a slice never appears twice in the same folder.
- **Re-runnable**: each execution draws a fresh random sample; `--seed N` for reproducibility.
- Script: `scripts/apply_Fictional-SterlingHelix_slice_cap.py`

## Net Change from Previous State (pre-cap)

| Before (2026-04-14 RPG build)    | After (this run)          | Delta  |
| -------------------------------- | ------------------------- | ------ |
| 2,944 total copies               | 1,063 total files         | −1,881 |
| ~77% Fictional-SterlingHelix slices in top folders | ~5% Fictional-SterlingHelix per folder      | Capped |
| 0 MedievalAmbience               | 8 placed (22 pool)        | +8     |
| 0 Fictional-Kw-287e9593 removals               | 44 removed from Wandering | −44    |
