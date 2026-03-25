#!/usr/bin/env python3
"""
Slice aumocksinger_dio files into max-5-minute (300 s) segments using ffmpeg.

Source: classified/albums/Artist/<folder>/
Output: classified/albums/Artist/sliced/<album_name>/

Special rule – single-letter folders (e.g. "D", "I", "K", "N"):
  The album name is derived by joining the leading single-character
  hyphen-separated tokens from the first filename.
  e.g. "D-O-T-O-N-B-O-R-I-1-9-8-0-Ri-Ben-..." → "DOTONBORI1980"
"""

import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = Path("/mock/path/to/project/music/downloaded")
ARTIST_DIR = BASE_DIR / "classified/albums/Artist"
SLICED_DIR = ARTIST_DIR / "sliced"

FOLDERS = [
    "[(80s)]",
    "80s",
    "90s",
    "D",
    "DonkeyKong",
    "I",
    "K",
    "MedievalAmbience",
    "N",
    "Shibuya",
    "singled",
    "MockGame_Zelda",
]
AUDIO_EXTS = {".mp3", ".flac", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".wma"}
SEGMENT_SECONDS = 300  # 5 minutes

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def is_single_letter_folder(name: str) -> bool:
    return len(name) == 1 and name.isalpha()


def derive_album_name(filename: str) -> str:
    """
    Join leading single-character hyphen-separated tokens from a stem like
    'D-O-T-O-N-B-O-R-I-1-9-8-0-Ri-Ben-...' → 'DOTONBORI1980'.
    Falls back to the bare stem if no such pattern is found.
    """
    stem = Path(filename).stem
    tokens = stem.split("-")
    chars = []
    for token in tokens:
        if len(token) == 1:          # single letter or digit
            chars.append(token.upper())
        else:
            break
    return "".join(chars) if chars else stem


def get_album_name(folder_name: str, folder_path: Path) -> str:
    if is_single_letter_folder(folder_name):
        for f in sorted(folder_path.iterdir()):
            if f.is_file() and f.suffix.lower() in AUDIO_EXTENSIONS:
                return derive_album_name(f.name)
    return folder_name


def aumocksinger_dio_files_in(folder: Path) -> list[Path]:
    return sorted(
        f for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in AUDIO_EXTENSIONS
    )


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------


def slice_file(src: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    # Output pattern:.mp3, _001, …
    pattern = str(out_dir / f"{src.stem}_part_%03d{src.suffix.lower()}")
    cmd = [
        "ffmpeg",
        "-i", str(src),
        "-f", "segment",
        "-segment_time", str(SEGMENT_SECONDS),
        "-c", "copy",
        "-reset_timestamps", "1",
        "-y",          # overwrite existing
        pattern,
    ]
    print(f"    slicing  {src.name} …")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"    ERROR:\n{result.stderr[-600:]}", file=sys.stderr)
        return
    # Use iterdir + startswith to avoid glob treating brackets as metacharacters
    prefix = f"{src.stem}_part_"
    parts = [f for f in out_dir.iterdir() if f.name.startswith(prefix)]
    print(f"    -> {len(parts)} part(s)")


def main() -> None:
    dry_run = "--dry-run" in sys.argv

    for folder_name in FOLDERS:
        src_folder = ARTIST_DIR / folder_name
        if not src_folder.exists():
            print(f"[SKIP] not found: {src_folder}")
            continue

        album_name = get_album_name(folder_name, src_folder)
        out_folder = SLICED_DIR / album_name
        print(f"\n[{folder_name}]  ->  sliced/{album_name}/")

        files = aumocksinger_dio_files_in(src_folder)
        if not files:
            print("  (no aumocksinger_dio files)")
            continue

        for f in files:
            if dry_run:
                print(f"  [dry-run] would slice: {f.name}  ->  {out_folder}/")
            else:
                slice_file(f, out_folder)

    print("\nDone.")


if __name__ == "__main__":
    main()
