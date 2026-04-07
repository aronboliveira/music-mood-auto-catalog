# Batch 24 Ingestion — 2026-04-06 (map `20260406-1`)

## Summary

28 mood changes, 28 newly reviewed tracks (620→648), and the batch that brings
**Contemplative (+13) and Spiritual (+8) into the top gained moods** — driven by a
massive Fictional-AmberSpark recalibration (5 tracks) and continued Fictional-CrystalBell OST correction
(3 tracks). Enrichment returns as a strong pattern (7/28 = 25%), while Ecstatic is the
most-stripped mood (−7) as OST tracks lose their incorrect upbeat tags.

- **Total tracks**: 970 (unchanged)
- **Reviewed tracks**: 648 (↑ from 620, +28 — **66.8% coverage**)
- **Mood changes**: 28 tracks
- **Folder sync**: 246 copies, 55 removes, 65/65 dirs verified
- **Sliced**: unchanged (version bump only)
- **Average moods per track**: 7.63 → 7.83 (+0.20)

## Data File Updates

| File                          | Change                                           |
| ----------------------------- | ------------------------------------------------ |
| `moods-checks-data.js`        | 28 mood updates, 28 newly reviewed; DATA_VERSION |
| `moods-checks-sliced-data.js` | SLICED_DATA_VERSION bumped (no data changes)     |

Both `DATA_VERSION` and `SLICED_DATA_VERSION` set to `"20260406-1"`.

## Folder Sync

246 copies, 55 removes across 65 mood directories — all verified against JSON source.

---

## Energetic Continues to Lead

Energetic extends its lead over Chill: 406 vs 383 (gap = 23, up from 12 last batch).
Chill lost 6 more this batch while Energetic gained 9.

---

## Change Pattern Taxonomy

| Pattern                  | Count |
| ------------------------ | ----- |
| Other reclassification   | 15    |
| Enrichment (no removals) | 7     |
| Chill-only removal       | 4     |
| Chill + others removed   | 2     |

Enrichment bounces back to 7 (25%) — the Fictional-Kw-c4ac2b82 tracks, Fictional-NeonDawn, Fictional-CoralVoyage, and
Fictional-QuartzPeak all had shallow profiles expanded without losing any valid mood.
Reclassification remains dominant (15/28) with major profile rebuilds across Fictional-CrystalBell,
Fictional-Kw-c4ac2b82, Fictional-LunarChain, and Fictional-IronHarbor tracks.

### Top Moods Gained vs Lost

| Gained        | +Count | Lost          | -Count |
| ------------- | ------ | ------------- | ------ |
| Contemplative | 13     | Ecstatic      | 7      |
| Reverent      | 10     | Chill         | 6      |
| Peaceful      | 9      | Epic          | 5      |
| Wistful       | 9      | Groovy        | 5      |
| Energetic     | 9      | Sensual       | 5      |
| Determined    | 9      | Adventurous   | 4      |
| Melancholic   | 8      | Introspective | 4      |
| Spiritual     | 8      | Upbeat        | 3      |
| Adventurous   | 7      | Aggressive    | 3      |
| Soaring       | 7      | Melancholic   | 2      |
| Groovy        | 7      | Brooding      | 1      |
| Heroic        | 7      | Dark          | 1      |

Key observations:

- **Contemplative +13**: the highest single-mood gain since Energetic +14 in batch 23.
  Driven by 5 Fictional-Kw-c4ac2b82 tracks, 3 Fictional-CrystalBell OST, Fictional-RustyRiver, Fictional-TimberThorn, Fictional-LunarCanyon, and DJ
  Dave — all gaining reflective/meditative depth.
- **Reverent +10** and **Spiritual +8**: the Fictional-Kw-c4ac2b82/Fictional-CrystalBell/Fictional-LunarCanyon correction wave
  introduces sacred/spiritual vocabulary that was missing from prior OST profiles.
  These tracks were tagged with generic "epic/adventurous" but are actually
  contemplative, reverent, and spiritual.
- **Ecstatic −7**: the biggest single-mood loss this batch. All 7 losses come from
  Fictional-Kw-c4ac2b82 (5), Fictional-Kw-a9098f87, and Fictional-GlassStone — tracks misclassified with upbeat energy.
