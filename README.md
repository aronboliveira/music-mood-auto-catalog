# Music Library Classification Pipeline

A semi-automated pipeline for classifying, organizing, and mood-tagging a personal music library of ~1,080 tracks (980 singles + ~100 album tracks) across three orthogonal taxonomies: **Artist**, **Genre**, and **Mood**.

## Quick Stats

| Dimension                | Count |
| ------------------------ | ----- |
| Unique singles           | 980   |
| Artist folders (singles) | 200   |
| Genre folders            | 55    |
| Mood labels              | 66    |
| Mood folders             | 68    |
| Album artist folders     | 61    |
| Automation scripts       | 25    |

## Architecture

```
classified/
  albums/Artist/<ArtistName>/*.mp3
  singles/
    Artist/<ArtistName>/*.mp3      # primary dimension
    Genre/<GenreName>/*.mp3        # multi-label
    Mood/<MoodLabel>/*.mp3         # multi-label (66 moods)
docs/
  guidelines/       # classification rules, moods-checks app, tuning
  maps/             # periodic snapshots (track-moods.json, etc.)
  specifications/   # deep technical documentation
  reviews/          # audit logs
scripts/            # Python + Bash automation (25 scripts)
logs/               # daily execution logs
```

Each track basename appears in **every** dimension — a file can simultaneously Fictional-Kw-d0dbe915 in `Artist/Fictional-GildedFalcon/`, `Genre/Metal/`, `Mood/Aggressive/`, and `Mood/Energetic/`. Files are copies (not hardlinks) due to external drive (exFAT/NTFS) portability.

## Pipeline Overview

### Phase 1 — Ingestion & Sanitization

Raw downloads (YouTube, streaming rips, CD rips) are placed in `classified/singles/new/`. The pipeline:

1. **Filename sanitization** (`apply_filename_sanitisation.py`, `rename_singles.py`): strips marketing tags ("Official Video", "HD Remaster", YouTube IDs, converter prefixes), transliterates CJK/Hangul/Kana via `unidecode`, removes diacriticals, normalizes hyphens.
2. **Collision handling**: same-size = skip, different-size = append `-dup1`, `-dup2`, etc.

### Phase 2 — Multi-label Classification

`classify_and_clean.py` runs a **keyword-score ensemble classifier**:

- **Artist** — direct keyword match on filename tokens
- **Genre** — keyword score + artist-to-genre boost (artist membership weights genre affinity)
- **Mood** — keyword score (expanded from 23 legacy moods to 66 fine-grained moods in March 2026)

Banned catch-all labels: `Various` (Artist), `Unclassified` (Genre). Any unresolvable track is flagged for manual review.

### Phase 3 — Mood Refinement (Human-in-the-loop)

A browser-based **Vue 3 + Bootstrap 5.3.8** single-page app (`docs/guidelines/moods-checks.html`) renders all 980 tracks with 66 mood checkboxes each. Features:

- Dark theme, responsive grid (auto-fill, minmax 165px columns)
- localStorage persistence with debounced (300ms) autosave
- Progress bar, search filter, reviewed-checkbox workflow
- Export to JSON / Copy as YAML

### Phase 4 — Similarity Ordering (k-NN + Semantic Clustering)

`scripts/_sort_moods.py` orders the 66 moods for UX proximity using:

1. **6D emotional vectors** — each mood mapped to `(valence, arousal, dominance, darkness, longing, inwardness)` in `[-1, 1]^6`
2. **15 semantic clusters** — hand-defined groups (Calm, Cozy, Romantic, Nostalgic, Reflective, etc.)
3. **Nearest-neighbor TSP** within each cluster (Euclidean distance)
4. **Boundary orientation** — cluster tails face adjacent cluster heads for smooth transitions

Emotional arc: Serene → Peaceful → ... → Nostalgic → Sad → Dark → Aggressive → Energetic → Heroic → Joyful → Ecstatic.

### Phase 5 — Filesystem Sync

Corrected mood assignments from the JSON export are synced back to `classified/singles/Mood/*/` — removing old incorrect placements and copying tracks to new mood folders.

## Tech Stack

