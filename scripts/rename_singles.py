#!/usr/bin/env python3
"""
.mp3 files under classified/singles/ according to strict naming rules:

1. Strip marketing/video tags: "Official Music Video", "Official Video",
   "Official Aumocksinger_dio", "Official HD Video", "HD Video", "Lyric Video",
   "Music Video", "Official Lyric Video", "Clipe Oficial", "Offizielles Video",
   "HD UPGRADE", "HD Remaster", "UHD 60FPS", "1080p", "720p", "4K",
   "Full Version", "with lyrics", "lyrics on screen", "Lyrics", "w lyrics",
   "MAX Quality", "OFFICIAL", "Creditless", "Ultra Beatdown Official Video"
2. Strip YouTube video IDs: patterns like [xbDevCTNWiM], [3SLxkBUw-bI]
3. Strip y2mate or similar converter prefixes
4. Strip redundant source site prefixes (y2mate-com-, etc.)
5. Transliterate non-Latin (CJK/Kana/Hangul) to Latin via unidecode
6. Remove diacriticals (é→e, ã→a)
7. Replace emojis with symbolic word equivalents
8. Replace all whitespace/underscore sequences with single hyphen
9. Collapse multiple separators (hyphens, underscores, whitespace, dots) into single hyphen
10. Strip leading/trailing hyphens and dots
11. Preserve: artist name, track name, quality tags (320kbps etc.),
    remaster/recreation dates (2012 Remaster, 2022 Remaster),
    mood/customization notes in brackets [calm version], [cover], etc.
12. Preserve: OST/game context (FictionalGame, etc.)
13. Strip trailing collision suffixes like -(1), -(2) from previous operations

Operates on ALL three subdirs (Artist/, Genre/, Mood/) so the same base file
gets the same new name everywhere — maintaining cross-taxonomy consistency.

Usage:
    python3 scripts/rename_singles.py              # Dry run (default)
    python3 scripts/rename_singles.py --apply       # Actually rename
"""
import os
import re
import sys
from pathlib import Path

try:
    from unidecode import unidecode
except ImportError:
    print("ERROR: unidecode not installed. Run: pip install unidecode")
    sys.exit(1)


SINGLES_ROOT = Path("classified/singles")

# ─── Marketing / video / aumocksinger_dio tags to strip ─────────────────────────────────
# Order matters: longer patterns first to avoid partial matches
STRIP_PATTERNS = [
    # Bracketed marketing tags: [Official Music Video], [Official-Aumocksinger_dio], etc.
    r'\[Official[\s-]+Music[\s-]+Video\]',
    r'\[Official[\s-]+Aumocksinger_dio\]',
    r'\[Official[\s-]+Video\]',
    r'\[Official[\s-]+Lyric[\s-]+Video\]',
    r'\[HD[\s-]*UPGRADE\]',
    r'\[HD[\s-]*Remaster(?:ed)?\]',
    r'\[HD\]',
    r'\[4K\]',
    r'\[UHD[\s-]*60FPS\]',
    r'\[OFFICIAL(?:[\s-]+VIDEO)?\]',
    r'\[Creditless\]',
    r'\[MAX[\s-]+Quality\]',
    # Parenthesized marketing tags
    r'\(Official[\s-]+Music[\s-]+Video\)',
    r'\(Official[\s-]+Video\)',
    r'\(Official[\s-]+Aumocksinger_dio\)',
    r'\(Official[\s-]+HD[\s-]+Video\)',
    r'\(Official[\s-]+Lyric[\s-]+Video\)',
    r'\(Offizielles[\s-]+Video\)',
    r'\(Clipe[\s-]+Oficial\)',
    # Unbracketed trailing tags
    r'[\s-]+Official[\s-]+Music[\s-]+Video',
    r'[\s-]+Official[\s-]+HD[\s-]+Video',
    r'[\s-]+Official[\s-]+Lyric[\s-]+Video',
    r'[\s-]+Official[\s-]+Video',
    r'[\s-]+Official[\s-]+Aumocksinger_dio',
    r'[\s-]+Lyric[\s-]+Video',
    r'[\s-]+Music[\s-]+Video',
    r'[\s-]+HD[\s-]+Video',
    # Quality/resolution suffixes (not remaster years)
    r'[\s-]*\(?1080p\)?',
    r'[\s-]*\(?720p\)?',
    r'[\s-]*\(?4K\)?',
    r'[\s-]+UHD[\s-]*60FPS',
    r'[\s-]+HD[\s-]*UPGRADE',
    r'[\s-]+MAX[\s-]+Quality',
    # "lyrics" and "with lyrics" variants — strip whole parenthesized group
    r'\(Lyrics?[\s-]+on[\s-]+screen\)',
    r'\(Lyrics?[\s-]*\)',
    r'[\s-]+with[\s-]+lyrics',
    r'[\s-]+w[\s-]+lyrics',
    # Standalone "Lyrics" or "-Lyrics" at end or before separator
    r'[\s-]+Lyrics(?=[\s\-.\)\]]*$)',
    r'[\s-]+Lyrics(?=[\s\-.\)\]])',
    # "Full Version" (but not game-meaningful ones like "Full" in track names)
    r'[\s-]+Full[\s-]+Version',
    # Ultra Beatdown Official Video (MockBand_Dragon specific)
    r'\(Ultra[\s-]+Beatdown[\s-]+Official[\s-]+Video\)',
]