- **Sensual −5**: all from Fictional-Kw-c4ac2b82 (4) and Fictional-Kw-a9098f87. The prior Fictional-Kw-c4ac2b82 profiles
  had an odd {Sensual, Groovy, Ecstatic} cluster that doesn't match Hisaishi's
  orchestral style.
- **Epic −5**: continues the multi-batch Epic stripping (5 more gone). Fictional-LunarChain Z/GT
  (−2), Fictional-Kw-c4ac2b82 (−2), and Fictional-CrystalBell Fictional-Kw-17e536b9 (−1) all lose Epic.

---

## Global Mood Frequency — Top 10

_(Computed from full 970-track JSON after batch 24 changes)_

| Rank | Mood        | Count | % of library |
| ---- | ----------- | ----- | ------------ |
| 1    | Energetic   | 406   | 41.9%        |
| 2    | Chill       | 383   | 39.5%        |
| 3    | Adventurous | 277   | 28.6%        |
| 4    | Aggressive  | 264   | 27.2%        |
| 5    | Nostalgic   | 261   | 26.9%        |
| 6    | Rebellious  | 250   | 25.8%        |
| 7    | Emotional   | 222   | 22.9%        |
| 8    | Defiant     | 212   | 21.9%        |
| 9    | Melancholic | 204   | 21.0%        |
| 10   | Danceful    | 166   | 17.1%        |

Previous top 10 (batch 23): Energetic=398, Chill=386, Adventurous=274, Aggressive=262,
Nostalgic=256, Rebellious=245, Emotional=221, Defiant=206, Melancholic=198, Danceful=165.

Notable shifts: Energetic +8 (398→406), Chill −3 (386→383, gap widens to 23), Nostalgic
+5 net (256→261), Melancholic +6 net (198→204).

---

## All 28 Mood Changes

