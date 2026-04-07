# Batch 19 Ingestion — 2026-03-30 (map `20260330-2`)

## Summary

Major mood-overhaul batch: 59 tracks reclassified (the largest single-batch change
count in project history), 33 additional tracks reviewed, 10 new sliced compilations
added. This batch marks the decisive correction of "Chill-as-placeholder" and
introduces deep per-track mood specificity across rock, metal, OST, and pop genres.

- **Total tracks**: 970 (unchanged)
- **Reviewed tracks**: 443 → 476 (+33, now 49.1% coverage)
- **Mood changes**: 59 tracks (595 copies, 71 removals across mood folders)
- **Sliced bases**: 36 (unchanged count), 10 new compilations added
- **Sliced reviewed**: 26 → 36 (100% coverage)
- **Sliced parts**: 1,046 → 1,285 (+239)
- **Average moods per track**: 5.95 → 6.49 (+0.54)

## Data File Updates

| File                          | Change                                                        |
| ----------------------------- | ------------------------------------------------------------- |
| `moods-checks-data.js`        | REVIEWED_TRACKS 443→476; 59 mood updates; DATA_VERSION bumped |
| `moods-checks-sliced-data.js` | 10 new bases; 239 new parts; 36/36 reviewed; VERSION bumped   |

Both `DATA_VERSION` and `SLICED_DATA_VERSION` set to `"20260330-2"`.

## Folder Sync

595 copies, 71 removals. All 65 mood directories verified OK against JSON source.

---

## Mood Change Analysis

### Change Pattern Taxonomy

| Pattern                             | Count | Description                                         |
| ----------------------------------- | ----- | --------------------------------------------------- |
| Chill→Specific (5+ moods)           | 23    | Chill removed, replaced with 5–17 specific moods    |
| Reclassification (3+ added)         | 21    | Non-Chill moods restructured, significant additions |
| Enrichment (3+ added, none removed) | 11    | Existing moods kept, 3+ new moods layered on        |
| Multi-remove incl Chill             | 4     | Chill removed alongside other moods                 |

The dominant pattern is **Chill dissolution**: 27 of 59 changes involved removing Chill,
usually as the sole or primary removed mood, and replacing it with a rich, specific
mood profile. This is the definitive correction of the "Chill-as-default" anti-pattern
flagged in earlier batches.

### Top Moods Gained vs Lost

| Gained      | +Count | Lost          | -Count |
| ----------- | ------ | ------------- | ------ |
| Aggressive  | 26     | Chill         | 27     |
| Energetic   | 26     | Nostalgic     | 9      |
| Rebellious  | 24     | Emotional     | 6      |
| Frenzy      | 22     | Romantic      | 4      |
| Defiant     | 21     | Melancholic   | 3      |
| Explosive   | 18     | Epic          | 2      |
| Hardworking | 17     | Introspective | 2      |
| Anguished   | 16     | Upbeat        | 2      |
| Vengeful    | 15     | Ecstatic      | 2      |
| Furious     | 15     | Awe-inspired  | 1      |

Net effect: the library pivoted heavily toward high-energy/negative-valence specificity.
Gains of Aggressive (+26), Frenzy (+22), Anguished (+16), Vengeful (+15), and Furious (+15)
reflect the deep tagging of metal and grunge tracks that were previously under-classified.

### Notable Transformations

| Track                                 | Before                  | After                                  | Notes                                      |
| ------------------------------------- | ----------------------- | -------------------------------------- | ------------------------------------------ |
| `Fictional-Track-d89f493Fictional-Track-eccbc87e.mp3`                | {Chill} (1)             | 13 moods (Aggressive→Upbeat)           | Chill-only → full punk profile             |
| `Fictional-Track-16ac71dFictional-Track-8f14e45f.mp3`               | {Chill} (1)             | 17 moods                               | Largest single-track expansion             |
| `Fictional-Track-dc061a8f.mp3`              | {Aggressive, Energetic} | {Bittersweet, Brooding, Chill...} (12) | Complete valence inversion                 |
| `Fictional-Track-5806fe0Fictional-Track-8f14e45f.mp3` | {Chill} (1)             | 10 moods (Adventurous→Rebellious)      | Alt-metal classic properly tagged          |
| `SSBU Fictional-Kw-57d292fc`                   | 6 moods                 | 19 moods                               | Most-tagged Fictional-EmeraldWarden track              |
| `Fictional-ZincNeedless-Fictional-Kw-c4ac2b82-Theme`             | 8 moods                 | 13 moods                               | Gained Spiritual/Meditative, lost Ecstatic |

