# Filename Sanitisation Guidelines

## Scope

Rules for standardising raw audio filenames (typically sourced from YouTube
downloads) into clean, metadata-friendly names.  
Implementation lives in `scripts/rename_singles.py` and any future helper in
`scripts/`.

---

## Target filename anatomy

After sanitisation a filename should contain **only**:

```
<ArtistName> - <TrackName>[ (<Year> <Remaster|Recreation>)][ [<observation>]][.<ext>]
```

Optional suffixes allowed:

- Quality tag already embedded in the original: `320kbps`, `FLAC`, etc.
- Remaster / recreation date: `(2012 Remaster)`, `(2022 HD Recreation)`
- Mood / customisation note in square brackets: `[calm version]`, `[cover]`,
  `[instrumental]`, `[authoral]`, `[live]`, `[acoustic]`, `[extended]`

---

## Transformation rules (applied in order)

### 1 — Strip irrelevant metadata tags

Remove any string slice that conveys **publication/platform status** rather than
musical identity. Non-exhaustive reference list:

| Category              | Examples to remove                                                                                                                                                                                 |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Officialness markers  | `Official Video`, `Official Music Video`, `Official Audio`, `Official HD`, `Clipe Oficial`, `Offizielles Video`, `OFFICIAL`, `Official Visualizer`                                                 |
| Clip / video notes    | `Music Video`, `Video Clipe`, `HD Video`, `Lyric Video`, `Lyrics Video`, `Lyrics on screen`, `with lyrics`, `Animated Video`, `Visualizer`, `Creditless`, `NCOP`, `NCED`                           |
| Platform / marketing  | `ft.` / `feat.` attribution fragments that are encoded in brackets or parentheses as filler (keep if contextually meaningful), `Uploaded by`, `Auto-generated`, `Topic`                            |
| Quality/tech metadata | `HD`, `HQ`, `UHD`, `4K`, `1080p`, `720p`, `480p`, `MAX Quality`, `HD Remaster` (keep _year_ + _Remaster_ if present), `HD UPGRADE`, `AAC`, `128kbps` (keep `320kbps`/`FLAC`/`lossless` if present) |
| Full-version markers  | `Full Version`, `Full Album`, `Full OST` (keep if literally the only description)                                                                                                                  |
| Playlist numbering    | `[(Playlist-90)]`, `[(Playlist-\d+)]`, `#\d+` at the end                                                                                                                                           |
| YouTube video IDs     | `[<10-12 char base64>]` at the end                                                                                                                                                                 |
| Converter prefixes    | `y2mate-com-`, `ytmp3-`, `snappea-`, and similar                                                                                                                                                   |
| Collision suffixes    | `-(1)`, `-(2)`, ` (1)`, ` (2)` appended by prior rename ops                                                                                                                                        |
| Duration hints        | `[1 Hour]`, `[2 Hours]`, `(10 Hours Loop)`, `1-Hour`, `2-Hour`                                                                                                                                     |

### 2 — Whitespace normalisation

- Replace every whitespace character (` `, `\t`, `\r`, `\n`) with `-`.
- Then collapse any run of two or more separator characters
  `[-_\s\t\r.,—–]{2,}` down to a **single instance of the first character
  found** in that run.

### 3 — Diacritics removal

Strip combining diacritical marks (Unicode category `Mn`) after applying
`unicodedata.normalize('NFD', …)` so that accented Latin characters are
reduced to their ASCII base letter.

Examples: `Café` → `Cafe`, `Ñoño` → `Nono`, `Björk` → `Bjork`

### 4 — Non-Latin script transliteration

Replace characters from non-Latin scripts with Latin-alphabet equivalents using
the standard romanisation conventions for each script:

| Script                  | Convention                                         |
| ----------------------- | -------------------------------------------------- |
| Japanese (kana + kanji) | Hepburn rōmaji                                     |
| Chinese (hanzi)         | Pinyin (without tone marks, after diacritics step) |
| Korean (hangul)         | Revised Romanisation of Korean                     |
| Cyrillic                | ISO 9 (or BGN/PCGN for Russian)                    |
| Arabic                  | ISO 233 simplified                                 |
| Greek                   | ISO 843                                            |
| Hebrew                  | ISO 259                                            |
| Other                   | Best-effort per `Unidecode` library fallback       |

Recommended library: `unidecode` (PyPI) as the catch-all fallback after
script-specific pre-processing.

### 5 — Emoji replacement

Replace emoji codepoints with a hyphen-delimited English word (or short phrase)
that represents the emoji's standard meaning.

Examples:

| Emoji   | Replacement |
| ------- | ----------- |
| 🔥      | `fire`      |
| 🎵 / 🎶 | `music`     |
| ❤️      | `heart`     |
| 🌙      | `moon`      |
| 🌊      | `wave`      |
| ✨      | `sparkle`   |
| 👑      | `crown`     |
| 🎮      | `gamepad`   |
| 🗡️      | `sword`     |
| 💀      | `skull`     |

For any emoji not listed above, derive the word from the official Unicode CLDR
short name (strip colons, replace spaces with `-`).

Recommended library: `emoji` (PyPI) — `emoji.demojize()` + strip the `:`
delimiters.

### 6 — Final trim

- Strip leading and trailing separators (`-`, `_`, `.`).
- Ensure the extension is lowercase.

---

## What to preserve

| Element                                                                                           | Notes                                           |
| ------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| Artist name                                                                                       | Primary identity — must not be stripped         |
| Track / album title                                                                               | Primary identity — must not be stripped         |
| `320kbps` / `FLAC` / `lossless`                                                                   | Meaningful quality tag                          |
| `(<Year> Remaster)` / `(<Year> Recreation)`                                                       | Historical/editorial context                    |
| `[calm version]`, `[cover]`, `[instrumental]`, `[live]`, `[acoustic]`, `[extended]`, `[authoral]` | Mood / customisation observations               |
| OST / game context in the title                                                                   | e.g. `Super-Smash-Bros`, `FictionalBand_6146d0`, `FictionalBand_c7bd66` |

---

## Script conventions

- Every renaming script must live under `scripts/`.
- Scripts must support a `--dry-run` flag that prints planned renames without
  applying them.
- Scripts must log actual renames to `logs/<YYYYMMDD>/rename-<script>.log`.
- No file must be silently overwritten — detect collisions and suffix `_v2`,
  `_v3`, etc.
