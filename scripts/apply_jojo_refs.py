#!/usr/bin/env python3
"""
Apply JoJo Reference Rule: scan a taxonomy root for tracks matching
entries in docs/guidelines/data/jojo-refs.yml and copy matches to
Artist/JoJoRef/.

Usage:
    python3 scripts/apply_jojo_refs.py --root classified/singles/sliced [--apply]
    python3 scripts/apply_jojo_refs.py --root classified/singles [--apply]

Without --apply, runs in dry-run mode and just prints matches.
"""
import os
import re
import sys
import shutil
import time
import argparse
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pyyaml is required: pip install pyyaml")

try:
    from unidecode import unidecode
except ImportError:
    sys.exit("unidecode is required: pip install unidecode")

JOJO_REFS_PATH = Path("docs/guidelines/data/jojo-refs.yml")


def normalize(text: str) -> str:
    """Lowercase, transliterate, strip non-alphanum, collapse separators."""
    text = unidecode(text).lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def parse_jojo_refs(yml_path: Path) -> list[tuple[str, str, str]]:
    """
    Parse jojo-refs.yml. Returns list of (character, norm_artist, norm_song).
    Each value is like: "Artist - Song Title (URL)"
    """
    with open(yml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    refs = []
    for character, value in data.items():
        # Strip URL in parentheses at the end
        cleaned = re.sub(r'\(https?://[^)]+\)\s*$', '', value).strip()
        # Split on first " - "
        parts = cleaned.split(' - ', 1)
        if len(parts) == 2:
            artist, song = parts[0].strip(), parts[1].strip()
        else:
            artist, song = cleaned, ""

        norm_artist = normalize(artist)
        norm_song = normalize(song) if song else ""

        # Skip very short tokens (<=2 chars) to avoid false positives
        if len(norm_artist) <= 2:
            norm_artist = ""
        if len(norm_song) <= 3:
            norm_song = ""

        if norm_artist or norm_song:
            refs.append((character, norm_artist, norm_song))

    return refs


def _word_boundary_match(token: str, text: str) -> bool:
    """Check if token appears as a whole-word sequence in text."""
    # Escape the token for regex, then wrap in word boundaries
    pattern = r'\b' + re.escape(token) + r'\b'
    return bool(re.search(pattern, text))


def find_matches(taxonomy_root: Path, refs: list[tuple[str, str, str]]) -> list[tuple[Path, str]]:
    """
    Walk Artist/ subfolders (excluding JoJoRef itself) and find files
    whose normalized stem matches any jojo ref (word-boundary match).
    Returns list of (path, character) tuples.
    """
    artist_dir = taxonomy_root / "Artist"
    if not artist_dir.exists():
        print(f"Artist directory not found: {artist_dir}")
        return []

    matches = []
    seen = set()
    for mp3 in artist_dir.rglob("*.mp3"):
        # Skip files already in JoJoRef
        if "JoJoRef" in mp3.parts:
            continue

        norm_stem = normalize(mp3.stem)
        if not norm_stem:
            continue

        for character, norm_artist, norm_song in refs:
            matched = False
            if norm_artist and _word_boundary_match(norm_artist, norm_stem):
                matched = True
            if norm_song and _word_boundary_match(norm_song, norm_stem):
                matched = True

            if matched and mp3.name not in seen:
                seen.add(mp3.name)
                matches.append((mp3, character))
                break  # One match is enough per file

    return matches


def copy_to_jojoref(matches: list[tuple[Path, str]], taxonomy_root: Path, dry_run: bool):
    """Copy matched files to Artist/JoJoRef/."""
    jojoref_dir = taxonomy_root / "Artist" / "JoJoRef"

    if not dry_run:
        jojoref_dir.mkdir(parents=True, exist_ok=True)

    copied = 0
    skipped = 0
    errors = []

    for src, character in matches:
        dst = jojoref_dir / src.name

        if dst.exists() and os.path.getsize(src) == os.path.getsize(dst):
            skipped += 1
            continue

        # Handle name collision with different content
        base, ext = os.path.splitext(src.name)
        counter = 1
        while dst.exists():
            dst = jojoref_dir / f"{base}-dup{counter}{ext}"
            counter += 1

        if dry_run:
            print(f"  [DRY] {src.name} -> JoJoRef/ (ref: {character})")
            copied += 1
        else:
            for attempt in range(3):
                try:
                    shutil.copy(src, dst)
                    copied += 1
                    break
                except OSError as e:
                    if attempt < 2:
                        time.sleep(2)
                    else:
                        print(f"  ERROR copying {src.name}: {e}")
                        errors.append((src.name, str(e)))

    return copied, skipped, errors


def main():
    parser = argparse.ArgumentParser(description="Apply JoJo Reference Rule")
    parser.add_argument("--root", required=True,
                        help="Taxonomy root (e.g. classified/singles/sliced)")
    parser.add_argument("--apply", action="store_true",
                        help="Actually copy files (default: dry-run)")
    args = parser.parse_args()

    taxonomy_root = Path(args.root)
    if not taxonomy_root.exists():
        sys.exit(f"Root does not exist: {taxonomy_root}")

    if not JOJO_REFS_PATH.exists():
        sys.exit(f"jojo-refs.yml not found: {JOJO_REFS_PATH}")

    print(f"Loading JoJo refs from {JOJO_REFS_PATH}...")
    refs = parse_jojo_refs(JOJO_REFS_PATH)
    print(f"Loaded {len(refs)} reference entries")

    print(f"\nScanning {taxonomy_root}/Artist/ for matches...")
    matches = find_matches(taxonomy_root, refs)
    print(f"Found {len(matches)} matching files")

    if not matches:
        print("No matches found. Nothing to do.")
        return

    print(f"\n{'DRY RUN' if not args.apply else 'APPLYING'}: "
          f"copying {len(matches)} files to Artist/JoJoRef/")
    copied, skipped, errors = copy_to_jojoref(
        matches, taxonomy_root, dry_run=not args.apply)

    print(f"\nCopied: {copied} | Skipped (dup): {skipped} | Errors: {len(errors)}")
    if errors:
        for fn, err in errors:
            print(f"  {fn}: {err}")


if __name__ == "__main__":
    main()
