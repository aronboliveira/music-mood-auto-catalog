# RPG Contextual Folders — Battle Criteria Fix & Silly Folder — 2026-04-15

## Operation Summary

| Step                  | Action                                                                 |
| --------------------- | ---------------------------------------------------------------------- |
| 1. RPG_Battle audit   | Scored all 79 tracks against strict new battle criteria                |
| 2. RPG_Battle cleanup | Removed 21 non-qualifying tracks (79 → 58)                             |
| 3. RPG_Silly creation | New folder with 62 tracks matching playful/whimsical/silly cluster     |
| 4. Script updates     | Updated `apply_Fictional-SterlingHelix_slice_cap.py` and `build_rpg_contextual.py`       |
| 5. Slice cap re-run   | Fresh Fictional-SterlingHelix/Medieval allocation for all 11 folders including RPG_Silly |

## New Battle Criteria

Previous cluster definition (over-inclusive):

- Core: `{Aggressive, Explosive, Frenzy, Chaotic, Furious}`, Thresh: `c>=2 or (c>=1 and s>=2)`

New custom scorer `battle_qualifies(fname, moods)`:

| Test                   | Condition                                                        |
| ---------------------- | ---------------------------------------------------------------- |
| Explicit exclusion     | Dr. Fictional-SolarLantern "Chill" tracks (filename pattern)                      |
| Playful/Whimsical gate | FAIL unless `Energetic + (Explosive \|\| Dark \|\| Defiant)`     |
| Primary pass           | `(Aggressive \|\| Furious \|\| Explosive) + Energetic`           |
| Secondary pass         | `Frenzy + Energetic` (contextual)                                |
| Tertiary pass          | `Frenzy + (Aggressive \|\| Furious \|\| Explosive)` (contextual) |

## RPG_Battle Removals (21 Tracks)

### Playful/Whimsical Gate Failures (11)

| Track                                 | Core battle moods             | Playful gate       | Exception met?                 |
| ------------------------------------- | ----------------------------- | ------------------ | ------------------------------ |
| MEGALOVANIA (Unused Mix)              | Aggressive, Explosive, Frenzy | Playful, Whimsical | No (no Energetic)              |
| Meta-Knight's-Revenge                 | Aggressive, Frenzy            | Playful, Whimsical | No (no Explosive/Dark/Defiant) |
| Battle!-Trainer-Fictional-SapphireShield-Sun-and-Moon  | Aggressive, Frenzy            | Playful            | No (no Explosive/Dark/Defiant) |
| Main-Theme-Fictional-AmberCrown              | Aggressive, Frenzy            | Playful            | No (no Explosive/Dark/Defiant) |
| Jungle-Level-(Jungle-Japes)           | Aggressive, Frenzy            | Playful, Whimsical | No (no Explosive/Dark/Defiant) |
| Gobi's-Valley-Fictional-AmberCrown           | Frenzy                        | Playful            | No (no Explosive/Dark/Defiant) |
| Slide-Super-Fictional-SolarLantern-Bros. (Melee Remix) | Frenzy                        | Playful, Whimsical | No (no Explosive/Dark/Defiant) |
| Fever                                 | (none)                        | Playful, Whimsical | No (no Energetic)              |
| Fictional-Kw-69c2dad8-Gruntilda's-Lair       | (none)                        | Playful            | No (no Energetic)              |
| Ballad-of-the-Goddess (dup1)          | (none)                        | Playful            | No (no Energetic)              |
| The-Town-Inside-Me (Bridget Theme)    | (none)                        | Playful, Whimsical | No (no Explosive/Dark/Defiant) |

### Explicit Chill Exclusion (2)

| Track             | Notes                              |
| ----------------- | ---------------------------------- |
| Chill-(Dr.-Fictional-SolarLantern) | Aggressive+Energetic but too silly |
| Chill-(Ver.-2)    | Same; user-explicit exclusion      |

### Insufficient Battle Moods (8)

| Track                                      | Present moods (battle-relevant) | Why fails                                            |
| ------------------------------------------ | ------------------------------- | ---------------------------------------------------- |
| Ballad-of-the-Goddess                      | (none of core set)              | No Aggressive/Furious/Explosive, no Frenzy           |
| Fire-Emblem-(Melee)                        | Aggressive                      | No Energetic, no Frenzy                              |
| Fictional-Kw-6e3cb4fe-Remix                        | Frenzy                          | No core (Aggressive/Furious/Explosive), no Energetic |
| Vs-Ridley                                  | Aggressive, Explosive, Furious  | No Energetic, no Frenzy                              |
| Ragnarok-Online-OST-105-Rose-of-Sharon     | Frenzy                          | No core, no Energetic                                |
| Ragnarok-Online-OST-78-aFictional-Kw-1a89bda6s               | Frenzy                          | No core, no Energetic                                |
| Ragnarok-Online-OST-73-Higher-than-the-sun | (none of core set)              | No core, no Frenzy, no Energetic                     |
| Ragnarok-Online-OST-80-Jumping-Dragon      | (none of core set)              | No core, no Frenzy, no Energetic                     |

