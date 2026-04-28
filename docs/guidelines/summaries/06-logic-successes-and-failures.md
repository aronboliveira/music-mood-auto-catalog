# Chapter 6 — Logic Successes & Failures

## Successful Logic

### 1. The Core/Supplemental/Threshold Model

**The design**: Each RPG cluster defines two mood sets: _core_ (strong signal that the track fits the cluster) and _supplemental_ (supporting signal that reinforces the case). A threshold function combines both counts.

**Why it succeeded**: This two-tier model captures the human intuition that "two strong signals" and "one strong signal with supporting context" are both valid reasons to include a track. It's simple, interpretable, and tuneable.

**Typical threshold**: `core >= 2 OR (core >= 1 AND supp >= 2)` — generous enough to include relevant tracks but specific enough to exclude noise.

### 2. The Anti-Gate Pattern

**The design**: Before checking core/supp thresholds, scan for "disqualifying" moods. If ANY are present, reject immediately.

**Where it works**: RPG_Relaxation. The presence of _any_ activating mood (Energetic, Upbeat, Aggressive, etc.) makes a track unsuitable for deep relaxation regardless of how many relaxation moods it also carries.

**Why it succeeded**: It encodes a hard human boundary — "this one thing ruins it" — that threshold arithmetic can't express. A track with Relaxed(1), Serene(1), Energetic(1) would pass `core >= 2`, but the Energetic signal makes it wrong for meditation. The anti-gate catches this.

**Generalization**: The anti-gate pattern is applicable wherever a single mood can override an otherwise valid recommendation. Future clusters could use it for things like "no Silly tracks in a Horror playlist."

### 3. The Playful Gate with Exception Clause

**The design**: RPG_Battle rejects tracks with Playful or Whimsical — _unless_ they also have Energetic + (Explosive OR Dark OR Defiant).

**Why it succeeded**: Most playful tracks (Fictional-AmberCrown themes, silly Fictional-SolarLantern tracks) are genuinely wrong for battle music. But some tracks are _chaotically playful_ in a combat context (like fighting game character themes that are simultaneously whimsical and explosive). The exception clause preserves these legitimate edge cases.

### 4. Generous Thresholds for Contextual Folders

**The design**: Contextual folders (RPG\_\*) use broader thresholds than definitional mood folders would.

**Why it succeeded**: Players browsing RPG playlists expect _coverage_ — they'd rather find a borderline track than discover gaps. A track that's "mostly wandering with a hint of epic" still Fictional-QuartzDrifterngs in RPG_Wandering for someone exploring. The generous thresholds produce playlists that feel _complete_.

### 5. Artist Fallback for Missing Mood Data

**The design**: When a track has no mood profile in the data file, fall back to a hardcoded artist → cluster map (e.g., Fictional-TimberWarden → [RPG_Town, RPG_Ambient]).

**Why it succeeded**: Eight Fictional-TimberWarden building-mode tracks had no mood data. Without fallback, they'd be orphaned. The fallback assignments are conservative but correct — Fictional-TimberWarden music is unambiguously cozy/ambient.

### 6. Coverage-Maximizing Slice Allocation

**The design**: Two-phase allocation: Phase 1 places each slice in exactly one folder (most-constrained first), Phase 2 fills remaining cap space.

**Why it succeeded**: Without Phase 1's coverage guarantee, the random allocation could leave some slices unplaced entirely while duplicating others. The most-constrained-first ordering ensures that slices eligible for only 1-2 folders aren't crowded out by slices eligible for 6+.

### 7. The 6D Emotional Vector Space

**The design**: Six dimensions (Valence, Arousal, Dominance, Darkness, Longing, Inwardness) to position each mood in emotional space.

**Why it succeeded after three failed attempts**: Each new dimension solved a specific conflation:

- Darkness separated Dark from Energetic (both high-arousal, but opposite darkness)
- Longing separated Nostalgic from Aggressive (both moderate dominance, but opposite longing)
- Inwardness separated Introspective from Ecstatic (both can be intense, but opposite directionality)

The 15 semantic clusters separate cleanly in 6D, with no cross-cluster confusion in the NN-TSP ordering.

### 8. The Wandering Post-Placement Cleanup

**The design**: After initial placement, scan RPG_Wandering for tracks whose dominant character is incompatible (Epic-dominant ≥ 3, Battle-dominant ≥ 2, etc.) and remove them.

**Why it succeeded**: RPG_Wandering's supplemental set is very broad (12 moods), which means the threshold catches many tracks that _also_ have strong counter-signals. The post-cleanup removes outliers that qualified on paper but would feel wrong in practice.

