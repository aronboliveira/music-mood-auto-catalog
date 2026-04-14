# Batch 34 — 20260414 Final Pass Learning

**Date:** 2026-04-14

## What This Batch Taught Us

## 1) Full-Coverage Review Does Not Mean Uniform Depth

The batch reached 972/972 reviewed (100%), but profile granularity remained uneven: 22 tracks now sit in very rich ranges (>=16 moods) while 9 tracks remain sparse (<=2 moods).

Takeaway: quality control should track both binary review state and depth distribution. Future QA dashboards should include profile-depth histograms, not only reviewed percentages.

## 2) Enrichment Wave Pattern: From Placeholders to Energetic Specificity

Largest positive deltas were Frenzy (+24), Energetic (+23), Defiant (+19), Danceful (+14), Determined (+14), Upbeat (+14). Largest losses were Chill (-9), Nostalgic (-4).

Takeaway: this pass did not just add moods; it replaced generic fallback moods with higher-information descriptors. This is consistent with a deliberate anti-placeholder strategy.

## 3) Semantic Arc Still Holds Under Load

The 13-cluster framework remained coherent after 42 profile changes. Coverage still forms a readable emotional arc (warm -> reflective -> longing -> sorrow -> darkness -> mystery -> tension -> confrontation -> movement -> heroism -> focus -> joy -> calm).

Takeaway: cluster model remains a valid backbone for future contextual playlist generation and for sanity checks when reviewing outliers.

## 4) Ambience Layer Is Useful as a Second Taxonomy

Using ambience archetypes (Combat-Adrenaline, Work-Focus, Heroic-Quest, Melancholic-Introspective, etc.) highlighted a key pattern: Focus signatures appear frequently as secondary color but almost never as primary identity.

Takeaway: Focus should likely stay an auxiliary axis in UX/filtering, while high-emotion archetypes drive playlist headers.

## 5) Marker Behavior (Playful / Macabre / Ethereal)

Marker intersections were informative:
- Playful + Ethereal appeared often enough to define a whimsical dream band.
- Ethereal + Macabre occurred in gothic-fantasy tracks.
- Playful + Macabre was rare and style-specific (carnival-gothic feel).
- Triple intersection did not occur.

Takeaway: these markers are discriminative and safe for context-level routing rules.

## 6) JoJo Constraint Handling Requires Two-Layer Policy

The requested policy worked well when split into:
- JoJo-reference matches: move copies under Genre/Mood into local .rejected subfolders.
- Non-JoJo matches from the user list: delete from Genre/Mood only.
- Preserve Artist copies in all cases.

Result in this pass: 104 moved-to-rejected, 13 deleted, Artist layer preserved.

Takeaway: this separation keeps discovery and historical auditability while honoring personal filtering constraints.

## 7) Historical Regression Guardrail Is Now Critical and Cheap

Cross-snapshot scan found 0 tracks where current profile regressed Fictional-QuartzDrifterw a richer historical profile.

Takeaway: this check should remain mandatory each batch. It is low-cost and prevents silent quality drift.

## 8) Previous Error Backlog Status

- WoW trailing silence issue: verified fixed (Legends of Azeroth at 2:40, Song of Elune at 2:15).
- Artist-folder contamination issues listed in earlier batches: re-audited and remained corrected.
- Fictional-TimberStrand folder checked: only Fictional-TimberStrand tracks present.

Takeaway: once fixed, targeted folder audits can be short and deterministic if we keep exact checklists.

## Practical Guidance for Future Final Passes

1. Keep running the depth audit even after 100% review.
2. Preserve ALL_MOODS and MOOD_COLORS during every data rebuild.
3. Run historical best-profile comparison before writing data.js.
4. Apply personal taste exclusions only in Genre/Mood layers, never Artist.
5. Track marker intersections in the journal to detect taxonomy drift early.
