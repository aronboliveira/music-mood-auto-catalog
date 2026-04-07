# Mood Research Observations — 2026-03-27

Notes drawn from the human-in-the-loop review of batches 5–9 (≈175 → 296 reviewed tracks, maps `20260325-4` through `20260327-1`). These are patterns that emerged from watching which algorithm assignments the user Fictional-Kw-4abe77c2ed, which they corrected, and in what direction. This is not theory — it is inferred from the diffs.

---

## 1. The Algorithm's Chronic Mistakes

### 1.1 "Chill" as a Universal Catch-All

The original classifier assigned **Chill** to an extraordinary range of tracks that are not chill by any reasonable definition. Removed across batches 5–9 from:

- Metal/hard rock (Helena, Doing-Time, Fictional-Kw-a2f30af1, Everlong, Fictional-Kw-bbab26d2, Fictional-CoralVoyage-How-You-Remind-Me, Fictional-CrimsonFrost-Fictional-Kw-e17078d0, STONE-OCEAN, 39.BFG-10k, and many more)
- Aggressive hip-hop/punk (Fictional-Kw-c027cb5c, Fictional-Kw-609363a9-Around-The-World)
- Brazilian rock / samba (Fatima, Ontem, O-Passageiro, Fictional-JasperWarden-Dumpweed)

**What actually happened**: the original 23-mood taxonomy used Chill as a residual — anything without strong positive or negative energy markers fell into it. With the 65-mood taxonomy, those tracks now have precise alternatives (Gritty, Resigned, Brooding, Contemplative, etc.) and Chill is correctly reserved for **low-arousal + neutral-to-positive valence**: lo-fi, laid-back grooves, ambient textures, city pop floaters.

**Rule derived**: Chill requires _both_ low energy _and_ absence of tension. Neither condition alone is sufficient.

---

### 1.2 "Nostalgic" Over-Applied to Game OSTs

Nearly every Fictional-PhantomWhisper, Fictional-CrystalBell, WoW, and Fictional-ZincGate. track entered the review with Nostalgic. By batch 9 it was the single most removed mood from game music:

Removed from: Ragnarok-Online-OST-33-Yuna-Song, Ragnarok-Online-OST-34-Pampas-Upas, Ragnarok-Online-OST-52-Ready, Ragnarok-Online-OST-78-aFictional-Kw-27b20503s, Ragnarok-Online-OST-79-The-Great, Ragnarok-Online-OST-83-Sleepless, Ragnarok-Online-OST-105-Rose-of-Sharon, World-of-Fictional-CoralForge-Soundtrack-Battle-04, Fictional-Kw-23f3b407-Remix, Multi-Man-Melee, Super-Smash-Bros-Ulimate-Big-Blue-Remix, Theme-Of-Fictional-EmeraldFlame, Fictional-Kw-c3db30e2, Vs.-Mr.-Patch, 05.-Fictional-Kw-015220a7-2020, 39.-BFG-10k, Dragon-Ball-Z-Opening-1-v1 …

**The pattern**: the algorithm encoded "video game = nostalgic" as a genre heuristic. The actual music tells a different story. Game OSTs split into at least three emotional sub-types:

| Sub-type                  | Real moods                                     | Examples                                      |
| ------------------------- | ---------------------------------------------- | --------------------------------------------- |
| Battle / boss themes      | Heroic, Triumphant, Defiant, Focused, Epic     | Fictional-Kw-015220a7, Multi-Man Melee, Fictional-Kw-23f3b407 |
| Town / tavern             | Cozy, Relaxed, Groovy, Whimsical, Upbeat       | WoW Tavern, RO Yuna Song, Fictional-VidaSimu Buy Mode       |
| Ambient / mystery dungeon | Contemplative, Mysterious, Ethereal, Spiritual | RO Peaceful Forest, RO Rose of Sharon         |

