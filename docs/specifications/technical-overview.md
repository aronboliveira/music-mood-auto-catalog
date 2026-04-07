# Technical Specifications

## Music Library Classification Pipeline — Deep Documentation

**Version**: 2.0 (March 2026)
**Maintainer**: Aron Boliveira
**LLM-assisted development**: Claude Opus 4.6 (primary), Sonnet 4.6, Haiku 4.5, Gemini 3.1

---

## Table of Contents

1. [System Architecture](#1-system-architecture)
2. [Classification Algorithm](#2-classification-algorithm)
3. [Mood Taxonomy & Emotional Model](#3-mood-taxonomy--emotional-model)
4. [Mood Similarity Ordering](#4-mood-similarity-ordering)
5. [Review Application](#5-review-application)
6. [Filesystem Sync Protocol](#6-filesystem-sync-protocol)
7. [Filename Sanitization](#7-filename-sanitization)
8. [Data Formats & Schemas](#8-data-formats--schemas)
9. [LLM Integration](#9-llm-integration)
10. [Operational Procedures](#10-operational-procedures)

---

## 1. System Architecture

### 1.1 High-Level Flow

```
raw downloads → sanitization → classification → mood review (Vue app)
                                                     ↓
                                            mood correction (human)
                                                     ↓
                                            JSON export → fs sync
```

### 1.2 Directory Structure

See [storage-conventions.yml](../guidelines/storage-conventions.yml) for the canonical definition.

The system uses a **multi-label copy model**: each track is physically copied (not hardlinked — external NTFS/exFAT drives don't support hardlinks reliably) into every matching folder across all dimensions.

**Dimensional cardinality** (as of 2026-03-24):

- Artist: 200 folders (singles) + 61 folders (albums)
- Genre: 55 folders
- Mood: 63 folders (65 canonical moods — functional context moods removed: Gaming, StudyFocus, Workout, Party, Cinematic)
- Total unique basenames: 980 singles + ~100 album tracks

### 1.3 Script Inventory

See [scripts-inventory.yml](scripts-inventory.yml) for the full 25-script manifest with descriptions and dependency graphs.

---

## 2. Classification Algorithm

### 2.1 Classifier Type

**Keyword-score ensemble** — a rule-based multi-label classifier operating on filename text tokens. Not ML-trained; relies on curated keyword dictionaries.

### 2.2 Pipeline Stages

```
                  filename
                     │
                ┌────▼────┐
                │ Normalize│  lowercase, strip noise, collapse whitespace
                └────┬────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐
   │ Artist  │ │  Genre  │ │  Mood   │
   │ matcher │ │ matcher │ │ matcher │
   └────┬────┘ └────┬────┘ └────┬────┘
        │            │            │
        ▼            ▼            ▼
   keyword      keyword +     keyword
   score        artist-genre  score
                boost
        │            │            │
        └────────────┼────────────┘
                     │
                ┌────▼────┐
                │ Validate│  reject "Various"/"Unclassified"
                └────┬────┘
                     │
                ┌────▼────┐
                │  Copy   │  cp to all matched folders
                └─────────┘
```

### 2.3 Normalization

Implemented in `classify_and_clean.py::clean_filename()`:

1. Lowercase the basename (without extension)
2. Strip noise patterns: `y2mate-com-`, bracketed YouTube IDs `[xbDevCTNWiM]`, marketing tags
3. Convert `_`, `-`, repeated `.` to spaces
4. Collapse whitespace to single space
5. Trim

### 2.4 Artist Matching

Direct keyword lookup against a dictionary of ~200 artist name patterns. Each entry maps keyword tokens to canonical artist folder name.

### 2.5 Genre Matching

Two-pass scoring:

1. **Direct keyword score**: genre keywords matched against normalized filename
2. **Artist-to-genre boost**: if an artist is resolved, their known genre affinities add partial score to matching genres

This ensemble behavior prevents genre misclassification when an artist spans multiple genres.

### 2.6 Mood Matching

Pure keyword-score against mood descriptor dictionaries. Originally 23 broad moods; expanded to 66 fine-grained moods in March 2026.

### 2.7 Tuning Parameters

See [classifier-tuning.toml](../guidelines/classifier-tuning.toml) for threshold values, boost weights, and keyword dictionaries.

---

## 3. Mood Taxonomy & Emotional Model

### 3.1 Evolution

| Version | Date       | Moods | Notes                                     |
| ------- | ---------- | ----- | ----------------------------------------- |
| v1      | 2026-03-17 | 23    | Broad categories (Chill, Energetic, etc.) |
| v2      | 2026-03-24 | 66    | Fine-grained, 6D emotional model          |
| v3      | 2026-03-25 | 65    | Removed functional context moods          |

### 3.2 The 65 Moods

Organized by semantic cluster (see [mood-vectors.json](mood-vectors.json)):

1. **Calm**: Serene, Peaceful, Relaxed, Chill, Sleepy
2. **Cozy**: Cozy, Tender
3. **Romantic**: Romantic, Sensual
4. **Emotional**: Emotional, Yearning, Bittersweet, Wistful
5. **Nostalgic**: Nostalgic
6. **Reflective**: Meditative, Contemplative, Spiritual, Reverent, Awe-inspired
7. **Withdrawn**: Jaded, Introspective
8. **Tension**: Suspenseful, Tense, Gritty
9. **Heartache**: Heartbreak, Melancholic, Lonely
10. **Grief**: Sad, Resigned, Depressive, Anguished, Desperate
11. **Dark**: Ominous, Macabre, Dark, Brooding
12. **Surreal**: Mysterious, Surreal, Hypnotic, Ethereal
13. **Chaos**: Chaotic, Frenzy, Explosive
14. **Rebellion**: Rebellious, Defiant, Aggressive, Furious, Vengeful
15. **Energy**: Energetic, Danceful, Groovy
16. **Soaring**: Soaring, Adventurous
17. **Heroic**: Triumphant, Heroic, Epic
18. **Focus**: Determined, Hardworking, Focused
19. **Joy**: Whimsical, Optimistic, Upbeat, Playful, Joyful, Ecstatic

### 3.3 6D Emotional Vector Space

Each mood is represented as a point in 6-dimensional emotional space:

| Dimension      | Range    | Semantic Poles         |
| -------------- | -------- | ---------------------- |
| Valence (V)    | [-1, +1] | Negative ←→ Positive   |
| Arousal (A)    | [-1, +1] | Calm ←→ Energetic      |
| Dominance (D)  | [-1, +1] | Submissive ←→ Powerful |
| Darkness (K)   | [-1, +1] | Light ←→ Dark          |
| Longing (L)    | [-1, +1] | Content ←→ Yearning    |
| Inwardness (I) | [-1, +1] | External ←→ Internal   |

The first three dimensions (VAD) follow the **Russell–Mehrabian** affective space model. Dimensions 4-6 were added to better separate moods that collapse in 3D (e.g., Nostalgic vs. Introspective both have similar VAD but differ in Longing and Inwardness).

See [mood-vectors.json](mood-vectors.json) for the complete 65×6 vector table.

### 3.4 Mood Color Palette

Each mood is assigned a unique `rgb()` color for the review app. Colors are chosen for:

- Perceptual distinctness between adjacent moods in the grid
- Thematic association (warm colors for energetic moods, cool for calm, dark for heavy)

See `MOOD_COLORS` in `docs/guidelines/moods-checks-data.js`.

---

## 4. Mood Similarity Ordering

### 4.1 Problem Statement

Given 66 moods to display in a 1D grid, order them so that emotionally similar moods are positionally adjacent. This is a variant of the **Shortest Hamiltonian Path** problem in 6D Euclidean space.

### 4.2 Algorithm

Implemented in `scripts/_sort_moods.py`:

```
Input:  65 mood vectors in R^6, 15 semantic clusters
Output: 1D ordering minimizing emotional discontinuity

for each cluster in CLUSTERS (ordered by emotional arc):
    members ← moods in this cluster
    path ← nearest_neighbor_tsp(members)
    if previous_cluster exists:
        orient path so its head faces previous cluster's tail
    append path to global ordering
```

### 4.3 Distance Metric

Euclidean distance in 6D:

$$d(a, b) = \sqrt{\sum_{i=1}^{6} (a_i - b_i)^2}$$

### 4.4 Nearest-Neighbor Within Clusters

For each cluster, the nearest-neighbor greedy TSP is applied:

1. Try every member as starting point
2. At each step, visit the unvisited member with minimum Euclidean distance
3. Select the tour with minimum total path cost

### 4.5 Boundary Orientation

After ordering each cluster, orient it (possibly reverse) to minimize distance between:

- The **tail** (last element) of the previous cluster
- The **head** (first element) of the current cluster

This ensures smooth transitions at cluster boundaries.

### 4.6 Iteration History

| Iteration | Dimensions | Strategy                   | Nostalgic→Yearning gap | Sad→Lonely gap |
| --------- | ---------- | -------------------------- | ---------------------- | -------------- |
| 1         | 4D (VAD+K) | Global NN-TSP + 2-opt      | 26                     | 15             |
| 2         | 6D         | Global NN-TSP + 2-opt      | 12                     | 8              |
| 3         | 6D         | 13 semantic clusters + NN  | 3                      | 1              |
| 4         | 6D         | 15 clusters (user reorder) | 3                      | 1              |

### 4.7 Validation

Key proximity checks (gap = positional distance in 66-mood ordering):

| Pair                    | Gap | Target |
| ----------------------- | --- | ------ |
| Nostalgic ↔ Yearning    | 3   | ≤ 5    |
| Nostalgic ↔ Melancholic | 12  | ≤ 15   |
| Focused ↔ Determined    | 2   | ≤ 5    |
| Sad ↔ Lonely            | 1   | ≤ 3    |
| Rebellious ↔ Aggressive | 2   | ≤ 3    |

---

## 5. Review Application

### 5.1 Architecture

```
moods-checks.html          Slim HTML shell (Vue 3 mount point)
moods-checks-app.js        Vue 3 Composition API (state, events, export)
moods-checks-data.js       Data bundle (ALL_MOODS, MOOD_COLORS, REVIEWED_TRACKS, TRACK_MOODS)
moods-checks.css            Dark theme stylesheet
```

### 5.2 Dependencies (CDN, SRI)

| Library       | Version | Integrity                                                                 |
| ------------- | ------- | ------------------------------------------------------------------------- |
| Bootstrap CSS | 5.3.8   | `sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB` |
| Bootstrap JS  | 5.3.8   | `sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI` |
| Vue 3         | latest  | CDN (unpkg, prod build)                                                   |

### 5.3 State Management

```
localStorage["moods-checks-state-v1"] = {
  "<Fictional-Track-435ed7e9.mp3>": {
    "reviewed": boolean,
    "open": boolean,
    "moods": ["Mood1", "Mood2", ...]
  },
  ...
}
```

- **Initialization**: TRACK_MOODS defaults → overlay REVIEWED_TRACKS → overlay localStorage
- **Persistence**: debounced 300ms autosave to localStorage on any state change
- **Export**: JSON download or YAML clipboard copy

### 5.4 UI Components

| Element        | Implementation                                    |
| -------------- | ------------------------------------------------- |
| Track cards    | `<details>` / `<summary>` with Vue `v-for`        |
| Mood grid      | CSS Grid `auto-fill, minmax(165px, 1fr)`          |
| Progress bar   | Bootstrap `.progress-bar` bound to reviewed count |
| Search         | Text input filtering `trackNames` array           |
| Autosave badge | Fading text indicator, pointer-events disabled    |

---

## 6. Filesystem Sync Protocol

### 6.1 Sync Process

When corrected mood assignments are exported as JSON:

1. Parse JSON → dict of `{filename: [moods]}`
2. For each track in the batch:
   a. Find source file in `classified/singles/Artist/*/`
   b. Scan existing `classified/singles/Mood/*/` for current placements
   c. **Remove** files from mood folders no longer assigned
   d. **Copy** files to mood folders newly assigned
3. Create new mood directories as needed (`os.makedirs`)

### 6.2 Conflict Resolution

Same as the main classifier:

- Same-size file exists at destination → skip
- Different-size file exists → append `-dup1`, `-dup2`

### 6.3 Backup SOP

```bash
rsync -aHX classified/ .backup/classified/
```

Always before and after large batch operations.

---

## 7. Filename Sanitization

See [filename-sanitisation.md](../guidelines/filename-sanitisation.md) for the complete reference.

Summary pipeline: emoji→words → CJK/Kana/Hangul→ASCII (unidecode) → strip diacriticals → remove unsafe chars → normalize hyphens → strip leading/trailing noise → preserve `.mp3`.

---

## 8. Data Formats & Schemas

### 8.1 track-moods.json

```json
{
  "<Fictional-Track-435ed7e9.mp3>": ["Mood1", "Mood2", ...],
  ...
}
```

- Keys: sanitized filenames with `.mp3` extension
- Values: sorted arrays of mood label strings
- Total entries: 970

### 8.2 moods-checks-data.js

JavaScript constants:

- `ALL_MOODS: string[]` — ordered list of 65 mood labels
- `MOOD_COLORS: Record<string, string>` — mood → `rgb()` color map
- `REVIEWED_TRACKS: string[]` — pre-reviewed track filenames
- `TRACK_MOODS: Record<string, string[]>` — filename → mood list

### 8.3 mood-vectors.json

See [mood-vectors.json](mood-vectors.json) for the 65×6 emotional vector definitions.

### 8.4 moods-guide.json

Descriptive guide with human-readable descriptions and example tracks for each mood.

See [moods-guide.json](../guidelines/moods-guide.json).

---

## 9. LLM Integration

### 9.1 Models Used

| Model                 | Provider  | Role                                                                      |
| --------------------- | --------- | ------------------------------------------------------------------------- |
| **Claude Opus 4.6**   | Anthropic | Primary agent — algorithm design, code generation, Vue app, documentation |
| **Claude Sonnet 4.6** | Anthropic | Quick iterations, refactoring                                             |
| **Claude Haiku 4.5**  | Anthropic | Lightweight data validation tasks                                         |
| **Gemini 3.1**        | Google    | Alternative perspective on mood clustering                                |

### 9.2 Agent Mode

All development conducted in **VS Code GitHub Copilot Agent Mode** with filesystem, terminal, and search tools. The LLM:

- Reads/writes files directly via workspace tools
- Executes Python scripts in terminal
- Runs validation commands
- Iterates on algorithm output with user feedback

### 9.3 Human-in-the-Loop Protocol

1. LLM proposes initial classification (keywords + heuristics)
2. Human reviews via Vue app (visual checkbox grid)
3. Human exports corrections as JSON
4. LLM ingests JSON and syncs filesystem
5. Repeat for next batch (alphabetical progression: A→Z)

---

## 10. Operational Procedures

### 10.1 Adding New Tracks

1. Place files in `classified/singles/new/`
2. Run `python3 scripts/process_singles_new.py`
3. Regenerate moods data: `python3 scripts/gen_moods_checks.py`
4. Review in browser app
5. Export and sync

### 10.2 Regenerating Maps

```bash
# After any structural change
python3 scripts/classify_and_clean.py --map-only
```

### 10.3 Backup & Recovery

```bash
# Before operations
rsync -aHX classified/ .backup/classified/

# After verification
rsync -aHX classified/ .backup/classified/
```

### 10.4 Daily Log Convention

Logs are stored in `logs/YYYYMMDD/` folders. One folder per day of active development.
