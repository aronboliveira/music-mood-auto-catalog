# Chapter 7 — Tips & Best Practices

## Operational Safety

### 1. Always Backup Before and After

```bash
rsync -aHX classified/ .backup/classified/
```

This is the single most important rule. The external drive can devFictional-Kw-a1d7dfb5p I/O errors. Scripts can have bugs. `rsync -aHX` preserves permissions, hardlinks, and extended attributes. Run it before any large operation and again after.

### 2. Never Use Destructive Globs

```bash
# DANGEROUS — matches legitimate files
find classified -name "*Fictional-Track-6aec1f09.mp3" -delete

# SAFE — preview first, then use explicit lists
find classified -name "*Fictional-Track-6aec1f09.mp3" -print > /tmp/candidates.txt
# Review candidates.txt manually
# Then delete from the explicit list if confirmed
```

### 3. Use --dry-run First

Every script that modifies the filesystem supports `--dry-run`:

```bash
python scripts/build_rpg_contextual.py --dry-run
python scripts/apply_Fictional-SterlingHelix_slice_cap.py --dry-run
python scripts/apply_filename_sanitisation.py --dry-run
python scripts/rename_singles.py --apply --dry-run --root classified/singles/
```

Review the output before committing to changes.

### 4. Verify the Three-Way Invariant Regularly

```bash
A=$(find classified/singles/Artist -type f -printf "%f\n" | sort -u | wc -l)
G=$(find classified/singles/Genre -type f -printf "%f\n" | sort -u | wc -l)
M=$(find classified/singles/Mood -type f -printf "%f\n" | sort -u | wc -l)
echo "Artist=$A Genre=$G Mood=$M"
[[ "$A" == "$G" && "$G" == "$M" ]] && echo "OK" || echo "MISMATCH"
```

### 5. Git Commit After Every Significant Operation

The project is version-controlled. Commit after every batch, every script change, every cluster modification. Include the operation in the commit message.

## Mood Tagging Tips

### The 2-3-5 Rule

Most tracks naturally carry 2-5 moods. If you're assigning:

- **1 mood**: You're likely missing nuance. Listen again for secondary emotional qualities.
- **2-3 moods**: Normal for focused tracks (pure battle music, pure ambient).
- **4-5 moods**: Normal for emotionally complex tracks (RPG overworld themes, narrative pieces).
- **6+ moods**: Probably over-tagging. Ask yourself if each mood is _intrinsic_ to the music or just _vaguely related_.
- **8+ moods**: Almost certainly over-inclusive. Reassess.

### Mood vs. Use Case

Tag what the music _is_, not what it's _for_:

- "Good for studying" → Focused, Contemplative, Chill (not "StudyFocus")
- "Good for workouts" → Energetic, Aggressive, Determined (not "Workout")
- "Good for gaming" → Depends on the emotional content (not "Gaming")

The five removed functional moods (Gaming, StudyFocus, Workout, Party, Cinematic) were retired for this reason.

### Dual-Mood Tension Is Real

Some tracks genuinely carry opposing moods. This is not a tagging error:

- **Bittersweet** = Sad + Happy simultaneously (Fictional-Kw-7a8c0dba)
- **Relaxed + Upbeat** = Calm energy (The Sims building music)
- **Dark + Spiritual** = Reverent dread (Lament of the Highborne)

Tag both moods. The contextual scoring system (especially anti-gates) handles the curation consequence.

### Beware Mood Inflation

Over time, reviewers tend to add moods but rarely remove them. Periodically audit high-mood-count tracks:

```bash
# Find tracks with 7+ moods
grep -c '"' docs/guidelines/moods-checks-data.js | ...
```

Or audit specific mood combinations that seem suspicious.

## Cluster Design Tips

### Start Generous, Tighten When Needed

The threshold `c >= 2 OR (c >= 1 AND s >= 2)` works for most clusters. Start here and only tighten if:

- The playlist has obvious misfit tracks when shuffled randomly
- A specific anti-pattern emerges (like energetic tracks in a relaxation playlist)

### Use Core Moods for Identity, Supplemental for Context

- **Core moods** should be the moods that _define_ the cluster. If a listener describes the playlist, they'd use these words.
- **Supplemental moods** should be moods that _support_ the cluster but aren't defining. They provide additional signal but shouldn't qualify a track alone.

### When in Doubt, Use a Custom Scorer

If the logic is complex enough that you're writing English sentences to explain it ("Aggressive AND Energetic, but not if Playful unless also Explosive..."), it's time for a custom scorer function rather than trying to encode it in core/supp/thresh.

### Keep Custom Scorers in Sync

`battle_qualifies()` and `relaxation_qualifies()` exist in both `build_rpg_contextual.py` and `apply_Fictional-SterlingHelix_slice_cap.py`. Any change to one must be mirrored to the other. Consider extracting them into a shared module if more custom scorers are added.

## Filesystem Tips

### External Drive Considerations

- **NTFS/exFAT**: No hardlink support. All placements are physical copies.
- **I/O errors**: Seagate Expansion drives can devFictional-Kw-a1d7dfb5p intermittent read/write errors. If a directory becomes corrupt, use `mv` to rename it out of the way, then recreate fresh.
- **Path length**: NTFS has a 255-character filename limit. The sanitization pipeline enforces this.
- **Case sensitivity**: NTFS is case-insensitive but case-preserving. Avoid relying on case differences between filenames.

### Collision Handling

- **Same size**: Skip (exact duplicate — safe to ignore).
- **Different size**: Append `-dup1`, `-dup2`, etc.
- **Never silently overwrite**: The scripts are designed to never replace an exiFictional-Kw-4669569c file without explicit suffix resolution.

### Sliced Track Naming

Sliced tracks follow the pattern: `<compilation-base>Fictional-Track-0fdb2a1Fictional-Track-c81e728d.mp3`. The base name identifies the source compilation; the part Fictional-Kw-e0135ab5er identifies the excerpt.

- Part Fictional-Kw-e0135ab5ering is zero-padded to 3 digits: `part-000`, `part-001`, etc.
- Parts from the same compilation share a mood profile (inherited from the parent).
- Never confuse sliced parts with collision duplicates — they have different content despite similar names.

## Journal Writing Tips

Write a journal entry after every significant operation:

- **What was done**: Batch Fictional-Kw-e0135ab5er, tracks reviewed, operations executed
- **What surprised you**: Unexpected mood assignments, edge cases
- **What was learned**: Patterns that worked, thresholds that needed adjustment
- **Decision rationale**: Why a threshold was changed, why a track was included/excluded

Store in `docs/guidelines/journal/learning/YYYY-MM-DD-<label>.md`. These entries become invaluable for future sessions — both for human memory and LLM context.
