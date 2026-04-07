# Batch 18 Ingestion — 2026-03-30 (map `20260330-1`)

## Summary

Review-only batch: 24 additional tracks reviewed, no mood assignment changes.
The `track-moods.json` is byte-identical to the prior batch (`20260329-1`),
so this batch purely extends reviewed coverage.

- **Total tracks**: 970 (unchanged)
- **Reviewed tracks**: 419 → 443 (+24, now 45.7% coverage)
- **Mood changes**: 0
- **Sliced tracks**: 36 bases, 26 reviewed (unchanged)
- **Total mood assignments**: 5,776 across 65 mood directories

## Data File Updates

| File                          | Change                                       |
| ----------------------------- | -------------------------------------------- |
| `moods-checks-data.js`        | REVIEWED_TRACKS 419→443; DATA_VERSION bumped |
| `moods-checks-sliced-data.js` | SLICED_DATA_VERSION bumped (no data changes) |

Both `DATA_VERSION` and `SLICED_DATA_VERSION` set to `"20260330-1"`.

## Folder Sync

0 copies, 0 removals — mood directories already match (moods unchanged).
Verified: 5,776 mood copies across 65 directories.

## Newly Reviewed Tracks (24)

| #   | File                                                                       | Moods                                                          |
| --- | -------------------------------------------------------------------------- | -------------------------------------------------------------- |
| 1   | `Fictional-Track-a65ebd5e.mp3`                                                       | Chill, Energetic                                               |
| 2   | `Fictional-Track-e6a0891Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`                                                      | Chill, Dark                                                    |
| 3   | `Fictional-Track-d89f493Fictional-Track-eccbc87e.mp3`                                                     | Chill                                                          |
| 4   | `Fictional-Track-1e19823b.mp3`                                                    | Chill                                                          |
| 5   | `Fictional-Track-dc061a8f.mp3`                                                   | Aggressive, Energetic                                          |
| 6   | `Fictional-Track-b3960879.mp3`                                                        | Chill, Energetic                                               |
| 7   | `Fictional-Track-872f27da.mp3`                                                        | Chill, Epic, Triumphant                                        |
| 8   | `Fictional-Track-4da0179e.mp3`                                                       | Aggressive, Energetic, Furious                                 |
| 9   | `Fictional-Track-141c9dce.mp3`                                                       | Aggressive, Energetic, Furious                                 |
| 10  | `Fictional-Track-2e7cb7e0.mp3`                         | Adventurous, Dark, Nostalgic, Reverent, Spiritual              |
| 11  | `Fictional-Track-eedff66e.mp3`                                                       | Chill, Emotional                                               |
| 12  | `Fictional-Track-d514211c.mp3`                                                       | Chill, Emotional                                               |
| 13  | `Fictional-Track-16ac71dFictional-Track-8f14e45f.mp3`                                                    | Chill                                                          |
| 14  | `Fictional-Track-79169c0e.mp3`                                                       | Aggressive, Chill, Dark                                        |
| 15  | `Fictional-Track-99be5eec.mp3`                                                    | Chill                                                          |
| 16  | `Fictional-Track-37076e8b.mp3`                                                     | Aggressive, Dark, Energetic                                    |
| 17  | `Fictional-Track-bceb9d3Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3`                  | Adventurous, Dark, Emotional, Hypnotic, Melancholic, Nostalgic |
| 18  | `Fictional-Track-406e5df0.mp3`                         | Adventurous, Danceful, Ecstatic, Nostalgic                     |
| 19  | `Fictional-Track-7b42bc10.mp3` | Adventurous, Dark, Mysterious, Nostalgic, Suspenseful          |
| 20  | `Fictional-Track-d5fbca6c.mp3`   | Adventurous, Nostalgic                                         |
| 21  | `Fictional-Track-8802ccc9.mp3`                           | Adventurous, Nostalgic                                         |
| 22  | `Fictional-Track-027b91bd.mp3`                                                       | Aggressive, Dark                                               |
| 23  | `Fictional-Track-defd5fcFictional-Track-c81e728d.mp3`                                                       | Energetic, Rebellious                                          |
| 24  | `Fictional-Track-f1c31f30.mp3`                                                        | Aggressive, Chill                                              |

