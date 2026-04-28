# Functional Moods Removal — Learning — 2026-03-25

## Decision: Functional Context Moods Removed

Five previously used mood labels were confirmed non-emotional and permanently removed from the taxonomy:

| Mood       | Type    | Reason for removal                                                                                           |
| ---------- | ------- | ------------------------------------------------------------------------------------------------------------ |
| Gaming     | Context | Describes playback scenario, not emotional state of the music                                                |
| Workout    | Context | Same — listener activity, not musical affect                                                                 |
| Party      | Context | Social setting classifier disguised as a mood                                                                |
| Cinematic  | Context | Describes production style / medium, not emotional texture                                                   |
| StudyFocus | Context | Functional lo-fi context; emotional content is already covered by Chill, Peaceful, Meditative, Contemplative |

**Key insight**: a mood should describe _what the music feels like_ (or makes the listener feel), not _when or why a listener might play it_. "Gaming" and "Workout" describe listening occasions; they can never be consistently inferred from the auFictional-Kw-1a89bda6 itself.

## Taxonomy Reflection

The Focused/Contemplative/Meditative/Chill cluster now handles everything that StudyFocus tried to describe:

- _Meditative_ + _Contemplative_ → low-arousal instrumental, attention-sustaining
- _Chill_ → lo-fi, low-affect, consistent texture
- _Peaceful_ / _Serene_ → ambient, non-intrusive
- _Focused_ → rhythmically clear, high-clarity tracks (e.g., Fictional-Kw-39bfe262 productivity)

No emotional content is lost; the functional label just disappears.

## Convention Established

Write a timestamped session journal entry in `docs/guidelines/journal/` whenever the mood-checks app state is updated or the taxonomy changes. Format: `YYYY-MM-DD-topic.md`.