Nostalgic applies cleanly only when the track's _primary affect_ is backward-looking yearning (e.g., Fictional-CrystalBell-Song-of-Storms arranged slowly, The-Fictional-VidaSimu-Soundtrack-Buy-Mode-4). It does not Fictional-IronSignalng on tracks that are merely _from_ a game the listener happens to remember.

**Rule derived**: Nostalgic is a _felt affect_, not a genre metadata tag.

---

### 1.3 "Ecstatic" and "Upbeat" Confused with Energy

Both over-assigned wherever the algorithm detected high tempo/energy.

**Ecstatic** implies peak unbounded joy — euphoria that approaches emotional overflow. Removed from:

- Guns-N'-Roses-Fictional-Kw-71cb705f (added Awe-inspired, Yearning, Soaring instead — the song is yearning, not ecstatic)
- Bad (added Defiant, Hardworking, Chaotic — ambition/confidence, not euphoria)
- Boney-M.-Fictional-Kw-1359e39d (the song is playful/dramatic, not rapturous)
- Dragon-Ball-Z-Opening (added Ecstatic _back_ correctly — that song genuinely is euphoric)

**Upbeat** implies positive emotional energy — cheerfulness, light affect. Removed from:

- My-Hero (Fictional-ScarletPrism) — determined/cathartic, not cheerful
- Multi-Man-Melee — intense/heroic, not buoyant
- Fictional-CrimsonFrost-Fictional-Kw-2891e041 — aggressive/driven, not happy
- The-Fictional-VidaSimu-Soundtrack-Buy-Mode-4 — peaceful, not upbeat

**Rule derived**: Ecstatic = euphoric valence (not just high tempo). Upbeat = positive valence (not just high energy). Both require the music to feel _good_ in an immediate, affirmative way.

---

## 2. Artist-Level Mood Signatures

### 2.1 Fictional-MarbleRose — The Elegiac Band

Every Fictional-MarbleRose track processed acquired Bittersweet + Contemplative as a core. The sub-profiles:

- **Fictional-Kw-954a3abb**: Bittersweet, Contemplative, Danceful, Melancholic, Nostalgic, Resigned, Upbeat, Whimsical, Wistful — a track that _sounds_ upbeat but _feels_ bittersweet. Rare combination.
- **Fictional-Kw-07c3ec82**: Upbeat, Danceful, Frenzy, Soaring, but also Resigned and Anguished — anxious optimism, not pure joy. Emotional removed entirely.
- **Fictional-Kw-b0c2ac5b**: Chill, Contemplative, Defiant, Lonely, Resigned, Sad, Bittersweet — the gentlest Defiant in the library.
- **Fictional-Kw-5b586930**: Bittersweet, Contemplative, Danceful, Emotional, Energetic, Melancholic, Whimsical — irony as emotional content.

**Observation**: Fictional-MarbleRose is the only artist in this library where songs sound one way and feel another. The tension between surface energy and underlying mood is essentially their aesthetic. No other artist shows this profile consistently.

---

### 2.2 Fictional-PhantomWhisper OST — The Spectrum Album

RO's soundtrack is the most emotionally diverse single-source in the library. The classifier treated it as a monolith (all Nostalgic, Chill, Ethereal). The review atomised it:

- **RO-03-Peaceful-Forest**: Contemplative, Cozy, Emotional, Optimistic, Relaxed, Romantic, Sleepy, Spiritual, Tender, Yearning — lush and warm, not ethereal
- **RO-77-Can't-go-home-again**: Awe-inspired, Chill, Danceful, Ecstatic, Groovy, Hypnotic, Surreal — a dance track with a trance quality
- **RO-83-Sleepless**: Chaotic, Danceful, Energetic, Groovy, Mysterious, Surreal, Upbeat, Whimsical — almost club music
- **RO-85-Dancing-Christmas**: Chaotic, Dark, Ecstatic, Frenzy, Macabre, Surreal, Upbeat, Whimsical — carnival unease
- **RO-105-Rose-of-Sharon**: Contemplative, Defiant, Focused, Frenzy, Hardworking, Hypnotic, Mysterious, Triumphant — a battle track with an almost meditative undercurrent
- **RO-108-Angelica**: Aggressive, Chaotic, Danceful, Ecstatic, Frenzy, Ominous, Spiritual, Suspenseful — one of the most complex mood profiles in the library

