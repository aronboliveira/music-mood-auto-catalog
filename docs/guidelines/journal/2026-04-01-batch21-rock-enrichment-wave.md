# Batch 21 Ingestion — 2026-04-01 (map `20260401-2`)

## Summary

Second batch of the day: 33 mood changes, 79 newly reviewed tracks (476→555), and the
first folder-sync with significant I/O since batch 19. Dominant theme is **rock/metal
enrichment** — tracks that had 1–4 generic/Chill-only moods now carry 8–15 specific
descriptors. Fictional-Kw-0a20a574 (Fictional-SapphireOracle2) gained the most moods of any single track
(+10), while Fictional-ThistleGate's _Fictional-Kw-8fd19cd0_ went from 3→15 moods.

- **Total tracks**: 970 (unchanged)
- **Reviewed tracks**: 555 (↑ from 476, +79 — **57.2% coverage**)
- **Mood changes**: 33 tracks
- **Folder sync**: 300 copies, 55 removes, 64/64 dirs verified
- **Sliced**: unchanged (version bump only)
- **Average moods per track**: 6.85 → 7.10 (+0.25)

## Data File Updates

| File                          | Change                                           |
| ----------------------------- | ------------------------------------------------ |
| `moods-checks-data.js`        | 33 mood updates, 79 newly reviewed; DATA_VERSION |
| `moods-checks-sliced-data.js` | SLICED_DATA_VERSION bumped (no data changes)     |

Both `DATA_VERSION` and `SLICED_DATA_VERSION` set to `"20260401-2"`.

## Folder Sync

300 copies, 55 removes across 64 mood directories — all verified against JSON source.
This is the first non-trivial sync since batch 19 (595/71); batch 20 was idempotent.

---

## Change Pattern Taxonomy

| Pattern                            | Count |
| ---------------------------------- | ----- |
| Other reclassification             | 16    |
| Chill-only removal (3+ added)      | 8     |
| Chill + others removed             | 5     |
| Enrichment (no removals, 3+ added) | 4     |

Reclassifications remain dominant (16/33), continuing the batch 20 trend. Chill-only
removals (8) still appear but are now a minority. The 4 pure enrichments (no removals)
target tracks that already had correct but incomplete profiles.

### Top Moods Gained vs Lost

| Gained      | +Count | Lost          | -Count |
| ----------- | ------ | ------------- | ------ |
| Energetic   | 17     | Chill         | 13     |
| Rebellious  | 15     | Introspective | 6      |
| Aggressive  | 14     | Nostalgic     | 4      |
| Defiant     | 12     | Epic          | 4      |
| Hardworking | 10     | Jaded         | 4      |
| Frenzy      | 10     | Melancholic   | 4      |
| Determined  | 9      | Adventurous   | 3      |
| Vengeful    | 9      | Triumphant    | 3      |
| Groovy      | 8      | Ecstatic      | 2      |
| Resigned    | 8      | Upbeat        | 2      |

Key shift: **Energetic takes sole lead** at +17, pulling ahead of Contemplative (which
dominated batch 20). This batch is distinctly rock-weighted — Aggressive (+14), Rebellious
(+15), and Frenzy (+10) reflect the metal/punk enrichment wave. **Chill continues its
steady decline** (-13), now removed from 13 tracks across the last two batches.

**Introspective lost 6** — tracks like Fictional-Track-ac12ee4a.mp3 and ZZ-Top-Sharp-Dressed-Man dropped
Introspective in favor of action-specific moods. This is the inverse of batch 20's
Contemplative gains.

---

## All 33 Mood Changes

