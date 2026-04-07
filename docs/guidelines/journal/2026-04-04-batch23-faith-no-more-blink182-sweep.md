# Batch 23 Ingestion — 2026-04-04 (map `20260404-2`)

## Summary

25 mood changes, 25 newly reviewed tracks (595→620), and the batch where
**Energetic overtakes Chill at #1** for the first time (398 vs 386). Dominant
clusters: Fictional-QuartzPeak (4 tracks), Fictional-JasperWarden (3), SSBU (3), Fictional-CrystalBell OST (2), Fictional-CoralVoyage (1).
The defining pattern is **reclassification from shallow placeholders to genre-accurate
rock profiles** — 8 more Chill-only removals plus 15 full reclassifications.

- **Total tracks**: 970 (unchanged)
- **Reviewed tracks**: 620 (↑ from 595, +25 — **63.9% coverage**)
- **Mood changes**: 25 tracks
- **Folder sync**: 65/65 dirs verified OK
- **Sliced**: unchanged (version bump only)
- **Average moods per track**: 7.43 → 7.63 (+0.20)

## Data File Updates

| File                          | Change                                           |
| ----------------------------- | ------------------------------------------------ |
| `moods-checks-data.js`        | 25 mood updates, 25 newly reviewed; DATA_VERSION |
| `moods-checks-sliced-data.js` | SLICED_DATA_VERSION bumped (no data changes)     |

Both `DATA_VERSION` and `SLICED_DATA_VERSION` set to `"20260404-2"`.

## Folder Sync

65/65 mood directories verified against JSON source (0 mismatched).

---

## Big Milestone: Energetic Overtakes Chill

After 22 batches in which Chill held #1 in global mood frequency, **Energetic
surpasses it this batch**: Energetic 398 (+14 net), Chill 386 (-9 net, gap = −12).
This was anticipated as inevitable after the Chill-only removal campaign that began
in batch 18, but this is the first batch where the inversion is confirmed.

The implication: the library's dominant mood posture is now energetic rather than
laid-back. Chill tracks are being refined to keep their correct chill assignments;
what's being stripped are the lazy Chill-as-catch-all placeholders.

---

## Change Pattern Taxonomy

| Pattern                       | Count |
| ----------------------------- | ----- |
| Other reclassification        | 15    |
| Chill-only removal (3+ added) | 8     |
| Chill + others removed        | 1     |
| Enrichment (no removals)      | 1     |

**Reclassification dominates** (15/25 = 60%) — tracks are not just losing a bad
placeholder but having their entire mood profile rebuilt. This accompanies the Faith
No More, Fictional-JasperWarden, and SSBU sweeps where prior entries had 1–2 obviously wrong moods.
Chill-only removal continues its long campaign (9 total Chill losses including the
multi-removal case).

### Top Moods Gained vs Lost

| Gained      | +Count | Lost          | -Count |
| ----------- | ------ | ------------- | ------ |
| Energetic   | 14     | Chill         | 9      |
| Aggressive  | 11     | Nostalgic     | 5      |
| Frenzy      | 10     | Epic          | 3      |
| Rebellious  | 10     | Adventurous   | 3      |
| Defiant     | 9      | Romantic      | 2      |
| Soaring     | 7      | Triumphant    | 2      |
| Adventurous | 6      | Soaring       | 1      |
| Dark        | 6      | Aggressive    | 1      |
| Determined  | 6      | Introspective | 1      |
| Groovy      | 6      | Melancholic   | 1      |
| Hardworking | 6      | Emotional     | 1      |
| Anguished   | 5      | Sad           | 1      |
| Optimistic  | 5      | Cozy          | 1      |
| Tender      | 5      | Yearning      | 1      |
| Upbeat      | 5      | Anguished     | 1      |

Key observations:

- **Energetic +14** is the largest single-mood gain in any batch to date. Driven by
  rock retaggings (Fictional-QuartzPeak, Fictional-JasperWarden, Fictional-CoralVoyage, Fictional-ScarletPrism, Flat-On-the-Floor,
  Fictional-Kw-bc9516a7) where Energetic was absent from prior placeholders.
- **Chill −9**: the Chill-stripping campaign continues. 8 Chill-only removals + 1 with
  Chill alongside Cozy. The vast majority of removed Chill entries are confirmed
  non-ambient tracks that were lazy-tagged.