| Component          | Technology                                                   |
| ------------------ | ------------------------------------------------------------ |
| Automation scripts | Python 3.10+, Bash                                           |
| Classification     | Keyword-score ensemble (Python)                              |
| Mood ordering      | k-NN, Euclidean TSP, 2-opt (Python, `math` stdlib)           |
| Review app         | Vue 3 (CDN), Bootstrap 5.3.8 (CDN SRI), vanilla JS           |
| File operations    | `shutil.copy2`, `os.walk`                                    |
| Backup             | `rsync -aHX`                                                 |
| LLM assistance     | Claude Opus 4.6 (primary), Sonnet 4.6, Haiku 4.5, Gemini 3.1 |
| Editor             | VS Code + GitHub Copilot Agent Mode                          |

## Filesystem Requirements

- External USB drive (Seagate Expansion, NTFS/exFAT formatted)
- Mount point: `/media/<user>/Seagate Expansion Drive1/music/downloaded/`
- Python 3.10+ with `unidecode` for transliteration
- No special database — all state in JSON/YAML files and filesystem structure
- Backup via `rsync` before/after large operations

## Scripts Reference

| Script                   | Purpose                                            |
| ------------------------ | -------------------------------------------------- |
| `classify_and_clean.py`  | Main classification pipeline                       |
| `process_singles_new.py` | Ingest new tracks from `singles/new/`              |
| `rename_singles.py`      | Filename sanitization                              |
| `_sort_moods.py`         | Mood similarity ordering (6D vectors + clustering) |
| `gen_moods_checks.py`    | Generate moods-checks Vue app data                 |
| `slice_tracks.py`        | AuFictional-Kw-1a89bda6 slicing for ambient/focus tracks             |
| `sync_smash_bros.sh`     | Sync Fictional-VolcanicRiver. OST tracks                  |
| `apply_Fictional-TimberTrail_refs.py`     | Apply Fictional-TimberTrailJourneys music references    |

---

<details>
<summary>🇧🇷 Português (pt-BR)</summary>

# Pipeline de Classificação de Biblioteca Musical

Pipeline semi-automatizado para classificação, organização e etiquetagem por humor de uma biblioteca musical pessoal com ~1.080 faixas (980 singles + ~100 faixas de álbuns) em três taxonomias ortogonais: **Artista**, **Gênero** e **Humor/Mood**.

## Visão Geral

### Fase 1 — Ingestão e Sanitização

Downloads brutos são colocados em `classified/singles/new/`. O pipeline sanitiza nomes de arquivo (remove tags de marketing, IDs do YouTube, prefixos de conversores), transliterar texto CJK/Hangul/Kana via `unidecode`, e normaliza hifens.

### Fase 2 — Classificação Multi-rótulo

`classify_and_clean.py` executa um classificador **ensemble de pontuação por palavras-chave**:

- **Artista** — correspondência direta de palavras-chave
- **Gênero** — pontuação por palavras-chave + impulso artista-para-gênero
- **Humor** — 66 moods granulares (expandido de 23 legados em março de 2026)

Rótulos proibidos: `Various` (Artista), `Unclassified` (Gênero).

### Fase 3 — Refinamento de Humor (Humano no Loop)

App navegador **Vue 3 + Bootstrap 5.3.8** com 980 faixas × 66 checkboxes de humor. Persistência localStorage, salvamento automático debounced, exportação JSON/YAML.

### Fase 4 — Ordenação por Similaridade (k-NN + Clusters Semânticos)

Vetores emocionais 6D (valência, excitação, dominância, escuridão, saudade, introspecção) → 15 clusters semânticos → TSP vizinho-mais-próximo dentro de cada cluster.

### Fase 5 — Sincronização do Sistema de Arquivos

Atribuições corrigidas de humor são sincronizadas de volta às pastas `classified/singles/Mood/*/`.

## Stack Tecnológica

Python 3.10+, Bash, Vue 3, Bootstrap 5.3.8, rsync. Assistência LLM: Claude Opus 4.6 (primário), Sonnet 4.6, Haiku 4.5, Gemini 3.1.

</details>

<details>
<summary>🇪🇸 Español (es-ES)</summary>

# Pipeline de Clasificación de Biblioteca Musical

Pipeline semi-automatizado para clasificar, organizar y etiquetar por estado de ánimo una biblioteca musical personal con ~1.080 pistas (980 singles + ~100 pistas de álbumes) en tres taxonomías ortogonales: **Artista**, **Género** y **Estado de Ánimo (Mood)**.

## Resumen

### Fase 1 — Ingesta y Sanitización