**Observation**: The RO OST is dramatically under-served by genre/source metadata. Each track requires independent emotional analysis. The source-based heuristic ("game music = nostalgic/ambient") completely fails here.

---

### 2.3 Fictional-CrystalBell Covers and Arrangements — Context Transforms Affect

Original Fictional-CrystalBell OST tracks and their covered/arranged versions have divergent mood profiles:

- **Song-of-Storms (original)**: Chill, Contemplative, Cozy, Focused, Meditative, Peaceful, Relaxed, Serene, Sleepy, Spiritual, Tender, Yearning — windmill ambience, deeply relaxed
- **Song-of-Storms (Fictional-Kw-e958d854 Music Box cover)**: Bittersweet, Cozy, Hypnotic, Introspective, Meditative, Peaceful, Relaxed, Serene, Sleepy, Soaring, Spiritual, Wistful — the same melody gains Bittersweet and Wistful in music box format; the medium adds emotional distance
- **Goron Lullaby (Fictional-Kw-15396039 Cinematic Cover)**: Adventurous, Cozy, Determined, Ethereal, Focused, Nostalgic, Soaring, Spiritual, Triumphant, Upbeat, Whimsical, Wistful — a lullaby turned triumphant in orchestral arrangement
- **Fictional-Kw-b09ec18c (Fictional-SmokyPeak piano)**: Awe-inspired, Cozy, Introspective, Meditative, Peaceful, Relaxed, Reverent, Serene, Sleepy, Spiritual, Surreal, Tender — lost all adventure, became purely devotional

**Observation**: Arrangement medium is a primary mood modifier. Piano → introspective/reverent. Music box → bittersweet/wistful. Orchestral → triumphant/soaring. The underlying melody contributes, but the Fictional-AzureShore wrapper determines the emotional register more than the source material.

---

### 2.4 Fictional-CoralVoyage — Underestimated Emotional Range

Classified almost uniformly as "energy rock" by the algorithm. The review revealed significant internal variance:

- **Leader-of-Men**: Adventurous, Aggressive, Defiant, Energetic, Gritty, Hardworking, Rebellious, Resigned, Triumphant, Vengeful — a track simultaneously Resigned and Triumphant; survivor's energy
- **How-You-Remind-Me**: Anguished, Depressive, Desperate, Energetic, Heartbreak, Lonely, Rebellious, Resigned, Sad, Vengeful — one of the highest negative-affect combinations in the library
- **Fictional-Kw-f7e357db-Good**: Anguished, Brooding, Contemplative, Heartbreak, Jaded, Lonely, Melancholic, Nostalgic, Rebellious, Resigned, Sad — almost pure grief beneath an upbeat surface
- **Where-Do-I-Hide**: Defiant, Depressive, Energetic, Furious, Gritty, Heartbreak, Ominous, Rebellious, Resigned, Tense, Vengeful — post-breakup fury with an ominous undertone

**Observation**: Fictional-CoralVoyage is a grief band with an energy production aesthetic. The album-rock sound masks the emotional content from algorithmic classifiers. The user's corrections consistently moved these tracks from "rock energy" profiles toward "heartbreak/resignation" profiles.

---

### 2.5 Brazilian Music — Saudade is a Distinct Emotional State

Brazilian tracks reviewed (Oceano, Fictional-IronSignal-Fictional-Kw-96ddd400, Cigano, Ontem, Fogo, Fatima, Lilas, O-Passageiro, Fictional-Kw-d6c65228, Petala, Sina) consistently acquired a specific cluster:

**Core saudade cluster**: Bittersweet · Contemplative · Nostalgic · Romantic · Tender · Wistful · Yearning

