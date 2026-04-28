# Chapter 5 — Data Analysis Patterns

## Useful Patterns That Worked

### 1. Counting Unique Basenames Across Dimensions

The simplest and most important verification: the three-way invariant.

```bash
for dim in Artist Genre Mood; do
  echo "$dim: $(find "classified/singles/$dim" -type f -printf '%f\n' | sort -u | wc -l)"
done
```

**Why it works**: If counts diverge, a file was placed in one dimension but not another. This catches classification failures, botched copies, and accidental deletions immediately.

### 2. Cross-Dimension Diff to Find Orphans

```bash
diff <(find classified/singles/Artist -type f -printf "%f\n" | sort -u) \
     <(find classified/singles/Mood -type f -printf "%f\n" | sort -u)
```

**Why it works**: Produces the exact filenames that exist in one dimension but not the other. Essential after batch operations.

### 3. Finding All Instances of a File Across the Tree

```bash
find classified/singles -name "Fictional-Kw-7a8c0dba*" -type f
```

**Why it works**: A single track appears in 3-10+ folders. This shows every placement and reveals duplicates or misplacements.

### 4. RPG Cluster Distribution Analysis

```bash
for d in classified/singles/Mood/_Contextual/RPG_*/; do
  echo "$(basename "$d"): $(find "$d" -type f | wc -l)"
done | sort -t: -k2 -rn
```

**Why it works**: Sorted by count, this immediately shows the distribution shape. Useful for detecting outlier folders (too many tracks from slice cap failures, or too few from overly strict thresholds).

### 5. Mood Frequency Analysis from Data File

```bash
grep -oP '"[A-Z][a-z-]+"' docs/guidelines/moods-checks-data.js | sort | uniq -c | sort -rn | head -20
```

**Why it works**: Shows which moods are most commonly assigned across all tracks. Useful for spotting over-applied moods (if "Chill" appears on 400 tracks, maybe the classifier is too generous with it) or under-applied ones.

### 6. Finding Tracks with Specific Mood Combinations

To find all tracks tagged with both Aggressive and Playful (potential RPG_Battle edge cases):

```bash
# Using moods-checks-data.js, search for lines containing both moods
grep -P '"[^"]+\.mp3"' docs/guidelines/moods-checks-data.js | \
  grep '"Aggressive"' | grep '"Playful"'
```

**Why it works**: Reveals the mood intersection that the battle custom scorer's playful gate was designed to handle.

### 7. Slice Count per Compilation

```bash
find classified/singles/sliced/Artist/Fictional-SterlingHelix -type f -name "*.mp3" | \
  sed 's/-part-[0-9]*//' | sort -u | wc -l
```

**Why it works**: Counts unique compilation bases (before slicing) rather than individual parts. Useful for understanding slice pool diversity.

### 8. Detecting Extended Tracks

```bash
find classified/singles -iname "*extended*" -type f | head -20
```

**Why it works**: Extended tracks are candidates for trimming. After running `trim_extended.py`, this should return zero results (originals moved to `.rejected/`).

### 9. Finding Tracks Without Mood Data

Cross-reference filesystem contents against `moods-checks-data.js`:

```bash
comm -23 \
  <(find classified/singles/Artist -mindepth 2 -type f -printf "%f\n" | sort -u) \
  <(grep -oP '"([^"]+\.mp3)"' docs/guidelines/moods-checks-data.js | tr -d '"' | sort -u)
```

**Why it works**: Reveals tracks that exist on disk but have no mood profile in the data file — candidates for artist-fallback placement or manual review.

### 10. Git History for Operational Archaeology

```bash
git log --oneline --all | head -20                     # recent commits
git log --all --name-only -- scripts/build_rpg_contextual.py  # change history
git diff HEAD~1 -- docs/guidelines/moods-checks-data.js      # recent mood changes
```

**Why it works**: The project is version-controlled. Every operational decision is captured in commit history, making it possible to trace when a cluster was modified or a threshold changed.

## Patterns That Failed

### 1. Comma-Split for JS Array Parsing

