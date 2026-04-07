# Batch 22 Ingestion — 2026-04-04 (map `20260404-1`)

## Summary

41 mood changes, 40 newly reviewed tracks (555→595), and the first batch where
**enrichment dominates** as the primary change pattern (18/41 = 44%). Tracks already
tagged with 1–2 correct moods now reach 8–13 descriptors. Major franchise clusters:
Fictional-JasperWarden (5 tracks), SSBU (4 tracks), Fictional-TwilightDrifter (3 tracks), Fictional-IronSignal (3 tracks). A strong
Romantic/Heartbreak wave accompanies pop enrichments.

- **Total tracks**: 970 (unchanged)
- **Reviewed tracks**: 595 (↑ from 555, +40 — **61.3% coverage**)
- **Mood changes**: 41 tracks
- **Folder sync**: 353 copies, 35 removes, 65/65 dirs verified
- **Sliced**: unchanged (version bump only)
- **Average moods per track**: 7.10 → 7.43 (+0.33)

## Data File Updates

| File                          | Change                                           |
| ----------------------------- | ------------------------------------------------ |
| `moods-checks-data.js`        | 41 mood updates, 40 newly reviewed; DATA_VERSION |
| `moods-checks-sliced-data.js` | SLICED_DATA_VERSION bumped (no data changes)     |

Both `DATA_VERSION` and `SLICED_DATA_VERSION` set to `"20260404-1"`.

## Folder Sync

353 copies, 35 removes across 65 mood directories — all verified against JSON source.

---

## Change Pattern Taxonomy

| Pattern                            | Count |
| ---------------------------------- | ----- |
| Enrichment (no removals, 2+ added) | 18    |
| Other reclassification             | 15    |
| Chill-only removal (3+ added)      | 7     |
| Chill + others removed             | 1     |

**Enrichment is now the dominant pattern for the first time.** 18 of 41 tracks had
correct but shallow profiles (1–3 moods) expanded into full descriptive sets of 6–13.
This marks a shift from the correction-of-errors phase (batches 19–21) toward a
completeness phase.

### Top Moods Gained vs Lost

| Gained        | +Count | Lost        | -Count |
| ------------- | ------ | ----------- | ------ |
| Energetic     | 14     | Chill       | 8      |
| Rebellious    | 13     | Nostalgic   | 5      |
| Contemplative | 12     | Energetic   | 4      |
| Tender        | 11     | Upbeat      | 3      |
| Soaring       | 11     | Groovy      | 3      |
| Melancholic   | 11     | Epic        | 2      |
| Relaxed       | 10     | Aggressive  | 2      |
| Romantic      | 10     | Romantic    | 1      |
| Heartbreak    | 10     | Adventurous | 1      |
| Groovy        | 10     | Ethereal    | 1      |
| Bittersweet   | 10     | Danceful    | 1      |
| Danceful      | 10     | Ecstatic    | 1      |

Key observations:

- **Romantic and Heartbreak (+10 each)** are the biggest emotional additions: driven by
  the Fictional-TwilightDrifter, Fictional-Kw-340af906, Fictional-IronSignal, and Fictional-CobaltSignal sweeps. These were pop/soul
  tracks that had generic 1-mood profiles.
- **Groovy recovers** (+10 gained vs -3 lost). In batch 21, Groovy was net negative.
  This batch's Fictional-EmeraldRaven, FAUN, Bayou-Boogie, and Fictional-MistyStrand enrichments bring it
  back strongly.
- **Contemplative (+12)**: second consecutive batch with Contemplative in the top 3
  gained — now reaching melancholy/pensive pop and folk tracks as well as OST.
- **Chill-only removal continues** (7 more tracks), but at the lowest rate since batch 18.
- **Energetic lost 4** — notably from Fictional-TwilightDrifter tracks that were incorrectly tagged
  with Aggressive+Energetic; now corrected to Romantic/Emotional profiles.

---

## All 41 Mood Changes

