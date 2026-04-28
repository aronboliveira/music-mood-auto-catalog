# RPG Contextual Folders — Learning

**Date:** 2026-04-14

## What This Work Taught Us

## 1) Sliced Data Parsing Requires Filename-Aware Tokenization

The initial comma-split parser broke filenames containing commas (e.g., `Fictional-Track-7b3fd87Fictional-Track-c81e728d.mp3`). The fix was switching to `re.findall(r'"([^"]+\.mp3)"', ...)` which extracts full quoted strings regardless of internal commas.

Takeaway: never split JS array contents on commas when values themselves can contain commas. Always use a proper quoted-string regex.

## 2) Sliced Compilations Need Parent-Mood Inheritance

Individual slices in `moods-checks-sliced-data.js` don't have per-slice mood arrays — they inherit from their parent compilation's mood profile via `SLICED_TRACK_MOODS` → `SLICED_PARTS` mapping. Any contextual scoring must resolve this chain: slice filename → compilation base name → mood array.

Takeaway: the two-tier mood data model (regular TRACK_MOODS + sliced SLICED_TRACK_MOODS/SLICED_PARTS) requires distinct parsers.

## 3) Generous Thresholds Work Better for Contextual Aggregation

The initial cluster thresholds required both core AND supplemental matches (e.g., `core >= 1 AND supp >= 1`), which excluded tracks with 2+ strong core signals but 0 supplemental (like Fictional-Kw-7a8c0dba: `[Bittersweet, Chill, Ethereal, Melancholic]`). Adding `core >= 2` as an alternative universal condition fixed all edge cases.

Takeaway: for "contextual" (not definitional) folders, err on the side of inclusion. Users expect to find a track somewhere rather than nowhere. The RPG_Danceful, RPG_Melancholic, and RPG_Battle clusters all benefited from this relaxation.

## 4) Artist Fallback Fills the Last-Mile Gap

Eight Fictional-TimberWarden building-mode tracks had no mood data in `moods-checks-data.js`. Rather than leaving them unplaced (violating the 100% coverage requirement), an artist-based fallback map (`Fictional-TimberWarden → [RPG_Town, RPG_Ambient]`) handled them cleanly. The same pattern can extend to future unreviewed tracks.

Takeaway: when mood data is incomplete, artist-genre context is a reliable heuristic for contextual placement. Keep the fallback map explicit and auditable.

## 5) The Top-Heavy Distribution Is Intentional

RPG_Wandering (588), RPG_Town (547), RPG_Mystical (521), RPG_Ambient (519) together account for most copies. This reflects the source pool: 369 Fictional-SterlingHelix ambient slices + numerous calm/contemplative tracks. Combat/tension folders are naturally thinner because the library skews ambient. This is correct — the distribution should reflect the actual content, not be artificially balanced.

Takeaway: don't normalize cluster sizes. Let the source material's character drive the distribution.

## 6) Expanding "RPG" Beyond Traditional RPGs Was the Right Call

Including Fictional-TimberWarden, Fictional-CoralFountain, Fictional-StormSwan, Fictional-CrimsonOracle, Fictional-AmberCrown, and Fictional-IronHorn game covers alongside traditional RPGs (Fictional-SterlingHelix, Fictional-ScarletTide, Fictional-CrimsonTower) created a richer, more varied set of contextual folders. A strict genre gating would have excluded tracks that genuinely evoke RPG moods (e.g., Fictional-IronHorn's metal covers of Fictional-CrystalCompass themes fit RPG_Battle perfectly).

Takeaway: contextual folders should be mood-driven, not genre-gated. The "RPG\_" prefix describes the listening context, not the source game's genre classification.