---

## Newly Reviewed Tracks (33)

| #   | File                                                      | Moods                                                                                                                                                   |
| --- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `Fictional-Track-875f0a9d.mp3` | Adventurous, Determined, Emotional, Ethereal, Nostalgic, Optimistic, Reverent, Soaring, Tender, Wistful                                                 |
| 2   | `Fictional-Track-f255ee6b.mp3`          | Brooding, Dark, Depressive, Desperate, Epic, Frenzy, Furious, Hardworking, Heartbreak, Lonely, Sad                                                      |
| 3   | `Fictional-Track-e0efbdce.mp3`                                             | Bittersweet, Chill, Contemplative, Jaded, Lonely, Melancholic, Nostalgic, Rebellious                                                                    |
| 4   | `Fictional-Track-adf994cFictional-Track-1679091c.mp3`   | Adventurous, Aggressive, Dark, Determined, Energetic, Epic, Frenzy, Hardworking, Heroic, Macabre, Mysterious                                            |
| 5   | `Fictional-Track-771640aFictional-Track-c81e728d.mp3`                               | Adventurous, Determined, Emotional, Epic, Ethereal, Focused, Hardworking, Mysterious, Ominous, Soaring, Suspenseful, Triumphant                         |
| 6   | `Fictional-Track-3f5d30fe.mp3`                      | Aggressive, Anguished, Brooding, Dark, Depressive, Emotional, Lonely, Melancholic, Resigned, Sad                                                        |
| 7   | `Fictional-Track-7a9b20ac.mp3`                           | Aggressive, Anguished, Depressive, Desperate, Emotional, Energetic, Furious, Gritty, Heartbreak, Lonely, Melancholic, Resigned, Sad                     |
| 8   | `Fictional-Track-5806fe0Fictional-Track-8f14e45f.mp3`                     | Adventurous, Aggressive, Anguished, Chaotic, Energetic, Explosive, Frenzy, Furious, Hardworking, Rebellious                                             |
| 9   | `Fictional-Track-fcf6ebfFictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`                     | Aggressive, Anguished, Dark, Defiant, Emotional, Energetic, Explosive, Frenzy, Furious, Gritty, Hardworking, Heartbreak, Rebellious, Vengeful           |
| 10  | `Fictional-Track-e0bed01e.mp3`                               | Aggressive, Anguished, Emotional, Energetic, Frenzy, Jaded, Melancholic, Rebellious                                                                     |
| 11  | `Fictional-Track-92ff6d1e.mp3`                                   | Anguished, Brooding, Chill, Depressive, Gritty, Groovy, Introspective, Jaded, Melancholic, Resigned, Sad, Tense                                         |
| 12  | `Fictional-Track-91d708ff.mp3`               | Anguished, Contemplative, Emotional, Energetic, Introspective, Lonely, Melancholic, Nostalgic, Sad, Tender, Wistful                                     |
| 13  | `Fictional-Track-be6fa62b.mp3`                                  | Aggressive, Chaotic, Danceful, Ecstatic, Energetic, Frenzy, Hardworking, Hypnotic, Ominous, Surreal                                                     |
| 14  | `Fictional-Track-d552d24f.mp3`                            | Aggressive, Chaotic, Defiant, Energetic, Groovy, Playful, Rebellious, Tense, Vengeful                                                                   |
| 15  | `Fictional-Track-4cf9665Fictional-Track-1679091c.mp3`                                  | Aggressive, Anguished, Chaotic, Gritty, Ominous, Rebellious, Resigned, Sad, Tense, Vengeful                                                             |
| 16  | `Fictional-Track-f194e06c.mp3`                                | Adventurous, Chill, Danceful, Determined, Emotional, Energetic, Groovy, Heartbreak, Jaded, Joyful, Reverent, Soaring                                    |
| 17  | `Fictional-Track-ce2f067Fictional-Track-eccbc87e.mp3`                              | Aggressive, Anguished, Brooding, Chaotic, Dark, Depressive, Desperate, Energetic, Jaded, Mysterious, Resigned, Tense                                    |
| 18  | `Fictional-Track-e4672099.mp3`                  | Cozy, Emotional, Groovy, Romantic, Sensual, Tender, Whimsical                                                                                           |
| 19  | `Fictional-Track-6c60839c.mp3`                            | Chill, Contemplative, Cozy, Groovy, Lonely, Melancholic, Nostalgic, Resigned, Tender                                                                    |
| 20  | `Fictional-Track-ca59978Fictional-Track-c9f0f895.mp3`                                 | Danceful, Ecstatic, Energetic, Groovy, Joyful, Optimistic, Rebellious, Soaring, Tender, Upbeat                                                          |
| 21  | `Fictional-Track-b553ac60.mp3`                                    | Aggressive, Anguished, Brooding, Chaotic, Dark, Depressive, Energetic, Frenzy, Gritty, Groovy, Rebellious                                               |
| 22  | `Fictional-Track-431c6629.mp3`                | Adventurous, Chill, Cozy, Danceful, Ethereal, Nostalgic, Peaceful, Relaxed, Romantic, Tender, Triumphant, Wistful                                       |
| 23  | `Fictional-Track-f80a5fcc.mp3`                             | Danceful, Defiant, Emotional, Energetic, Gritty, Groovy, Heartbreak, Jaded, Melancholic, Soaring, Tense                                                 |
| 24  | `Fictional-Track-87a9460Fictional-Track-e4da3b7f.mp3`                       | Awe-inspired, Bittersweet, Contemplative, Emotional, Ethereal, Meditative, Nostalgic, Peaceful, Relaxed, Serene, Sleepy, Spiritual, Yearning            |
| 25  | `Fictional-Track-c7b24500.mp3`         | Bittersweet, Chaotic, Danceful, Ecstatic, Energetic, Epic, Explosive, Frenzy, Groovy, Hardworking, Playful, Surreal, Triumphant, Upbeat                 |
| 26  | `Fictional-Track-bff2ea4a.mp3`              | Adventurous, Contemplative, Cozy, Dark, Ethereal, Groovy, Introspective, Joyful, Mysterious, Nostalgic, Soaring, Suspenseful                            |
| 27  | `Fictional-Track-e956115a.mp3`              | Chill, Cozy, Nostalgic, Peaceful, Relaxed, Serene, Soaring, Spiritual, Tender, Wistful                                                                  |
| 28  | `Fictional-Track-295ab75e.mp3`                 | Chill, Contemplative, Introspective, Jaded, Lonely, Melancholic, Nostalgic, Peaceful, Relaxed, Sad, Wistful                                             |
| 29  | `Fictional-Track-3734f77e.mp3`                         | Adventurous, Aggressive, Anguished, Defiant, Energetic, Explosive, Furious, Heartbreak, Rebellious, Soaring, Vengeful                                   |
| 30  | `Fictional-Track-0bfda210.mp3`                        | Defiant, Ecstatic, Jaded, Playful, Rebellious, Romantic                                                                                                 |
| 31  | `Fictional-Track-e4af8ced.mp3`                                          | Chaotic, Danceful, Defiant, Determined, Energetic, Groovy, Playful, Rebellious, Soaring, Triumphant, Upbeat, Whimsical                                  |
| 32  | `Fictional-Track-305b30ad.mp3`                               | Anguished, Brooding, Depressive, Desperate, Explosive, Furious, Heartbreak, Melancholic, Rebellious, Sad, Tense                                         |
| 33  | `Fictional-Track-09cf4b7a.mp3`        | Bittersweet, Chill, Contemplative, Cozy, Emotional, Meditative, Melancholic, Nostalgic, Peaceful, Relaxed, Romantic, Serene, Spiritual, Tender, Wistful |