| #   | Track                                           | Count | Delta                                                                        |
| --- | ----------------------------------------------- | ----- | ---------------------------------------------------------------------------- |
| 1   | `Fictional-Track-b2743afFictional-Track-c9f0f895.mp3`       | 1→6   | +Emotional, +Relaxed, +Romantic, +Sensual, +Tender (enrichment)              |
| 2   | `Fictional-Track-c76ea34Fictional-Track-a87ff679.mp3`        | 1→11  | +Bittersweet…Yearning (enrichment, +10)                                      |
| 3   | `Fictional-Track-2686953Fictional-Track-8f14e45f.mp3`         | 2→11  | +Chill…Yearning (enrichment, +9)                                             |
| 4   | `Fictional-Track-c332c9eFictional-Track-eccbc87e.mp3`           | 4→8   | +Aggressive…Triumphant; -Epic, -Nostalgic                                    |
| 5   | `Fictional-Track-e0b8c7ca.mp3`          | 2→13  | +Chill…Suspenseful (enrichment, +11 moods)                                   |
| 6   | `Fictional-Track-6f8ac4bFictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`               | 1→11  | +Chaotic…Vengeful; -Chill                                                    |
| 7   | `Fictional-Track-5634112Fictional-Track-1679091c.mp3`                     | 5→9   | +Anguished…Sad (enrichment, +4)                                              |
| 8   | `Fictional-Track-a4b9804e.mp3`                            | 1→9   | +Desperate…Vengeful; -Chill                                                  |
| 9   | `Fictional-Track-465f02ec.mp3`                           | 2→10  | +Chaotic…Surreal; -Chill                                                     |
| 10  | `Fictional-Track-4604863Fictional-Track-eccbc87e.mp3`               | 2→12  | +Bittersweet…Wistful (enrichment, +10)                                       |
| 11  | `Fictional-Track-2707712Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`                | 2→12  | +Contemplative…Yearning (enrichment, +10)                                    |
| 12  | `Fictional-Track-9433aecFictional-Track-e4da3b7f.mp3`                   | 2→13  | +Bittersweet…Wistful (enrichment, +11)                                       |
| 13  | `Fictional-Track-91d8f84Fictional-Track-8f14e45f.mp3`     | 1→8   | +Chaotic…Yearning; -Chill                                                    |
| 14  | `Fictional-Track-b32421fFictional-Track-c81e728d.mp3`                        | 2→11  | +Adventurous…Whimsical; -Upbeat _(excluded from REVIEWED per standing rule)_ |
| 15  | `Fictional-Track-20060fdf.mp3`                      | 1→2   | +Soaring (minimal enrichment)                                                |
| 16  | `Fictional-Track-f0ab3ad9.mp3`              | 1→10  | +Adventurous…Vengeful; -Chill                                                |
| 17  | `Fictional-Track-c56a69aa.mp3`            | 2→14  | +Anguished…Tense; -Romantic                                                  |
| 18  | `Fictional-Track-8925e5eFictional-Track-e4da3b7f.mp3`             | 1→11  | +Bittersweet…Tender (enrichment, +10)                                        |
| 19  | `Fictional-Track-6a485Fictional-Track-757b505c.mp3`              | 1→9   | +Bittersweet…Tender (enrichment, +8)                                         |
| 20  | `Fictional-Track-e15a20fc.mp3`       | 1→11  | +Bittersweet…Tender (enrichment, +10)                                        |
| 21  | `Fictional-Track-5d81adaFictional-Track-c81e728d.mp3`    | 4→9   | +Bittersweet…Suspenseful; -Adventurous, -Ethereal, -Groovy, -Nostalgic       |
| 22  | `Fictional-Track-3cf415df.mp3`             | 4→12  | +Dark…Vengeful; -Chill, -Danceful, -Ecstatic                                 |
| 23  | `Fictional-Track-1bb7a54a.mp3`                  | 1→13  | +Aggressive…Resigned; -Chill                                                 |
| 24  | `Fictional-Track-4e763e5b.mp3`           | 2→11  | +Awe-inspired…Yearning; -Aggressive, -Energetic                              |
| 25  | `Fictional-Track-504bc90Fictional-Track-e4da3b7f.mp3`           | 2→12  | +Anguished…Yearning (enrichment, +10)                                        |
| 26  | `Fictional-Track-a32c4219.mp3`            | 2→11  | +Bittersweet…Wistful; -Aggressive, -Energetic                                |
| 27  | `Fictional-Track-84f4fcdFictional-Track-c9f0f895.mp3`          | 1→8   | +Cozy…Wistful (enrichment, +7)                                               |
| 28  | `Fictional-Track-a8613eeFictional-Track-c81e728d.mp3`                           | 2→11  | +Aggressive…Soaring; -Chill                                                  |
| 29  | `Fictional-Track-f852c56Fictional-Track-a87ff679.mp3`                    | 3→7   | +Danceful…Surreal (enrichment, +4)                                           |
| 30  | `Fictional-Track-01ccbccFictional-Track-c81e728d.mp3`             | 7→13  | +Defiant…Yearning; -Epic, -Nostalgic                                         |
| 31  | `Fictional-Track-fbf364a9.mp3`                           | 2→13  | +Contemplative…Wistful; -Energetic (enrichment, +11)                         |
| 32  | `Fictional-Track-ce768a5Fictional-Track-a87ff679.mp3`   | 4→11  | +Contemplative…Upbeat; -Playful                                              |
| 33  | `Fictional-Track-c85c3a6Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`                  | 4→10  | +Aggressive…Upbeat; -Groovy, -Nostalgic                                      |
| 34  | `Fictional-Track-5386f09Fictional-Track-eccbc87e.mp3`                     | 5→11  | +Defiant…Tense; -Gritty, -Groovy, -Nostalgic, -Upbeat                        |
| 35  | `Fictional-Track-024a40de.mp3`                         | 3→7   | +Aggressive…Reverent; -Upbeat                                                |
| 36  | `Fictional-Track-fb363cfFictional-Track-c81e728d.mp3` | 2→8   | +Danceful…Whimsical (enrichment, +6)                                         |
| 37  | `Fictional-Track-9c173a8a.mp3`    | 2→10  | +Cozy…Whimsical (enrichment, +8)                                             |
| 38  | `Fictional-Track-eab5dd6d.mp3`                        | 2→6   | +Chill…Whimsical (enrichment, +4)                                            |
| 39  | `Fictional-Track-5e6e638c.mp3`           | 2→12  | +Adventurous…Surreal; -Introspective                                         |
| 40  | `Fictional-Track-d6ba71f0.mp3`                         | 2→7   | +Chaotic…Soaring; -Energetic                                                 |
| 41  | `Fictional-Track-39547cdFictional-Track-a87ff679.mp3`       | 4→10  | +Aggressive…Playful; -Chill                                                  |