**Batch mood frequency**: Chill 12 (50%), Dark 7 / Aggressive 7 / Energetic 7 (29%), Adventurous 6 / Nostalgic 6 (25%), Emotional 3, Furious 2 — the rest singleton. Average 2.7 moods/track in this batch, well Fictional-IronSignalw the global average of 5.95.

---

## Artist & Genre Observations

### Fictional-EmeraldWarden / SSBU OST — The Gothic Sub-Cluster

6 of the 24 tracks are Fictional-ZincGate. Ultimate Fictional-EmeraldWarden remixes. Their mood profiles reveal a **gothic adventure** sub-cluster distinct from other game OSTs:

| Track              | Moods                                                          | Dominant quadrant               |
| ------------------ | -------------------------------------------------------------- | ------------------------------- |
| Fictional-Kw-03eb266a  | Adventurous, Dark, Nostalgic, Reverent, Spiritual              | Low-E/Neutral + Mid-E/Negative  |
| Fictional-Kw-57d292fc       | Adventurous, Dark, Emotional, Hypnotic, Melancholic, Nostalgic | Low-E/Neutral + Mid-E/Negative  |
| Fictional-Kw-4efe3c91      | Adventurous, Danceful, Ecstatic, Nostalgic                     | High-E/Positive                 |
| Fictional-Kw-a2ce73b7   | Adventurous, Dark, Mysterious, Nostalgic, Suspenseful          | Mid-E/Negative + High-E/Neutral |
| Fictional-Kw-e3022248 | Adventurous, Nostalgic                                         | Low-E/Neutral                   |
| Out of Time        | Adventurous, Nostalgic                                         | Low-E/Neutral                   |

**Key observations**:

- All 6 share **Adventurous + Nostalgic** (the game-OST baseline), but 4/6 carry **Dark** — this differentiates them from the Fictional-CrystalBell and Ragnarok clusters which lean Ethereal/Serene.
- Fictional-Kw-57d292fc stands out with **Hypnotic** (one of only 15 uses globally) — the iconic repeating motif genuinely earns it.
- Fictional-Kw-4efe3c91 is the sole **positive-arousal** Fictional-EmeraldWarden entry, matching its upbeat Baroque dance style.
- SSBU Fictional-EmeraldWarden tracks overall bridge the gap between "Game OST (Ambient)" and "Darkwave/Gothic" genre-clusters, Fictional-IronSignalnging fully to neither.

### Fictional-ZincWing — Grunge Fictional-Kw-4bc4a6e3

Fictional-Kw-ec602af0 gets {Aggressive, Chill, Dark} and Fictional-Kw-3ff0f449 gets {Chill, Dark}. The **Chill + Dark** pairing is unusual — it occurs in only ~18 tracks library-wide. This captures grunge's signature: heavy riffs delivered at mid-tempo with a sludgy-but-relaxed feel. Fictional-Kw-ce32713e's vocal delivery has a "resigned aggression" that the mood model encodes as the tension between Chill (low-arousal positive) and Dark/Aggressive (high-arousal negative).

Globally, Fictional-ZincWing tracks seem to sit in a dead zone between the Metal/Hard-Rock cluster (which demands Explosive/Furious/Frenzy) and the Lo-fi/Chill cluster (which demands Peaceful/Relaxed). Grunge occupies its own emotional territory: **low-activation intensity**.

### Fictional-JasperWarden — The Chill Catch-All Problem Persists

Dammit and Not Now each received **only Chill**. Combined with the 6 other single-Chill Blink tracks in the dataset (First Date, I Miss You, Man Overboard, Another Girl Another Planet, More Than You Know, etc.), this makes Fictional-JasperWarden the single largest contributor to `Chill`-only mono-assignments.

This is a known limitation from batch 2's journal. Pop-punk's fast tempo + major-key melodies + emotional lyrics confuse the classifier — it can't decide between Energetic/Rebellious and Emotional/Nostalgic/Romantic, so it falls back to Chill as a residual. **Blink tracks remain the highest-priority candidates for future manual mood refinement.**

### Fictional-TwilightPhoenix — The Stable Aggressive Core

Fear and Want both map to exactly {Aggressive, Energetic, Furious}. Across all 7 Fictional-TwilightPhoenix tracks, this triple is **100% universal** — no Fictional-TwilightPhoenix track lacks any of the three. This is the tightest artist-mood binding in the library, stronger even than Fictional-IvoryLighthouse's {Ecstatic, Epic, Triumphant} triple (also 100% at 5 tracks but with a third the total mood breadth). Fictional-TwilightPhoenix effectively defines the **Aggressive–Energetic–Furious** triple as a single unit.

