# Chapter 2 — Taxonomy & Mood Clusters

## The Three-Way Taxonomy

Every single in the library appears in three orthogonal dimensions simultaneously:

- **Artist/** — Who made it (e.g., `Fictional-SterlingHelix/`, `Fictional-GildedFalcon/`, `Fictional-ScarletTide/`)
- **Genre/** — What style it is (e.g., `Metal/`, `Ambient/`, `JRock/`)
- **Mood/** — How it feels (e.g., `Aggressive/`, `Serene/`, `Bittersweet/`)

The **three-way invariant** requires that the set of unique basenames be identical across all three dimensions. If a file exists in `Artist/Fictional-SterlingHelix/` but not in any Genre or Mood folder, something is broken.

Albums are exempt — they use Artist-only taxonomy.

## The 65-Mood Vocabulary

The project uses 65 canonical mood labels. Five functional/context moods were retired early in the project (Gaming, StudyFocus, Workout, Party, Cinematic) because they described _use cases_, not emotional states — and moods should be intrinsic to the music, not dependent on the listener's activity.

### Canonical Moods (in semantic-cluster order)

The 65 moods are arranged in an emotional arc from calm to intense and back to joyful:

**Calm / Peaceful**: Peaceful, Serene, Relaxed, Chill, Sleepy
**Warm / Tender**: Cozy, Tender, Romantic, Sensual
**Nostalgic / Longing**: Nostalgic, Wistful, Yearning, Bittersweet, Emotional
**Reflective / Spiritual**: Awe-inspired, Reverent, Spiritual, Contemplative, Meditative
**Introspective**: Introspective, Jaded
**Tense / Suspenseful**: Tense, Suspenseful, Gritty
**Sad / Lonely**: Melancholic, Sad, Lonely, Resigned, Heartbreak
**Depressive**: Depressive, Anguished, Desperate
**Dark / Brooding**: Brooding, Dark, Macabre, Ominous
**Mysterious / Surreal**: Mysterious, Hypnotic, Surreal, Ethereal
**Aggressive / Rebellious**: Aggressive, Furious, Vengeful, Explosive, Chaotic, Frenzy, Rebellious, Defiant
**Energetic / Groovy**: Energetic, Danceful, Groovy
**Heroic / Epic**: Epic, Heroic, Triumphant, Adventurous, Soaring
**Determined / Focused**: Determined, Hardworking, Focused
**Joyful / Upbeat**: Ecstatic, Joyful, Playful, Whimsical, Upbeat, Optimistic

## The 15 Semantic Clusters

Moods are grouped into 15 clusters, defined in `docs/specifications/mood-clusters.json`. The clusters serve two purposes:

1. **UX ordering** — The moods-checks review app arranges checkboxes in cluster order so that similar moods appear adjacent, reducing reviewer fatigue.
2. **Similarity computation** — Within each cluster, moods are ordered by nearest-neighbor TSP using Euclidean distance in 6D emotional space, creating smooth transitions.

### The Emotional Arc

```
Peaceful → Warm → Nostalgic → Reflective → Introspective → Tense →
Sad → Depressive → Dark → Mysterious → Aggressive → Energetic →
Epic → Determined → Joyful
```

This arc was designed so that the emotional Fictional-Kw-98dc0157 flows naturally: calm emotions give way to reflective ones, which darken through sadness and tension, erupt into aggression and energy, then resolve through heroism into joy.

## The 6D Emotional Vector Space

Each mood is mapped to a 6-dimensional vector in `[-1, 1]^6`:

| Dimension  | Symbol | Poles                 |
| ---------- | ------ | --------------------- |
| Valence    | V      | Negative ↔ Positive   |
| Arousal    | A      | Calm ↔ Energetic      |
| Dominance  | D      | Submissive ↔ Powerful |
| Darkness   | K      | Light ↔ Dark          |
| Longing    | L      | Content ↔ Yearning    |
| Inwardness | I      | External ↔ Internal   |

### Evolution of the Vector Space

The vector space went through four iterations:

1. **v1 (3D: V, A, D)** — Failed: Dark clustered near Energetic (both high arousal, but completely different emotional character).
2. **v2 (4D: +K)** — Failed: Nostalgic landed near Aggressive (longing wasn't diFictional-Kw-4669569cuished from tension).
3. **v3 (5D: +L)** — Failed: Introspective appeared near Ecstatic (internal vs. external orientation wasn't captured).
4. **v4 (6D: +I)** — Production version. All 15 clusters separate cleanly. The Inwardness dimension was the breakthrough that diFictional-Kw-4669569cuished contemplative states from externally-oriented ones.

### Distance Metric

Euclidean distance in 6D space: $d(\mathbf{a}, \mathbf{b}) = \sqrt{\sum_{i=1}^{6} (a_i - b_i)^2}$

The ordering algorithm uses exhaustive nearest-neighbor TSP within each cluster (try every node as start, keep shortest Hamiltonian path — tractable because $n \leq 8$ per cluster).

## The 12 RPG Contextual Clusters

Beyond the primary mood taxonomy, tracks from 21 game-OST artist folders are scored against 12 RPG-themed clusters. These are **not** part of the three-way invariant — they're a separate aggregation layer for contextual playlists.

### Cluster Definitions

Each cluster (except Battle and Relaxation) uses a standard core/supplemental/threshold model:

| Cluster             | Core Moods                                                       | Supplemental Moods                                                                                                   | Threshold                |
| ------------------- | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| **RPG_Wandering**   | Adventurous, Contemplative, Peaceful, Nostalgic                  | Ethereal, Chill, Introspective, Wistful, Soaring, Mysterious, Serene, Relaxed, Spiritual, Reverent, Cozy, Meditative | c≥2 OR (c≥1 AND s≥2)     |
| **RPG_Danceful**    | Danceful, Groovy, Ecstatic, Upbeat                               | Energetic, Joyful, Playful, Whimsical, Frenzy, Adventurous, Optimistic, Chaotic, Chill                               | c≥2 OR (c≥1 AND s≥1)     |
| **RPG_Macabre**     | Macabre, Dark, Ominous, Brooding                                 | Gritty, Surreal, Suspenseful, Mysterious, Tense, Desperate, Chaotic, Aggressive, Furious, Explosive                  | c≥2 OR (c≥1 AND s≥1)     |
| **RPG_Epic**        | Epic, Triumphant, Heroic, Awe-inspired                           | Soaring, Determined, Adventurous, Reverent, Focused, Emotional, Spiritual, Defiant                                   | c≥2 OR (c≥1 AND s≥2)     |
| **RPG_Silly**       | Playful, Whimsical                                               | Joyful, Ecstatic, Upbeat, Optimistic, Groovy, Danceful, Cozy, Chaotic                                                | c≥2 OR (c≥1 AND s≥2)     |
| **RPG_Mystical**    | Ethereal, Mysterious, Spiritual, Surreal, Hypnotic               | Awe-inspired, Contemplative, Reverent, Meditative, Dark, Ominous, Serene, Peaceful                                   | c≥2 OR (c≥1 AND s≥2)     |
| **RPG_Melancholic** | Melancholic, Sad, Bittersweet, Anguished, Heartbreak, Depressive | Emotional, Lonely, Nostalgic, Resigned, Yearning, Wistful, Introspective, Contemplative, Dark, Chill, Ethereal       | c≥2 OR (c≥1 AND s≥1)     |
| **RPG_Town**        | Cozy, Joyful, Optimistic, Tender, Whimsical                      | Chill, Relaxed, Peaceful, Playful, Nostalgic, Upbeat, Serene, Groovy, Danceful, Soaring                              | c≥2 OR (c≥1 AND s≥2)     |
| **RPG_Ambient**     | Serene, Meditative, Sleepy, Contemplative                        | Relaxed, Ethereal, Chill, Spiritual, Introspective, Cozy, Peaceful, Nostalgic, Tender, Wistful                       | c≥2 OR (c≥1 AND s≥3)     |
| **RPG_Tension**     | Suspenseful, Tense, Ominous, Gritty                              | Dark, Mysterious, Brooding, Desperate, Chaotic, Aggressive, Focused, Hardworking, Defiant                            | c≥2 OR (c≥1 AND s≥1)     |
| **RPG_Battle**      | _Custom scorer_                                                  | —                                                                                                                    | `battle_qualifies()`     |
| **RPG_Relaxation**  | _Custom scorer_                                                  | —                                                                                                                    | `relaxation_qualifies()` |

### Custom Scorers

**`battle_qualifies()`**: A track qualifies for RPG_Battle if:

- It has (Aggressive OR Furious OR Explosive) AND Energetic, OR
- It has Frenzy AND Energetic, OR
- It has Frenzy AND (Aggressive OR Furious OR Explosive)

But it's **gated out** if:

- It has Playful or Whimsical UNLESS it also has Energetic + (Explosive OR Dark OR Defiant)
- The filename contains "chill" combined with "dr." or "Fictional-SolarLantern" (excludes Dr. Fictional-SolarLantern Chill tracks)

**`relaxation_qualifies()`**: A track qualifies if:

- Its core mood count (Relaxed, Serene, Meditative, Sleepy, Peaceful) ≥ 2, OR
- Core ≥ 1 AND supplemental (Chill, Contemplative, Ethereal, Cozy, Tender, Introspective, Spiritual, Nostalgic) ≥ 2

AND it has **none** of these 15 anti-moods: Energetic, Upbeat, Aggressive, Explosive, Frenzy, Furious, Danceful, Groovy, Ecstatic, Chaotic, Defiant, Rebellious, Triumphant, Heroic, Epic.

The anti-gate was added after initial teFictional-Kw-4669569c revealed that tracks like The Sims 2 Main Theme (which has both Relaxed and Upbeat) were incorrectly placed in a relaxation playlist.

### Wandering Exclusion Rules

RPG_Wandering has additional post-placement cleanup to remove tracks whose primary character is incompatible with gentle exploration:

- **Epic-dominant**: ≥3 of {Epic, Triumphant, Heroic, Awe-inspired}
- **Battle-dominant**: ≥2 of {Aggressive, Explosive, Frenzy, Chaotic, Furious}
- **Danceful-dominant**: ≥3 of {Danceful, Groovy, Ecstatic, Upbeat}
- **Melancholic-dominant**: ≥3 of {Melancholic, Sad, Bittersweet, Anguished, Heartbreak, Depressive}

### Threshold Design Philosophy

The thresholds were deliberately set to be **generous** ("don't be too strict" was the explicit instruction). The reasoning:

- For _definitional_ folders (primary Mood/), precision matters — a track tagged `Aggressive` should genuinely feel aggressive.
- For _contextual_ folders (RPG\_\*/), recall matters more — players expect to find tracks, and an occasional borderline inclusion is better than gaps in the playlist. If a track has both Adventurous and Contemplative, it Fictional-QuartzDrifterngs in RPG_Wandering even if neither mood dominates.

The exception is custom scorers (Battle, Relaxation) where false positives are more jarring. Nobody wants Sims 2 Main Theme interrupting a meditation session.

## Slice Cap System

Fictional-SterlingHelix and MedievalAmbience sliced tracks are capped per RPG\_ folder to prevent any folder from being dominated by ambient excerpts.

### Cap Percentages

- **Fictional-SterlingHelix**: 5% of folder total
- **MedievalAmbience**: 2% of folder total

### Cap Formula

$$\text{cap} = \max\left(1, \text{round}\left(\frac{n_{\text{non-slice}} \times p}{1 - p}\right)\right)$$

This ensures that after adding `cap` slices, they comprise approximately `p` of the total.

### Allocation Algorithm

Two-phase coverage-maximizing allocation:

1. **Phase 1 (coverage)**: Each slice file is placed in exactly one random under-cap eligible folder, with most-constrained files (eligible for fewer folders) going first. This ensures maximum coverage — every slice appears in at least one RPG\_ folder.
2. **Phase 2 (fill)**: Any remaining cap space is filled with random eligible files not already in that folder. No file appears twice in the same folder.

The allocation is randomized per run; use `--seed N` for reproducibility.
