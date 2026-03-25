#!/usr/bin/env python3
"""
apply_filename_sanitisation.py

Applies the filename sanitisation guidelines from
docs/guidelines/filename-sanitisation.md to every aumocksinger_dio file under classified/.

Exclusions:
  - classified/singles/new/**  — left untouched per user instruction.

Supports --dry-run to preview without applying.
"""

import os
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

import emoji
from unidecode import unidecode

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BASE = Path("/mock/path/to/project/music/downloaded")
CLASSIFIED = BASE / "classified"
EXCLUDE_PREFIXES = [
    CLASSIFIED / "singles" / "new",
]
AUDIO_EXTS = {".mp3", ".flac", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".wma"}

TODAY = datetime.now().strftime("%Y%m%d")
LOG_DIR = BASE / "logs" / TODAY
LOG_FILE = LOG_DIR / "rename-apply_filename_sanitisation.log"

DRY_RUN = "--dry-run" in sys.argv

# ---------------------------------------------------------------------------
# 0.  Join single-char-dash sequences  (D-O-T-O-N → DOTON)
# ---------------------------------------------------------------------------

def join_single_char_dashes(name: str) -> str:
    """
    Collapse runs of single-char tokens separated by hyphens.
    D-O-T-O-N-B-O-R-I-1-9-8-0 → DOTONBORI1980

    Walk hyphen-split tokens and greedily merge consecutive single-char tokens.
    """
    tokens = name.split("-")
    result: list[str] = []
    buf: list[str] = []

    def flush_buf():
        if buf:
            result.append("".join(buf))
            buf.clear()

    for tok in tokens:
        if len(tok) == 1 and tok.isalnum():
            buf.append(tok)
        else:
            flush_buf()
            result.append(tok)

    flush_buf()
    return "-".join(result)


def join_single_char_dots(name: str) -> str:
    """
    Collapse runs of 4+ single-char tokens separated by dots, per hyphen-segment.
    B.R.U.N.O → BRUNO   C.h.u.c.k-B.e.r.r.y → Chuck-Berry
    MockBand_REM. stays (only 3 chars).
    """
    segments = name.split("-")
    processed = []
    for segment in segments:
        tokens = segment.split(".")
        result_parts: list[str] = []
        buf: list[str] = []

        def flush_dot_buf():
            if len(buf) >= 4:
                result_parts.append("".join(buf))
            elif buf:
                result_parts.append(".".join(buf))
            buf.clear()

        for tok in tokens:
            if len(tok) == 1 and tok.isalnum():
                buf.append(tok)
            else:
                flush_dot_buf()
                result_parts.append(tok)
        flush_dot_buf()
        processed.append(".".join(result_parts))
    return "-".join(processed)


# ---------------------------------------------------------------------------
# 1.  Strip irrelevant metadata tags
# ---------------------------------------------------------------------------

# Patterns that should be removed entirely (case-insensitive).
_GARBAGE_LITERALS = [
    # Officialness
    "Official Music Video", "Official Video", "Official Aumocksinger_dio",
    "Official HD", "Clipe Oficial", "Offizielles Video", "OFFICIAL",
    "Official Visualizer",
    # Clip / video
    "Music Video", "Video Clipe", "HD Video", "Lyric Video",
    "Lyrics Video", "Lyrics on screen", "with lyrics",
    "Animated Video", "Visualizer", "Creditless", "NCOP", "NCED",
    # Platform / marketing
    "Uploaded by", "Auto-generated", "Topic",
    # Quality / tech  (keep 320kbps / FLAC / lossless)
    "MAX Quality", "HD UPGRADE", "UHD 60FPS",
    # Full-version markers (only when in brackets/parens)
    "Full Version",
    # Duration hints
    "10 Hours Loop",
]

_GARBAGE_REGEXES: list[re.Pattern] = [
    # Quality / resolution tags
    re.compile(r"[-_\s](?:4K|UHD|1080p|720p|480p|HQ|HD)(?=[-_\s.\]\)]|$)", re.I),
    # YouTube video IDs at the end:  -[xbDevCTNWiM] or [xbDevCTNWiM]
    re.compile(r"[-_\s]?\[[\w_-]{10,12}\](?=\.[a-z0-9]+$|$)"),
    # Converter prefixes
    re.compile(r"^(?:y2mate[_-]com[_-]|ytmp3[_-]|snappea[_-])", re.I),
    # Collision suffixes  -(1)  (2)  — only 1-2 digit numbers to avoid eating years
    re.compile(r"[-_\s]?\(\d{1,2}\)(?=\.[a-z0-9]+$|$)"),
    # Playlist numbering  [(Playlist-90)]  [(Playlist-\d+)]
    re.compile(r"\[\(Playlist[-_\s]?\d+\)\]", re.I),
    # Standalone playlist numbering  #123 at end
    re.compile(r"\s*#\d+(?=\.[a-z0-9]+$|$)"),
    # Duration hints: [1 Hour], [2 Hours], [1-Hour], (10 Hours Loop)
    re.compile(r"[\[\(]\d+[-\s]?Hours?\s*(?:Loop)?[\]\)]", re.I),
    # Duration hints:  1-Hour  2-Hour  that appear as standalone token
    re.compile(r"(?<=[-_\s])\d+-Hours?(?=[-_\s]|$)", re.I),
    # "Full Album" in brackets (with spaces or hyphens)
    re.compile(r"[\[\(]Full[\s-]+Album[\]\)]", re.I),
    # Standalone "Full Album" (with spaces or hyphens)
    re.compile(r"[-_\s]Full[-_\s]Album(?=[-_\s]|$)", re.I),
    # "Full OST" in brackets
    re.compile(r"[\[\(]Full\s+OST[\]\)]", re.I),
    # DVD at start
    re.compile(r"^DVD[-_\s]+(?:COMPLETO[-_\s]+)?", re.I),
]