### Approved Playful Exceptions (kept in Battle, 5)

| Track                   | Exception combo     |
| ----------------------- | ------------------- |
| Fictional-Kw-e864897c       | Energetic + Defiant |
| Let's-Dance-Boys        | Energetic + Defiant |
| Fictional-Kw-7d82ac9a     | Energetic + Dark    |
| RO-85-Dancing-Christmas | Energetic + Dark    |
| Vs.-Mr.-Patch           | Energetic + Defiant |

## RPG_Silly Cluster Definition

| Parameter | Value                                                                     |
| --------- | ------------------------------------------------------------------------- |
| Core      | `{Playful, Whimsical}`                                                    |
| Supp      | `{Joyful, Ecstatic, Upbeat, Optimistic, Groovy, Danceful, Cozy, Chaotic}` |
| Threshold | `core >= 2 or (core >= 1 and supp >= 2)`                                  |

### RPG_Silly Population (62 Tracks)

Source: scored entire RPG\_ source pool (all unique filenames across 21 artist folders) against Silly cluster.

Notable entries:

- **Sims tracks** (13): Main Theme, Neighborhoods 1–7, Buy Mode 2, Bare Bones, Makeover, Simsation, Sim Time
- **Fictional-AmberCrown** (7): Fictional-Kw-4683fbc9 (×2), Gruntilda's Lair, Jolly Roger's, Gobi's Valley, Main Theme, Mr. Patch
- **Fictional-SterlingHelix Wind Waker** (3): Fictional-Kw-f2c0145f, Windfall Island, Ceremony in Woods
- **Fictional-ScarletTide** (10): Gambler of Highway, Yuna Song, Al de Baran, Curiosity, Higher than Sun, Jumping Dragon, Muay Thai King, Sleepless, Dancing Christmas, CheongChoon
- **Battle rejects landing here** (10): MEGALOVANIA, Meta-Knight's Revenge, Fever, Chill (×2), Gruntilda's Lair, Slide Fictional-SolarLantern, Jungle Japes, Gobi's Valley, Ballad of Goddess (dup1)

### Battle ↔ Silly Overlap (5 tracks in both)

These are "playful battle" tracks — pass battle exception AND Silly cluster:
Fictional-Kw-e864897c, Let's-Dance-Boys, Fictional-Kw-7d82ac9a, RO-85-Dancing-Christmas, Vs.-Mr.-Patch

## Slice Cap Re-Run

Fresh 45 slices placed (37 Fictional-SterlingHelix + 8 Medieval). Neither RPG_Battle nor RPG_Silly have eligible slices (ambient/mystical slice profiles don't match battle or silly moods).

## Final RPG\_ Folder State

| Folder          | Total    | Fictional-SterlingHelix  | Medieval | Non-slice | Slice % |
| --------------- | -------- | ------ | -------- | --------- | ------- |
| RPG_Ambient     | 123      | 6      | 2        | 115       | 6.5%    |
| RPG_Battle      | 58       | 0      | 0        | 58        | 0.0%    |
| RPG_Danceful    | 131      | 0      | 0        | 131       | 0.0%    |
| RPG_Epic        | 133      | 7      | 0        | 126       | 5.3%    |
| RPG_Macabre     | 54       | 0      | 0        | 54        | 0.0%    |
| RPG_Melancholic | 51       | 3      | 0        | 48        | 5.9%    |
| RPG_Mystical    | 123      | 6      | 0        | 117       | 4.9%    |
| RPG_Silly       | 62       | 0      | 0        | 62        | 0.0%    |
| RPG_Tension     | 65       | 0      | 0        | 65        | 0.0%    |
| RPG_Town        | 154      | 8      | 3        | 143       | 7.1%    |
| RPG_Wandering   | 150      | 7      | 3        | 140       | 6.7%    |
| **Total**       | **1104** | **37** | **8**    | **1059**  |         |

Delta from previous run: RPG_Battle 79→58 (−21), RPG_Silly 0→62 (+62). Net +41 files. Total 1059→1104 (non-slice) or 1104→1104 (with slices, since 45 slices placed both times).