---

## Newly Reviewed Tracks (40)

| #   | Track                                           | Moods                                                                                                                                       |
| --- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `Fictional-Track-b2743afFictional-Track-c9f0f895.mp3`       | Chill, Emotional, Relaxed, Romantic, Sensual, Tender                                                                                        |
| 2   | `Fictional-Track-c76ea34Fictional-Track-a87ff679.mp3`        | Bittersweet, Chill, Contemplative, Emotional, Heartbreak, Jaded, Resigned, Reverent, Romantic, Sensual, Yearning                            |
| 3   | `Fictional-Track-2686953Fictional-Track-8f14e45f.mp3`         | Chill, Contemplative, Emotional, Nostalgic, Relaxed, Romantic, Soaring, Tender, Upbeat, Wistful, Yearning                                   |
| 4   | `Fictional-Track-c332c9eFictional-Track-eccbc87e.mp3`           | Adventurous, Aggressive, Chaotic, Energetic, Frenzy, Playful, Rebellious, Triumphant                                                        |
| 5   | `Fictional-Track-e0b8c7ca.mp3`          | Adventurous, Chill, Contemplative, Cozy, Determined, Focused, Groovy, Introspective, Meditative, Nostalgic, Relaxed, Soaring, Suspenseful   |
| 6   | `Fictional-Track-6f8ac4bFictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`               | Aggressive, Chaotic, Danceful, Dark, Defiant, Energetic, Explosive, Frenzy, Ominous, Rebellious, Vengeful                                   |
| 7   | `Fictional-Track-5634112Fictional-Track-1679091c.mp3`                     | Anguished, Chill, Contemplative, Introspective, Jaded, Lonely, Melancholic, Rebellious, Sad                                                 |
| 8   | `Fictional-Track-a4b9804e.mp3`                            | Desperate, Energetic, Explosive, Furious, Gritty, Heartbreak, Jaded, Rebellious, Vengeful                                                   |
| 9   | `Fictional-Track-465f02ec.mp3`                           | Aggressive, Chaotic, Danceful, Dark, Defiant, Ecstatic, Energetic, Explosive, Frenzy, Surreal                                               |
| 10  | `Fictional-Track-4604863Fictional-Track-eccbc87e.mp3`               | Bittersweet, Chill, Contemplative, Emotional, Heartbreak, Jaded, Lonely, Melancholic, Peaceful, Resigned, Romantic, Wistful                 |
| 11  | `Fictional-Track-2707712Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`                | Chill, Contemplative, Emotional, Joyful, Nostalgic, Optimistic, Relaxed, Romantic, Sensual, Tender, Upbeat, Yearning                        |
| 12  | `Fictional-Track-410fd09Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`    | Bittersweet, Brooding, Chill, Contemplative, Emotional, Groovy, Jaded, Lonely, Melancholic, Peaceful, Resigned, Romantic, Wistful           |
| 13  | `Fictional-Track-91d8f84Fictional-Track-8f14e45f.mp3`     | Chaotic, Determined, Energetic, Rebellious, Romantic, Soaring, Upbeat, Yearning                                                             |
| 14  | `Fictional-Track-8925e5eFictional-Track-e4da3b7f.mp3`             | Bittersweet, Brooding, Chill, Contemplative, Jaded, Lonely, Melancholic, Relaxed, Romantic, Sad, Tender                                     |
| 15  | `Fictional-Track-6a485Fictional-Track-757b505c.mp3`              | Bittersweet, Chill, Contemplative, Emotional, Melancholic, Nostalgic, Relaxed, Resigned, Tender                                             |
| 16  | `Fictional-Track-e15a20fc.mp3`       | Bittersweet, Chill, Contemplative, Emotional, Nostalgic, Peaceful, Relaxed, Reverent, Serene, Spiritual, Tender                             |
| 17  | `Fictional-Track-5d81adaFictional-Track-c81e728d.mp3`    | Bittersweet, Danceful, Energetic, Epic, Focused, Heroic, Melancholic, Mysterious, Suspenseful                                               |
| 18  | `Fictional-Track-3cf415df.mp3`             | Dark, Determined, Emotional, Energetic, Explosive, Frenzy, Furious, Hardworking, Heartbreak, Melancholic, Rebellious, Vengeful              |
| 19  | `Fictional-Track-1bb7a54a.mp3`                  | Aggressive, Brooding, Dark, Depressive, Desperate, Energetic, Explosive, Heartbreak, Jaded, Lonely, Melancholic, Rebellious, Resigned       |
| 20  | `Fictional-Track-4e763e5b.mp3`           | Awe-inspired, Chill, Determined, Emotional, Joyful, Optimistic, Romantic, Sensual, Tender, Upbeat, Yearning                                 |
| 21  | `Fictional-Track-504bc90Fictional-Track-e4da3b7f.mp3`           | Aggressive, Anguished, Bittersweet, Danceful, Emotional, Energetic, Groovy, Heartbreak, Melancholic, Reverent, Romantic, Yearning           |
| 22  | `Fictional-Track-a32c4219.mp3`            | Bittersweet, Emotional, Heartbreak, Lonely, Melancholic, Nostalgic, Relaxed, Romantic, Sad, Tender, Wistful                                 |
| 23  | `Fictional-Track-84f4fcdFictional-Track-c9f0f895.mp3`          | Chill, Cozy, Nostalgic, Peaceful, Relaxed, Romantic, Tender, Wistful                                                                        |
| 24  | `Fictional-Track-a8613eeFictional-Track-c81e728d.mp3`                           | Aggressive, Anguished, Brooding, Energetic, Gritty, Heartbreak, Jaded, Melancholic, Rebellious, Resigned, Soaring                           |
| 25  | `Fictional-Track-f852c56Fictional-Track-a87ff679.mp3`                    | Danceful, Dark, Ethereal, Melancholic, Mysterious, Sad, Surreal                                                                             |
| 26  | `Fictional-Track-01ccbccFictional-Track-c81e728d.mp3`             | Adventurous, Defiant, Determined, Ecstatic, Energetic, Frenzy, Groovy, Hardworking, Heroic, Rebellious, Triumphant, Upbeat, Yearning        |
| 27  | `Fictional-Track-fbf364a9.mp3`                           | Chill, Contemplative, Danceful, Ethereal, Groovy, Nostalgic, Peaceful, Reverent, Serene, Soaring, Spiritual, Whimsical, Wistful             |
| 28  | `Fictional-Track-ce768a5Fictional-Track-a87ff679.mp3`   | Adventurous, Chill, Contemplative, Cozy, Joyful, Nostalgic, Peaceful, Serene, Soaring, Tender, Upbeat                                       |
| 29  | `Fictional-Track-c85c3a6Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`                  | Adventurous, Aggressive, Defiant, Determined, Epic, Focused, Hardworking, Heroic, Triumphant, Upbeat                                        |
| 30  | `Fictional-Track-5386f09Fictional-Track-eccbc87e.mp3`                     | Adventurous, Defiant, Determined, Energetic, Focused, Frenzy, Hardworking, Heroic, Rebellious, Soaring, Tense                               |
| 31  | `Fictional-Track-024a40de.mp3`                         | Aggressive, Danceful, Defiant, Energetic, Hardworking, Rebellious, Reverent                                                                 |
| 32  | `Fictional-Track-fb363cfFictional-Track-c81e728d.mp3` | Chill, Danceful, Ecstatic, Energetic, Groovy, Soaring, Upbeat, Whimsical                                                                    |
| 33  | `Fictional-Track-9c173a8a.mp3`    | Chill, Cozy, Danceful, Focused, Groovy, Relaxed, Soaring, Tender, Upbeat, Whimsical                                                         |
| 34  | `Fictional-Track-eab5dd6d.mp3`                        | Chill, Energetic, Groovy, Introspective, Reverent, Whimsical                                                                                |
| 35  | `Fictional-Track-5e6e638c.mp3`           | Adventurous, Chaotic, Danceful, Defiant, Determined, Energetic, Groovy, Hardworking, Rebellious, Reverent, Soaring, Surreal                 |
| 36  | `Fictional-Track-b705d8cFictional-Track-a87ff679.mp3`       | Adventurous, Aggressive, Dark, Defiant, Energetic, Frenzy, Heroic, Mysterious, Ominous, Suspenseful                                         |
| 37  | `Fictional-Track-d6ba71f0.mp3`                         | Chaotic, Chill, Gritty, Groovy, Nostalgic, Rebellious, Soaring                                                                              |
| 38  | `Fictional-Track-39547cdFictional-Track-a87ff679.mp3`       | Aggressive, Anguished, Chaotic, Emotional, Energetic, Heartbreak, Jaded, Melancholic, Playful, Rebellious                                   |
| 39  | `Fictional-Track-f0ab3ad9.mp3`              | Adventurous, Aggressive, Anguished, Brooding, Chaotic, Energetic, Explosive, Frenzy, Resigned, Vengeful                                     |
| 40  | `Fictional-Track-c56a69aa.mp3`            | Anguished, Bittersweet, Desperate, Emotional, Energetic, Frenzy, Gritty, Heartbreak, Lonely, Melancholic, Nostalgic, Rebellious, Sad, Tense |