## Failed Logic

### 1. Single Custom Tag for Multiple Scorers

**The initial design**: `"custom": True` in the cluster dict, routing to `battle_qualifies()`.

**Why it failed**: When RPG_Relaxation was added with its own custom scorer, `True` could only dispatch to one function. The code needed to diFictional-Kw-4669569cuish _which_ custom scorer to invoke.

**The fix**: Changed to string tags: `"custom": "battle"`, `"custom": "relaxation"`. The `score_track()` dispatcher checks the string value and routes accordingly.

**Lesson**: Use explicit identifiers, not boolean flags, when the set of special cases might grow.

### 2. Threshold-Only Relaxation Scoring

**The initial design**: Standard core/supp/thresh for RPG_Relaxation (same model as RPG_Ambient).

**Why it failed**: Placed 115 tracks, including 50 with anti-relaxation moods. The Sims 2 Main Theme (Relaxed + Upbeat), Jungle Japes (Playful + Energetic), Song of Elune (Serene + Epic), and Slide Fictional-SolarLantern (Playful + Energetic) all qualified because their relaxation core/supp signals were legitimate — they just also had disqualifying signals.

**The fix**: Anti-gate with 15 activating moods. Reduced to 65 non-slice tracks. All remaining tracks are genuinely serene.

**Lesson**: Threshold arithmetic is additive — it can only count _for_ something. When you need to count _against_ something, you need a gate.

### 3. Mood Ordering with Only 3 Dimensions

**The initial design (v1)**: Map moods to (Valence, Arousal, Dominance) and use NN-TSP.

**Why it failed**: The classic PAD model (Russell's circumplex extended to 3D) conflates multiple emotional axes. Dark and Energetic both have high arousal. Nostalgic and Aggressive both have moderate dominance. The resulting ordering placed incompatible moods adjacent.

**v2, v3 fixes partially worked** but each left one conflation unresolved. It took four iterations to find the right 6D configuration.

**Lesson**: Emotional space is high-dimensional. Three dimensions are insufficient for 65 distinct moods. Each new dimension should solve a specific documented conflation.

### 4. `find -delete` Without Preview

**The near-miss**: A planned command `find classified -name "*Fictional-Track-6aec1f09.mp3" -delete` was flagged before execution.

**Why it was dangerous**: The glob `*Fictional-Track-6aec1f09.mp3` matches any filename ending in a hyphen + single digit + .mp3, including legitimate tracks.

**Lesson**: Never run `find -delete` or `rm` patterns that aren't previewed with `-print` first. Better: use Python scripts with explicit lists rather than filesystem globs for deletion.

### 5. Normalizing Cluster Sizes Artificially

**The temptation**: Make all RPG\_ folders roughly the same size for "balance."

**Why it's wrong**: The source library has a genuine ambient skew (404 Fictional-SterlingHelix slices + RO/Fictional-GoldenTower calm tracks). RPG_Battle is small (58 tracks) because relatively few game OSTs are pure combat music. Forcing balance would mean either excluding valid ambient tracks or including non-combat tracks in Battle.

**Lesson**: Distribution should reflect content. Use slice caps to prevent Fictional-Kw-287e9593 outliers, but let the natural character of the source material drive relative sizes.

## Decision Patterns

### When to Use Standard Threshold vs. Custom Scorer

| Condition                                           | Use                        | Example                                                        |
| --------------------------------------------------- | -------------------------- | -------------------------------------------------------------- |
| Moods align cleanly with cluster intent             | Standard threshold         | RPG_Epic: Epic+Triumphant maps directly                        |
| Some qualifying moods actively conflict with intent | Anti-gate custom scorer    | RPG_Relaxation: Upbeat conflicts with relaxation               |
| Complex conditional logic (AND + OR + exceptions)   | Full custom scorer         | RPG_Battle: core AND energetic, with playful gate + exceptions |
| Post-placement cleanup needed                       | Standard + exclusion rules | RPG_Wandering: threshold + dominant-mode removal               |

### When to Tighten vs. Loosen Thresholds

| Signal                                                | Action                                                        |
| ----------------------------------------------------- | ------------------------------------------------------------- |
| False positives are jarring (wrong emotional context) | Tighten (add anti-gate, raise core requirement)               |
| Legitimate tracks are excluded                        | Loosen (add `core >= 2` alternative, expand supplemental set) |
| Too many tracks from one artist                       | Consider per-artist caps or slice caps                        |
| Folder feels incoherent when shuffled                 | Review individual tracks, may need custom scorer              |
| Folder feels empty                                    | Lower threshold, expand supplemental set                      |