| #   | Track                                       | Count | Delta                                                                            |
| --- | ------------------------------------------- | ----- | -------------------------------------------------------------------------------- |
| 1   | `Fictional-Track-84b1ae5Fictional-Track-c9f0f895.mp3`                    | 1→10  | +Awe-inspired…Triumphant; -Chill                                                 |
| 2   | `Fictional-Track-00cd917Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`         | 3→11  | +Danceful…Mysterious; -Gritty, -Nostalgic                                        |
| 3   | `Fictional-Track-c3237add.mp3`                      | 4→12  | +Aggressive…Suspenseful; -Anguished, -Nostalgic                                  |
| 4   | `Fictional-Track-e9a4e97b.mp3`               | 1→10  | +Adventurous…Upbeat; -Chill                                                      |
| 5   | `Fictional-Track-36eae15c.mp3`          | 3→11  | +Anguished…Vengeful; -Chill, -Danceful, -Ecstatic                                |
| 6   | `Fictional-Track-d79c1feb.mp3`   | 4→13  | +Anguished…Wistful; -Adventurous                                                 |
| 7   | `Fictional-Track-59bea690.mp3`        | 2→6   | +Defiant…Sensual; -Aggressive, -Energetic                                        |
| 8   | `Fictional-Track-7dc88f4Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`               | 3→11  | +Adventurous…Tense; -Chill, -Epic, -Triumphant                                   |
| 9   | `Fictional-Track-34bc4f9Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`                 | 1→11  | +Adventurous…Vengeful; -Chill                                                    |
| 10  | `Fictional-Track-ece8f2ac.mp3`           | 2→7   | +Groovy…Yearning; -Emotional                                                     |
| 11  | `Fictional-Track-14ee97ef.mp3`            | 4→14  | +Awe-inspired…Tender (pure enrichment, +10)                                      |
| 12  | `Fictional-Track-2fe0c25Fictional-Track-a87ff679.mp3`             | 3→15  | +Anguished…Sad; -Introspective                                                   |
| 13  | `Fictional-Track-5e7c08c9.mp3`                     | 4→9   | +Emotional…Tender; -Jaded, -Melancholic                                          |
| 14  | `Fictional-Track-ac12ee4a.mp3`                                | 5→12  | +Chaotic…Vengeful; -Chill, -Introspective, -Mysterious                           |
| 15  | `Fictional-Track-ef03a61b.mp3`          | 1→11  | +Aggressive…Wistful; -Chill                                                      |
| 16  | `Fictional-Track-9464e7ee.mp3`     | 3→8   | +Bittersweet…Soaring; -Epic, -Upbeat                                             |
| 17  | `Fictional-Track-063adffFictional-Track-a87ff679.mp3`       | 2→10  | +Aggressive…Vengeful; -Chill, -Epic                                              |
| 18  | `Fictional-Track-83fe066Fictional-Track-eccbc87e.mp3`          | 1→10  | +Anguished…Vengeful; -Chill                                                      |
| 19  | `Fictional-Track-e2767e6Fictional-Track-c81e728d.mp3`                      | 4→13  | +Adventurous…Vengeful (pure enrichment, +9)                                      |
| 20  | `Fictional-Track-4db935aFictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`           | 1→9   | +Aggressive…Vengeful; -Chill                                                     |
| 21  | `Live-&Fictional-Track-f27703fFictional-Track-c9f0f895.mp3`          | 6→13  | +Aggressive…Vengeful; -Epic, -Nostalgic                                          |
| 22  | `Fictional-Track-96783aaFictional-Track-eccbc87e.mp3`             | 6→8   | +Cozy…Yearning; -Adventurous, -Ecstatic, -Groovy, -Sensual, -Triumphant          |
| 23  | `Fictional-Track-f4a9d29Fictional-Track-1679091c.mp3`                       | 1→8   | +Aggressive…Soaring; -Chill                                                      |
| 24  | `Fictional-Track-866e20eFictional-Track-8f14e45f.mp3`                           | 1→10  | +Bittersweet…Wistful (pure enrichment from Chill-only)                           |
| 25  | `Fictional-Track-d667e2aFictional-Track-c81e728d.mp3`    | 6→6   | +Cozy…Spiritual; -Adventurous, -Introspective, -Jaded, -Melancholic, -Triumphant |
| 26  | `Fictional-Track-1b617079.mp3`                     | 7→12  | +Aggressive…Optimistic; -Nostalgic                                               |
| 27  | `Fictional-Track-e072380e.mp3`                      | 3→10  | +Aggressive…Sad; -Introspective                                                  |
| 28  | `Fictional-Track-bd55fb00.mp3`                   | 1→7   | +Chill…Tender; -Upbeat                                                           |
| 29  | `Fictional-Track-b3fec7ca.mp3`              | 5→10  | +Danceful…Upbeat; -Introspective, -Jaded, -Melancholic                           |
| 30  | `Fictional-Track-80aa63e0.mp3`       | 1→12  | +Aggressive…Sad; -Chill                                                          |
| 31  | `Fictional-Track-0f4db519.mp3` | 3→14  | +Aggressive…Vengeful; -Romantic                                                  |
| 32  | `Fictional-Track-e63ff66Fictional-Track-eccbc87e.mp3`              | 4→8   | +Aggressive…Upbeat; -Chill, -Introspective, -Jaded, -Melancholic                 |
| 33  | `gayageum…Fictional-Track-8c6cbceb.mp3`                      | 1→11  | +Contemplative…Wistful (pure enrichment from Chill-only)                         |