---

## Franchise / Genre Cluster Analysis

### SSBU / Game OST (4 tracks changed + 2 more newly reviewed)

The 4 changed SSBU/game tracks all lost {Nostalgic, Epic} in favor of combat-specific
profiles:

- **Battle!-Trainer-Fictional-BrassHorizon (Sun/Moon)**: 4→8 — added Aggressive/Chaotic/Frenzy/Rebellious;
  dropped Epic+Nostalgic. Correct shift from "retro feel" to actual tension-driven battle energy.
- **Fictional-Kw-a1dc2820 (SSBU/SA2)**: 7→13 — added Defiant/Ecstatic/Frenzy/Groovy/
  Heroic/Rebellious/Yearning; dropped Epic+Nostalgic. The Fictional-AzureShore Adventure 2 run-track
  quality is now fully represented.
- **Fire-Emblem (Melee/SSBU)**: 4→10 — added Aggressive/Defiant/Determined/Heroic/
  Triumphant; dropped Groovy+Nostalgic.
- **Fire-Field (Brawl)**: 5→11 — added Defiant/Determined/Heroic/Soaring; dropped
  Gritty+Groovy+Nostalgic+Upbeat. The Fictional-ThistleOrchid race track character.

Two more SSBU tracks were newly reviewed (King-Bowser, Battle!-Trainer) bringing the
reviewed SSBU footprint to 6+ tracks.