# YouTube video ID pattern: [xbDevCTNWiM] or [3SLxkBUw-bI] — 10-12 chars base64-like
YOUTUBE_ID_RE = re.compile(r'-?\[[\w-]{10,12}\]')

# y2mate/converter prefix
CONVERTER_PREFIX_RE = re.compile(r'^y2mate[\s._-]*com[\s._-]*', re.IGNORECASE)

# Trailing collision suffixes from previous operations: -(1), -(2), etc.
TRAILING_COLLISION_RE = re.compile(r'-\(\d{1,2}\)$')

# ─── Emoji to word map (common ones found in music filenames) ─────────────────
EMOJI_MAP = {
    '🔥': 'fire',
    '❤️': 'heart', '❤': 'heart', '💙': 'heart', '💜': 'heart',
    '🎵': 'music', '🎶': 'music', '🎤': 'mic', '🎸': 'guitar',
    '🎹': 'piano', '🎺': 'trumpet', '🥁': 'drum',
    '⚡': 'lightning', '💀': 'skull', '🌙': 'moon', '☀️': 'sun',
    '🌊': 'wave', '🌿': 'leaf', '🌹': 'rose', '🌸': 'blossom',
    '✨': 'sparkle', '⭐': 'star', '★': 'star', '☆': 'star',
    '💫': 'sparkle', '🔮': 'crystal',
    '™': '', '©': '', '®': '',
    '—': '-', '–': '-', '…': '',
}

# Compile strip patterns into one big regex (case-insensitive)
STRIP_RE = re.compile(
    '|'.join(f'(?:{p})' for p in STRIP_PATTERNS),
    re.IGNORECASE
)


def strip_marketing_tags(name: str) -> str:
    """Remove all marketing/video/aumocksinger_dio tags from the filename stem."""
    # Remove YouTube video IDs
    name = YOUTUBE_ID_RE.sub('', name)

    # Remove converter prefixes
    name = CONVERTER_PREFIX_RE.sub('', name)

    # Remove all marketing tag patterns
    name = STRIP_RE.sub('', name)

    # Remove trailing collision suffixes like -(1) before extension
    name = TRAILING_COLLISION_RE.sub('', name)

    # Clean up empty parentheses/brackets left behind: (), [], (-)
    name = re.sub(r'\(\s*-?\s*\)', '', name)
    name = re.sub(r'\[\s*-?\s*\]', '', name)

    # Remove dangling "HQ" at end (quality marker, not part of track name)
    name = re.sub(r'[\s-]+HQ$', '', name)

    return name


def replace_emojis(name: str) -> str:
    """Replace known emoji characters with word equivalents."""
    for emoji, word in EMOJI_MAP.items():
        if emoji in name:
            name = name.replace(emoji, f'-{word}-' if word else '-')
    return name