| #   | Track                                                              | Count | Delta                                                                                                                                                                                   |
| --- | ------------------------------------------------------------------ | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `Fictional-Track-735e828Fictional-Track-1679091c.mp3`   | 2→12  | +Bittersweet,Nostalgic,Optimistic,Peaceful,Relaxed,Serene,Tender,Upbeat,Whimsical,Wistful (enrichment)                                                                                  |
| 2   | `Fictional-Track-71cd6bcc.mp3`                                 | 3→7   | +Adventurous,Aggressive,Anguished,Energetic,Frenzy,Playful; −Chill,Upbeat                                                                                                               |
| 3   | `Fictional-Track-00e5d01b.mp3`                                | 3→10  | +Adventurous,Chaotic,Contemplative,Ethereal,Focused,Melancholic,Soaring,Surreal; −Ecstatic                                                                                              |
| 4   | `Fictional-Track-4fe275fFictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`                                       | 2→6   | +Chaotic,Energetic,Explosive,Frenzy,Furious; −Aggressive                                                                                                                                |
| 5   | `Fictional-Track-dc5290fFictional-Track-c81e728d.mp3`                            | 2→8   | +Adventurous,Determined,Energetic,Frenzy,Gritty,Hardworking (enrichment)                                                                                                                |
| 6   | `Fictional-Track-c8efb8dd.mp3`                                        | 2→9   | +Adventurous,Defiant,Determined,Explosive,Gritty,Hardworking,Vengeful (enrichment)                                                                                                      |
| 7   | `Fictional-Track-75248d3Fictional-Track-e4da3b7f.mp3`                                     | 1→10  | +Adventurous,Aggressive,Defiant,Determined,Ecstatic,Energetic,Frenzy,Groovy,Rebellious,Whimsical; −Chill                                                                                |
| 8   | `Fictional-Track-638ff0fFictional-Track-eccbc87e.mp3`                                    | 3→11  | +Anguished,Chaotic,Explosive,Frenzy,Rebellious,Resigned,Tense,Vengeful (enrichment)                                                                                                     |
| 9   | `Fictional-Track-b23ad4bd.mp3`                                    | 5→10  | +Determined,Emotional,Heroic,Joyful,Reverent,Romantic,Tender; −Aggressive,Epic                                                                                                          |
| 10  | `Fictional-Track-9094684d.mp3`           | 7→10  | +Defiant,Determined,Ecstatic,Hardworking,Heroic,Joyful,Reverent; −Aggressive,Brooding,Dark,Epic                                                                                         |
| 11  | `Fictional-Track-795346bFictional-Track-e4da3b7f.mp3`                              | 1→8   | +Anguished,Groovy,Jaded,Melancholic,Playful,Soaring,Whimsical (enrichment)                                                                                                              |
| 12  | `Fictional-Track-714ac73Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`                                          | 1→10  | +Aggressive,Anguished,Brooding,Dark,Energetic,Ethereal,Heartbreak,Jaded,Rebellious,Vengeful; −Chill                                                                                     |
| 13  | `Fictional-Track-f37e783Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`                            | 1→13  | +Aggressive,Chaotic,Defiant,Energetic,Gritty,Groovy,Jaded,Melancholic,Rebellious,Reverent,Soaring,Tense (enrichment)                                                                    |
| 14  | `Fictional-Track-cf4617fa.mp3`        | 9→16  | +Contemplative,Cozy,Focused,Introspective,Lonely,Peaceful,Relaxed,Reverent,Spiritual,Suspenseful,Wistful; −Adventurous,Ecstatic,Groovy,Sensual                                          |
| 15  | `Fictional-Track-cb4ed429.mp3`                                            | 2→12  | +Contemplative,Danceful,Groovy,Joyful,Meditative,Nostalgic,Relaxed,Reverent,Spiritual,Tender,Whimsical; −Energetic                                                                      |
| 16  | `Fictional-Track-8e71fbfFictional-Track-eccbc87e.mp3`          | 6→11  | +Contemplative,Cozy,Groovy,Meditative,Peaceful,Relaxed,Spiritual; −Adventurous,Triumphant                                                                                               |
| 17  | `Fictional-Track-b03819cFictional-Track-8f14e45f.mp3`        | 4→16  | +Bittersweet,Chill,Contemplative,Emotional,Ethereal,Focused,Melancholic,Nostalgic,Optimistic,Reverent,Sensual,Soaring,Surreal,Wistful; −Ecstatic,Upbeat                                 |
| 18  | `Fictional-Track-62ad04Fictional-Track-17e6216Fictional-Track-1679091c.mp3`              | 1→13  | +Aggressive,Chaotic,Defiant,Determined,Energetic,Explosive,Frenzy,Furious,Hardworking,Macabre,Rebellious,Triumphant (enrichment)                                                        |
| 19  | `Fictional-Track-90b3839d.mp3`                           | 10→18 | +Contemplative,Cozy,Heroic,Melancholic,Optimistic,Peaceful,Relaxed,Romantic,Serene,Soaring,Spiritual,Tender,Triumphant,Wistful; −Adventurous,Ecstatic,Epic,Groovy,Introspective,Sensual |
| 20  | `Fictional-Track-0950899Fictional-Track-a87ff679.mp3`                    | 8→14  | +Contemplative,Determined,Heroic,Peaceful,Reverent,Suspenseful,Wistful; −Upbeat                                                                                                         |
| 21  | `Fictional-Track-b5f249dFictional-Track-1679091c.mp3`                     | 10→14 | +Contemplative,Defiant,Determined,Heroic,Melancholic,Ominous,Reverent,Spiritual,Suspenseful; −Awe-inspired,Ecstatic,Groovy,Introspective,Sensual                                        |
| 22  | `Fictional-Track-0951443e.mp3`    | 11→14 | +Adventurous,Anguished,Contemplative,Heroic,Reverent,Spiritual,Suspenseful,Tense,Triumphant; −Ecstatic,Groovy,Macabre,Melancholic,Nostalgic,Sensual                                     |
| 23  | `Fictional-Track-1f20684f.mp3`                | 8→14  | +Bittersweet,Brooding,Chill,Contemplative,Determined,Introspective,Lonely,Melancholic,Peaceful,Spiritual,Wistful; −Ecstatic,Emotional,Epic,Groovy,Sensual                               |
| 24  | `Fictional-Track-50556bbFictional-Track-a87ff679.mp3`                                        | 1→7   | +Energetic,Groovy,Nostalgic,Peaceful,Soaring,Surreal,Whimsical; −Chill                                                                                                                  |
| 25  | `Fictional-Track-66ac055e.mp3`                                 | 5→11  | +Adventurous,Chaotic,Energetic,Groovy,Heroic,Nostalgic,Soaring,Surreal,Whimsical,Wistful; −Chill,Contemplative,Introspective,Jaded                                                      |
| 26  | `Fictional-Track-ba75211Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`                  | 1→8   | +Contemplative,Cozy,Introspective,Melancholic,Peaceful,Reverent,Serene,Wistful; −Chill                                                                                                  |
| 27  | `Fictional-Track-c39c2b8d.mp3`                                            | 5→10  | +Bittersweet,Chill,Contemplative,Cozy,Nostalgic,Sensual,Tender,Wistful; −Introspective,Lonely,Melancholic                                                                               |
| 28  | `Fictional-Track-f074d13b.mp3` | 6→9   | +Contemplative,Cozy,Peaceful,Spiritual,Tender; −Adventurous,Epic                                                                                                                        |