### Fictional-JasperWarden (5 tracks changed)

Largest single-artist change group. Clear two-tier split:

- **Chaos/punk** (Another-Girl-Another-Planet, MORE-THAN-YOU-KNOW, No-Heart-To-Speak-Of):
  gained Aggressive/Chaotic/Frenzy/Vengeful profiles, each 8–14 moods.
- **Minimal correction** (I-Miss-You: +Soaring only): the track was already mostly correct.
- **Dark complexity** (No-Heart-To-Speak-Of 2→14): one of the largest single-track
  expansions. Added {Anguished, Desperate, Gritty, Heartbreak, Lonely, Melancholic,
  Nostalgic, Rebellious, Sad, Tense} — a fully realized dark blink track.
- **Dumpweed** (2→11): mood-changed but excluded from REVIEWED_TRACKS per standing rule.

### Fictional-TwilightDrifter (3 tracks changed)

All three Fictional-TwilightDrifter tracks had incorrect {Aggressive, Energetic} that are now removed:

- **Fictional-Kw-97490351** → pure romantic enrichment: Awe-inspired/Joyful/Optimistic/
  Romantic/Sensual/Tender/Yearning.
- **Talking-To-The-Moon** → piano ballad: Bittersweet/Heartbreak/Lonely/Melancholic/Sad.
- **Fictional-Kw-461bd9d0** → retained its danceful quality but gained Anguished/
  Bittersweet/Heartbreak alongside Groovy/Romantic.