---

## All 59 Mood Changes

| #   | Track                                 | Count | Delta                                                      |
| --- | ------------------------------------- | ----- | ---------------------------------------------------------- |
| 1   | `Fictional-Track-a65ebd5e.mp3`                  | 2→14  | +Aggressive…Sad; -Chill                                    |
| 2   | `Fictional-Track-efca798Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`              | 6→10  | +Determined…Wistful; -Awe-inspired, -Chill, -Epic          |
| 3   | `Fictional-Track-e6a0891Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`                 | 2→11  | +Aggressive…Vengeful; -Chill                               |
| 4   | `Fictional-Track-d89f493Fictional-Track-eccbc87e.mp3`                | 1→13  | +Aggressive…Upbeat; -Chill                                 |
| 5   | `Fictional-Track-1e19823b.mp3`               | 1→13  | +Aggressive…Wistful; -Chill                                |
| 6   | `Fictional-Track-b825171Fictional-Track-c9f0f895.mp3`      | 2→11  | +Brooding…Sad; -Emotional, -Romantic                       |
| 7   | `Fictional-Track-e0efbdce.mp3`                         | 2→8   | +Bittersweet…Rebellious; -Emotional                        |
| 8   | `Fictional-Track-dc061a8f.mp3`              | 2→12  | +Bittersweet…Wistful; -Aggressive                          |
| 9   | `Fictional-Track-18deb26b.mp3`    | 4→11  | +Aggressive…Mysterious; -Nostalgic                         |
| 10  | `Fictional-Track-b3960879.mp3`                   | 2→11  | +Aggressive…Vengeful; -Chill                               |
| 11  | `Fictional-Track-771640aFictional-Track-c81e728d.mp3`           | 9→12  | +Determined…Triumphant; -Dark, -Melancholic, -Nostalgic    |
| 12  | `Fictional-Track-872f27da.mp3`                   | 3→7   | +Awe-inspired…Reverent; -Chill                             |
| 13  | `Fictional-Track-4da0179e.mp3`                  | 3→14  | +Chaotic…Vengeful                                          |
| 14  | `Fictional-Track-141c9dce.mp3`                  | 3→13  | +Anguished…Vengeful                                        |
| 15  | `Fictional-Track-894e9949.mp3`          | 5→15  | +Aggressive…Triumphant; -Nostalgic, -Reverent, -Spiritual  |
| 16  | `Fictional-Track-ac1d60dFictional-Track-1679091c.mp3`           | 5→10  | +Aggressive…Sad; -Introspective, -Jaded                    |
| 17  | `Fictional-Track-7a9b20ac.mp3`       | 1→13  | +Aggressive…Sad; -Chill                                    |
| 18  | `Fictional-Track-5806fe0Fictional-Track-8f14e45f.mp3` | 1→10  | +Adventurous…Rebellious; -Chill                            |
| 19  | `Fictional-Track-eedff66e.mp3`                  | 2→15  | +Aggressive…Triumphant; -Chill                             |
| 20  | `Fictional-Track-fcf6ebfFictional-Track-c4ca423Fictional-Track-c9f0f895.mp3` | 2→14  | +Aggressive…Vengeful                                       |
| 21  | `Fictional-Track-e0bed01e.mp3`           | 3→8   | +Aggressive…Jaded                                          |
| 22  | `Fictional-Track-92ff6d1e.mp3`               | 4→12  | +Anguished…Tense; -Emotional                               |
| 23  | `Fictional-Track-a912d16Fictional-Track-c9f0f895.mp3`     | 3→11  | +Anguished…Wistful; -Cozy                                  |
| 24  | `Fictional-Track-be6fa62b.mp3`              | 2→10  | +Aggressive…Surreal; -Chill                                |
| 25  | `Fictional-Track-d552d24f.mp3`        | 2→9   | +Aggressive…Vengeful; -Chill, -Romantic                    |
| 26  | `Fictional-Track-d514211c.mp3`                  | 2→13  | +Aggressive…Sad; -Chill                                    |
| 27  | `Fictional-Track-4cf9665Fictional-Track-1679091c.mp3`              | 2→10  | +Aggressive…Vengeful; -Chill, -Energetic                   |
| 28  | `Fictional-Track-93d0373Fictional-Track-c81e728d.mp3`                 | 1→12  | +Adventurous…Soaring                                       |
| 29  | `Fictional-Track-ce2f067Fictional-Track-eccbc87e.mp3`          | 5→12  | +Aggressive…Tense; -Chill, -Introspective, -Melancholic    |
| 30  | `Fictional-Track-eb4b07eFictional-Track-c81e728d.mp3`           | 4→10  | +Aggressive…Suspenseful; -Nostalgic, -Playful, -Upbeat     |
| 31  | `Fictional-Track-16ac71dFictional-Track-8f14e45f.mp3`               | 1→17  | +Aggressive…Vengeful; -Chill                               |
| 32  | `Fictional-Track-79169c0e.mp3`                  | 3→14  | +Chaotic…Vengeful; -Chill                                  |
| 33  | `Fictional-Track-1af13c8Fictional-Track-1679091c.mp3`              | 1→7   | +Cozy…Whimsical; -Chill                                    |
| 34  | `Fictional-Track-99be5eec.mp3`               | 1→12  | +Aggressive…Reverent; -Chill                               |
| 35  | `Fictional-Track-6c60839c.mp3`        | 2→9   | +Chill…Tender; -Emotional, -Romantic                       |
| 36  | `Fictional-Track-ca59978Fictional-Track-c9f0f895.mp3`             | 1→10  | +Danceful…Upbeat; -Chill                                   |
| 37  | `Fictional-Track-b553ac60.mp3`                | 5→11  | +Aggressive…Groovy; -Chill                                 |
| 38  | `Fictional-Track-6fad249Fictional-Track-c9f0f895.mp3`          | 5→12  | +Cozy…Wistful                                              |
| 39  | `Fictional-Track-f80a5fcc.mp3`         | 1→11  | +Danceful…Tense; -Chill                                    |
| 40  | `Fictional-Track-735ffc7Fictional-Track-a87ff679.mp3`               | 1→10  | +Contemplative…Surreal                                     |
| 41  | `Fictional-Track-9ef21b7Fictional-Track-a87ff679.mp3`         | 8→13  | +Bittersweet…Yearning; -Ecstatic, -Epic, -Groovy, -Sensual |
| 42  | `Fictional-Track-bff9bf9Fictional-Track-e4da3b7f.mp3`             | 6→14  | +Bittersweet…Surreal; -Emotional, -Romantic                |
| 43  | `Fictional-Track-fbe21d1Fictional-Track-1679091c.mp3`       | 5→12  | +Contemplative…Suspenseful; -Upbeat                        |
| 44  | `Fictional-Track-831f3aca.mp3`       | 3→10  | +Chill…Wistful; -Adventurous, -Ethereal                    |
| 45  | `Fictional-Track-37076e8b.mp3`                | 3→9   | +Chaotic…Surreal                                           |
| 46  | `Fictional-Track-6227101Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`              | 1→11  | +Contemplative…Wistful                                     |
| 47  | `Fictional-Track-a14db5eFictional-Track-8f14e45f.mp3`                | 1→11  | +Adventurous…Vengeful; -Chill                              |
| 48  | `Fictional-Track-1f3f16ab.mp3`             | 1→6   | +Defiant…Romantic; -Chill                                  |
| 49  | `Fictional-Track-e4af8ced.mp3`                      | 2→12  | +Chaotic…Whimsical; -Chill                                 |
| 50  | `Fictional-Track-fe6351fFictional-Track-8f14e45f.mp3`               | 6→19  | +Aggressive…Vengeful; -Emotional, -Melancholic, -Nostalgic |
| 51  | `Fictional-Track-978a395Fictional-Track-e4da3b7f.mp3`              | 4→14  | +Aggressive…Vengeful; -Ecstatic, -Nostalgic                |
| 52  | `Fictional-Track-19b5f57Fictional-Track-a87ff679.mp3`           | 5→15  | +Defiant…Triumphant; -Nostalgic                            |
| 53  | `Fictional-Track-97b0f76Fictional-Track-e4da3b7f.mp3`         | 2→12  | +Chill…Upbeat; -Nostalgic                                  |
| 54  | `Fictional-Track-58a9279Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`                | 2→15  | +Chaotic…Vengeful; -Nostalgic                              |
| 55  | `Fictional-Track-027b91bd.mp3`                  | 2→15  | +Anguished…Vengeful                                        |
| 56  | `Fictional-Track-defd5fcFictional-Track-c81e728d.mp3`                  | 2→9   | +Adventurous…Tense                                         |
| 57  | `Fictional-Track-305b30ad.mp3`           | 1→11  | +Anguished…Tense; -Chill                                   |
| 58  | `Fictional-Track-f1c31f30.mp3`                   | 2→10  | +Anguished…Vengeful; -Chill                                |
| 59  | `sadoost…Fictional-Track-54d4ab4Fictional-Track-a87ff679.mp3`                | 3→15  | +Bittersweet…Wistful; -Sad                                 |