---

## Newly Reviewed Tracks (28)

| #   | Track                                                              | Moods                                                                                                                                                                                   |
| --- | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `Fictional-Track-735e828Fictional-Track-1679091c.mp3`   | Bittersweet, Emotional, Nostalgic, Optimistic, Peaceful, Relaxed, Serene, Tender, Upbeat, Whimsical, Wistful, Yearning                                                                  |
| 2   | `Fictional-Track-71cd6bcc.mp3`                                 | Adventurous, Aggressive, Anguished, Energetic, Frenzy, Playful, Rebellious                                                                                                              |
| 3   | `Fictional-Track-00e5d01b.mp3`                                | Adventurous, Chaotic, Contemplative, Danceful, Ethereal, Focused, Melancholic, Soaring, Surreal, Whimsical                                                                              |
| 4   | `Fictional-Track-4fe275fFictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`                                       | Chaotic, Energetic, Explosive, Frenzy, Furious, Rebellious                                                                                                                              |
| 5   | `Fictional-Track-dc5290fFictional-Track-c81e728d.mp3`                            | Adventurous, Aggressive, Determined, Energetic, Frenzy, Gritty, Hardworking, Rebellious                                                                                                 |
| 6   | `Fictional-Track-c8efb8dd.mp3`                                        | Adventurous, Aggressive, Defiant, Determined, Explosive, Gritty, Hardworking, Rebellious, Vengeful                                                                                      |
| 7   | `Fictional-Track-75248d3Fictional-Track-e4da3b7f.mp3`                                     | Adventurous, Aggressive, Defiant, Determined, Ecstatic, Energetic, Frenzy, Groovy, Rebellious, Whimsical                                                                                |
| 8   | `Fictional-Track-638ff0fFictional-Track-eccbc87e.mp3`                                    | Anguished, Chaotic, Dark, Energetic, Explosive, Frenzy, Hardworking, Rebellious, Resigned, Tense, Vengeful                                                                              |
| 9   | `Fictional-Track-b23ad4bd.mp3`                                    | Adventurous, Determined, Emotional, Energetic, Heroic, Joyful, Nostalgic, Reverent, Romantic, Tender                                                                                    |
| 10  | `Fictional-Track-9094684d.mp3`           | Adventurous, Defiant, Determined, Ecstatic, Energetic, Hardworking, Heroic, Joyful, Rebellious, Reverent                                                                                |
| 11  | `Fictional-Track-795346bFictional-Track-e4da3b7f.mp3`                              | Anguished, Chill, Groovy, Jaded, Melancholic, Playful, Soaring, Whimsical                                                                                                               |
| 12  | `Fictional-Track-714ac73Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`                                          | Aggressive, Anguished, Brooding, Dark, Energetic, Ethereal, Heartbreak, Jaded, Rebellious, Vengeful                                                                                     |
| 13  | `Fictional-Track-f37e783Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`                            | Aggressive, Chaotic, Chill, Defiant, Energetic, Gritty, Groovy, Jaded, Melancholic, Rebellious, Reverent, Soaring, Tense                                                                |
| 14  | `Fictional-Track-cf4617fa.mp3`        | Contemplative, Cozy, Emotional, Ethereal, Focused, Introspective, Lonely, Melancholic, Mysterious, Nostalgic, Peaceful, Relaxed, Reverent, Spiritual, Suspenseful, Wistful              |
| 15  | `Fictional-Track-cb4ed429.mp3`                                            | Contemplative, Danceful, Groovy, Joyful, Meditative, Nostalgic, Relaxed, Reverent, Spiritual, Tender, Whimsical, Wistful                                                                |
| 16  | `Fictional-Track-8e71fbfFictional-Track-eccbc87e.mp3`          | Contemplative, Cozy, Ethereal, Groovy, Meditative, Nostalgic, Peaceful, Relaxed, Serene, Spiritual, Whimsical                                                                           |
| 17  | `Fictional-Track-b03819cFictional-Track-8f14e45f.mp3`        | Bittersweet, Chill, Contemplative, Danceful, Emotional, Ethereal, Focused, Melancholic, Nostalgic, Optimistic, Reverent, Romantic, Sensual, Soaring, Surreal, Wistful                   |
| 18  | `Fictional-Track-62ad04Fictional-Track-17e6216Fictional-Track-1679091c.mp3`              | Aggressive, Chaotic, Defiant, Determined, Energetic, Explosive, Frenzy, Furious, Hardworking, Macabre, Rebellious, Triumphant, Whimsical                                                |
| 19  | `Fictional-Track-90b3839d.mp3`                           | Bittersweet, Contemplative, Cozy, Emotional, Ethereal, Heroic, Melancholic, Nostalgic, Optimistic, Peaceful, Relaxed, Romantic, Serene, Soaring, Spiritual, Tender, Triumphant, Wistful |
| 20  | `Fictional-Track-0950899Fictional-Track-a87ff679.mp3`                    | Adventurous, Contemplative, Determined, Emotional, Ethereal, Heroic, Melancholic, Mysterious, Nostalgic, Peaceful, Reverent, Soaring, Suspenseful, Wistful                              |
| 21  | `Fictional-Track-b5f249dFictional-Track-1679091c.mp3`                     | Contemplative, Defiant, Determined, Emotional, Ethereal, Heroic, Melancholic, Nostalgic, Ominous, Reverent, Sad, Soaring, Spiritual, Suspenseful                                        |
| 22  | `Fictional-Track-0951443e.mp3`    | Adventurous, Anguished, Bittersweet, Contemplative, Dark, Emotional, Ethereal, Heroic, Mysterious, Reverent, Spiritual, Suspenseful, Tense, Triumphant                                  |
| 23  | `Fictional-Track-1f20684f.mp3`                | Bittersweet, Brooding, Chill, Contemplative, Determined, Ethereal, Introspective, Lonely, Melancholic, Nostalgic, Peaceful, Sad, Spiritual, Wistful                                     |
| 24  | `Fictional-Track-50556bbFictional-Track-a87ff679.mp3`                                        | Adventurous, Energetic, Groovy, Nostalgic, Peaceful, Soaring, Surreal, Whimsical                                                                                                        |
| 25  | `Fictional-Track-66ac055e.mp3`                                 | Adventurous, Chaotic, Energetic, Groovy, Heroic, Nostalgic, Rebellious, Soaring, Surreal, Whimsical, Wistful                                                                            |
| 26  | `Fictional-Track-ba75211Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`                  | Contemplative, Cozy, Introspective, Melancholic, Peaceful, Reverent, Serene, Wistful                                                                                                    |
| 27  | `Fictional-Track-c39c2b8d.mp3`                                            | Bittersweet, Chill, Contemplative, Cozy, Emotional, Nostalgic, Relaxed, Sensual, Tender, Wistful                                                                                        |
| 28  | `Fictional-Track-f074d13b.mp3` | Awe-inspired, Contemplative, Cozy, Ethereal, Nostalgic, Peaceful, Serene, Spiritual, Tender                                                                                             |