- **Nostalgic −5** and **Epic −3**: the SSBU Epic+Nostalgic removal pattern continues.
  Dragon-Ball-FighterZ, Fist-Bump, and Jet-Black-Wings all shed both or one of these —
  game tracks were over-tagged with "retro nostalgia" moods that don't suit their
  combat/dynamic characters.
- **Adventurous −3**: Fictional-CrystalBell OST corrections (Earth-God's-Lyric, Sun's-Song) and
  Game-Over all lost Adventurous when the tracks are clearly not adventurous in character.

---

## Global Mood Frequency — Top 10

_(Computed from full 970-track JSON after batch 23 changes)_

| Rank | Mood        | Count | % of library |
| ---- | ----------- | ----- | ------------ |
| 1    | Energetic   | 398   | 41.0%        |
| 2    | Chill       | 386   | 39.8%        |
| 3    | Adventurous | 274   | 28.2%        |
| 4    | Aggressive  | 262   | 27.0%        |
| 5    | Nostalgic   | 256   | 26.4%        |
| 6    | Rebellious  | 245   | 25.3%        |
| 7    | Emotional   | 221   | 22.8%        |
| 8    | Defiant     | 206   | 21.2%        |
| 9    | Melancholic | 198   | 20.4%        |
| 10   | Danceful    | 165   | 17.0%        |

Previous top 10 (batch 22): Chill=392, Energetic=384, Adventurous=271, Nostalgic=258,
Aggressive=252, Rebellious=235, Emotional=219, Defiant=197, Melancholic=195, Danceful=161.