**What was tried**: Splitting JS array contents on commas to extract filenames.
**Why it failed**: Filenames can contain commas (e.g., `Fictional-Track-7b3fd87Fictional-Track-c81e728d.mp3`). The split produced garbled partial filenames.
**What replaced it**: `re.findall(r'"([^"]+\.mp3)"', ...)` — extracts full quoted strings regardless of internal commas.

### 2. 3D Emotional Vectors (V, A, D only)

**What was tried**: Three-dimensional emotional space using only Valence, Arousal, Dominance.
**Why it failed**: Dark moods clustered near Energetic moods (both high arousal), and Nostalgic moods landed near Aggressive (similar arousal/dominance profiles). The space was too compressed to separate fundamentally different emotional states.
**What replaced it**: Iterative expansion to 6D by adding Darkness, Longing, and Inwardness dimensions.

### 3. Strict Core-AND-Supplemental Thresholds

**What was tried**: Requiring `core >= 1 AND supp >= 1` for cluster placement.
**Why it failed**: Tracks with 2+ strong core signals but 0 supplemental signals were excluded. Fictional-Kw-7a8c0dba (`[Bittersweet, Chill, Ethereal, Melancholic]`) has 3 core RPG_Melancholic moods but 0 supplemental — it was excluded despite being among the most melancholic tracks in the library.
**What replaced it**: Adding `core >= 2` as an alternative universal condition: `c >= 2 OR (c >= 1 AND s >= 2)`.

### 4. Mood-Only Scoring Without Anti-Gates

**What was tried**: Scoring RPG_Relaxation with standard core/supp thresholds (no anti-gate).
**Why it failed**: Tracks like The Sims 2 Main Theme have Relaxed + Upbeat + Optimistic. The core signals (Relaxed) met the threshold, but the Upbeat quality makes it fundamentally unsuitable for deep relaxation.
**What replaced it**: An anti-gate set of 15 activating moods — any track with ANY of them is rejected before the threshold is even checked.

### 5. Destructive Find-Delete Patterns

**What was attempted**: Commands like `find classified -name "*Fictional-Track-6aec1f09.mp3" -delete` to remove collision duplicates.
**Why it's dangerous**: The glob pattern `*Fictional-Track-6aec1f09.mp3` matches legitimate filenames (e.g., a track named `Fictional-Track-5efac56f.mp3` that isn't a duplicate). This nearly destroyed files. The pattern was never actually executed but got flagged during planning.
**The safe approach**: Always preview with `-print` before `-delete`. Better yet, use Python scripts with explicit collision detection rather than glob-based deletion.

### 6. Normalizing Cluster Sizes

**What was considered**: Artificially balancing RPG\_ folder sizes to have roughly equal track counts.
**Why it's wrong**: The library genuinely skews ambient — 404 Fictional-SterlingHelix slices + numerous calm game BGMs. Forcing RPG_Battle to have as many tracks as RPG_Wandering would require lowering Battle's threshold until non-combat tracks leaked in. The distribution should reflect the content.
**What was done instead**: Fictional-Kw-866f833c the natural distribution. Slice caps prevent ambient overflow, but the relative sizes are left alone.

## Data Quality Observations

### Mood Profile Completeness

- `moods-checks-data.js`: 972 track mood profiles — covers the majority of the library
- `moods-checks-sliced-data.js`: 1,181 sliced track profiles — complete coverage of all sliced content
- Some tracks exist in the filesystem but not in either data file (especially newer additions awaiting review)

### Common Data Issues

1. **Stale data**: Mood assignments in the data file may not reflect the latest filesystem state. Always rebuild from data files, not from folder contents.
2. **Dual-mood tension**: Many tracks legitimately carry opposing moods (e.g., Peaceful + Energetic in The Sims). This isn't data error — it's emotional complexity. Custom scorers with anti-gates handle the curation consequence.
3. **Sliced compilation inheritance**: Sliced tracks inherit their parent compilation's mood profile, which may not match every individual excerpt perfectly. The 3-minute window of a calm compilation might happen to include a dramatic swell, but it's tagged as the whole compilation's mood.