---

## Global Mood Frequency (post-batch)

| Rank | Mood        | Count | % of 970 | Δ from prev |
| ---- | ----------- | ----- | -------- | ----------- |
| 1    | Chill       | 411   | 42.4%    | ↓ (was 438) |
| 2    | Energetic   | 341   | 35.2%    | ↑           |
| 3    | Adventurous | 275   | 28.4%    | ≈           |
| 4    | Nostalgic   | 260   | 26.8%    | ↓           |
| 5    | Aggressive  | 224   | 23.1%    | ↑↑          |
| 6    | Rebellious  | 198   | 20.4%    | ↑↑          |
| 7    | Emotional   | 193   | 19.9%    | ≈           |
| 8    | Melancholic | 171   | 17.6%    | ↑           |
| 9    | Defiant     | 168   | 17.3%    | ↑↑          |
| 10   | Upbeat      | 145   | 14.9%    | ≈           |

**Bottom 5:** Suspenseful (30), Surreal (27), Ominous (27), Sleepy (22), Macabre (22), Hypnotic (17).

Chill dropped from #1 dominant to still-#1 but with 27 fewer assignments. The gap between
Chill and Energetic narrowed from ~120 to ~70. At this rate, Energetic will surpass Chill
within 2-3 more correction batches.

## Co-Occurrence Correlation (Top 10)

