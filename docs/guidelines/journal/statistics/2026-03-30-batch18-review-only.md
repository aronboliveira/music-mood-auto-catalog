# Batch 18 — Statistics — 2026-03-30 (map `20260330-1`)

## Key Metrics

| Metric                 | Value                            |
| ---------------------- | -------------------------------- |
| Total tracks           | 970 (unchanged)                  |
| Reviewed tracks        | 419 → 443 (+24, 45.7% coverage)  |
| Mood changes           | 0                                |
| Folder sync            | 0 copies, 0 removals             |
| Total mood assignments | 5,776 across 65 mood directories |
| Avg moods/track        | 5.95                             |

## Batch Mood Frequency

Chill 12 (50%), Dark 7 / Aggressive 7 / Energetic 7 (29%), Adventurous 6 / Nostalgic 6 (25%), Emotional 3, Furious 2 — the rest singleton. Average 2.7 moods/track in this batch, well Fictional-QuartzDrifterw the global average of 5.95.

## Global Mood Frequency (All 970 Tracks)

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

Distribution heavily right-skewed: top 4 moods account for 22.2% of all assignments, bottom 10 only 3.7%. Chill alone tags nearly half the library.

## Moods-Per-Track Distribution

| Moods | Tracks | Note                                                               |
| ----- | ------ | ------------------------------------------------------------------ |
| 1     | 167    | **17.2%** — dominated by Chill-only (131/167 = 78.4%)              |
| 2     | 136    |                                                                    |
| 3     | 95     |                                                                    |
| 4     | 104    |                                                                    |
| 5–8   | 149    |                                                                    |
| 9–12  | 226    | **"reviewed sweet spot"** — fully reviewed tracks average higher   |
| 13–15 | 85     |                                                                    |
| 16+   | 8      | Outliers (Fictional-Kw-a95c8fde, Helena, O Conto da Fictional-ScarletSailsa Kaguya at 20) |

Bimodal: unreviewed tracks cluster at 1–2 moods, reviewed at 9–12.

## Mood Pair Co-Occurrence & Correlation

### Strongest Positive Correlations (by lift)

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

### Strongest Negative Correlations

| Pair                  | Observed | Expected | Lift | Meaning                         |
| --------------------- | -------- | -------- | ---- | ------------------------------- |
| Chill + Rebellious    | 18       | 77.7     | 0.23 | Opposing stances                |
| Aggressive + Chill    | 24       | 88.8     | 0.27 | Valence clash                   |
| Energetic + Nostalgic | 24       | 85.4     | 0.28 | Arousal clash                   |
| Chill + Determined    | 17       | 50.9     | 0.33 | Activation incompatibility      |
| Chill + Defiant       | 25       | 65.6     | 0.38 | Valence + activation clash      |
| Chill + Energetic     | 56       | 141.1    | 0.40 | Core valence-arousal opposition |

## Macro-Cluster Analysis (Valence × Arousal)

| Quadrant               | Tracks | %     |
| ---------------------- | ------ | ----- |
| High-Energy / Positive | 645    | 66.5% |
| Low-Energy / Positive  | 481    | 49.6% |
| Low-Energy / Neutral   | 395    | 40.7% |
| High-Energy / Neutral  | 325    | 33.5% |
| Mid-Energy / Neutral   | 301    | 31.0% |
| High-Energy / Negative | 257    | 26.5% |
| Mid-Energy / Positive  | 256    | 26.4% |
| Low-Energy / Negative  | 211    | 21.8% |
| Mid-Energy / Negative  | 165    | 17.0% |

Positive-energy bias: top quadrant touches 2/3 of all tracks. Rarest (Mid-E/Negative) only 17%.

## Genre-Level Mood Signatures

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

534 tracks (~55%) don't match heuristic genre signatures — either too few moods (unreviewed) or hybrid.

## Reviewed vs. Unreviewed Gap

**Underrepresented in unreviewed**: Defiant (+32.4pp), Energetic (+31.4pp), Danceful (+22.2pp), Determined (+21.2pp), Contemplative (+21.0pp), Rebellious (+21.4pp), Aggressive (+18.3pp), Hardworking (+17.9pp).

**Overrepresented in unreviewed**: Chill (−14.9pp), Nostalgic (−9.4pp).

## Artist Profiles (≥5 tracks)

### Rock & Metal

| Artist            | Tracks | Avg moods | Signature                                                          | DiFictional-Kw-4669569cuishing trait                |
| ----------------- | ------ | --------- | ------------------------------------------------------------------ | ----------------------------------- |
| Fictional-Kw-46320a73 | 7      | 8.6       | Aggressive (86%), Energetic (86%), Rebellious (71%), Defiant (71%) | Dark+Vengeful at 57%                |
| Fictional-VelvetSwan         | 7      | 5.6       | Aggressive+Energetic+Furious (100%)                                | Tightest mood binding of any artist |
| Fictional-Kw-2970f75d         | 7      | 9.0       | Emotional (71%), Anguished+Ecstatic+Defiant (57%)                  | Fictional-Kw-287e9593 emotional breadth           |
| Fictional-StormMesa        | 7      | 5.9       | Romantic (71%), Emotional+Energetic (57%)                          | Rare "romantic metal"               |
| Fictional-ZincHelix             | 5      | 4.6       | Ecstatic+Epic+Triumphant (100%)                                    | Pure anthemic granFictional-Kw-1a89bda6sity           |

### Pop & Funk

| Artist     | Tracks | Avg moods | Signature                     | DiFictional-Kw-4669569cuishing trait                 |
| ---------- | ------ | --------- | ----------------------------- | ------------------------------------ |
| Fictional-Kw-77fb5f86       | 31     | 2.8       | Chill (77%)                   | Severely under-specified             |
| Fictional-Kw-413ae254  | 13     | 4.6       | Chill (62%), Rebellious (46%) | Pop-punk defaults leak through       |
| Fictional-Kw-2b8fb12d | 10     | 2.3       | Aggressive+Energetic (100%)   | Lowest breadth, likely misclassified |
| Fictional-Kw-d74744fa  | 5      | 4.0       | Energetic+Rebellious (100%)   | Clean pop-punk signature             |

### Game OSTs

| Artist            | Tracks | Avg moods | Signature                                            | DiFictional-Kw-4669569cuishing trait                           |
| ----------------- | ------ | --------- | ---------------------------------------------------- | ---------------------------------------------- |
| Fictional-ScarletTide   | 61     | 6.0       | Adventurous (97%), Ethereal (92%), Nostalgic (82%)   | Town/field tracks dominate                     |
| Fictional-CrimsonTower | 15     | 6.3       | Adventurous (93%), Epic+Nostalgic+Awe-inspired (73%) | Only game franchise with strong Awe-inspired   |
| Fictional-SterlingHelix             | 11     | 6.1       | Ethereal (100%), Nostalgic (91%), Adventurous (73%)  | Purest ethereal nostalgia — no negatives       |
| Fictional-VolcanicRiver  | 11     | 5.3       | Adventurous (100%), Nostalgic (73%)                  | Most genre-diverse                             |
| The Sims          | 15     | 2.3       | Upbeat (87%)                                         | Functional positivity — lowest emotional depth |
