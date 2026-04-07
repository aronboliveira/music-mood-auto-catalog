# Batch 20 Ingestion — 2026-04-01 (map `20260401-1`)

## Summary

Mood-update batch with no HTML review file: 42 tracks reclassified, reviewed count
unchanged. Dominant theme is **Fictional-PhantomWhisper OST deepening** (13 of 42 changes)
alongside Fictional-CrystalBell Wind Waker enrichment, Fictional-SilverLighthouse expansion, and continued Chill→Specific
corrections for rock/pop tracks. No sliced changes.

- **Total tracks**: 970 (unchanged)
- **Reviewed tracks**: 476 (unchanged, 49.1% coverage)
- **Mood changes**: 42 tracks (copies/removes already applied to folder structure)
- **Sliced**: unchanged (version bump only)
- **Average moods per track**: 6.49 → 6.85 (+0.35)

## Data File Updates

| File                          | Change                                       |
| ----------------------------- | -------------------------------------------- |
| `moods-checks-data.js`        | 42 mood updates; DATA_VERSION bumped         |
| `moods-checks-sliced-data.js` | SLICED_DATA_VERSION bumped (no data changes) |

Both `DATA_VERSION` and `SLICED_DATA_VERSION` set to `"20260401-1"`.

## Folder Sync

All 63 affected mood directories verified correct against JSON source.

---

## Change Pattern Taxonomy

| Pattern                            | Count |
| ---------------------------------- | ----- |
| Other reclassification             | 19    |
| Enrichment (no removals, 3+ added) | 10    |
| Chill-only removal (3+ added)      | 9     |
| Chill + others removed             | 4     |

For the first time, pure reclassifications (no Chill removal, significant restructuring)
dominate at 19 of 42. The Chill-dissolution pattern continues but is no longer the majority.

### Top Moods Gained vs Lost

| Gained        | +Count | Lost        | -Count |
| ------------- | ------ | ----------- | ------ |
| Contemplative | 18     | Chill       | 13     |
| Energetic     | 18     | Adventurous | 9      |
| Emotional     | 13     | Nostalgic   | 8      |
| Soaring       | 12     | Ethereal    | 5      |
| Chaotic       | 12     | Epic        | 4      |
| Joyful        | 10     | Upbeat      | 2      |
| Reverent      | 10     | Sensual     | 2      |
| Aggressive    | 10     | —           | —      |

Notable shift: **Contemplative tied with Energetic** as most-gained (+18 each). This
reflects the extensive RO OST and Fictional-CrystalBell reclassifications — atmospheric tracks that
previously had generic Adventurous/Nostalgic/Ethereal now carry specific
Contemplative/Introspective/Spiritual profiles.

**Adventurous heavily lost** (-9): near-exclusively from RO OST tracks that had
Adventurous as a catch-all for atmospheric tracks — now replaced by accurate
introspective/meditative/lowercase moods.

---

## All 42 Mood Changes

