# Batch 34 — 20260414 Final Pass Statistics

**Date:** 2026-04-14  
**DATA_VERSION:** 20260414

## Review Progress

| Metric | Value |
| --- | --- |
| Total tracks (TRACK_MOODS) | 972 |
| Reviewed (REVIEWED_TRACKS) | 972 (100.0%) |
| Unreviewed | 0 |
| Mood changes applied | 42 |
| Tracks added / removed | 0 / 0 |

## Mood Assignment Density

| Metric | Value |
| --- | --- |
| Total mood assignments | 10,407 |
| Avg moods/track | 10.71 |
| High-density outliers (>=16 moods) | 22 tracks |
| Low-density outliers (<=2 moods) | 9 tracks |

### Top 10 Moods

| Mood | Count |
| --- | --- |
| Energetic | 548 |
| Aggressive | 344 |
| Rebellious | 325 |
| Chill | 322 |
| Adventurous | 308 |
| Defiant | 305 |
| Emotional | 282 |
| Groovy | 278 |
| Contemplative | 272 |
| Danceful | 263 |

### Bottom 10 Moods

| Mood | Count |
| --- | --- |
| Hypnotic | 28 |
| Macabre | 32 |
| Sleepy | 34 |
| Ominous | 48 |
| Sensual | 50 |
| Depressive | 54 |
| Meditative | 54 |
| Suspenseful | 55 |
| Desperate | 73 |
| Spiritual | 75 |

## Mood Delta vs Previous Data Version

Largest growth concentrations in this pass:

| Mood | Delta |
| --- | --- |
| Frenzy | +24 |
| Energetic | +23 |
| Defiant | +19 |
| Danceful | +14 |
| Determined | +14 |
| Upbeat | +14 |
| Chaotic | +13 |
| Emotional | +11 |
| Gritty | +11 |
| Whimsical | +11 |

Largest reductions:

| Mood | Delta |
| --- | --- |
| Chill | -9 |
| Nostalgic | -4 |
| Epic | -2 |
| Suspenseful | -1 |

Interpretation: this batch strongly rebalanced formerly impoverished profiles into high-energy and expressive vectors (Frenzy/Energetic/Defiant), reducing overuse of generic placeholder moods (especially Chill/Nostalgic).

## Co-Occurrence Signatures

Top stable mood pairings by absolute co-occurrence:

1. Aggressive + Energetic (306)
2. Energetic + Rebellious (285)
3. Defiant + Energetic (257)
4. Aggressive + Rebellious (240)
5. Adventurous + Energetic (219)
6. Danceful + Energetic (205)
7. Energetic + Frenzy (204)
8. Determined + Energetic (200)
9. Aggressive + Defiant (191)
10. Energetic + Groovy (184)

These pairings continue to indicate a dominant kinetic core in the library: high-drive tracks tend to be tagged as movement + confrontation + momentum rather than movement alone.

## 13 Semantic Cluster Coverage

Cluster definitions follow the established 13-cluster emotional arc used in prior journals.

| Cluster | Tracks with at least one mood in cluster |
| --- | --- |
| 1. Cozy/Tender/Romantic/Sensual | 280 |
| 2. Awe/Reverent/Spiritual/Contemplative/Meditative | 427 |
| 3. Nostalgic/Yearning/Wistful/Bittersweet/Emotional | 472 |
| 4. Sad/Introspective family | 485 |
| 5. Brooding/Dark/Macabre/Ominous | 259 |
| 6. Mysterious/Hypnotic/Surreal/Ethereal | 230 |
| 7. Suspenseful/Tense/Gritty | 254 |
| 8. Aggressive/Rebellious/Chaos/Frenzy | 552 |
| 9. Energetic/Danceful/Groovy | 667 |
| 10. Epic/Heroic/Triumphant/Adventurous/Soaring | 490 |
| 11. Determined/Hardworking/Focused/StudyFocus | 372 |
| 12. Ecstatic/Joyful/Playful/Whimsical/Upbeat/Optimistic | 431 |
| 13. Serene/Peaceful/Relaxed/Chill/Sleepy | 376 |

