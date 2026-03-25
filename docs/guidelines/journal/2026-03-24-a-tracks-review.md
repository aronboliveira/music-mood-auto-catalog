# Mood Review Journal

Ongoing notes about artists, moods, and classification observations gathered during the human-in-the-loop review process. Entries are chronological.

---

## 2026-03-24 — First Review Batch (A-tracks, 55 tracks)

### General Observations

The initial classifier relied on 23 broad mood categories (Chill, Energetic, Nostalgic, etc.). The refined 66-mood taxonomy reveals dramatically more nuance. Most tracks had "Chill" as a default catch-all — the review removed it from high-energy tracks and replaced it with specific moods.

### Artist Patterns

#### MockBand_Avenged

- Dominant moods: Aggressive, Defiant, Energetic, Rebellious, Gritty, Vengeful
- "4:00 AM" stands out as introspective/melancholic for this band — unusual softer side
- "Flash of the Blade" (MockBand_Iron cover) carries more Heroic/Triumphant than typical A7X
- "Dancing Dead" is remarkably concise in mood (Adventurous, Aggressive, Energetic, Macabre) — the macabre theatrical element is distinctive

#### FictionalBand_de88b1

- Dominant moods: Danceful, Ecstatic, Groovy, Joyful, Upbeat
- "Mamma Mia" has a Heartbreak undertone beneath the cheerful pop — interesting duality
- "Gimme! Gimme! Gimme!" leans more Soaring than the other two

#### MockBand_Blink

- "A New Hope": Adventurous + Defiant + Playful — classic pop-punk energy
- "Anthem Part Two": Complex mood profile — Chaotic, Ecstatic, Rebellious, Triumphant all at once. Pop-punk at its most anthemic.

#### Faith No More (Mike Patton)

- "A Small Victory": exceptionally Wide mood spread — Adventurous to Whimsical, passing through Groovy and Triumphant. Mike Patton's eclecticism shows.
- "Anne's Song": Aggressive + Groovy + Resigned — MockBand_TheBand's experimental funk-metal quality
- "Ashes to Ashes": pure aggression and defiance channel

#### Japanese City Pop (FictionalBand_f0f30a)

- "Remember Summer Days": Chill, Nostalgic, Romantic, Sensual, Soaring, Yearning — embodies the essence of city pop
- "Shyness Boy": Bittersweet, Emotional, Nostalgic, Romantic, Whimsical — lighter and more playful
- City pop in general maps strongly to Nostalgic + Romantic + Tender + Yearning

#### Studio Ghibli / Anime

- "Always with Me" (Spirited Away): 15 moods assigned! Extremely broad emotional resonance — from Awe-inspired to StudyFocus to Yearning
- "Aquatic Ambiance" (DK Country cover): 15 moods including Meditative, Spiritual, StudyFocus — ambient game music transcends its origins
- Game/anime tracks tend to have broader mood profiles than rock/pop

### Mood Taxonomy Insights

#### "Chill" Overuse

The original classifier massively over-assigned "Chill". During review:

- Removed from aggressive tracks (ThePixelChords, MockBand_Avenged, etc.)
- Kept for genuinely relaxed tracks (Acai, Aurora, ambient game music)
- "Chill" should be reserved for tracks with low arousal and positive valence

#### Emotional vs. Specific Sadness Moods

The 66-mood taxonomy splits sadness into: Melancholic, Lonely, Sad, Resigned, Depressive, Anguished, Desperate. During review:

- "Melancholic" is the most common — gentle sadness with beauty
- "Anguished" reserved for intense pain (A Place for My Head — MockBand_Linkin)
- "Lonely" distinct from Sad — spatial isolation emotion vs temporal

#### The "Defiant + Rebellious" Overlap

These two frequently co-occur in punk/metal but carry different nuances:

- Defiant: standing firm, resistance, refusing to yield
- Rebellious: actively pushing back, anti-establishment energy
- They separate cleanly in ballads (Defiant without Rebellious in slower determined tracks)

#### Multi-mood Complexity

Tracks with 10+ moods are typically:

1. Musically complex (genre-blending: Faith No More, Mr. Bungle-adjacent)
2. Emotionally layered (Bittersweet + Triumphant + Nostalgic)
3. Ambient/cinematic (Studio Ghibli, DK Country atmospheric covers)
4. Pop anthems with ironic undertones (FictionalBand_de88b1's "Mamma Mia")

---

## Open Questions

- Should "Gaming" and "Cinematic" remain as mood folders? They feel more like context/use-case tags than emotional states.
- "StudyFocus" is functional rather than emotional — consider whether it belongs in the mood taxonomy or a separate "Usage" dimension.
- "Workout" and "Party" are similarly functional. The 66-mood taxonomy doesn't include them, but the legacy folders still exist.