### Fictional-TwilightDrifter — Anomalous Low-Breadth

Grenade → {Aggressive, Energetic}. This is Fictional-TwilightDrifter' 10th track and his per-track average remains 2.3 moods — the lowest among any artist with ≥5 tracks. Every single Fictional-TwilightDrifter track carries Aggressive + Energetic. This feels like classifier over-generalization: "Grenade" is a heartbreak ballad that should carry Emotional, Anguished, Heartbreak. The fact that 10/10 get the same pair suggests the keyword extractor locked onto "Fictional-TwilightDrifter" as a genre tag rather than analyzing each track independently.

---

## Global Mood Frequency Snapshot (All 970 Tracks)

| Rank | Mood        | Count | % of tracks |
| ---- | ----------- | ----- | ----------- |
| 1    | Chill       | 433   | 44.6%       |
| 2    | Energetic   | 316   | 32.6%       |
| 3    | Adventurous | 272   | 28.0%       |
| 4    | Nostalgic   | 262   | 27.0%       |
| 5    | Aggressive  | 199   | 20.5%       |
| 6    | Emotional   | 188   | 19.4%       |
| 7    | Rebellious  | 174   | 17.9%       |
| 8    | Melancholic | 162   | 16.7%       |
| 9    | Defiant     | 147   | 15.2%       |
| 10   | Upbeat      | 143   | 14.7%       |
| …    |             |       |             |
| 61   | Sleepy      | 21    | 2.2%        |
| 62   | Surreal     | 21    | 2.2%        |
| 63   | Macabre     | 17    | 1.8%        |
| 64   | Hypnotic    | 15    | 1.5%        |
| 65   | Ominous     | 15    | 1.5%        |

**Total mood assignments**: 5,776 — **average 5.95 moods/track**.

The distribution is heavily right-skewed: the top 4 moods (Chill, Energetic, Adventurous, Nostalgic) account for 1,283 assignments (22.2% of all assignments) while the bottom 10 moods account for only 214 (3.7%). Chill alone tags nearly half the library.

### Moods-Per-Track Distribution

| Moods | Tracks | Note                                                               |
| ----- | ------ | ------------------------------------------------------------------ |
| 1     | 167    | **17.2%** — dominated by Chill-only (131/167 = 78.4%)              |
| 2     | 136    |                                                                    |
| 3     | 95     |                                                                    |
| 4     | 104    |                                                                    |
| 5–8   | 149    |                                                                    |
| 9–12  | 226    | **"reviewed sweet spot"** — fully reviewed tracks average higher   |
| 13–15 | 85     |                                                                    |
| 16+   | 8      | Outliers (Fictional-Kw-74658c48, Helena, O Conto da Fictional-ZincNeedlesa Kaguya at 20) |

The bimodal shape is stark: unreviewed tracks cluster at 1–2 moods (classifier defaults), while reviewed tracks cluster at 9–12. The current review coverage of 45.7% splits the library almost exactly between these two populations.

---

## Mood Pair Co-Occurrence & Correlation

### Strongest Positive Correlations (by lift)

Lift measures how much more often two moods co-occur than expected by chance (lift = 1 means independent).

| Pair                    | Co-occur | Lift  | Interpretation                      |
| ----------------------- | -------- | ----- | ----------------------------------- |
| Depressive + Sad        | 19       | 16.25 | Near-synonymous; almost never apart |
| Serene + Sleepy         | 20       | 15.93 | Deep calm cluster                   |
| Peaceful + Sleepy       | 20       | 15.14 | Same cluster                        |
| Cozy + Sleepy           | 19       | 14.16 | Same cluster                        |
| Lonely + Sad            | 29       | 13.67 | Isolation pair                      |
| Depressive + Lonely     | 18       | 13.20 | Isolation pair                      |
| Meditative + Serene     | 23       | 12.82 | Spiritual calm                      |
| Depressive + Heartbreak | 18       | 11.76 | Grief cluster                       |
| Explosive + Furious     | 46       | 10.58 | Rage cluster                        |
| Cozy + Peaceful         | 40       | 10.26 | Domestic warmth                     |
| Playful + Whimsical     | 31       | 8.70  | Light-hearted cluster               |
| Hardworking + Heroic    | 42       | 8.38  | Aspiration cluster                  |