def strip_tags(name: str) -> str:
    # Literal garbage (case-insensitive, word-boundary-ish)
    for lit in _GARBAGE_LITERALS:
        pat = re.compile(re.escape(lit), re.I)
        name = pat.sub("", name)
    # Regex garbage
    for rx in _GARBAGE_REGEXES:
        name = rx.sub("", name)
    # Clean up empty brackets/parens left after stripping
    name = re.sub(r"\(\s*\)", "", name)
    name = re.sub(r"\[\s*\]", "", name)
    name = re.sub(r"\[\(\s*\)\]", "", name)
    return name


# ---------------------------------------------------------------------------
# 2.  Whitespace normalisation
# ---------------------------------------------------------------------------

def normalise_whitespace(name: str) -> str:
    # All whitespace → hyphen
    name = re.sub(r"[\s\t\r\n]+", "-", name)
    # Collapse same-char separator runs:  -- → -   .. → .   __ → _
    name = re.sub(r"([-_.\u2014\u2013])\1+", r"\1", name)
    # Collapse mixed runs of hyphens/underscores/dashes (but NOT periods)
    name = re.sub(r"[-_\u2014\u2013]{2,}", lambda m: m.group(0)[0], name)
    return name


# ---------------------------------------------------------------------------
# 3.  Diacritics removal
# ---------------------------------------------------------------------------

def strip_diacritics(name: str) -> str:
    nfkd = unicodedata.normalize("NFD", name)
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")


# ---------------------------------------------------------------------------
# 4.  Non-Latin transliteration  (unidecode catch-all)
# ---------------------------------------------------------------------------

def transliterate(name: str) -> str:
    # Only transliterate characters that are NOT basic latin/ascii-printable
    out = []
    for ch in name:
        if ord(ch) < 128:
            out.append(ch)
        else:
            out.append(unidecode(ch))
    return "".join(out)


# ---------------------------------------------------------------------------
# 5.  Emoji replacement
# ---------------------------------------------------------------------------

def replace_emojis(name: str) -> str:
    demojized = emoji.demojize(name, delimiters=("", ""))
    # demojize turns 🔥 into "fire", 🎵 into "musical_note", etc.
    # Clean underscores from the replacement words → hyphens
    return demojized.replace("_", "-")


# ---------------------------------------------------------------------------
# 6.  Final trim
# ---------------------------------------------------------------------------

def final_trim(name: str, ext: str) -> str:
    name = name.strip("-_.  ")
    ext = ext.lower()
    return name + ext


# ---------------------------------------------------------------------------
# Master pipeline
# ---------------------------------------------------------------------------

def sanitise(filename: str) -> str:
    stem = Path(filename).stem
    ext = Path(filename).suffix

    s = stem
    s = join_single_char_dashes(s)   # Step 0a
    s = join_single_char_dots(s)     # Step 0b
    s = strip_tags(s)                # Step 1
    s = normalise_whitespace(s)      # Step 2
    s = strip_diacritics(s)          # Step 3
    s = transliterate(s)            # Step 4
    s = replace_emojis(s)           # Step 5
    s = final_trim(s, ext)          # Step 6

    return s


# ---------------------------------------------------------------------------
# Collision-safe rename
# ---------------------------------------------------------------------------

def safe_target(target: Path) -> Path:
    if not target.exists():
        return target
    stem = target.stem
    ext = target.suffix
    parent = target.parent
    v = 2
    while True:
        candidate = parent / f"{stem}_v{v}{ext}"
        if not candidate.exists():
            return candidate
        v += 1


# ---------------------------------------------------------------------------
# Walk & rename
# ---------------------------------------------------------------------------

def is_excluded(path: Path) -> bool:
    for prefix in EXCLUDE_PREFIXES:
        try:
            path.relative_to(prefix)
            return True
        except ValueError:
            pass
    return False


def main() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_lines: list[str] = []
    rename_count = 0
    skip_count = 0

    for dirpath, _dirnames, filenames in os.walk(CLASSIFIED):
        dp = Path(dirpath)
        if is_excluded(dp):
            continue
        for fname in sorted(filenames):
            fpath = dp / fname
            if fpath.suffix.lower() not in AUDIO_EXTS:
                continue

            new_name = sanitise(fname)
            if new_name == fname:
                skip_count += 1
                continue

            target = safe_target(dp / new_name)
            line = f"{fpath}  ->  {target}"

            if DRY_RUN:
                print(f"[dry-run] {line}")
            else:
                fpath.rename(target)
                print(f"[rename]  {line}")

            log_lines.append(line)
            rename_count += 1

    # Write log
    with open(LOG_FILE, "w") as lf:
        lf.write(f"# apply_filename_sanitisation  {datetime.now().isoformat()}\n")
        lf.write(f"# mode: {'dry-run' if DRY_RUN else 'live'}\n")
        lf.write(f"# renamed: {rename_count}  unchanged: {skip_count}\n\n")
        lf.write("\n".join(log_lines) + "\n")

    print(f"\n{'[DRY-RUN] ' if DRY_RUN else ''}Done.  renamed={rename_count}  unchanged={skip_count}")
    print(f"Log written to {LOG_FILE}")


if __name__ == "__main__":
    main()