## Ambience Archetypes (Proposal)

Secondary semantic overlay proposed for future playlisting and review filters.

Coverage (track Fictional-QuartzDrifterngs to archetype if it contains at least one anchor mood):

| Archetype | Coverage |
| --- | --- |
| Combat-Adrenaline | 644 |
| Work-Focus | 573 |
| Heroic-Quest | 544 |
| Melancholic-Introspective | 531 |
| Groove-Dance | 507 |
| Pastoral-Cozy | 404 |
| Ritual-Ambient | 356 |
| Dark-Cinematic | 347 |

Primary assignment (highest anchor overlap) shows strong skew:

| Archetype | Primary count |
| --- | --- |
| Combat-Adrenaline | 342 |
| Melancholic-Introspective | 197 |
| Groove-Dance | 131 |
| Pastoral-Cozy | 102 |
| Heroic-Quest | 97 |
| Ritual-Ambient | 67 |
| Dark-Cinematic | 34 |
| Work-Focus | 2 |

Implication: Focus appears mostly as a secondary modifier, not a primary emotional identity. This supports keeping Focus as an augmentation axis in UI, rather than a top-level mood family.

## Emotional Polarity Buckets

Assignment totals by broad emotional families:

| Bucket | Assignment count |
| --- | --- |
| Positive (joy/hope/warmth) | 1,852 |
| Negative (grief/darkness/decay) | 1,758 |
| Tension (conflict/drive/pressure) | 2,422 |
| Transcendent (awe/mystic/calm/reflective) | 1,997 |

The collection is tension-forward, but not one-dimensional: transcendent and positive totals remain high, sustaining emotional contrast for sequencing.

## Strong Marker Analysis

Requested marker audit:

| Marker | Track count |
| --- | --- |
| Playful | 125 |
| Macabre | 32 |
| Ethereal | 138 |

Marker intersections:

| Intersection | Count |
| --- | --- |
| Playful + Ethereal | 11 |
| Playful + Macabre | 5 |
| Ethereal + Macabre | 6 |
| Playful + Macabre + Ethereal | 0 |

Observations:
- Playful and Ethereal co-occur enough to support whimsical dream-state contexts.
- Macabre rarely intersects with Playful; when it does, it usually produces carnival-gothic ambience.
- No triple intersection means the current taxonomy avoids collapsing into contradictory tonal overloading.

## Outlier Tracks

### Highest-density profiles (>=16 moods)

- Fictional-Track-bcb50ef2.mp3 (20)
- Fictional-Track-2b0773b9.mp3 (19)
- Fictional-ScarletSailss-Mononoke-Ashitaka-and-San.mp3 (18)
- Fictional-Track-0e5c3b42.mp3 (18)
- Fictional-Track-497fd553.mp3 (17)
- Fictional-Track-8335154c.mp3 (17)
- Fictional-Track-1da30faa.mp3 (16)
- Fictional-OpalCastle-Question!.mp3 (16)
- Fictional-Track-99a569e1.mp3 (16)
- (plus 13 additional tracks at 16)

### Low-density profiles (<=2 moods)

- Fictional-Track-4dd944b4.mp3 (1)
- Fictional-Track-86deaff5.mp3 (1)
- Fictional-Track-b215e8a7.mp3 (1)
- Fictional-Track-c645d224.mp3 (1)
- Fictional-Track-89987eda.mp3 (2)
- Fictional-Track-4ff7322a.mp3 (2)
- Fictional-Track-24c9ba60.mp3 (2)
- Fictional-Track-d92acd29.mp3 (2)
- Fictional-Kw-a134d547.mp3 (2)

Historical regression scan across prior map snapshots found no richer historical profiles for these low-density tracks in this pass.