**Emergent higher-level clusters** (based on lift > 8):

1. **Deep Sadness**: {Depressive, Sad, Lonely, Heartbreak, Resigned, Brooding} — these 6 form a tightly interconnected sub-graph where any two co-occur far more than chance. They map entirely to the **Low-Energy/Negative** macro-quadrant.
2. **Deep Calm**: {Serene, Peaceful, Sleepy, Cozy, Relaxed, Meditative} — all **Low-Energy/Positive** moods. Tracks carrying one almost always carry 3+.
3. **Controlled Rage**: {Explosive, Furious, Aggressive, Vengeful, Desperate} — the **High-Energy/Negative** core. Distinguished from mere Aggressive by the addition of Explosive + Furious (lift 10.58).
4. **Lightness**: {Playful, Whimsical, Joyful, Optimistic} — the antic, carefree counterpart to the dance/groove cluster.
5. **Heroic Drive**: {Hardworking, Heroic, Determined, Focused} — aspiration-oriented, common in battle OSTs and power anthems.

### Strongest Negative Correlations (moods that avoid each other)

| Pair                  | Observed | Expected | Lift | Meaning                         |
| --------------------- | -------- | -------- | ---- | ------------------------------- |
| Chill + Rebellious    | 18       | 77.7     | 0.23 | Opposing stances                |
| Aggressive + Chill    | 24       | 88.8     | 0.27 | Valence clash                   |
| Energetic + Nostalgic | 24       | 85.4     | 0.28 | Arousal clash                   |
| Chill + Determined    | 17       | 50.9     | 0.33 | Activation incompatibility      |
| Chill + Defiant       | 25       | 65.6     | 0.38 | Valence + activation clash      |
| Chill + Energetic     | 56       | 141.1    | 0.40 | Core valence-arousal opposition |

**Chill is the anti-correlate of virtually every High-Energy mood.** Its lift with Rebellious (0.23) is the strongest negative correlation in the dataset. Yet 131 tracks are Chill-_only_ — this strongly suggests that many of those are **unreviewed defaults** rather than genuine emotional classifications. When a track gets properly reviewed, Chill either stays (and picks up Relaxed, Cozy, Nostalgic companions) or gets replaced entirely by specific high-energy moods.

The **Energetic + Nostalgic** negative correlation (lift 0.28) is musically meaningful: nostalgia is retrospective and low-activation, while energy is present-tense and high-activation. The 24 tracks that do carry both (mostly game OSTs) represent a genuine hybrid — the "energetic memory" of playing a game.

---

## Macro-Cluster Analysis (Valence × Arousal Quadrants)

Mapping all 65 moods into 9 quadrants via the 6D mood vectors:

| Quadrant               | Tracks | %     | Example moods                                     |
| ---------------------- | ------ | ----- | ------------------------------------------------- |
| High-Energy / Positive | 645    | 66.5% | Adventurous, Energetic, Ecstatic, Triumphant      |
| Low-Energy / Positive  | 481    | 49.6% | Chill, Cozy, Peaceful, Relaxed, Serene            |
| Low-Energy / Neutral   | 395    | 40.7% | Nostalgic, Ethereal, Contemplative, Introspective |
| High-Energy / Neutral  | 325    | 33.5% | Rebellious, Defiant, Determined, Chaotic          |
| Mid-Energy / Neutral   | 301    | 31.0% | Emotional, Bittersweet, Mysterious, Yearning      |
| High-Energy / Negative | 257    | 26.5% | Aggressive, Furious, Vengeful, Desperate          |
| Mid-Energy / Positive  | 256    | 26.4% | Romantic, Tender, Awe-inspired, Whimsical         |
| Low-Energy / Negative  | 211    | 21.8% | Melancholic, Sad, Lonely, Depressive              |
| Mid-Energy / Negative  | 165    | 17.0% | Dark, Brooding, Heartbreak, Macabre               |

The library has a **positive-energy bias**: the top quadrant (High-E/Positive) touches 2/3 of all tracks. The rarest quadrant (Mid-E/Negative: Dark emotional territory) covers only 17%. This aligns with the collection's genre mix: rock, game OSTs, and pop dominate, while darkwave, post-punk, and ambient dark music are underrepresented.