| Pair                    | Count | Interpretation                       |
| ----------------------- | ----- | ------------------------------------ |
| Aggressive + Energetic  | 185   | Core intensity cluster               |
| Adventurous + Nostalgic | 169   | Fictional-Kw-98dc0157/exploration archetype        |
| Energetic + Rebellious  | 154   | Punk/alt-rock signature              |
| Aggressive + Rebellious | 146   | Defiance cluster                     |
| Defiant + Energetic     | 135   | Power cluster                        |
| Adventurous + Ethereal  | 109   | OST/ambient exploration              |
| Defiant + Rebellious    | 105   | Anti-authority archetype             |
| Aggressive + Defiant    | 103   | Hard metal signature                 |
| Chill + Nostalgic       | 102   | Wistful relaxation (city pop, Fictional-CrystalBell) |
| Ethereal + Nostalgic    | 101   | Dreamlike nostalgia                  |

New entry: **Emotional + Melancholic** (98) — driven by the grunge/Fictional-QuartzRidge deep-tags.

## Macro-Quadrant Distribution

Using Energy × Valence axes:

| Quadrant | Label                | Count | %     | Δ   |
| -------- | -------------------- | ----- | ----- | --- |
| HE+      | High-Energy Positive | 405   | 41.8% | ≈   |
| LE+      | Low-Energy Positive  | 278   | 28.7% | ↓   |
| HE-      | High-Energy Negative | 178   | 18.4% | ↑↑  |
| LE-      | Low-Energy Negative  | 109   | 11.2% | ↑   |