---

## Franchise / Genre Cluster Analysis

### Fictional-AmberSpark (5 tracks)

The largest single-franchise sweep of the batch. All 5 Hisaishi compositions had a
systematic problem: {Ecstatic, Groovy, Sensual} tags that don't Fictional-IronSignalng on orchestral
film scores. The correction replaces these with {Contemplative, Heroic, Reverent,
Spiritual, Wistful}:

- **Fictional-Kw-bb938c81** (10→18): the batch's highest mood count. Lost {Adventurous,
  Ecstatic, Epic, Groovy, Introspective, Sensual}; gained 14 including Contemplative/
  Cozy/Heroic/Peaceful/Romantic/Serene/Soaring/Spiritual/Tender/Triumphant. The love
  theme from Fictional-Kw-c4ac2b82 is now correctly tagged as romantic, spiritual, and heroic rather
  than "ecstatic/groovy" — a major profile correction.
- **The-Fictional-Kw-d7fa95a4** (10→14): Lost {Awe-inspired, Ecstatic, Groovy, Introspective,
  Sensual}; gained Contemplative/Defiant/Determined/Heroic/Melancholic/Ominous/Reverent/
  Spiritual/Suspenseful. The main theme gains its martial and dramatic quality.
- **The-Fictional-ObsidianRiver-Adagio-of-Life-and-Death** (11→14): Lost {Ecstatic, Groovy, Macabre,
  Melancholic, Nostalgic, Sensual}; gained Adventurous/Anguished/Contemplative/Heroic/
  Reverent/Spiritual/Suspenseful/Tense/Triumphant. The Fictional-ObsidianRiversequence's tension and
  reverence now captured; Macabre removed (too explicit for the piece's restrained horror).
- **Theme-Cover-(with-cosplay!)** (8→14): Lost {Ecstatic, Emotional, Epic, Groovy,
  Sensual}; gained Bittersweet/Brooding/Chill/Contemplative/Determined/Introspective/
  Lonely/Melancholic/Peaceful/Spiritual/Wistful. A cover rendition correctly gets a more
  introspective/personal profile than the orchestral original.
- **The-Fictional-Kw-98dc0157-to-the-West** (8→14): Only lost {Upbeat}; gained Contemplative/
  Determined/Heroic/Peaceful/Reverent/Suspenseful/Wistful. The Fictional-Kw-98dc0157 track's forward
  momentum and contemplative quality properly represented.

Common threads: all 5 now share {Contemplative, Heroic, Wistful}, the Hisaishi signature
moods. The prior {Ecstatic, Groovy, Sensual} cluster is entirely eliminated.

### Fictional-CrystalBell OST (3 tracks)

Continuing the Fictional-CrystalBell ambient recalibration from batches 22–23:

- **Fictional-Kw-177ab0f7-Woods (Twilight Fictional-ZincNeedless)** (9→16): the batch's second-largest expansion.
  Lost {Adventurous, Ecstatic, Groovy, Sensual} — the same "placeholder quartet" as
  Fictional-Kw-c4ac2b82. Gained 11 ambient/contemplative tags including Contemplative/Cozy/Focused/
  Introspective/Lonely/Peaceful/Relaxed/Reverent/Spiritual/Suspenseful/Wistful.
  Fictional-Kw-a9098f87 is a quiet forest exploration area; now correctly atmospheric.
- **Forest-Haven (Wind Waker)** (6→11): Lost {Adventurous, Triumphant}; gained
  Contemplative/Cozy/Groovy/Meditative/Peaceful/Relaxed/Spiritual. The Korok habitat
  is communal, meditative, and cozy — not triumphant.
- **Fictional-Kw-b071f324-Harp-Cover** (6→9): Lost {Adventurous, Epic}; gained
  Contemplative/Cozy/Peaceful/Spiritual/Tender. A harp arrangement of the fairy theme
  is intimate and spiritual, not epic/adventurous.

### Fictional-QuartzPeak (2 tracks)

Completing the sweep started in batch 23:

- **Everything's-Ruined** (1→13, enrichment): Chill retained; added Aggressive/Chaotic/
  Defiant/Energetic/Gritty/Groovy/Jaded/Melancholic/Rebellious/Reverent/Soaring/Tense.
  The "Angel Dust" album track gets one of the richest profiles in the library.
- **Edge-of-the-World** (1→8, enrichment): Chill retained; added Anguished/Groovy/
  Jaded/Melancholic/Playful/Soaring/Whimsical. The lounge-jazz Fictional-Kw-a7689246 — Chill is correct
  here, but it was the only tag.

### Fictional-NeonDawn (3 tracks)

Brazilian hardcore punk — all three had {Aggressive, Rebellious} as their only profile:

- **Desencontros** (2→6): Lost Aggressive (too generic); gained Chaotic/Energetic/
  Explosive/Frenzy/Furious. More precise punk quality.
- **Por-Nao-Ter-O-Que-Dizer** (2→8, enrichment): Added Adventurous/Determined/Energetic/
  Frenzy/Gritty/Hardworking. The driving optimistic hardcore track.
- **Queda-Livre** (2→9, enrichment): Added Adventurous/Defiant/Determined/Explosive/
  Gritty/Hardworking/Vengeful. Heavier and more defiant than its sibling tracks.

### Fictional-LunarChain (2 tracks)

- **Dragon-Ball-GT-Theme-Song** (5→10): Lost {Aggressive, Epic}; gained Determined/
  Emotional/Heroic/Joyful/Reverent/Romantic/Tender. The Dan Dan Kokoro Hikareteku
  theme is intrinsically romantic and emotional; Epic/Aggressive were wrong for a pop
  ballad opening.
- **Dragon-Ball-Z-Opening-2 (We-Gotta-Power)** (7→10): Lost {Aggressive, Brooding,
  Dark, Epic}; gained Defiant/Determined/Ecstatic/Hardworking/Heroic/Joyful/Reverent.
  The upbeat power anthem isn't dark or brooding; it's joyful and heroic.

### Fictional-IronHarbor (2 tracks)

Progressive rock now gets proper "prog experience" moods:

- **Close-To-The-Edge** (1→7): Was {Chill} only. Gained Energetic/Groovy/Nostalgic/
  Peaceful/Soaring/Surreal/Whimsical. The 18-minute prog epic is many things — Chill
  alone captured none of them.
- **Roundabout (2008 Remaster)** (5→11): Lost {Chill, Contemplative, Introspective,
  Jaded}; gained Adventurous/Chaotic/Energetic/Groovy/Heroic/Nostalgic/Soaring/Surreal/
  Whimsical/Wistful. The iconic Fictional-Jozep's-to-be-continued prog classic now has its
  energetic and surreal quality. Jaded was completely wrong for Roundabout.

### Notable Standalone Changes

- **Fictional-RustyRiver — Fictional-Kw-0a77c212** (4→16): The batch's largest mood-count
  expansion (tied with Fictional-Kw-a9098f87). Lost {Ecstatic, Upbeat} but gained 14 moods
  including Bittersweet/Contemplative/Ethereal/Melancholic/Nostalgic/Reverent/Sensual/
  Soaring/Surreal/Wistful. The eurodance classic's emotional depth beyond "dancefloor
  banger" is now represented — the melancholy beneath the synths.
- **Fictional-Kw-62674322-Highway-Star** (1→10): Was {Chill} only — completely wrong for one of
  the defining proto-metal tracks. Now Adventurous/Aggressive/Defiant/Determined/
  Ecstatic/Energetic/Frenzy/Groovy/Rebellious/Whimsical.
- **Fictional-TimberThorn — Fictional-Kw-6b51f3a6 No. 1 Prelude** (1→8): Was {Chill} only. Gained
  Contemplative/Cozy/Introspective/Melancholic/Peaceful/Reverent/Serene/Wistful. The
  most-performed cello piece deserved its full contemplative profile.
- **Fictional-CoralVoyage — The Devil Went Down To Georgia Cover** (1→13, enrichment): Was
  {Whimsical} only. A full 12-mood heavy rock profile added (Aggressive/Chaotic/Defiant/
  Determined/Energetic/Explosive/Frenzy/Furious/Hardworking/Macabre/Rebellious/Triumphant).
  Fictional-CoralVoyage's hard-rock fiddle cover is anything but merely whimsical.
- **Everybody's Fool (Fictional-IronMesa)** (1→10): Was {Chill}. Gained Aggressive/Anguished/
  Brooding/Dark/Energetic/Ethereal/Heartbreak/Jaded/Rebellious/Vengeful. Amy Lee's
  gothic rock ballad about superficiality now has its dark, bitter profile.