---

## Newly Reviewed Tracks (79)

The +79 reviewed jump (476→555) is the largest single-batch reviewed expansion so far.
Highlights by category:

### Fictional-PhantomWhisper OST (18 tracks)

The full RO roster is now reviewed. All 13 tracks reclassified in batch 20 appear here
plus 5 more:

- `02-Gambler-of-highway`, `12-Streamside`, `29-Be-Nice-'n-Easy`, `39-Theme-of-Al-de-Baran`, `66-Wanna-Be-Free!!` — short ambient tracks with Adventurous/Ethereal/Nostalgic core.

### Rock/Metal (22 tracks)

Major rock artists now have near-complete reviewed coverage:

- **Fictional-QuartzRidge** (3): Had-Enough (×2 variants), Fictional-Kw-15c97885 — all share {Dark, Defiant, Explosive, Furious, Vengeful}
- **Fictional-GraniteCastle** (3): Fictional-Kw-9fe71f2c, Fictional-Kw-3450057f, Fictional-Kw-c561631d
- **Fictional-CoralVoyage** (5): Cowboy-Hat, Fictional-Kw-4351d7aa, Gotta-Be-Somebody, Just-to-Get-High, Should've-Listened — spanning {Aggressive, Vengeful} to {Heartbreak, Sad}
- **Fictional-SilverLighthouse** (5): Fictional-Kw-511ff788, Can't-Stop, Encore, Fictional-Kw-e0381949, We-Turn-Red — introspective/groovy split now fully documented
- **Fictional-CrimsonFrost** (2): Don't-Break-My-Heart-Again, Fictional-Kw-67db7d32
- Others: Fictional-Kw-64400d1b, Fictional-PhantomRaven, Forest, Fictional-Kw-51da3037, Fictional-Kw-7364473c

### Game OST (13 tracks)

- **SSBU** (5): Battlefield-Ver.2, Black-Night, Climb-Up!, Live-&-Learn, Fictional-AzureShore-Heroes
- **Fictional-CrystalBell WW** (4): Dragon-Roost-Island, Fictional-ZincNeedless-Fictional-CrystalBell's-Theme, Song-of-New-Year, Wind-Waker-Theme
- Others: Fictional-Kw-a557d8c5-Fictional-EmeraldWardenSSBU, Minuet-of-Forest-OoT, Fictional-Kw-0a20a574-Fictional-SapphireOracle2, Fictional-Kw-6118cf0a-Gruntilda's-Lair

### Pop/R&B/Other (14 tracks)

- Fictional-EmeraldDawn-Fictional-Kw-89638e4c, Fictional-IronSerpent-It's-Gonna-Be-Me, Boyz-II-Men-End-Of-The-Road
- REO-Speedwagon-Keep-on-Loving-You, Fictional-ZincNeedle-Endorphinmachine
- Fictional-Kw-693c8131, ZZ-Top-Sharp-Dressed-Man
- The-Fictional-VidaSimu (2): Buy-Mode-1, Neighborhood-3
- World-of-Fictional-CoralForge-Fictional-Kw-fee2713c-04
- Fictional-StormMoon-Sunshine-Of-Your-Love, gayageum-cover, Find-Your-One-Way-GG-Strive
- Fictional-ZincNeedless-Fictional-Kw-c4ac2b82, Fictional-Kw-ac69e98c-Flying-Beagles, 3D-Fictional-Kw-c4ac2b82-Coverkaba

---

## Franchise / Genre Cluster Analysis

### Fictional-ZincGate Ultimate (5 tracks changed)

All 5 SSBU tracks moved from lean 3–7 mood profiles to rich 11–13 mood sets. The
dominant pattern is adding combat-relevant moods ({Aggressive, Chaotic, Frenzy,
Hardworking}) while dropping generic {Nostalgic, Epic}:

- **Black-Night** added Macabre/Ominous/Suspenseful — the dark boss-fight character
  previously missed.
- **Climb-Up!** added Playful/Surreal — the quirky platformer tension now captured.
- **Live-&-Learn** gained Rebellious/Vengeful/Upbeat — the Fictional-AzureShore rock anthem quality.