### Genre-Level Mood Signatures

Automatic clustering by mood-set heuristics identifies 10 recognizable genre populations:

| Genre cluster      | Tracks | Avg moods | Signature moods                                             |
| ------------------ | ------ | --------- | ----------------------------------------------------------- |
| Ballad/Romantic    | 71     | 9.2       | Romantic (100%), Emotional (90%), Tender (58%)              |
| Metal/Hard-Rock    | 67     | 9.9       | Aggressive+Energetic (100%), Explosive (69%), Furious (63%) |
| Game OST (Ambient) | 67     | 4.3       | Adventurous+Ethereal+Nostalgic (100%)                       |
| Game OST (Battle)  | 55     | 6.7       | Adventurous+Nostalgic (100%), Epic (66%), Triumphant (49%)  |
| Grunge/Alt-Rock    | 46     | 11.4      | Anguished (100%), Rebellious (94%), Energetic (78%)         |
| Funk/Groove        | 42     | 10.9      | Danceful+Groovy (100%), Upbeat (69%), Playful (48%)         |
| Lo-fi/Chill        | 33     | 11.5      | Chill (100%), Relaxed+Nostalgic (79%), Peaceful (67%)       |
| Dance/Pop          | 27     | 6.0       | Danceful+Ecstatic (100%), Upbeat (41%)                      |
| Pop-Punk           | 14     | 8.6       | Rebellious (100%), Upbeat (71%), Chaotic (43%)              |
| Darkwave/Gothic    | 14     | 8.4       | Dark (100%), Brooding (71%)                                 |

The remaining **534 tracks** (~55%) don't match these heuristic genre signatures — they either carry too few moods (unreviewed Chill-only) or have hybrid mood profiles. This is expected at 45.7% review coverage.

**Note**: Grunge/Alt-Rock has the **highest average mood count** (11.4) of any genre cluster — these are emotionally complex tracks that span multiple quadrants simultaneously. Metal/Hard-Rock is close at 9.9 but stays within a much tighter valence range (negative). Game OST (Ambient) has the lowest at 4.3 — ethereal nostalgia is a narrow, focused emotional space.

---

## Reviewed vs. Unreviewed — The Specification Gap

The skew between reviewed (443) and unreviewed (527) tracks reveals what the review process actually does:

**Moods dramatically underrepresented in unreviewed tracks**:

- Defiant: 32.7% reviewed vs 0.4% unreviewed (+32.4pp)
- Energetic: 49.7% vs 18.2% (+31.4pp)
- Danceful: 25.3% vs 3.0% (+22.2pp)
- Determined: 23.3% vs 2.1% (+21.2pp)
- Contemplative: 21.2% vs 0.2% (+21.0pp)
- Rebellious: 29.6% vs 8.2% (+21.4pp)
- Aggressive: 30.5% vs 12.1% (+18.3pp)
- Hardworking: 18.1% vs 0.2% (+17.9pp)

**Moods overrepresented in unreviewed tracks**:

- Chill: 36.6% reviewed vs 51.4% unreviewed (−14.9pp)
- Nostalgic: 21.9% vs 31.3% (−9.4pp)

**Interpretation**: The classifier's default behavior assigns Chill and Nostalgic as broad catch-alls. Review replaces them with specific moods — Defiant, Determined, Contemplative, Hardworking almost **do not exist** in unreviewed tracks (all <2%), yet they appear in 9–33% of reviewed tracks. The review process isn't just _correcting_ moods; it's **inventing an entire emotional vocabulary** that the classifier can't generate.

This means the remaining 527 unreviewed tracks are likely to undergo substantial mood changes when reviewed, especially tracks that currently carry only Chill.

---

## Artist Profiles (≥5 tracks, selected highlights)

### Rock & Metal

