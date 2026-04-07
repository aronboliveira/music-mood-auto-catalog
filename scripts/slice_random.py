#!/usr/bin/env python3
"""
slice_random.py

Re-slices auFictional-Kw-27b20503 from specified source folders.
Segment length is randomised between SEG_MIN and SEG_MAX seconds (inclusive).
The LAST segment always captures all remaining auFictional-Kw-27b20503 so no seconds are ever lost.

ffmpeg is invoked directly as a CLI command via subprocess.run().

Output: classified/singles/new/sliced-3/<album_name>/
Naming: full filename-sanitisation guidelines applied to every output stem.

Usage:
    python scripts/slice_random.py [--dry-run]
"""

import random
import re
import subprocess
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

import emoji
from unidecode import unidecode

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BASE = Path("/media/aronboliveira/Seagate Expansion Drive1/music/downloaded")
ARTIST_DIR = BASE / "classified/albums/Artist"
OUT_ROOT = BASE / "classified/singles/new/sliced-3"

FOLDERS = [
    "[(80s)]",
    "80s",
    "90s",
    "D",
    "Fictional-SapphireOracle",
    "I",
    "K",
    "MedievalAmbience",
    "N",
    "Shibuya",
    "singled",
    "Fictional-CrystalBell",
]

AUDIO_EXTS = {".mp3", ".flac", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".wma"}

SEG_MIN = 120   # 2 minutes in seconds
SEG_MAX = 240   # 4 minutes in seconds

DRY_RUN = "--dry-run" in sys.argv

TODAY = datetime.now().strftime("%Y%m%d")
LOG_DIR = BASE / "logs" / TODAY
LOG_FILE = LOG_DIR / "slice_random.log"


# ---------------------------------------------------------------------------
# Album-name derivation  (mirrors slice_tracks.py)
# ---------------------------------------------------------------------------

def _is_single_letter_folder(name: str) -> bool:
    return len(name) == 1 and name.isalpha()


def _derive_name_from_file(filename: str) -> str:
    """Join leading single-char tokens from a filename stem."""
    tokens = Path(filename).stem.split("-")
    chars = []
    for tok in tokens:
        if len(tok) == 1:
            chars.append(tok.upper())
        else:
            break
    return "".join(chars) if chars else Path(filename).stem


def album_name_for(folder_name: str, folder_path: Path) -> str:
    if _is_single_letter_folder(folder_name):
        for f in sorted(folder_path.iterdir()):
            if f.is_file() and f.suffix.lower() in AUDIO_EXTS:
                return _derive_name_from_file(f.name)
    return folder_name


# ---------------------------------------------------------------------------
# Filename sanitisation  (same rules as apply_filename_sanitisation.py)
# ---------------------------------------------------------------------------

def _join_dashes(name: str) -> str:
    """D-O-T-O-N → DOTON"""
    tokens = name.split("-")
    result: list[str] = []
    buf: list[str] = []
    for tok in tokens:
        if len(tok) == 1 and tok.isalnum():
            buf.append(tok)
        else:
            if buf:
                result.append("".join(buf))
                buf.clear()
            result.append(tok)
    if buf:
        result.append("".join(buf))
    return "-".join(result)


def _join_dots(name: str) -> str:
    """B.R.U.N.O → BRUNO (runs ≥ 4), Fictional-MarbleRose left alone (run = 3)."""
    parts = name.split("-")
    out_parts = []
    for part in parts:
        tokens = part.split(".")
        segment_out: list[str] = []
        run: list[str] = []
        for tok in tokens:
            if len(tok) == 1 and tok.isalnum():
                run.append(tok)
            else:
                if len(run) >= 4:
                    segment_out.append("".join(run))
                elif run:
                    segment_out.append(".".join(run))
                run = []
                segment_out.append(tok)
        if len(run) >= 4:
            segment_out.append("".join(run))
        elif run:
            segment_out.append(".".join(run))
        out_parts.append(".".join(segment_out))
    return "-".join(out_parts)


_GARBAGE_LITERALS = [
    "Official Music Video", "Official Video", "Official AuFictional-Kw-27b20503",
    "Official HD", "Clipe Oficial", "Offizielles Video", "OFFICIAL",
    "Official Visualizer",
    "Music Video", "Video Clipe", "HD Video", "Lyric Video",
    "Lyrics Video", "Lyrics on screen", "with lyrics",
    "Animated Video", "Visualizer", "Creditless", "NCOP", "NCED",
    "Uploaded by", "Auto-generated", "Topic",
    "MAX Quality", "HD UPGRADE", "UHD 60FPS",
    "Full Version",
    "10 Hours Loop",
]

_GARBAGE_RE: list[re.Pattern] = [
    re.compile(r"[-_\s](?:4K|UHD|1080p|720p|480p|HQ|HD)(?=[-_\s.\]\)]|$)", re.I),
    re.compile(r"[-_\s]?\[[\w_-]{10,12}\](?=\.[a-z0-9]+$|$)"),
    re.compile(r"^(?:y2mate[_-]com[_-]|ytmp3[_-]|snappea[_-])", re.I),
    re.compile(r"[-_\s]?\(\d{1,2}\)(?=\.[a-z0-9]+$|$)"),
    re.compile(r"\[\(Playlist[-_\s]?\d+\)\]", re.I),
    re.compile(r"\s*#\d+(?=\.[a-z0-9]+$|$)"),
    re.compile(r"[\[\(]\d+[-\s]?Hours?\s*(?:Loop)?[\]\)]", re.I),
    re.compile(r"(?<=[-_\s])\d+-Hours?(?=[-_\s]|$)", re.I),
    re.compile(r"[\[\(]Full[\s-]+Album[\]\)]", re.I),
    re.compile(r"[-_\s]Full[-_\s]Album(?=[-_\s]|$)", re.I),
    re.compile(r"[\[\(]Full\s+OST[\]\)]", re.I),
    re.compile(r"^DVD[-_\s]+(?:COMPLETO[-_\s]+)?", re.I),
]


