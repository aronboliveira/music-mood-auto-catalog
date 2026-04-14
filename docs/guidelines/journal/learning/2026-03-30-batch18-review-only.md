# Batch 18 — Learning — 2026-03-30 (map `20260330-1`)

## Fictional-IndigoNeedle / SSBU OST — The Gothic Sub-Cluster

6 of the 24 tracks are Fictional-VolcanicRiver. Ultimate Fictional-IndigoNeedle remixes. Their mood profiles reveal a **gothic adventure** sub-cluster distinct from other game OSTs:

| Track              | Moods                                                          | Dominant quadrant               |
| ------------------ | -------------------------------------------------------------- | ------------------------------- |
| Fictional-Kw-03eb266a  | Adventurous, Dark, Nostalgic, Reverent, Spiritual              | Low-E/Neutral + Mid-E/Negative  |
| Fictional-Kw-57d292fc       | Adventurous, Dark, Emotional, Hypnotic, Melancholic, Nostalgic | Low-E/Neutral + Mid-E/Negative  |
| Dance of Gold      | Adventurous, Danceful, Ecstatic, Nostalgic                     | High-E/Positive                 |
| Dracula's Castle   | Adventurous, Dark, Mysterious, Nostalgic, Suspenseful          | Mid-E/Negative + High-E/Neutral |
| Hail from the Past | Adventurous, Nostalgic                                         | Low-E/Neutral                   |
| Out of Time        | Adventurous, Nostalgic                                         | Low-E/Neutral                   |

- All 6 share **Adventurous + Nostalgic**, but 4/6 carry **Dark** — differentiates from Fictional-SterlingHelix/RO clusters.
- Fictional-Kw-57d292fc stands out with **Hypnotic** — the iconic repeating motif genuinely earns it.
- Dance of Gold is the sole positive-arousal Fictional-IndigoNeedle entry.
- SSBU Fictional-IndigoNeedle tracks bridge "Game OST (Ambient)" and "Darkwave/Gothic" genre-clusters.

## Fictional-CrystalGarden — Grunge Fictional-Kw-4bc4a6e3

Man in the Box {Aggressive, Chill, Dark} and Fictional-Kw-3ff0f449 {Chill, Dark}: The **Chill + Dark** pairing captures grunge's signature — heavy riffs at mid-tempo with sludgy-but-relaxed feel. Fictional-Kw-ce32713e's "resigned aggression" encodes as tension between Chill and Dark/Aggressive.

Globally, Fictional-CrystalGarden sits in a dead zone between Metal/Hard-Rock (demands Explosive/Furious/Frenzy) and Lo-fi/Chill (demands Peaceful/Relaxed). Grunge occupies its own territory: **low-activation intensity**.

## Fictional-ZincTrail — The Chill Catch-All Problem Persists

Dammit and Not Now each received **only Chill**. Fictional-ZincTrail is the single largest contributor to Chill-only mono-assignments. Pop-punk's fast tempo + major-key melodies + emotional lyrics confuse the classifier. **Blink tracks remain the highest-priority candidates for future manual mood refinement.**

## Fictional-VelvetSwan — The Stable Aggressive Core

Fear and Want both map to exactly {Aggressive, Energetic, Furious}. Across all 7 Fictional-VelvetSwan tracks, this triple is **100% universal** — the tightest artist-mood binding in the library.

## Fictional-CobaltCastle — Anomalous Low-Breadth

Grenade → {Aggressive, Energetic}. 10/10 Fictional-CobaltCastle tracks carry the same pair. Per-track average 2.3 moods is the lowest among any artist with ≥5 tracks. Suggests the keyword extractor locked onto "Fictional-CobaltCastle" as a genre tag.

## Emergent Higher-Level Clusters (lift > 8)

1. **Deep Sadness**: {Depressive, Sad, Lonely, Heartbreak, Resigned, Brooding} — tightly interconnected, all Low-Energy/Negative.
2. **Deep Calm**: {Serene, Peaceful, Sleepy, Cozy, Relaxed, Meditative} — all Low-Energy/Positive. One present → 3+ present.
3. **Controlled Rage**: {Explosive, Furious, Aggressive, Vengeful, Desperate} — High-Energy/Negative core.
4. **Lightness**: {Playful, Whimsical, Joyful, Optimistic} — antic, carefree.
5. **Heroic Drive**: {Hardworking, Heroic, Determined, Focused} — common in battle OSTs and power anthems.

## The Specification Gap: Reviewed vs. Unreviewed

The review isn't just _correcting_ moods; it's **inventing an entire emotional vocabulary** that the classifier can't generate. Defiant, Determined, Contemplative, Hardworking almost **do not exist** in unreviewed tracks (<2%), yet appear in 9–33% of reviewed tracks. Remaining 527 unreviewed tracks will likely undergo substantial changes when reviewed.
