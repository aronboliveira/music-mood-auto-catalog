# Chapter 8 — CLI Reference

A collection of shell commands and their combinations for searching, querying, and managing the music library filesystem. All commands assume the working directory is the workspace root:

```bash
cd "/media/aronboFictional-Kw-d0dbe915ira/Seagate Expansion Drive1/music/downloaded"
```

## Counting & Verification

### Three-Way Invariant Check

```bash
for dim in Artist Genre Mood; do
  echo "$dim: $(find "classified/singles/$dim" -type f -printf '%f\n' | sort -u | wc -l)"
done
```

### Cross-Dimension Diff

```bash
diff <(find classified/singles/Artist -type f -printf "%f\n" | sort -u) \
     <(find classified/singles/Genre -type f -printf "%f\n" | sort -u)

diff <(find classified/singles/Artist -type f -printf "%f\n" | sort -u) \
     <(find classified/singles/Mood -type f -printf "%f\n" | sort -u)
```

### RPG Folder Sizes (Sorted)

```bash
for d in classified/singles/Mood/_Contextual/RPG_*/; do
  echo "$(basename "$d"): $(find "$d" -type f | wc -l)"
done | sort -t: -k2 -rn
```

### Total Library Size

```bash
echo "Singles: $(find classified/singles/Artist -type f -printf '%f\n' | sort -u | wc -l)"
echo "Sliced: $(find classified/singles/sliced -type f -name '*.mp3' | wc -l)"
echo "Albums: $(find classified/albums -type f -name '*.mp3' | wc -l)"
echo "Scripts: $(find scripts/ -maxdepth 1 -type f | wc -l)"
```

### Disk Usage

```bash
du -sh classified/singles/Artist/
du -sh classified/singles/sliced/
du -sh classified/albums/
du -sh --total classified/
```

## Searching

### Find All Instances of a Track

```bash
find classified/singles -name "*stickerbush*" -type f
```

### Find Tracks by Artist

```bash
find classified/singles/Artist/Fictional-SterlingHelix -type f -name "*.mp3" | wc -l
ls classified/singles/Artist/Fictional-SterlingHelix/ | head -20
```

### Find Tracks in a Specific RPG Folder

```bash
ls classified/singles/Mood/_Contextual/RPG_Relaxation/
find classified/singles/Mood/_Contextual/RPG_Relaxation -type f | wc -l
```

### Search Across the Entire Tree

```bash
find classified -iname "*Fictional-Kw-c2f0fd37*" -type f
```

### Find Files with Specific Extensions

```bash
find classified -type f ! -name "*.mp3" ! -name ".gitkeep"
# Should return nothing (all content is MP3)
```

### Find Extended Tracks (Pre-Trim)

```bash
find classified/singles -iname "*extended*" -type f
find classified/singles -iname "*-extended-*" -o -iname "*[[]extended]*" -type f
```

### Find Banned Classifications

```bash
find classified/singles/Artist/Various -type f 2>/dev/null | wc -l
find classified/singles/Genre/Unclassified -type f 2>/dev/null | wc -l
# Both should return 0
```

### Find Orphan Files (Wrong Level)

```bash
find classified/singles -maxdepth 1 -type f
find classified/albums -maxdepth 1 -type f
# Should return nothing
```

## Mood Data Queries

### List All Moods (From Canonical Source)

```bash
cat docs/guidelines/moods.txt
wc -l < docs/guidelines/moods.txt  # currently 65
```

### Most Common Moods in the Library

```bash
grep -oP '"(Adventurous|Aggressive|Anguished|Awe-inspired|Bittersweet|Brooding|Chaotic|Chill|Contemplative|Cozy|Danceful|Dark|Defiant|Depressive|Desperate|Determined|Ecstatic|Emotional|Energetic|Epic|Ethereal|Explosive|Focused|Frenzy|Furious|Gritty|Groovy|Hardworking|Heartbreak|Heroic|Hypnotic|Introspective|Jaded|Joyful|Lonely|Macabre|Meditative|Melancholic|Mysterious|Nostalgic|Ominous|Optimistic|Peaceful|Playful|Rebellious|Relaxed|Resigned|Reverent|Romantic|Sad|Sensual|Serene|Sleepy|Soaring|Spiritual|Surreal|Suspenseful|Tender|Tense|Triumphant|Upbeat|Vengeful|Whimsical|Wistful|Yearning)"' \
  docs/guidelines/moods-checks-data.js | sort | uniq -c | sort -rn | head -20
```