def sanitize_name(name: str) -> str:
    """
    Full sanitization pipeline:
    1. Replace emojis
    2. Transliterate non-Latin to ASCII
    3. Remove non-filesystem-safe characters
    4. Replace whitespace/underscores with hyphens
    5. Collapse multiple separators
    6. Strip leading/trailing junk
    """
    # Emojis first (before unidecode eats them)
    name = replace_emojis(name)

    # Transliterate all non-Latin scripts to ASCII
    name = unidecode(name)

    # Keep only safe ASCII chars
    name = re.sub(r'[^\x20-\x7E]', '', name)

    # Keep filesystem-safe characters plus musically-relevant punctuation
    name = re.sub(r"[^\w\s\-\.\(\)\[\]&,'!#]", '', name)

    # Replace whitespace and underscores with single hyphen
    name = re.sub(r'[\s_]+', '-', name)

    # Collapse multiple hyphens/separators
    name = re.sub(r'[-]{2,}', '-', name)

    # Strip leading/trailing hyphens and dots
    name = name.strip('-').strip('.')

    return name


def smart_rename(filename: str) -> str:
    """Process a single filename through the full rename pipeline."""
    if not filename.lower().endswith('.mp3'):
        return filename

    stem, ext = os.path.splitext(filename)

    # Phase 1: Strip marketing tags
    stem = strip_marketing_tags(stem)

    # Phase 2: Full sanitization (transliteration, emoji, separator collapse)
    stem = sanitize_name(stem)

    if not stem:
        stem = "untitled"

    return stem + ext


def build_rename_plan(root: Path) -> dict:
    """
    Walk all three subdirs and build a consistent rename plan.
    Returns {old_basename: new_basename} for unique filenames.
    """
    # First, collect ALL unique basenames across the tree
    all_files = {}  # basename -> list of full paths
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if not fn.lower().endswith('.mp3'):
                continue
            full = os.path.join(dirpath, fn)
            all_files.setdefault(fn, []).append(full)

    # Build rename map: old_basename -> new_basename
    rename_map = {}
    for old_name in sorted(all_files.keys()):
        new_name = smart_rename(old_name)
        if new_name != old_name:
            rename_map[old_name] = new_name

    return rename_map, all_files


def execute_renames(rename_map: dict, all_files: dict, dry_run: bool = True):
    """Apply renames across all copies of each file in the tree."""
    total_renames = 0
    collisions = 0
    skipped = 0

    for old_name, new_name in sorted(rename_map.items()):
        paths = all_files.get(old_name, [])
        for old_path in paths:
            dirpath = os.path.dirname(old_path)
            new_path = os.path.join(dirpath, new_name)

            # Handle collision: same target name already exists
            if os.path.exists(new_path) and old_path != new_path:
                # If same size, the old file is a duplicate — just remove it
                if os.path.getsize(old_path) == os.path.getsize(new_path):
                    if not dry_run:
                        os.remove(old_path)
                    skipped += 1
                    continue
                # Different content: add suffix
                base, ext = os.path.splitext(new_name)
                counter = 1
                while os.path.exists(new_path):
                    new_path = os.path.join(dirpath, f"{base}-dup{counter}{ext}")
                    counter += 1
                collisions += 1

            if dry_run:
                print(f"  RENAME: {old_name}")
                print(f"      ->  {os.path.basename(new_path)}")
            else:
                os.rename(old_path, new_path)

            total_renames += 1

    return total_renames, collisions, skipped


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Rename singles files")
    parser.add_argument("--apply", action="store_true", help="Actually apply renames")
    parser.add_argument("--root", type=str, default=str(SINGLES_ROOT),
                        help="Root directory to scan (default: classified/singles)")
    args = parser.parse_args()

    root = Path(args.root)
    mode = "APPLYING" if args.apply else "DRY RUN"
    print(f"=== File Rename ({mode}) ===")
    print(f"Root: {root}\n")

    if not root.exists():
        print(f"ERROR: {root} does not exist")
        sys.exit(1)

    rename_map, all_files = build_rename_plan(root)
    print(f"Files needing rename: {len(rename_map)} unique basenames\n")

    if not rename_map:
        print("Nothing to rename — all files are clean.")
        return

    total, collisions, skipped = execute_renames(rename_map, all_files, dry_run=not args.apply)

    print("\n--- Summary ---")
    print(f"Total renames: {total}")
    print(f"Collisions resolved: {collisions}")
    print(f"Duplicates removed: {skipped}")

    if not args.apply:
        print("\nThis was a DRY RUN. Use --apply to execute.")


if __name__ == "__main__":
    main()