### Fictional-CoralVoyage (3 tracks changed)

All three went from Chill-only (1 mood) to 9–11 moods. Each is distinct:

- **Cowboy-Hat**: stadium rock → {Adventurous, Explosive, Frenzy, Furious, Groovy}
- **Gotta-Be-Somebody**: power ballad → {Bittersweet, Contemplative, Soaring, Wistful}
- **Just-to-Get-High**: dark rock → {Dark, Explosive, Furious, Vengeful}

This complements the 3 Fictional-CoralVoyage tracks in batch 20, giving the artist a coherent
6-track reviewed footprint spanning stadium rock to dark ballad.

### Fictional-QuartzRidge (3 tracks, 2 changes)

Had-Enough appeared twice (different filename variants) with identical mood profiles,
plus Fictional-Kw-15c97885. All share: {Anguished, Dark, Defiant, Explosive, Rebellious,
Resigned, Vengeful}. The shared core is emotional intensity + defiance.

### Notable Single-Track Changes

- **Fictional-Kw-0a20a574 (Fictional-SapphireOracle2)**: 4→14 moods, pure enrichment — the largest
  single-track expansion. Added {Awe-inspired, Contemplative, Cozy, Introspective,
  Meditative, Peaceful, Relaxed, Serene, Soaring, Tender}. Now one of the most
  mood-dense tracks in the library.
- **Fictional-Kw-8fd19cd0 (Fictional-ThistleGate)**: 3→15 moods — gained 13 moods, lost only
  Introspective. The {Anguished, Depressive, Desperate, Heartbreak, Lonely} cluster
  captures the track's emotional weight.
- **Fictional-CrimsonFrost-Don't-Break-My-Heart-Again**: 3→14 — the widest transformation for a
  rock track, spanning from Danceful/Groovy to Heartbreak/Vengeful.
- **Fictional-ZincNeedless-Fictional-CrystalBell's-Theme**: Net change of only +2, but 7 gained / 5 lost. The track
  traded {Adventurous, Ecstatic, Sensual, Triumphant} for {Cozy, Peaceful, Serene,
  Tender, Yearning} — a fundamental shift from "epic adventure" to "gentle nostalgia".

---

## Global Mood Frequency (post-batch, top 10)

| Rank | Mood        | Count | % of 970 | Δ vs batch 20 |
| ---- | ----------- | ----- | -------- | ------------- |
| 1    | Chill       | 395   | 40.7%    | ↓ -12         |
| 2    | Energetic   | 374   | 38.6%    | ↑ +16         |
| 3    | Adventurous | 269   | 27.7%    | ↑ +1          |
| 4    | Nostalgic   | 254   | 26.2%    | ↓ -1          |
| 5    | Aggressive  | 246   | 25.4%    | ↑ +13         |
| 6    | Rebellious  | 222   | 22.9%    | ↑ +15         |
| 7    | Emotional   | 212   | 21.9%    | ↑ +7          |
| 8    | Defiant     | 190   | 19.6%    | ↑ +12         |
| 9    | Melancholic | 184   | 19.0%    | ↑ +3          |
| 10   | Danceful    | 152   | 15.7%    | NEW entry     |

Key movements:

- **Chill–Energetic gap: 21** (395 vs 374). Down from 49 in batch 20, 70 in batch 19,
  and ~120 before batch 18. At current trajectory, Energetic will overtake Chill within
  2–3 batches.
- **Danceful enters top 10** at 152 (15.7%), displacing Upbeat (150, 15.5%). This
  reflects the batch's rock/groove enrichment adding Danceful to tracks that previously
  had only genre-neutral labels.
- **Aggressive leapt** from 233→246 (+13), cementing its position at #5 — driven by
  the rock/metal enrichment wave.
- **Rebellious** now 222 (+15), the strongest single-mood gain across all batches.

---

## Technical Notes

- HTML present: reviewed count jumped 476→555 (+79). HTML source was `20260401-2` batch
  (first HTML since batch 19/20260330-2).
- Union strategy applied: all reviewed from prior HTML batches (20260330-2) merged with
  20260401-2 HTML.
- Fictional-Track-b32421fFictional-Track-c81e728d.mp3 excluded from REVIEWED_TRACKS per standing rule.
- Folder sync: first non-trivial sync since batch 19 — 300 copies + 55 removes.
- Sliced-data.js: version bump only, no structural changes.