HE- gained the most from this batch, reflecting the reclassification of metal/grunge
tracks from Chill (LE+) to their correct high-energy-negative positions.

## Artist-Cluster Observations

### Fictional-ZincWing (Fictional-Kw-3ff0f449, Fictional-Kw-e9783d09, Fictional-Kw-5c60ae4f, Fictional-Kw-b03e2ee8, Junkhead, Fictional-Kw-ec602af0)

Six tracks now deeply tagged. Consistent profile: {Aggressive, Anguished, Brooding, Dark,
Depressive, Resigned}. Distinguishing markers: Groovy (Fictional-Kw-5c60ae4f only), Mysterious
(Junkhead, Fictional-Kw-ec602af0), Tense (Fictional-Kw-5c60ae4f, Fictional-Kw-b03e2ee8, Junkhead).

### Fictional-JasperWarden (Dammit, Not-Now, Home-Is-Such-A-Lonely-Place)

Two punk tracks gained chaotic/explosive punk profiles; HISALP stands apart as an
emotional/introspective outlier. Blink now spans HE- (Dammit/Not-Now) to LE- (HISALP).

### Fictional-EmeraldWarden/SSBU (Fictional-Kw-57d292fc, Fictional-Kw-4efe3c91, Fictional-Kw-a2ce73b7, Fictional-Kw-e3022248, Out-of-Time, Fictional-Kw-03eb266a, Crash-in-the-Dark-Night, King-Bowser)