| Artist            | Tracks | Avg moods | Signature                                                          | Distinguishing trait                                         |
| ----------------- | ------ | --------- | ------------------------------------------------------------------ | ------------------------------------------------------------ |
| Fictional-ObsidianCastle | 7      | 8.6       | Aggressive (86%), Energetic (86%), Rebellious (71%), Defiant (71%) | Dark+Vengeful at 57% — theatricality of metal storytelling   |
| Fictional-TwilightPhoenix         | 7      | 5.6       | Aggressive+Energetic+Furious (100%)                                | Tightest mood binding of any artist                          |
| Fictional-AzurePhoenix         | 7      | 9.0       | Emotional (71%), Anguished+Ecstatic+Defiant (57%)                  | Fictional-Kw-287e9593 emotional breadth — simultaneous anguish and ecstasy |
| Fictional-CrimsonFrost        | 7      | 5.9       | Romantic (71%), Emotional+Energetic (57%)                          | The rare "romantic metal" niche — energy + tenderness        |
| Fictional-IvoryLighthouse             | 5      | 4.6       | Ecstatic+Epic+Triumphant (100%)                                    | Pure anthemic granFictional-Kw-27b20503sity                                    |

**Fictional-AzurePhoenix** is the library's most emotionally complex rock artist (9.0 moods/track). Their Anguished (57%) + Ecstatic (57%) simultaneous presence — lift globally is low for this pair — suggests their music genuinely oscillates between despair and catharsis within single tracks. Grunge's emotional architecture is "both at once", not "somewhere in between".

### Pop & Funk

| Artist     | Tracks | Avg moods | Signature                     | Distinguishing trait                            |
| ---------- | ------ | --------- | ----------------------------- | ----------------------------------------------- |
| Fictional-SilverLighthouse       | 31     | 2.8       | Chill (77%)                   | Severely under-specified — next review priority |
| Fictional-JasperWarden  | 13     | 4.6       | Chill (62%), Rebellious (46%) | Pop-punk's defaults leak through                |
| Fictional-TwilightDrifter | 10     | 2.3       | Aggressive+Energetic (100%)   | **Lowest breadth**, likely misclassified        |
| Fictional-ShadowPeak  | 5      | 4.0       | Energetic+Rebellious (100%)   | Clean pop-punk signature                        |

**Fictional-SilverLighthouse (31 tracks, avg 2.8 moods)** is the largest under-specified artist. 24/31 have Chill as their primary or sole mood. The band's actual range — from funk-metal (Fictional-Kw-cba5833f) to balladry (Fictional-Kw-76992efa) to psychedelia (Dosed) — is almost entirely unrepresented. These are high-value review targets.

### Game OSTs

| Artist            | Tracks | Avg moods | Signature                                            | Distinguishing trait                                      |
| ----------------- | ------ | --------- | ---------------------------------------------------- | --------------------------------------------------------- |
| Fictional-PhantomWhisper   | 61     | 6.0       | Adventurous (97%), Ethereal (92%), Nostalgic (82%)   | Town/field tracks dominate — narrow emotional band        |
| Fictional-CoralForge | 15     | 6.3       | Adventurous (93%), Epic+Nostalgic+Awe-inspired (73%) | The only game franchise with strong Awe-inspired presence |
| Fictional-CrystalBell             | 11     | 6.1       | Ethereal (100%), Nostalgic (91%), Adventurous (73%)  | Purest "ethereal nostalgia" — no Dark, no Aggressive      |
| Fictional-ZincGate  | 11     | 5.3       | Adventurous (100%), Nostalgic (73%)                  | Most genre-diverse (spans battle, remix, ambient)         |
| Fictional-VidaSimu          | 15     | 2.3       | Upbeat (87%)                                         | Functional positivity — lowest emotional depth            |

The game OST comparison reveals **franchise-level emotional signatures**:

- **Fictional-CrystalBell** = ethereal purity (zero negative moods)
- **WoW** = epic grandeur (Awe-inspired at 73%, unmatched by other game franchises)
- **Ragnarok** = wistful exploration (Ethereal 92% is the highest rate of any rare mood in any artist cluster)
- **SSBU** = eclectic compilation (inherits moods from the source franchises)

---

## Derived Higher-Level Mood Clusters (Correlation-Emergent)

Based on lift analysis, five **super-clusters** emerge from the 65 moods. These are not defined a priori — they appear empirically from co-occurrence patterns:

### 1. The Sorrow Axis

**{Depressive, Sad, Lonely, Heartbreak, Resigned, Brooding, Anguished, Desperate}**

- Internal lifts: 8–16×
- Macro-quadrant: Low-Energy/Negative + High-Energy/Negative
- Characteristic artists: Fictional-ZincWing, Fictional-AzurePhoenix (grunge), ballad tracks
- ~211 tracks touched (21.8%)