### Fictional-IronSignal (3 tracks changed)

Three Brazilian pop/soul tracks now have fully developed profiles:

- **Pra-Ver-o-Sol-Brilhar**: sunny/romantic enrichment → Joyful/Optimistic/Romantic/Tender
- **Desafio-2000**: heartbreak ballad → Bittersweet/Heartbreak/Lonely/Melancholic
- **Procura-se-Um-Amor**: melancholy samba → Bittersweet/Brooding/Jaded/Lonely/Wistful

The three tracks demonstrate the artist's full tonal range from longing to optimism.

### Fictional-CobaltSignal (2 tracks changed)

Both Dylan tracks went from Chill-only (1 mood) to rich introspective profiles:

- **Going,-Going,-Gone**: Bittersweet/Contemplative/Emotional/Melancholic/Nostalgic/Resigned/Tender
- **Knockin'-On-Heaven's-Door**: Bittersweet/Contemplative/Emotional/Peaceful/Reverent/Serene/Spiritual/Tender

The shared {Bittersweet, Contemplative, Tender} core defines Dylan's late-period ballad style.

### Fictional-EmeraldRaven (2 tracks changed)

Two stylistically opposite Tull tracks:

- **Bouree**: classical/baroque flute cover → {Chill, Groovy, Reverent, Whimsical} — the
  gentle chamber quality