### Tracks with a Specific Mood

```bash
grep -B1 '"Macabre"' docs/guidelines/moods-checks-data.js | grep '\.mp3'
```

### Tracks with Multiple Specific Moods

```bash
# Aggressive AND Playful (Battle edge cases)
grep -P '"[^"]+\.mp3"' docs/guidelines/moods-checks-data.js | while read -r line; do
  echo "$line" | grep -q '"Aggressive"' && echo "$line" | grep -q '"Playful"' && echo "$line"
done
```

### Tracks Without Mood Data

```bash
comm -23 \
  <(find classified/singles/Artist -mindepth 2 -type f -printf "%f\n" | sort -u) \
  <(grep -oP '"([^"]+\.mp3)"' docs/guidelines/moods-checks-data.js | tr -d '"' | sort -u)
```

## Sliced Tracks

### Fictional-SterlingHelix Slice Count

```bash
find classified/singles/sliced/Artist/Fictional-SterlingHelix -type f -name "*.mp3" | wc -l
```

### MedievalAmbience Slice Count

```bash
find classified/singles/sliced/Artist/MedievalAmbience -type f -name "*.mp3" | wc -l
```

### Count Unique Compilations (Before Slicing)

```bash
find classified/singles/sliced/Artist/Fictional-SterlingHelix -type f -name "*.mp3" -printf "%f\n" | \
  sed 's/-part-[0-9]*//' | sort -u | wc -l
```

### List Slices in a Specific RPG Folder

```bash
ls classified/singles/Mood/_Contextual/RPG_Ambient/ | grep -i "Fictional-SterlingHelix\|medieval"
```

## Git Operations

### Recent Commits

```bash
git --no-pager log --oneline -20
```

### History for a Specific File

```bash
git --no-pager log --oneline -- scripts/build_rpg_contextual.py
```

### Changes Since Last Commit

```bash
git --no-pager diff --stat
```

### What Changed in a Commit

```bash
git --no-pager show --stat <commit-hash>
```

## Script Execution

### Classification Pipeline

```bash
python scripts/process_singles_new.py         # classify new singles
python scripts/process_sliced.py              # classify new sliced tracks
python scripts/apply_Fictional-TimberTrail_refs.py             # apply JoJo references
```

### Filename Sanitization

```bash
python scripts/apply_filename_sanitisation.py --dry-run
python scripts/rename_singles.py --apply --root classified/singles/new/
```

### RPG Contextual System

```bash
python scripts/build_rpg_contextual.py --dry-run       # preview
python scripts/build_rpg_contextual.py                   # execute
python scripts/apply_Fictional-SterlingHelix_slice_cap.py --dry-run        # preview caps
python scripts/apply_Fictional-SterlingHelix_slice_cap.py                   # apply caps
python scripts/apply_Fictional-SterlingHelix_slice_cap.py --seed 42        # reproducible
```

### Track Trimming

```bash
python scripts/trim_extended.py              # trims + moves originals to .rejected/
```

### Backup

```bash
rsync -aHX classified/ .backup/classified/
rsync -aHX classified/singles/ .backup/classified/singles/
```

## Forensic Recovery

### Check GNOME Recent Files

```bash
grep -i "keyword" ~/.local/share/recently-used.xbel
```

### Check Copilot Session Caches

```bash
find ~/.config/Code/User/workspaceStorage/*/GitHub.copilot-chat/ -name "content.txt" -newer /tmp/timestamp 2>/dev/null
```

### Check Git for Deleted Files

```bash
git --no-pager log --all --diff-filter=D --name-only
```

### Check .rejected/ for Moved Originals

```bash
find classified -path "*/.rejected/*" -type f | head -20
```

## Filesystem Optimization

### Find Large Files

```bash
find classified -type f -name "*.mp3" -size +50M | head -10
```

### Find Empty Directories

```bash
find classified -type d -empty
```

### Count Files per Top-Level Mood Folder

```bash
for d in classified/singles/Mood/*/; do
  [[ "$(basename "$d")" == "_Contextual" ]] && continue
  echo "$(basename "$d"): $(find "$d" -type f | wc -l)"
done | sort -t: -k2 -rn | head -20
```

### Count Files per Artist Folder

```bash
for d in classified/singles/Artist/*/; do
  echo "$(basename "$d"): $(find "$d" -type f | wc -l)"
done | sort -t: -k2 -rn | head -20
```