Notable shifts vs batch 22: Energetic +14 (384→398, +1 rank), Chill −6 (392→386, −1
rank), Aggressive +10 (252→262, holds #4), Nostalgic −2 net (258→256).

---

## All 25 Mood Changes

| #   | Track                                                                                         | Count | Delta                                                                                                                              |
| --- | --------------------------------------------------------------------------------------------- | ----- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `Fictional-Track-3c4adb3Fictional-Track-c9f0f895.mp3`                                                                    | 1→11  | +Adventurous,Determined,Energetic,Explosive,Frenzy,Optimistic,Romantic,Soaring,Tender,Upbeat,Yearning; −Chill                      |
| 2   | `Fictional-Track-20060fdf.mp3`                                                                    | 2→10  | +Aggressive,Anguished,Depressive,Heartbreak,Lonely,Melancholic,Nostalgic,Rebellious,Wistful; −Soaring                              |
| 3   | `Fictional-Track-32917b2Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`                                                    | 1→13  | +Aggressive,Brooding,Dark,Defiant,Depressive,Emotional,Energetic,Heartbreak,Melancholic,Rebellious,Sad,Tense,Vengeful; −Romantic   |
| 4   | `Fictional-Track-66d9c8aFictional-Track-eccbc87e.mp3`                                                                     | 2→13  | +Awe-inspired,Danceful,Determined,Ecstatic,Groovy,Optimistic,Playful,Romantic,Soaring,Tender,Upbeat,Yearning; −Aggressive          |
| 5   | `Fictional-Track-f0a743aFictional-Track-8f14e45f.mp3`                                                                    | 1→8   | +Danceful,Determined,Ecstatic,Energetic,Groovy,Romantic,Tender,Upbeat; −Chill                                                      |
| 6   | `Fictional-Track-8930877Fictional-Track-eccbc87e.mp3`                                                                    | 2→8   | +Emotional,Energetic,Optimistic,Reverent,Soaring,Upbeat,Wistful; −Chill                                                            |
| 7   | `Fictional-Track-983b61Fictional-Track-17e6216Fictional-Track-1679091c.mp3`                                                                    | 1→9   | +Aggressive,Energetic,Frenzy,Furious,Gritty,Heartbreak,Jaded,Lonely,Rebellious; −Chill                                             |
| 8   | `Fictional-Track-e295bdc0.mp3`                                                                        | 2→13  | +Adventurous,Awe-inspired,Danceful,Defiant,Determined,Emotional,Energetic,Hardworking,Heroic,Reverent,Triumphant,Whimsical; −Chill |
| 9   | `Fictional-Track-3bd8d7f9.mp3`                                    | 7→10  | +Defiant,Determined,Frenzy,Furious,Hardworking; −Epic,Nostalgic                                                                    |
| 10  | `Fictional-Track-f756f589.mp3`                                | 4→9   | +Awe-inspired,Cozy,Peaceful,Relaxed,Serene,Sleepy,Spiritual; −Adventurous,Triumphant                                               |
| 11  | `Fictional-Track-1ca9d65e.mp3`                                                    | 4→8   | +Bittersweet,Contemplative,Cozy,Groovy,Nostalgic,Relaxed; −Introspective,Melancholic                                               |
| 12  | `Fictional-Track-dd7c9daa.mp3`                                                                    | 3→12  | +Bittersweet,Chill,Contemplative,Cozy,Introspective,Meditative,Melancholic,Nostalgic,Peaceful,Relaxed,Wistful; −Emotional,Romantic |
| 13  | `Fictional-Track-71f9305c.mp3`                                                                      | 1→11  | +Adventurous,Aggressive,Chaotic,Defiant,Energetic,Frenzy,Groovy,Hardworking,Playful,Rebellious,Reverent; −Epic                     |
| 14  | `Fictional-Track-d26660fFictional-Track-c9f0f895.mp3`                                                        | 2→12  | +Aggressive,Anguished,Chaotic,Dark,Energetic,Gritty,Rebellious,Resigned,Suspenseful,Tense,Vengeful; −Sad                           |
| 15  | `Fictional-Track-6df5f41c.mp3`                                                             | 1→11  | +Aggressive,Anguished,Chaotic,Dark,Energetic,Frenzy,Groovy,Introspective,Playful,Rebellious,Reverent; −Chill                       |
| 16  | `Fictional-Track-2e64d8dFictional-Track-eccbc87e.mp3`                                                         | 1→10  | +Adventurous,Aggressive,Anguished,Chaotic,Ecstatic,Energetic,Frenzy,Groovy,Rebellious,Soaring; −Chill                              |
| 17  | `Fictional-Track-2544992Fictional-Track-eccbc87e.mp3`                                   | 7→12  | +Aggressive,Defiant,Frenzy,Hardworking,Heroic,Optimistic,Rebellious; −Epic,Nostalgic                                               |
| 18  | `Fictional-Track-5dc47dee.mp3`                                                                       | 2→11  | +Dark,Explosive,Frenzy,Furious,Gritty,Hardworking,Rebellious,Resigned,Tense,Vengeful; −Chill                                       |
| 19  | `Fictional-Track-9f27a139.mp3`                                                                         | 3→13  | +Adventurous,Aggressive,Dark,Defiant,Explosive,Gritty,Jaded,Rebellious,Resigned,Tense,Triumphant,Vengeful; −Chill,Cozy             |
| 20  | `Fictional-Track-a388361Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`                                                                   | 2→12  | +Adventurous,Aggressive,Anguished,Brooding,Defiant,Energetic,Gritty,Hardworking,Jaded,Soaring,Upbeat; −Yearning                    |
| 21  | `Fictional-Track-ca94a69Fictional-Track-1679091c.mp3`                                                                               | 3→9   | +Chaotic,Dark,Desperate,Energetic,Frenzy,Furious,Macabre,Melancholic; −Adventurous,Nostalgic                                       |
| 22  | `Fictional-Track-9ac5f2cFictional-Track-e4da3b7f.mp3`                                               | 6→9   | +Aggressive,Defiant,Energetic,Frenzy,Heroic,Suspenseful; −Anguished,Nostalgic,Triumphant                                           |
| 23  | `Fictional-Track-99fc033c.mp3` | 2→8   | +Chill,Defiant,Determined,Ominous,Soaring,Suspenseful,Triumphant; −Nostalgic                                                       |
| 24  | `Fictional-Track-85f8aa6f.mp3`                                          | 3→6   | +Cozy,Peaceful,Relaxed,Tender; −Adventurous                                                                                        |
| 25  | `Fictional-Track-65bb18bFictional-Track-a87ff679.mp3`                                                          | 1→13  | +Chill,Cozy,Danceful,Energetic,Focused,Joyful,Optimistic,Peaceful,Relaxed,Serene,Soaring,Tender (pure enrichment, +12)             |

---

## Newly Reviewed Tracks (25)

| #   | Track                                                                                         | Moods                                                                                                                                      |
| --- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | `Fictional-Track-3c4adb3Fictional-Track-c9f0f895.mp3`                                                                    | Adventurous, Determined, Energetic, Explosive, Frenzy, Optimistic, Romantic, Soaring, Tender, Upbeat, Yearning                             |
| 2   | `Fictional-Track-20060fdf.mp3`                                                                    | Aggressive, Anguished, Chill, Depressive, Heartbreak, Lonely, Melancholic, Nostalgic, Rebellious, Wistful                                  |
| 3   | `Fictional-Track-32917b2Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`                                                    | Aggressive, Brooding, Dark, Defiant, Depressive, Emotional, Energetic, Heartbreak, Melancholic, Rebellious, Sad, Tense, Vengeful           |
| 4   | `Fictional-Track-66d9c8aFictional-Track-eccbc87e.mp3`                                                                     | Awe-inspired, Danceful, Determined, Ecstatic, Energetic, Groovy, Optimistic, Playful, Romantic, Soaring, Tender, Upbeat, Yearning          |
| 5   | `Fictional-Track-f0a743aFictional-Track-8f14e45f.mp3`                                                                    | Danceful, Determined, Ecstatic, Energetic, Groovy, Romantic, Tender, Upbeat                                                                |
| 6   | `Fictional-Track-8930877Fictional-Track-eccbc87e.mp3`                                                                    | Emotional, Energetic, Optimistic, Reverent, Romantic, Soaring, Upbeat, Wistful                                                             |
| 7   | `Fictional-Track-983b61Fictional-Track-17e6216Fictional-Track-1679091c.mp3`                                                                    | Aggressive, Energetic, Frenzy, Furious, Gritty, Heartbreak, Jaded, Lonely, Rebellious                                                      |
| 8   | `Fictional-Track-e295bdc0.mp3`                                                                        | Adventurous, Awe-inspired, Danceful, Defiant, Determined, Emotional, Energetic, Epic, Hardworking, Heroic, Reverent, Triumphant, Whimsical |
| 9   | `Fictional-Track-3bd8d7f9.mp3`                                    | Adventurous, Aggressive, Defiant, Determined, Energetic, Frenzy, Furious, Hardworking, Rebellious, Triumphant                              |
| 10  | `Fictional-Track-f756f589.mp3`                                | Awe-inspired, Cozy, Ethereal, Nostalgic, Peaceful, Relaxed, Serene, Sleepy, Spiritual                                                      |
| 11  | `Fictional-Track-1ca9d65e.mp3`                                                    | Bittersweet, Chill, Contemplative, Cozy, Groovy, Jaded, Nostalgic, Relaxed                                                                 |
| 12  | `Fictional-Track-dd7c9daa.mp3`                                                                    | Bittersweet, Chill, Contemplative, Cozy, Introspective, Meditative, Melancholic, Nostalgic, Peaceful, Relaxed, Serene, Wistful             |
| 13  | `Fictional-Track-71f9305c.mp3`                                                                      | Adventurous, Aggressive, Chaotic, Defiant, Energetic, Frenzy, Groovy, Hardworking, Playful, Rebellious, Reverent                           |
| 14  | `Fictional-Track-d26660fFictional-Track-c9f0f895.mp3`                                                        | Aggressive, Anguished, Chaotic, Dark, Energetic, Gritty, Melancholic, Rebellious, Resigned, Suspenseful, Tense, Vengeful                   |
| 15  | `Fictional-Track-6df5f41c.mp3`                                                             | Aggressive, Anguished, Chaotic, Dark, Energetic, Frenzy, Groovy, Introspective, Playful, Rebellious, Reverent                              |
| 16  | `Fictional-Track-2e64d8dFictional-Track-eccbc87e.mp3`                                                         | Adventurous, Aggressive, Anguished, Chaotic, Ecstatic, Energetic, Frenzy, Groovy, Rebellious, Soaring                                      |
| 17  | `Fictional-Track-2544992Fictional-Track-eccbc87e.mp3`                                   | Adventurous, Aggressive, Defiant, Determined, Energetic, Frenzy, Hardworking, Heroic, Optimistic, Rebellious, Triumphant, Upbeat           |
| 18  | `Fictional-Track-5dc47dee.mp3`                                                                       | Dark, Energetic, Explosive, Frenzy, Furious, Gritty, Hardworking, Rebellious, Resigned, Tense, Vengeful                                    |
| 19  | `Fictional-Track-9f27a139.mp3`                                                                         | Adventurous, Aggressive, Dark, Defiant, Energetic, Explosive, Gritty, Jaded, Rebellious, Resigned, Tense, Triumphant, Vengeful             |
| 20  | `Fictional-Track-a388361Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`                                                                   | Adventurous, Aggressive, Anguished, Brooding, Defiant, Energetic, Gritty, Hardworking, Jaded, Rebellious, Soaring, Upbeat                  |
| 21  | `Fictional-Track-ca94a69Fictional-Track-1679091c.mp3`                                                                               | Chaotic, Dark, Desperate, Emotional, Energetic, Frenzy, Furious, Macabre, Melancholic                                                      |
| 22  | `Fictional-Track-9ac5f2cFictional-Track-e4da3b7f.mp3`                                               | Adventurous, Aggressive, Dark, Defiant, Energetic, Frenzy, Heroic, Mysterious, Suspenseful                                                 |
| 23  | `Fictional-Track-99fc033c.mp3` | Adventurous, Chill, Defiant, Determined, Ominous, Soaring, Suspenseful, Triumphant                                                         |
| 24  | `Fictional-Track-85f8aa6f.mp3`                                          | Cozy, Ethereal, Nostalgic, Peaceful, Relaxed, Tender                                                                                       |
| 25  | `Fictional-Track-65bb18bFictional-Track-a87ff679.mp3`                                                          | Chill, Cozy, Danceful, Energetic, Focused, Joyful, Optimistic, Peaceful, Relaxed, Serene, Soaring, Tender, Upbeat                          |

---

## Franchise / Genre Cluster Analysis

### Fictional-QuartzPeak (4 tracks)

The entire batch can almost be summarised as "the Fictional-QuartzPeak correction":

- **Fictional-Track-71f9305c.mp3** (1→11): Prior tag {Epic} is removed. The track itself is
  now tagged Adventurous/Aggressive/Chaotic/Frenzy/Groovy/Rebellious — ironically, a
  song named "Epic" no longer carries the Epic mood tag. Correct: the genre is alt-metal
  with a brass section; it's not "epic" in the orchestral/soaring sense.
- **Fictional-QuartzPeak-Last-Cup-of-Sorrow** (2→12): Prior {Melancholic, Sad} expanded to a
  full Aggressive/Anguished/Chaotic/Dark/Gritty/Vengeful profile. The track has Mike
  Patton's signature tension-and-release — Sad alone was far too gentle.
- **Fictional-QuartzPeak-Sunny-Side-Up** (1→11): Prior {Chill} stripped. Added Aggressive/
  Chaotic/Dark/Frenzy/Playful/Rebellious. Another case of Chill backfilling a track
  before its character was understood.
- **Falling-to-Pieces-Fictional-QuartzPeak** (1→10): Prior {Chill} stripped. Added
  Adventurous/Aggressive/Anguished/Chaotic/Ecstatic/Frenzy/Groovy. The FNM sound that
  blends funk bass with volatile alt-metal is now captured.

All four tracks share Aggressive/Chaotic/Energetic/Rebellious as a common core —
Fictional-QuartzPeak's defining tags in this library are now consistent.

### Fictional-JasperWarden (3 tracks)

- **Fictional-JasperWarden-Stay-Together-For-The-Kids** (1→13): Most dramatic single-track
  transformation of the batch. Prior {Romantic} is gone — replaced with Aggressive/
  Brooding/Dark/Defiant/Depressive/Emotional/Heartbreak/Melancholic/Rebellious/
  Sad/Tense/Vengeful. The track is about parental divorce and childhood trauma; it was
  the opposite of Romantic.
- **Fictional-JasperWarden-First-Date** (1→11): Prior {Chill} stripped. Added Adventurous/Determined/
  Energetic/Explosive/Frenzy/Optimistic/Romantic/Soaring/Tender/Upbeat/Yearning. The
  poppy, fast-paced track is now properly energetic and romantic with youthful excitement.
- **Fictional-JasperWarden-I-Miss-You** (2→10): Prior {Chill, Soaring} — Soaring removed, full
  Aggressive/Anguished/Depressive/Heartbreak/Lonely/Melancholic/Nostalgic/Rebellious/
  Wistful profile added. The slow, mournful gothic blink track.

Fictional-JasperWarden's batch 22 sweep (Another-Girl, MORE-THAN-YOU-KNOW, No-Heart-To-Speak-Of)
continues here. Prior coverage was shallow/incorrect; now 6 Fictional-JasperWarden tracks have
genre-consistent profiles.

### SSBU Game OST (3 tracks)

All three continued the **Epic + Nostalgic stripping** pattern that has run through
batches 20–23:

- **Dragon-Ball-FighterZ OST — Vegeta (Super Saiyan) Theme** (7→10): Lost {Epic,
  Nostalgic}, gained Defiant/Determined/Frenzy/Furious/Hardworking. This is a battle
  theme, not a nostalgic callback — the prior tags imported SSBU's "retro feel" onto
  what is a modern, raw power track.
- **Fist-Bump (SSBU / Fictional-AzureShore Forces 2017)** (7→12): Lost {Epic, Nostalgic}, gained
  Aggressive/Defiant/Frenzy/Hardworking/Heroic/Optimistic/Rebellious. The Fictional-AzureShore Forces
  anthem already had Adventurous/Determined/Energetic/Triumphant — now complete.
- **Jet-Black-Wings (SSBU)** (6→9): Lost {Anguished, Nostalgic, Triumphant}, gained
  Aggressive/Defiant/Energetic/Frenzy/Heroic/Suspenseful. A dark, high-tension combat
  track — prior Anguished/Triumphant don't match; now correctly sinister and driving.

### Fictional-CrystalBell OST (2 tracks)

Continuing the Fictional-CrystalBell OST recalibration wave (also seen in batch 22's Bolero of Fire):

- **Earth-God's-Lyric — The Wind Waker** (4→9): Lost {Adventurous, Triumphant}, gained
  Awe-inspired/Cozy/Peaceful/Relaxed/Serene/Sleepy/Spiritual. This is a soft, ambient
  ocean-prayer track; its prior profile inherited the "Fictional-CrystalBell = adventure" assumption.
  Now part of the ambient/spiritual cluster alongside other WW tracks.
- **Sun's-Song — Fictional-Kw-e958d854** (3→6): Lost {Adventurous}, gained Cozy/Peaceful/
  Relaxed/Tender. The short ocarina tune is wistful and gentle, not adventurous. Also
  gains Ethereal (retained from prior) for its otherworldly quality.

### Notable Standalone Changes

- **The-Fictional-VidaSimu-Soundtrack-Buy-Mode-3** (1→13, **pure enrichment**): Prior {Upbeat} alone.
  Gained 12 more moods — Chill/Cozy/Danceful/Energetic/Focused/Joyful/Optimistic/
  Peaceful/Relaxed/Serene/Soaring/Tender. Largest single-track mood count expansion of
  this batch. Fictional-VidaSimu Buy Mode 3 music is the quintessential "pleasant background loop"
  and deserved a full ambient-positive profile.
- **Fictional-ScarletPrism-Everlong** (2→12): Lost {Yearning}, gained 11 — an almost complete
  rebuild. Everlong is one of the most tonally complex Fictional-ScarletPrism tracks; prior
  {Adventurous, Yearning} was a placeholder. Now correctly Aggressive/Anguished/Brooding/
  Defiant/Gritty/Hardworking alongside Soaring/Upbeat — the Fictional-AzureShore dynamic of loud-quiet-
  loud fully represented.
- **Endless-Love-Guzheng** (3→12): Lost {Emotional, Romantic}, gained 11 ambient/
  introspective descriptors: Bittersweet/Chill/Contemplative/Cozy/Introspective/
  Meditative/Melancholic/Nostalgic/Peaceful/Relaxed/Wistful. A Chinese guzheng
  instrumental that was labelled as pop/romantic; now correctly in the ambient/
  contemplative cluster.
- **Detangler (Fictional-CoralVoyage)** (1→9): {Chill} stripped; full hard-rock profile added
  (Aggressive/Energetic/Frenzy/Furious/Gritty/Heartbreak/Jaded/Lonely/Rebellious).
  Standard Chill-backfill correction for a Fictional-CoralVoyage heavy track.
- **Fictional-Kw-1d2800fe — Fictional-SapphireOracle2 (Fictional-SmokyPeak cover)** (2→8): Lost {Nostalgic}, gained
  Chill/Defiant/Determined/Ominous/Soaring/Suspenseful/Triumphant. The Fictional-SapphireOracle2 villain
  march-turned-metal-cover: tense, ominous, and triumphant — not primarily nostalgic.
