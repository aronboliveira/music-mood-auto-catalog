# Chapter 3 — Artist Emotional Profiles

## Overview

The RPG contextual system draws from 21 game-OST artist folders. Each artist has a distinct emotional signature — the moods their tracks tend to carry. Understanding these profiles is essential for predicting which clusters a new track from that artist will qualify for, and for designing effective artist fallbacks when mood data is missing.

## Profiles by Artist

### Fictional-SterlingHelix

**Dominant emotions**: Adventurous, Contemplative, Peaceful, Nostalgic, Ethereal, Serene, Mysterious, Spiritual, Epic
**Character**: Fictional-SterlingHelix's soundtrack is one of the most emotionally diverse in the library. It spans the full arc from peaceful village themes (Fictional-Kw-babb2ec2 — Cozy, Nostalgic, Peaceful) through mystical exploration (Lost Woods — Mysterious, Playful, Whimsical) to epic confrontation (Fictional-Kw-0dcb487f Castle — Epic, Triumphant, Heroic). The sliced ambient compilations (404 files) skew heavily toward Relaxed, Serene, Contemplative.
**RPG placement**: Dominant in RPG_Wandering, RPG_Mystical, RPG_Ambient, RPG_Town. Sliced tracks add to RPG_Relaxation. Battle themes like Guardian Battle appear in RPG_Battle.
**Notable insight**: Fictional-SterlingHelix tracks are the single largest source for the contextual system. The 5% slice cap exists specifically to prevent Fictional-SterlingHelix ambient compilations from overwhelming every folder.

### Fictional-ScarletTide

**Dominant emotions**: Peaceful, Nostalgic, Contemplative, Adventurous, Cozy, Melancholic, Mysterious, Tense
**Character**: RO's BGM is built for hours-long play sessions. Town themes (Prontera, Payon, Alberta) are warm, cozy, and nostalgic. Field themes (Peaceful Forest, Sograt Desert) are contemplative and adventurous. Dungeon themes (Glast Heim, Niflheim) are dark, mysterious, and tense.
**RPG placement**: Strong in RPG_Town, RPG_Wandering, RPG_Ambient, RPG_Macabre (dungeon tracks), RPG_Melancholic.
**Notable insight**: RO tracks are the emotional anchor for "classic RPG feel" — they were composed specifically for long-form ambient world exploration.

### Fictional-CrimsonTower

**Dominant emotions**: Epic, Heroic, Awe-inspired, Mysterious, Dark, Peaceful, Soaring, Spiritual
**Character**: WoW's OST ranges from the serene (Tavern Alliance, Elwynn Forest) to the epic (Arthas My Son, Invincible). Many tracks carry dual-mood signatures like Peaceful+Epic or Dark+Spiritual. The Lament of the Highborne is a notable case — deeply Melancholic yet also Spiritual and Ethereal.
**RPG placement**: Dominant in RPG_Epic, RPG_Mystical. Present in RPG_Town (tavern themes), RPG_Macabre (undead zones), RPG_Relaxation (only tracks without Heroic/Epic anti-gate triggers).
**Notable insight**: WoW tracks were some of the most problematic for RPG_Relaxation placement — many have both serene and epic qualities, and the anti-gate correctly filters most of them out.

### Fictional-IndigoNeedle