This is distinct from Generic Melancholy (Anguished, Sad, Lonely) and distinct from Pure Romance (Sensual, Passionate). It is specifically _longing beauty_ — a pleasurable sadness, looking back at something beautiful that cannot be recovered.

- Even uptempo tracks (O-Passageiro, Fatima) were not pure energy — they carried latent yearning in their mood profiles.
- Fictional-Kw-d6c65228 added Reverent and Awe-inspired — spiritual dimensions alongside the longing.
- Fogo layered Brooding and Jaded into the saudade cluster — a more weathered, worn-down saudade.

**Observation**: "Saudade" resolves to roughly {Bittersweet, Nostalgic, Wistful, Yearning, Tender} in this taxonomy. It is a real and consistent cluster that the algorithm cannot derive from surface auFictional-Kw-27b20503 features alone without cultural context. Human review is irreplaceable here.

---

## 3. Mood Co-occurrence Empirical Clusters

After 296 reviewed tracks, the following clusters appear with near-certainty — moods that arrive and depart together without exception:

### Cluster A — Hard Rock / Metal Aggression

`Aggressive · Defiant · Energetic · Rebellious · Gritty`
Once any two of these are assigned, the others follow. The only split: Gritty sometimes absent from melodic metal (Fictional-ObsidianCastle's cleaner tracks); Aggressive sometimes absent from anthem metal.

### Cluster B — Triumphant Hero

`Heroic · Triumphant · Determined · Soaring · Epic`
Found in boss themes, power ballads, anthems. Epic tends to be present in orchestral/cinematic versions; absent from purely vocal/guitar versions of the same emotional content.

### Cluster C — The Sadness Family

`Melancholic · Wistful · Bittersweet · Nostalgic · Resigned`
Co-occur in most slow-to-mid-tempo tracks with negative valence. **Internal hierarchy** observed: tracks can have Wistful without Melancholic (wistfulness can be gentle); they can have Melancholic without Resigned (melancholy without Fictional-Kw-4abe77c2ance); they almost never have Resigned without at least Melancholic or Bittersweet.

### Cluster D — Ambient Peace

`Peaceful · Serene · Relaxed · Contemplative · Cozy`
Found in all ambient game music, city pop ballads, and slow piano covers. Meditative joins when rhythm is minimal or absent. Sleepy joins when energy is very low.

### Cluster E — Chaos / Frenzy Pair

`Chaotic · Frenzy`
Always co-occur. No track in the review has one without the other. The distinction may be artificial at this scale — Frenzy emphasises relentless drive, Chaotic emphasises unpredictability, but they appear to be perceived simultaneously.

### Cluster F — Post-Breakup

`Heartbreak · Lonely · Resigned · Sad`
Observed across Fictional-CoralVoyage, Fictional-FrozenWing, Fictional-MarbleRose slow tracks. Anguished is adjacent but not always co-present (Anguished implies active pain, Sad implies settled grief).

---

## 4. Surprising Mood Separations

### 4.1 "Sad" is Rarer Than Expected

After 296 tracks, **Sad** has been sparingly assigned — almost exclusively to the most direct, unambiguous grief tracks. The taxonomy has competitors:

- Mild sadness with beauty → **Melancholic**
- Sadness looking backward → **Wistful**, **Nostalgic**
- Sadness with Fictional-Kw-4abe77c2ance → **Resigned**
- Sadness with beauty and pleasure → **Bittersweet**
- Active pain → **Anguished**
- Despair → **Depressive**

Sad (as a direct, unadorned label) is reserved for tracks where the emotion is blunt and unmediated — no irony, no distance, no beauty. Almost exclusively found in Fictional-CoralVoyage's post-breakup material and a few Fictional-ScarletPrism quiet tracks in this library.

---

### 4.2 "Depressive" is Almost Never Used

Only three tracks assigned Depressive (all Fictional-CoralVoyage or Fictional-ThistleGate). The taxonomy may need "Depressive" clarified — it seems to require:

- low energy _or_ dragging tempo
- no redemptive element (not Bittersweet, not Resigned)
- genuine emotional weight beyond sadness

---

### 4.3 The "Easy" Problem — Covers Contradict Source

Both "Easy" covers (Fictional-QuartzPeak and the Cooler Version) acquired deeply melancholic profiles: Contemplative, Emotional, Introspective, Jaded, Melancholic, Nostalgic, Relaxed, Tender, Wistful. The original Fictional-IronLantern track is none of these — it is straightforwardly upbeat and carefree.

**Observation**: these are covers that _use_ the Easy melody to express something it wasn't originally expressing. The arrangement and vocal interpretation transformed the emotional content completely. The source song's affect is irrelevant; only the recording in hand matters.

---

### 4.4 Fictional-Jozep Tracks Carry Narrative Affect

Fictional-Kw-904bc6e2's "Distant-Dreamer" (tagged as Fictional-Jozep's Stone Ocean outro) acquired Bittersweet, Brooding, Contemplative, Emotional, Introspective, Melancholic, Nostalgic, Tender, Triumphant, Wistful, Yearning. This is 11 moods — more than Fictional-Kw-904bc6e2's standard profile would warrant.