def _strip_tags(name: str) -> str:
    for lit in _GARBAGE_LITERALS:
        name = re.compile(re.escape(lit), re.I).sub("", name)
    for rx in _GARBAGE_RE:
        name = rx.sub("", name)
    name = re.sub(r"\(\s*\)", "", name)
    name = re.sub(r"\[\s*\]", "", name)
    name = re.sub(r"\[\(\s*\)\]", "", name)
    return name


def _normalise_ws(name: str) -> str:
    name = re.sub(r"[\s\t\r\n]+", "-", name)
    name = re.sub(r"([-_.\u2014\u2013])\1+", r"\1", name)
    name = re.sub(r"[-_\u2014\u2013]{2,}", lambda m: m.group(0)[0], name)
    return name


def _strip_diacritics(name: str) -> str:
    nfkd = unicodedata.normalize("NFD", name)
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")


def _transliterate(name: str) -> str:
    return "".join(ch if ord(ch) < 128 else unidecode(ch) for ch in name)


def _replace_emojis(name: str) -> str:
    return emoji.demojize(name, delimiters=("", "")).replace("_", "-")


def sanitise_stem(stem: str) -> str:
    s = _join_dashes(stem)
    s = _join_dots(s)
    s = _strip_tags(s)
    s = _normalise_ws(s)
    s = _strip_diacritics(s)
    s = _transliterate(s)
    s = _replace_emojis(s)
    return s.strip("-_. ")


# ---------------------------------------------------------------------------
# ffprobe: get total duration via CLI
# ---------------------------------------------------------------------------

def get_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True, text=True,
    )
    return float(result.stdout.strip())


# ---------------------------------------------------------------------------
# Segment plan: randomised lengths, last always catches remainder
# ---------------------------------------------------------------------------

def plan_segments(total: float) -> list[tuple[float, float | None]]:
    """
    Returns [(start, duration), ...] where the last item has duration=None
    meaning 'go to end of file', ensuring zero auFictional-Kw-27b20503 loss.
    """
    segments: list[tuple[float, float | None]] = []
    pos = 0.0
    while pos < total:
        remaining = total - pos
        if remaining <= SEG_MAX:
            segments.append((pos, None))
            break
        dur = float(random.randint(SEG_MIN, SEG_MAX))
        segments.append((pos, dur))
        pos += dur
    return segments


# ---------------------------------------------------------------------------
# Slice a single file via ffmpeg CLI
# ---------------------------------------------------------------------------

def slice_file(src: Path, out_dir: Path, clean_stem: str, ext: str) -> list[str]:
    """
    Calls ffmpeg (CLI) for each segment.
    Returns list of ffmpeg command strings (for logging errors).
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    total = get_duration(src)
    segs = plan_segments(total)
    errors: list[str] = []

    for i, (start, dur) in enumerate(segs):
        part_name = f"{clean_stem}_part_{i:03d}{ext}"
        out_path = out_dir / part_name

        # Build ffmpeg CLI command
        # -ss before -i  → fast input seeking (no decode overhead)
        # -c copy        → no re-encode, preserve quality
        cmd = ["ffmpeg", "-ss", f"{start:.3f}"]
        if dur is not None:
            cmd += ["-t", f"{dur:.3f}"]
        cmd += ["-i", str(src), "-c", "copy", "-y", str(out_path)]

        cmd_str = " ".join(
            f'"{c}"' if (" " in c or "[" in c or "(" in c) else c
            for c in cmd
        )

        if DRY_RUN:
            print(f"    {cmd_str}")
        else:
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0:
                msg = f"ERROR part {i:03d}: {src.name}\n{res.stderr[-500:]}"
                print(f"    {msg}")
                errors.append(cmd_str)
            else:
                print(f"    -> {part_name}")

    if not DRY_RUN:
        print(f"    {len(segs)} part(s)  |  total={total:.1f}s")
    return errors


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    all_errors: list[str] = []
    random.seed()  # fresh seed each run so durations truly vary

    for folder_name in FOLDERS:
        src_folder = ARTIST_DIR / folder_name
        if not src_folder.exists():
            print(f"[SKIP – not found] {src_folder}")
            continue

        album = album_name_for(folder_name, src_folder)
        out_dir = OUT_ROOT / album
        print(f"\n[{folder_name}]  →  sliced-3/{album}/")

        for f in sorted(src_folder.iterdir()):
            if not f.is_file() or f.suffix.lower() not in AUDIO_EXTS:
                continue

            clean = sanitise_stem(f.stem)
            ext = f.suffix.lower()
            print(f"  {f.name}  →  {clean}*{ext}")

            errors = slice_file(f, out_dir, clean, ext)
            all_errors.extend(errors)

    # Write log
    with open(LOG_FILE, "a") as lf:
        lf.write(f"\n# slice_random  {datetime.now().isoformat()}\n")
        lf.write(f"# mode: {'dry-run' if DRY_RUN else 'live'}\n")
        if all_errors:
            lf.write("# ERRORS:\n")
            for e in all_errors:
                lf.write(e + "\n")
        else:
            lf.write("# result: OK – no errors\n")

    if all_errors:
        print(f"\n{'[DRY-RUN] ' if DRY_RUN else ''}Done with {len(all_errors)} error(s). See {LOG_FILE}")
    else:
        print(f"\n{'[DRY-RUN] ' if DRY_RUN else ''}Done – no errors. Log: {LOG_FILE}")


if __name__ == "__main__":
    main()