- **Steel-Monkey**: uptempo British folk-rock → 12 moods with Adventurous/Chaotic/Defiant/
  Soaring/Surreal

### Fictional-CobaltRiver Flying Beagles (2 tracks changed)

Tracks 2 (Baby-Talk) and 3 (Fluffy) were the second and third album pieces to be enriched
after track 8 (A-Seagull-And-Clouds, batch 21). All three now share a Chill/Groovy/Soaring/
Whimsical core appropriate for their jazz-influenced style.

### Fictional-QuartzRidge (2 tracks changed)

The BB cleanup continues:

- **Torn-in-Two** (4→12): was incorrectly tagged Chill/Danceful/Ecstatic — now
  Dark/Determined/Explosive/Furious/Heartbreak/Melancholic/Vengeful.
- **Breath** (1→13): was Chill-only — expanded to full dark rock: Aggressive/Brooding/
  Dark/Depressive/Desperate/Explosive/Lonely/Melancholic/Resigned.

---

## Global Mood Frequency (post-batch, top 10)

| Rank | Mood        | Count | % of 970 | Δ vs batch 21 |
| ---- | ----------- | ----- | -------- | ------------- |
| 1    | Chill       | 392   | 40.4%    | ↓ -3          |
| 2    | Energetic   | 384   | 39.6%    | ↑ +10         |
| 3    | Adventurous | 271   | 27.9%    | ↑ +2          |
| 4    | Nostalgic   | 258   | 26.6%    | ↑ +4          |
| 5    | Aggressive  | 252   | 26.0%    | ↑ +6          |
| 6    | Rebellious  | 235   | 24.2%    | ↑ +13         |
| 7    | Emotional   | 219   | 22.6%    | ↑ +7          |
| 8    | Defiant     | 197   | 20.3%    | ↑ +7          |
| 9    | Melancholic | 195   | 20.1%    | ↑ +11         |
| 10   | Danceful    | 161   | 16.6%    | ↑ +9          |

Key movements:

- **Chill–Energetic gap: 8** (392 vs 384). Down from 21 last batch (395 vs 374). At
  this rate, Energetic will surpass Chill in the next batch. Four consecutive batches of
  convergence.
- **Melancholic climbs** to 195 (+11), now #9 — driven by the pop/soul enrichment wave.
  Was #11 two batches ago.
- **Nostalgic recovers** (+4) after two batches of decline — influenced by Fictional-SapphireOracle2, Fictional-CobaltSignal,
  and Fictional-EmeraldRaven tracks gaining Nostalgic.
- **Rebellious +13** continues its streak as one of the fastest-growing moods across all
  batches.

---

## Technical Notes

- HTML present: reviewed count jumped 555→595 (+40).
- All 40 newly reviewed tracks were identified from HTML vs git HEAD diff.
- `Fictional-Track-b32421fFictional-Track-c81e728d.mp3` mood-changed (2→11) but excluded from REVIEWED_TRACKS per
  standing rule.
- Folder sync: 353 copies, 35 removes — normal I/O (non-trivial).
- Sliced-data.js: version bump only, no structural changes.