| #   | Track                                     | Count | Delta                                                       |
| --- | ----------------------------------------- | ----- | ----------------------------------------------------------- |
| 1   | `3D…Fictional-Kw-c4ac2b82…Fictional-Track-c3d2b47b.mp3`               | 4→10  | +Awe-inspired…Triumphant; -Emotional                        |
| 2   | `Fictional-Track-18b6f0ea.mp3`         | 1→9   | +Anguished…Wistful                                          |
| 3   | `Fictional-Track-cec16630.mp3`                    | 2→10  | +Aggressive…Sad; -Chill                                     |
| 4   | `Fictional-Track-be1c566e.mp3`          | 4→14  | +Chill…Yearning; -Ethereal, -Triumphant                     |
| 5   | `Fictional-Track-364b45dFictional-Track-1679091c.mp3`                     | 2→12  | +Aggressive…Vengeful; -Chill                                |
| 6   | `Fictional-Track-b8b3c5fFictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`         | 3→9   | +Chaotic…Vengeful; -Adventurous, -Epic, -Nostalgic          |
| 7   | `Fictional-Track-5e2474dFictional-Track-1679091c.mp3`     | 4→9   | +Chaotic…Upbeat; -Aggressive, -Energetic, -Nostalgic        |
| 8   | `Fictional-Track-fc9fcd7Fictional-Track-c9f0f895.mp3` | 3→13  | +Adventurous…Vengeful; -Chill, -Epic, -Upbeat               |
| 9   | `Fictional-Track-52bcdaaFictional-Track-c9f0f895.mp3` | 2→14  | +Contemplative…Yearning                                     |
| 10  | `Fictional-Track-7241a48Fictional-Track-c9f0f895.mp3`                   | 2→10  | +Aggressive…Vengeful; -Chill                                |
| 11  | `Fictional-Track-a0079ccFictional-Track-e4da3b7f.mp3`               | 4→14  | +Anguished…Yearning; -Upbeat                                |
| 12  | `Fictional-Track-829cbe2f.mp3`                | 5→11  | +Awe-inspired…Triumphant; -Adventurous                      |
| 13  | `Fictional-Track-baa5f4cFictional-Track-c81e728d.mp3`              | 1→12  | +Bittersweet…Upbeat; -Chill                                 |
| 14  | `Fictional-Track-dcf5399f.mp3`            | 1→6   | +Danceful…Melancholic; -Chill                               |
| 15  | `Fictional-Track-1a5fb96d.mp3`            | 1→10  | +Aggressive…Triumphant; -Chill                              |
| 16  | `Fictional-Track-c0e69c3Fictional-Track-eccbc87e.mp3`                  | 1→11  | +Adventurous…Tense; -Chill                                  |
| 17  | `Fictional-Track-aa28954Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`             | 4→13  | +Aggressive…Upbeat; -Chill, -Sensual                        |
| 18  | `Fictional-Track-a0cdf409.mp3`             | 5→14  | +Chill…Wistful; -Ecstatic, -Groovy, -Sensual                |
| 19  | `Fictional-Track-18d7aa2Fictional-Track-a87ff679.mp3`   | 1→8   | +Contemplative…Yearning; -Chill                             |
| 20  | `Fictional-Track-3eb3f86a.mp3`       | 3→14  | +Chill…Wistful; -Adventurous                                |
| 21  | `Fictional-Track-b85687fd.mp3`           | 4→11  | +Chill…Suspenseful; -Adventurous, -Cozy                     |
| 22  | `Fictional-Track-c82e563Fictional-Track-c81e728d.mp3`         | 4→12  | +Awe-inspired…Tender; -Adventurous, -Chill                  |
| 23  | `Fictional-Track-c70a0dbe.mp3`         | 4→15  | +Anguished…Suspenseful; -Adventurous, -Ethereal, -Nostalgic |
| 24  | `Fictional-Track-0ba787aFictional-Track-8f14e45f.mp3`         | 5→11  | +Contemplative…Spiritual; -Adventurous, -Groovy             |
| 25  | `Fictional-Track-27dc306Fictional-Track-eccbc87e.mp3`              | 4→11  | +Contemplative…Suspenseful; -Adventurous                    |
| 26  | `Fictional-Track-486e8e2Fictional-Track-c9f0f895.mp3`     | 4→11  | +Awe-inspired…Triumphant; -Adventurous, -Chill, -Nostalgic  |
| 27  | `Fictional-Track-53c13129.mp3`        | 6→13  | +Chaotic…Surreal                                            |
| 28  | `Fictional-Track-b3b56a1Fictional-Track-a87ff679.mp3`              | 3→14  | +Awe-inspired…Triumphant; -Ethereal, -Nostalgic             |
| 29  | `Fictional-Track-e0aa0d7Fictional-Track-c9f0f895.mp3`            | 3→10  | +Chill…Suspenseful; -Ethereal                               |
| 30  | `Fictional-Track-94d3b3cc.mp3`      | 5→13  | +Contemplative…Upbeat; -Ethereal                            |
| 31  | `Fictional-Track-cc0a1090.mp3`               | 3→13  | +Aggressive…Triumphant; -Nostalgic                          |
| 32  | `Fictional-Track-ad71808Fictional-Track-1679091c.mp3`                 | 3→9   | +Danceful…Upbeat; -Nostalgic                                |
| 33  | `Fictional-Track-64bbe91f.mp3`                | 2→10  | +Chaotic…Resigned                                           |
| 34  | `Fictional-Track-4f486bfa.mp3`                     | 1→7   | +Bittersweet…Wistful                                        |
| 35  | `Fictional-Track-e9e2cede.mp3`                | 1→9   | +Chaotic…Whimsical                                          |
| 36  | `Fictional-Track-57b1c3eFictional-Track-8f14e45f.mp3`                    | 1→10  | +Chaotic…Whimsical                                          |
| 37  | `Fictional-Track-249f867Fictional-Track-e4da3b7f.mp3`       | 1→11  | +Aggressive…Sad; -Chill                                     |
| 38  | `Fictional-Track-b3350fbFictional-Track-c9f0f895.mp3`             | 1→10  | +Chill…Whimsical                                            |
| 39  | `Fictional-Track-cd38cf29.mp3`   | 2→10  | +Aggressive…Rebellious                                      |
| 40  | `Fictional-Track-6c9f7840.mp3`             | 3→16  | +Chill…Yearning; -Epic                                      |
| 41  | `Fictional-Track-1030ba1Fictional-Track-c9f0f895.mp3`              | 6→11  | +Defiant…Optimistic                                         |
| 42  | `Fictional-Track-171f83aFictional-Track-eccbc87e.mp3`               | 5→7   | +Chaotic…Reverent; -Awe-inspired, -Epic, -Nostalgic         |

---

## Franchise / Genre Cluster Analysis

### Fictional-PhantomWhisper OST (13 tracks)