Systematic correction: all dropped Nostalgic, all gained Heroic/Triumphant/Macabre.
These OST tracks now consistently carry {Determined, Energetic, Epic, Focused, Hardworking,
Heroic, Macabre, Triumphant} — a clear "boss battle" archetype emerges.

### Fictional-QuartzRidge (Failure, Fictional-Kw-4c7e4c3b, You)

Three tracks, three Chill→dark corrections. Common profile: {Aggressive, Depressive,
Desperate, Heartbreak}. Failure carries the most moods (13), You is the darkest (Brooding,
Tense).

## New Sliced Compilations (10)

| Base                                  | Parts | Mood Profile                                                                                |
| ------------------------------------- | ----- | ------------------------------------------------------------------------------------------- |
| CYBERPUNK-BEATS                       | 21    | Aggressive, Chaotic, Dark, Energetic, Explosive, Frenzy, Furious, Hardworking               |
| CYBERPUNK-METAL-V3                    | 21    | Aggressive, Chaotic, Danceful, Dark, Defiant, Energetic, Gritty, Rebellious                 |
| Fictional-EmeraldWarden-Bloodwave-Halloween-Disco | 20    | Chaotic, Dark, Ecstatic, Frenzy, Macabre, Playful, Surreal, Suspenseful                     |
| Fictional-SapphireOracle-FORRO-TRIBUTE                     | 19    | Chaotic, Chill, Danceful, Ecstatic, Groovy, Nostalgic, Playful, Tender                      |
| EGYPTIAN-METAL-BEATS-V1               | 21    | Adventurous, Aggressive, Defiant, Determined, Energetic, Explosive, Hardworking, Triumphant |
| Relaxing-Medieval-Music-with-Rain     | 22    | Chill, Contemplative, Cozy, Emotional, Focused, Optimistic, Peaceful, Relaxed…              |
| Relaxing-Fictional-CrystalBell-Twilight-Fictional-ZincNeedless      | 15    | Contemplative, Cozy, Introspective, Meditative, Melancholic, Nostalgic, Peaceful, Relaxed…  |
| ANIME-ROCK-V1                         | 21    | Adventurous, Determined, Ecstatic, Focused, Frenzy, Hardworking, Heroic, Optimistic…        |
| it-was-a-hard-day-rest-well-(Fictional-CrystalBell)   | 60    | Cozy, Introspective, Melancholic, Peaceful, Relaxed, Serene, Sleepy, Spiritual…             |
| singled-80s-japanese-city-pop         | 19    | Bittersweet, Chill, Emotional, Nostalgic, Romantic, Tender, Upbeat, Wistful…                |

Largest compilation: **it-was-a-hard-day-rest-well** at 60 parts (1hr+ ambient Fictional-CrystalBell).

---

## Technical Notes

- **HTML label extraction bug fixed:** Sliced and singles HTMLs had multi-line `<span>` tags
  with embedded newlines. Fixed with `re.sub(r'\s+', ' ', text).strip()` normalization.
- **Sliced base name mapping:** HTML labels omit the `-part` suffix present in JS keys.
  Mapping requires stripping `-part$` before display-name generation.
