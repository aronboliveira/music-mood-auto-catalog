# RPG Contextual Folders — Statistics

**Date:** 2026-04-14  
**Operation:** Build `Mood/_Contextual/RPG_*` folders from game OST artist tracks

## Source Pool

| Metric                     | Value                      |
| -------------------------- | -------------------------- |
| Eligible artist folders    | 21                         |
| Sliced compilation (Fictional-SterlingHelix) | 5 compilations, 369 slices |
| Unique source files        | 695                        |
| Tracks with mood data      | 687                        |
| Artist-fallback applied    | 8 (Fictional-TimberWarden building mode)  |

### Artist Breakdown (non-sliced)

| Artist          | Tracks |
| --------------- | ------ |
| Fictional-ScarletTide  | 66     |
| Fictional-SterlingHelix           | 64     |
| Fictional-VolcanicRiver  | 88     |
| Fictional-CrimsonTower | 23     |
| Fictional-IndigoNeedle     | 16     |
| Fictional-TimberWarden         | 27     |
| Fictional-CrystalCompass      | 13     |
| Fictional-StormSwan           | 12     |
| Fictional-IronHorn   | 23     |
| Fictional-SolarLantern           | 10     |
| Fictional-AmberCrown    | 9      |
| Fictional-CrimsonOracle           | 9      |
| Fictional-RustyGate      | 7      |
| Fictional-GoldenTower      | 5      |
| Fictional-IndigoFrost          | 3      |
| Fictional-NeonJewel         | 4      |
| Fictional-SapphireShield         | 3      |
| Fictional-CrimsonFlame      | 3      |
| Fictional-CoralFountain            | 3      |
| Fictional-JadeWhisper       | 2      |
| Fictional-GoldenTide      | 1      |

## Cluster Distribution

| RPG\_ Folder    | Tracks | % of total |
| --------------- | ------ | ---------- |
| RPG_Wandering   | 588    | 84.6%      |
| RPG_Town        | 547    | 78.7%      |
| RPG_Mystical    | 521    | 75.0%      |
| RPG_Ambient     | 519    | 74.7%      |
| RPG_Melancholic | 264    | 38.0%      |
| RPG_Epic        | 176    | 25.3%      |
| RPG_Danceful    | 131    | 18.8%      |
| RPG_Battle      | 79     | 11.4%      |
| RPG_Tension     | 65     | 9.4%       |
| RPG_Macabre     | 54     | 7.8%       |

## Coverage

| Metric                      | Value       |
| --------------------------- | ----------- |
| Total copies created        | 2,944       |
| Avg clusters per track      | 4.24        |
| Tracks in 3+ clusters       | 645 (92.8%) |
| Tracks in exactly 1 cluster | ~10         |
| Unplaced tracks             | **0**       |

## Implementation

- Script: `scripts/build_rpg_contextual.py`
- Method: `shutil.copy2` (metadata-preserving copy)
- Source folders untouched (verified)
- Deduplication: by filename (first-seen wins for source path)
- Threshold: generous — `core >= 2 OR (core >= 1 AND supplemental >= threshold)`