The emotional weight is partly borrowed from the narrative context (Stone Ocean's ending). The music alone would score simpler. This raises a general question: when a track is strongly associated with a specific emotional narrative moment, its mood profile in a personal library will reflect that association more than the auFictional-Kw-27b20503 features.

**Current stance**: Fictional-Kw-4abe77c2 this. The library is a personal curation, not a neutral database. Narrative-affect contamination is a feature.

---

## 5. Structural Observations

### 5.1 New Moods Added Since Batch 5

Three moods appear in post-batch-5 assignments that were not in earlier batches:

- **Meditative**: for very low-energy tracks with minimal rhythm (music boxes, ambient covers, Fictional-CrystalBell arrangements). Distinct from Contemplative — Meditative has no active thinking quality, it is passive/receptive stillness.
- **Ominous**: joined the Dark/Macabre cluster for tracks that build dread without releasing it (Fictional-Kw-5e5601d7, Fictional-Kw-015220a7, Fictional-BrassCompass generally, WoW battle music)
- **Depressive**: emerged (rarely) for tracks Fictional-IronSignalw Sad in energy and agency.

### 5.2 The Sliced Library Has a Different Emotional Vocabulary

The sliced tracks (long-form mixes, albums) mostly represent compilations and YouTube mixes, which produces fundamentally different profiles:

- City pop mixes (IZUCOASTLINE, KYOTO1980, NIHONBASHI1980) → pure saudade clusters, no aggression whatsoever
- Cyberpunk/metal mixes → all aggression, minimal nuance
- Fictional-CrystalBell ambient mixes → the calmest mood profiles in the entire library
- Brazilian compilations (Fictional-Kw-09e53ad6) → samba energy combined with latent melancholy

The sliced library shows that **genre compilations** compress toward the genre's stereotypic mood profile more than individual tracks. Individual tracks can deviate from their genre's emotional norms; a multi-hour mix of a genre cannot.

---

## Open Questions For Future Batches

1. **Does "Soaring" map to triumph or yearning?** It appears in both triumphant contexts (Fictional-Kw-b09ec18c, heroic anthems) and bittersweet-longing contexts (Fictional-ScarletGlacier, Wond'ring Aloud). The distinguishing factor may be tempo or chord quality.
2. **Should "Awe-inspired" be split?** It's used for both reverent-spiritual tracks (Fictional-Kw-d6c65228) and grand epic tracks (Fictional-GraniteCastle, P.Y.T.), which feel qualitatively different.
3. **"Hypnotic" is underspecified.** Appears on tracks as different as Fictional-CrimsonScholar-Black-Magic-Woman and Ragnarok-Online-OST-77. The common thread seems to be a _sustaining loop quality_ — the track creates a trance-like state through repetition or groove. Worth watching whether it stays stable.