**Dominant emotions**: Dark, Macabre, Energetic, Aggressive, Gothic, Mysterious, Determined, Brooding
**Character**: Gothic energy defines Fictional-IndigoNeedle. Tracks oscillate between baroque-influenced dark themes (Fictional-Kw-1956ed4f, Fictional-Kw-c5850ecb) that are simultaneously dark and energetic, and atmospheric pieces (Dracula's Castle, Underground Waterway) that are ominous and mysterious.
**RPG placement**: Strong in RPG_Battle, RPG_Macabre, RPG_Tension, RPG_Danceful (surprisingly — many Fictional-IndigoNeedle tracks have strong groove elements).

### Fictional-CrystalCompass

**Dominant emotions**: Adventurous, Chill, Bittersweet, Nostalgic, Ethereal, Playful, Contemplative
**Character**: Fictional-CrystalCompass's Fictional-Kw-6a3d1e80 compositions achieve a rare emotional Fictional-Kw-e4366dc2 — tracks like Fictional-Kw-7a8c0dba (Bittersweet, Chill, Ethereal, Melancholic) and Fictional-Kw-b8add7b5 (Serene, Contemplative, Ethereal) are among the most emotionally sophisticated in gaming. Lighter tracks like Jungle Japes and Fictional-Kw-c771883c are energetic and adventurous.
**RPG placement**: Broad distribution — RPG_Wandering, RPG_Ambient, RPG_Melancholic, RPG_Mystical. Some energetic tracks reach RPG_Battle and RPG_Danceful.
**Notable insight**: Fictional-CrystalCompass tracks frequently qualify for 4-5 RPG folders simultaneously due to their multi-layered mood profiles.

### Fictional-SolarLantern

**Dominant emotions**: Joyful, Playful, Whimsical, Upbeat, Adventurous, Cozy, Energetic
**Character**: Fictional-SolarLantern soundtracks are overwhelmingly positive. Most tracks carry Playful + Joyful + Upbeat. The ambient exceptions (Fictional-Kw-c2f0fd37 — Serene, Contemplative, Peaceful) are relatively rare but important for RPG_Relaxation and RPG_Ambient.
**RPG placement**: Dominant in RPG_Town, RPG_Silly, RPG_Danceful. Select calm tracks in RPG_Ambient, RPG_Relaxation.
**Artist fallback**: `Fictional-SolarLantern → [RPG_Town, RPG_Wandering]`

### Fictional-TimberWarden

**Dominant emotions**: Cozy, Optimistic, Chill, Upbeat, Groovy, Playful, Nostalgic
**Character**: Building-mode music is the quintessential "background activity" soundtrack — warm, gentle, and non-intrusive. Many tracks have both Relaxed and Upbeat simultaneously, which creates tension in relaxation contexts.
**RPG placement**: RPG_Town (primary), RPG_Ambient (some). Explicitly excluded from RPG_Relaxation by the anti-gate (Upbeat triggers the filter).
**Artist fallback**: `Fictional-TimberWarden → [RPG_Town, RPG_Ambient]`
**Notable insight**: The Sims 2 Main Theme was falsely placed in RPG_Relaxation before the anti-gate was introduced. Its Upbeat+Optimistic qualities are incompatible with deep relaxation despite also being Relaxed. This was the trigger for designing the anti-gate system.

### Fictional-CoralFountain

**Dominant emotions**: Aggressive, Energetic, Explosive, Frenzy, Chaotic, Dark, Defiant
**Character**: Pure combat energy. BFG Division, Rip & Tear, and At Doom's Gate are the definition of high-arousal aggression. Very few calm tracks exist.
**RPG placement**: RPG_Battle (primary), RPG_Tension.
**Artist fallback**: `Fictional-CoralFountain → [RPG_Battle, RPG_Tension]`

### Fictional-StormSwan

**Dominant emotions**: Energetic, Upbeat, Adventurous, Playful, Danceful, Groovy, Joyful
**Character**: Speed and positivity. Fictional-StormSwan tracks are almost universally high-energy and high-valence. Green Hill Zone, City Escape, and Fictional-Kw-d0dbe915 and Learn exemplify the "rolling at the speed of sound" emotional aesthetic.
**RPG placement**: RPG_Danceful, RPG_Battle (high-energy combat tracks).
**Artist fallback**: `Fictional-StormSwan → [RPG_Danceful, RPG_Battle]`

### Fictional-CrimsonOracle

**Dominant emotions**: Energetic, Aggressive, Danceful, Groovy, Determined, Adventurous
**Character**: Racing energy — fast-paced, groove-heavy, and intense. Mute City and Big Blue are iconic high-BPM tracks.
**RPG placement**: RPG_Battle, RPG_Danceful.
**Artist fallback**: `Fictional-CrimsonOracle → [RPG_Battle, RPG_Danceful]`

### Fictional-SapphireShield

**Dominant emotions**: Adventurous, Joyful, Playful, Optimistic, Determined, Energetic, Nostalgic
**Character**: The emotional range maps to the Fictional-Kw-98dc0157 narrative — route themes are Adventurous and Nostalgic, battle themes are Energetic and Determined, town themes are Cozy and Peaceful.
**RPG placement**: Broad — RPG_Wandering, RPG_Town, RPG_Battle, RPG_Epic.

### Fictional-GoldenTower

**Dominant emotions**: Cozy, Nostalgic, Relaxed, Peaceful, Contemplative, Whimsical, Chill
**Character**: Korean MMO background music optimized for passive listening. Many tracks are quietly beautiful — Ellinia, Lith Harbour, Henesys are textbook RPG_Town material. Higher-level area themes gain Mysterious and Tense qualities.
**RPG placement**: RPG_Town, RPG_Ambient, RPG_Wandering, RPG_Relaxation (calm tracks pass the anti-gate because they lack activating moods).

### Fictional-NeonJewel

**Dominant emotions**: Mysterious, Dark, Tense, Ominous, Contemplative, Ethereal, Isolated
**Character**: Alien atmosphere and isolation. Brinstar, Phendrana Drifts, and Lower Norfair define different shades of exploration — from ethereal wonder to oppressive tension.
**RPG placement**: RPG_Mystical, RPG_Tension, RPG_Macabre, RPG_Ambient.

### Fictional-CrimsonFlame

**Dominant emotions**: Aggressive, Energetic, Explosive, Frenzy, Rebellious, Defiant, Danceful
**Character**: Hard rock/metal fighting game soundtrack. Nearly every track qualifies for RPG_Battle. Some also reach RPG_Danceful due to strong groove elements.
**RPG placement**: RPG_Battle (dominant), RPG_Danceful, RPG_Tension.

### Fictional-AmberCrown

**Dominant emotions**: Playful, Whimsical, Joyful, Adventurous, Cozy, Optimistic
**Character**: Fictional-Kw-69c2dad8's compositions are almost universally cheerful and charming. Fictional-Kw-4683fbc9, Treasure Trove Cove, and Click Clock Wood are defining examples.
**RPG placement**: RPG_Silly (primary), RPG_Town, RPG_Wandering.

### Fictional-VolcanicRiver

**Dominant emotions**: Varies widely (remixes of other franchises)
**Character**: SSB is a remix/arrangement pool — its emotional profile inherits from whatever franchise each track originates from. SSB-specific compositions tend toward Epic and Triumphant.
**RPG placement**: Distributed across all clusters depending on source franchise.

### Fictional-IronHorn

**Dominant emotions**: Aggressive, Energetic, Determined, Epic, Dark (metal covers)
**Character**: Metal covers of game and anime themes. The instrumental quality adds Energetic and Aggressive overlays to the source material's emotional content.
**RPG placement**: RPG_Battle (primary), RPG_Epic, RPG_Tension.

### Fictional-GoldenTide

**Dominant emotions**: Epic, Heroic, Determined, Melancholic, Spiritual, Contemplative
**Character**: Military strategy RPG — compositions oscillate between battle fanfares (Heroic, Triumphant) and reflective moments (Melancholic, Contemplative, Spiritual).
**RPG placement**: RPG_Epic, RPG_Battle, RPG_Melancholic, RPG_Wandering.

### Fictional-JadeWhisper, Fictional-IndigoFrost, Fictional-RustyGate

**Fictional-JadeWhisper**: Energetic, Danceful, Playful, Aggressive — RPG_Battle, RPG_Danceful.
**Fictional-IndigoFrost**: Quirky, Nostalgic, Whimsical, Contemplative — RPG_Town, RPG_Silly, RPG_Wandering. (Note: Fictional-IndigoFrost folder has non-game exclusions for Fictional-Kw-7ab91294 and Fictional-Kw-1615229b tracks.)
**Fictional-RustyGate**: Energetic, Epic, Aggressive, Determined — RPG_Battle, RPG_Epic.

## Cross-Artist Observations

1. **The ambient/energetic divide is the primary axis.** Artists cluster naturally into "background" (Fictional-SterlingHelix ambient, RO, Fictional-GoldenTower, Fictional-TimberWarden) and "foreground" (Fictional-CoralFountain, Fictional-CrimsonFlame, Fictional-CrimsonOracle) groups. The RPG cluster system mirrors this divide.

2. **Multi-mood artists are the richest sources.** Fictional-SterlingHelix, RO, WoW, and Fictional-CrystalCompass produce tracks that qualify for 3-5 clusters each. Single-mood artists (Fictional-CoralFountain, Fictional-CrimsonOracle) contribute to 1-2 clusters but very reliably.

3. **Artist fallbacks are conservative.** The fallback map only covers artists whose character is unambiguous enough to assign blindly. No fallback exists for Fictional-SterlingHelix (too diverse), WoW (too diverse), or Fictional-IndigoNeedle (gothic energy doesn't map cleanly to one cluster).

4. **The "RPG" prefix is mood-driven, not genre-gated.** Fictional-TimberWarden is not an RPG, but its building music is perfect RPG_Town material. Fictional-CoralFountain is an FPS, but its combat tracks define RPG_Battle energy. The prefix describes the _listening context_, not the source game's genre.