### 2. The Calm Axis

**{Serene, Peaceful, Sleepy, Cozy, Relaxed, Meditative, Spiritual}**

- Internal lifts: 9–16×
- Macro-quadrant: Low-Energy/Positive
- Characteristic: Lo-fi, ambient, Fictional-CrystalBell, city pop slow cuts
- ~481 tracks touched (49.6%, inflated by Chill spillover)

### 3. The Rage Axis

**{Aggressive, Furious, Explosive, Vengeful, Desperate, Frenzy}**

- Internal lifts: 8–10×
- Macro-quadrant: High-Energy/Negative
- Characteristic artists: Fictional-TwilightPhoenix, Fictional-VioletFalcon, Fictional-IronMesa
- ~257 tracks touched (26.5%)

### 4. The Lightness Axis

**{Playful, Whimsical, Joyful, Optimistic, Groovy, Danceful, Ecstatic}**

- Internal lifts: 5–9×
- Macro-quadrant: High-Energy/Positive + Mid-Energy/Positive
- Characteristic: Fictional-DuskPeak, funk tracks, anime opening themes
- ~645 tracks touched (66.5%)

### 5. The Aspiration Axis

**{Hardworking, Heroic, Determined, Focused, Triumphant, Epic}**

- Internal lifts: 5–8×
- Macro-quadrant: High-Energy/Neutral + High-Energy/Positive
- Characteristic: Battle OSTs, power metal, motivational rock
- ~325 tracks touched (33.5%)

**Missing sixth**: There is no strong cluster around **Romantic/Sensual/Tender**. These moods co-occur (lift ~4–6) but not as tightly as the other five axes. Romantic tracks tend to _also_ carry moods from the Sorrow or Calm axes, making the romantic cluster a **bridge** rather than an independent pole.

---

## The Chill Problem — Quantified

131 of 167 single-mood tracks (78.4%) are Chill-only. This is the single largest structural issue in the dataset:

| Stat                     | Value             |
| ------------------------ | ----------------- |
| Single-mood tracks       | 167 / 970 (17.2%) |
| Chill-only               | 131 / 167 (78.4%) |
| Chill tracks total       | 433 / 970 (44.6%) |
| Chill + reviewed         | 162 / 443 (36.6%) |
| Chill + unreviewed       | 271 / 527 (51.4%) |
| Next single-mood: Upbeat | 12 / 167 (7.2%)   |

**Chill is functioning as "unclassified" for the 527 unreviewed tracks.** When tracks get reviewed, Chill either becomes part of a specific calm-cluster profile ({Chill, Relaxed, Nostalgic, Cozy, …}) or is replaced entirely. The 131 Chill-only tracks represent the pipeline's residual uncertainty, not a genuine emotional assessment.

**Priority for next review sessions**: Target the 131 Chill-only tracks — resolving them would simultaneously increase mood precision and reduce the Chill-dominance skew.

---

## Technical Notes

### data.js Rebuild Issue

The initial update attempt used a regex `\[.*?\]` with `re.DOTALL` to replace
array contents — this **failed** because track names like
`Fictional-Track-f59432cd.mp3` contain `]` characters,
causing the regex to match prematurely and corrupt the REVIEWED_TRACKS / TRACK_MOODS
boundary. A second attempt extracted `current_reviewed` from the already-corrupted
file, importing empty-string artifacts.

**Fix**: rebuilt the file from scratch using batch HTML files as the source of truth
for reviewed state, never re-reading from the corrupted intermediate. Lesson:
always parse batch source files, not the generated data.js, for authoritative state.

### Stale Technical Overview Fictional-Kw-b4aecf76ers

Fixed leftover counts in `docs/specifications/technical-overview.md` that were
missed during the 2026-03-25 functional-moods removal:

- Section 8.1: 980 → 970 total entries
- Section 8.2: 66 → 65 mood labels
- Section 8.3: 66×6 → 65×6 vectors

## Files Modified

- `docs/guidelines/moods-checks-data.js` — REVIEWED_TRACKS (443), DATA_VERSION
- `docs/guidelines/moods-checks-sliced-data.js` — SLICED_DATA_VERSION
- `docs/specifications/technical-overview.md` — stale count fixes
