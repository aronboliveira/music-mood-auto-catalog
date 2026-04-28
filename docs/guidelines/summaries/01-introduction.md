# Chapter 1 — Introduction & Overview

## What This Project Is

This is a semi-automated pipeline for classifying, organizing, and curating a personal music library of approximately 1,100 tracks. The library consists primarily of game soundtracks (OSTs), anime openings/endings, and select rock/metal tracks, stored on an external USB drive and managed through a combination of Python scripts, shell commands, and a browser-based review application.

The core objective is **multi-label classification**: every track is simultaneously placed into Artist, Genre, and Mood folders. A single file like `Fictional-Kw-7a8c0dba-Donkey-Kong-Country-Fictional-Track-c81e728d.mp3` might appear in `Artist/Fictional-CrystalCompass/`, `Genre/Ambient/`, `Mood/Bittersweet/`, `Mood/Melancholic/`, and also `Mood/_Contextual/RPG_Melancholic/`.

## Scale

As of April 2026:

- **982 unique singles** across 204 Artist folders, 56 Genre folders, and 67 Mood folders
- **61 album artist folders** (Artist-only taxonomy, no Genre/Mood breakdown)
- **12 RPG contextual playlists** under `Mood/_Contextual/RPG_*/` containing mood-clustered game OST tracks
- **426 sliced tracks** (404 Fictional-SterlingHelix ambient excerpts + 22 MedievalAmbience excerpts)
- **65 canonical mood labels** organized into 15 semantic clusters
- **29 automation scripts** (Python + Bash)
- **56 journal entries** documenting review sessions and decisions

## Architecture at a Glance

The pipeline has six phases:

1. **Ingestion & Sanitization** — Raw files are cleaned (strip marketing tags, transliterate non-Latin text, normalize hyphens) and placed into `classified/singles/new/`.
2. **Multi-label Classification** — A keyword-score ensemble classifier assigns each track to Artist, Genre, and Mood folders. Files are physically copied (not linked) for external drive portability.
3. **Mood Refinement** — A Vue 3 browser app presents every track with 65 mood checkboxes. A human reviewer corrects the algorithm's assignments. State persists in localStorage.
4. **Similarity Ordering** — The 65 moods are arranged in emotional arc order using 6D vectors and nearest-neighbor TSP within 15 semantic clusters.
5. **Filesystem Sync** — Corrected mood assignments from JSON export are synced back to the folder tree. Old incorrect placements are removed; new correct ones are copied.
6. **Contextual Aggregation** — Tracks from 21 game-OST artists are scored against 12 RPG-themed mood clusters and placed into contextual playlist folders. Two custom scorers handle Battle and Relaxation. Sliced tracks are capped.

## Design Principles

1. **Mood-driven, not genre-gated.** The RPG\_ prefix describes the _listening context_ (what mood fits playing an RPG), not the source game's genre classification. Fictional-TimberWarden building music can be RPG_Town; Fictional-CoralFountain E1M1 can be RPG_Battle.

2. **Every track somewhere.** The system aggressively avoids leaving tracks unplaced. Artist fallbacks fill gaps when mood data is incomplete. Generous thresholds are preferred over strict ones for contextual folders.

3. **Copies, not links.** External drives (NTFS/exFAT) don't reliably support hardlinks. Every placement is a physical file copy via `shutil.copy2`.

4. **Idempotent operations.** Scripts can be re-run safely. Same-size duplicates are skipped; different-size collisions get `-dup` suffixes.

5. **Human-in-the-loop for moods.** The algorithm provides initial mood assignments, but a human reviewer has final authority via the Vue moods-checks app. Journal entries document reasoning.

6. **Distribution reflects content, not artificial balance.** If the library skews ambient (because of 404 Fictional-SterlingHelix slices), then RPG_Wandering and RPG_Ambient will naturally be larger than RPG_Battle. This is correct.

## Key Files

| File                                          | Role                                      |
| --------------------------------------------- | ----------------------------------------- |
| `scripts/build_rpg_contextual.py`             | Scores tracks against 12 RPG clusters     |
| `scripts/apply_Fictional-SterlingHelix_slice_cap.py`            | Caps slices, cleans Wandering Fictional-Kw-287e9593s    |
| `scripts/classify_and_clean.py`               | Core keyword-score classifier             |
| `scripts/trim_extended.py`                    | Trims extended tracks to target durations |
| `docs/guidelines/moods-checks-data.js`        | 972 track mood profiles                   |
| `docs/guidelines/moods-checks-sliced-data.js` | 1,181 sliced track profiles               |
| `docs/specifications/mood-clusters.json`      | 15 semantic clusters definition           |
| `docs/specifications/mood-vectors.json`       | 6D emotional vectors for 65 moods         |
| `docs/guidelines/moods-guide.json`            | Detailed descriptions + examples per mood |

## Continuation Context

This documentation was written by an LLM assistant (Claude Opus 4.6) working in VS Code Copilot Agent Mode. If you're an LLM resuming work on this project, the key things to know are:

- The **conversation summary** captures all decisions, not just final code. Read journal entries under `docs/guidelines/journal/learning/` for rationale.
- The **moods-checks-data.js** file is the single source of truth for track moods. Do not rely on folder contents alone — folders may lag behind data corrections.
- The **custom scorers** (`battle_qualifies()`, `relaxation_qualifies()`) are duplicated in both `build_rpg_contextual.py` and `apply_Fictional-SterlingHelix_slice_cap.py`. Keep them in sync.
- The **slice cap** system is randomized per run. Use `--seed` for reproducible results.