The largest single-franchise correction sweep in one batch. Near-universal pattern:
removed **Adventurous** (used as catchall for ambient/exploration tracks) and
replaced with accurate temporal/textural descriptors.

Sub-clusters emerging across the 13 RO tracks:

- **Peaceful ambient** (05, 116, 117, 129, 138): gained Contemplative, Introspective,
  Meditative, Spiritual, Peaceful. These are town/field BGMs with quiet exploratory tone.
- **Dark atmospheric** (119-Stained-Memories): gained Anguished/Brooding/Macabre/Surreal —
  this track had a dark ambient profile missed by the old Adventurous label.
- **Energetic/upbeat** (41-Rag-All-Night-Long, 89-We-have-Lee, 93-Latinnova): gained
  Chaotic/Energetic/Frenzy or Danceful/Groovy profile. Battle/town-party BGMs.
- **Triumphant epic** (64-One-Fine-Day, 185-Once-upon-a-December): gained
  Awe-inspired/Epic/Heroic/Triumphant — finale/seasonal event cues.

Before this batch, Adventurous appeared in nearly every RO track. It is now reserved
only for tracks with genuinely adventurous character.

### Fictional-CrystalBell Wind Waker (Dragon-Roost-Island, Wind-Waker-Theme)

Two major WW tracks gained the thematic {Chill, Contemplative, Cozy, Peaceful, Relaxed,
Spiritual, Soaring} cluster. Wind-Waker-Theme grew from 3→16 moods (largest single-track
enrichment in this batch), adding Yearning and dropping Epic — Fictional-Kw-7550156c is emotionally
vast but not epic in the triumphant sense.

Dragon-Roost dropped Ethereal+Triumphant in favor of Danceful+Groovy+Joyful — a
correct shift from the ambiguous "epic sailing" cue to its actual reggae-inspired upbeat
character.

### Fictional-SilverLighthouse (4 tracks)

Fictional-SilverLighthouse now has a coherent profile split:

- **Introspective** (My-Friends, Fictional-Kw-511ff788, Road-Trippin'): Contemplative,
  Introspective, Melancholic, Resigned — mellow end of the catalog.
- **Groovy/Playful** (Fictional-Kw-e0381949, We-Turn-Red): Chaotic, Danceful, Groovy,
  Whimsical — funk-adjacent tracks.

### Fictional-CoralVoyage (Should've-Listened, Next-Go-Round, Too-Bad)

Three tracks, clear split:

- Dark ballads (Should've-Listened, Too-Bad): {Anguished, Heartbreak, Melancholic, Sad}
- Stadium rock (Next-Go-Round): {Aggressive, Chaotic, Frenzy, Triumphant}

### Fictional-BrassWhisper Strive / Game OST (Find-Your-One-Way, Windy-Hill-Zone, Fictional-Kw-fee2713c)

OST tracks losing Nostalgic+Adventurous in favor of combat-specific tags:
Chaotic/Defiant/Furious/Triumphant for GG Strive sol theme, Heroic/Optimistic for
Fictional-AzureShore SSBU, Macabre/Ominous for WoW Fictional-Kw-fee2713c.

---

## Global Mood Frequency (post-batch, top 10)

| Rank | Mood        | Count | % of 970 | Δ     |
| ---- | ----------- | ----- | -------- | ----- |
| 1    | Chill       | 407   | 42.0%    | ↓ -4  |
| 2    | Energetic   | 358   | 36.9%    | ↑     |
| 3    | Adventurous | 268   | 27.6%    | ↓↓ -7 |
| 4    | Nostalgic   | 255   | 26.3%    | ↓ -5  |
| 5    | Aggressive  | 233   | 24.0%    | ↑     |
| 6    | Rebellious  | 207   | 21.3%    | ↑     |
| 7    | Emotional   | 205   | 21.1%    | ↑↑    |
| 8    | Melancholic | 181   | 18.7%    | ↑     |
| 9    | Defiant     | 178   | 18.4%    | ↑     |
| 10   | Upbeat      | 150   | 15.5%    | ↑     |

Key movements:

- **Adventurous** fell from 275→268 (-7) — now dropping steadily as the RO/game OST
  catchall is corrected.
- **Nostalgic** fell from 260→255 (-5) — same pattern, same correction wave.
- **Emotional** climbed to 205 (+12), tied neck-and-neck with Rebellious — driven by
  Fictional-SilverLighthouse, RO peaceful clusters, Fictional-Kw-c4ac2b82, and Fictional-IronSerpent soul.
- **Energetic gap vs Chill**: 407 vs 358 — now only 49 apart (was 70 last batch, was ~120
  before batch 18). Convergence trajectory continues.

---

## Technical Notes

- No HTML in this batch: reviewed count frozen at 476 (49.1% coverage).
- Folder sync was idempotent (0 copies/removes) — files were pre-placed.
- Sliced-data.js received version bump only; no structural or mood changes.