Las descargas se depositan en `classified/singles/new/`. El pipeline sanitiza nombres de archivo, transliterar texto CJK/Hangul/Kana y normaliza guiones.

### Fase 2 — Clasificación Multi-etiqueta

Clasificador ensemble basado en puntuación de palabras clave. 66 estados de ánimo granulares.

### Fase 3 — Refinamiento de Estados de Ánimo (Humano en el Bucle)

App Vue 3 + Bootstrap 5.3.8. 980 pistas × 66 checkboxes. Persistencia localStorage.

### Fase 4 — Ordenación por Similitud

Vectores emocionales 6D → 15 clusters semánticos → TSP vecino-más-cercano.

### Fase 5 — Sincronización del Sistema de Archivos

Las asignaciones corregidas se sincronizan con las carpetas `classified/singles/Mood/*/`.

## Stack

Python 3.10+, Bash, Vue 3, Bootstrap 5.3.8, rsync. LLMs: Claude Opus 4.6, Sonnet 4.6, Haiku 4.5, Gemini 3.1.

</details>

<details>
<summary>🇫🇷 Français</summary>

# Pipeline de Classification de Bibliothèque Musicale

Pipeline semi-automatisé pour classifier, organiser et étiqueter par humeur une bibliothèque musicale personnelle de ~1 080 pistes en trois taxonomies orthogonales : **Artiste**, **Genre** et **Humeur (Mood)**.

### Phases

1. **Ingestion** — sanitisation des noms de fichiers, translittération CJK, normalisation
2. **Classification multi-étiquette** — classificateur ensemble par mots-clés (66 humeurs)
3. **Raffinement humain** — app Vue 3 avec 980 pistes × 66 cases à cocher
4. **Ordonnancement par similarité** — vecteurs émotionnels 6D, 15 clusters sémantiques, TSP k-NN
5. **Synchronisation** — corrections appliquées au système de fichiers

### Stack

Python 3.10+, Bash, Vue 3, Bootstrap 5.3.8, rsync. LLMs : Claude Opus 4.6, Sonnet 4.6, Haiku 4.5, Gemini 3.1.

</details>

<details>
<summary>🇩🇪 Deutsch (de-DE)</summary>

# Musikbibliothek-Klassifizierungspipeline

Halbautomatische Pipeline zur Klassifizierung, Organisation und Stimmungskennzeichnung einer persönlichen Musikbibliothek mit ~1.080 Tracks in drei orthogonalen Taxonomien: **Künstler**, **Genre** und **Stimmung (Mood)**.

### Phasen

1. **Aufnahme** — Dateinamen-Bereinigung, CJK-Transliteration, Normalisierung
2. **Multi-Label-Klassifizierung** — Keyword-Score-Ensemble-Klassifizierer (66 Stimmungen)
3. **Menschliche Verfeinerung** — Vue 3-App mit 980 Tracks × 66 Kontrollkästchen
4. **Ähnlichkeitssortierung** — 6D-Emotionsvektoren, 15 semantische Cluster, k-NN-TSP
5. **Dateisystem-Synchronisation** — korrigierte Zuordnungen zurück in die Ordnerstruktur

### Stack

Python 3.10+, Bash, Vue 3, Bootstrap 5.3.8, rsync. LLMs: Claude Opus 4.6, Sonnet 4.6, Haiku 4.5, Gemini 3.1.

</details>

<details>
<summary>🇨🇳 中文 (zh)</summary>

# 音乐库分类管道

半自动化管道，用于对约1,080首个人音乐曲目（980首单曲 + 约100首专辑曲目）进行分类、整理和情绪标注。采用三个正交分类体系：**艺术家**、**流派**和**情绪（Mood）**。

### 阶段

1. **导入** — 文件名清理、CJK音译、规范化
2. **多标签分类** — 关键词评分集成分类器（66种情绪）
3. **人工细化** — Vue 3应用，980首曲目 × 66个情绪复选框
4. **相似度排序** — 6D情感向量、15个语义聚类、k-NN旅行商问题
5. **文件系统同步** — 修正后的分配写回文件夹结构

### 技术栈

Python 3.10+、Bash、Vue 3、Bootstrap 5.3.8、rsync。LLM：Claude Opus 4.6（主力）、Sonnet 4.6、Haiku 4.5、Gemini 3.1。

</details>

---

## License

Personal project — not licensed for redistribution. Music files are personal copies only.
