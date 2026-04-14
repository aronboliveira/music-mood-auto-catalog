#!/usr/bin/env python3
"""
Fill all empty (and under-filled) folders under classified/singles/Genre,
classified/singles/Mood, classified/singles/new, and classified/singles/new-sliced
with zero-byte faker MP3 files named Fictional-Track-{8hex}.mp3.

Naming is deterministic via MD5(artist + "_" + category + "_" + index) so
re-running produces the same filenames.

Usage:
    python3 scripts/fill_classified.py           # dry run
    python3 scripts/fill_classified.py --apply   # create files
"""

import argparse
import hashlib
import os
import sys
from pathlib import Path

CLASSIFIED_ROOT = Path("classified")

# ── Fake artist pool (all Fictional-*) for cross-reference tagging in filenames
FAKE_ARTISTS: list[str] = [
    "Fictional-AmberCastle", "Fictional-AzureBeacon", "Fictional-BlazingCastle",
    "Fictional-BrassBeacon", "Fictional-CobaltCanyon", "Fictional-CoralArrow",
    "Fictional-CrimsonBloom", "Fictional-CrystalArrow", "Fictional-DuskBloom",
    "Fictional-EmeraldBell", "Fictional-FrozenBell", "Fictional-GildedCastle",
    "Fictional-GlassBeacon", "Fictional-GoldenCanyon", "Fictional-GraniteBeacon",
    "Fictional-HollowCanyon", "Fictional-IndigoArrow", "Fictional-IronBloom",
    "Fictional-JadeBloom", "Fictional-LunarBell", "Fictional-MidnightBell",
    "Fictional-MistyCastle", "Fictional-NeonBeacon", "Fictional-ObsidianCanyon",
    "Fictional-OpalArrow", "Fictional-PhantomCanyon", "Fictional-QuartzArrow",
    "Fictional-RustyBloom", "Fictional-ScarletBloom", "Fictional-SilverBell",
    "Fictional-SolarBeacon", "Fictional-SpectralCastle", "Fictional-SterlingBeacon",
    "Fictional-StormCanyon", "Fictional-ThistleArrow", "Fictional-ThunderCanyon",
    "Fictional-TimberArrow", "Fictional-TwilightBloom", "Fictional-VioletBell",
    "Fictional-ZincBell",
]

# Target fill counts per zone
GENRE_TARGET: int = 5   # ensure at least this many tracks per genre folder
MOOD_TARGET: int = 5    # ensure at least this many tracks per mood folder
NEW_COUNT: int = 8      # files to place in singles/new
NEW_SLICED_COUNT: int = 6  # files to place in singles/new-sliced
SLICED_TARGET: int = 3  # min per existing genre/mood for sliced


def _hash8(seed: str) -> str:
    """Return first 8 hex chars of MD5(seed)."""
    return hashlib.md5(seed.encode("utf-8")).hexdigest()[:8]


def fictional_track_name(artist: str, category: str, index: int) -> str:
    """Generate a deterministic Fictional-Track filename."""
    seed = f"{artist}_{category}_{index}"
    return f"Fictional-Track-{_hash8(seed)}.mp3"


def fill_folder(
    folder: Path,
    category: str,
    target: int,
    dry_run: bool,
    created_total: list[int],
) -> None:
    """Ensure `folder` contains at least `target` .mp3 files."""
    existing: set[str] = {
        f.name for f in folder.iterdir() if f.suffix == ".mp3"
    } if folder.exists() else set()

    needed = max(0, target - len(existing))
    if needed == 0:
        return

    folder.mkdir(parents=True, exist_ok=True)
    artist_cycle = len(FAKE_ARTISTS)

    generated = 0
    idx = 0
    while generated < needed:
        artist = FAKE_ARTISTS[idx % artist_cycle]
        name = fictional_track_name(artist, category, idx)
        # Avoid collisions with existing names
        if name not in existing:
            fpath = folder / name
            if dry_run:
                print(f"  WOULD CREATE: {fpath}")
            else:
                fpath.touch()
            existing.add(name)
            generated += 1
            created_total[0] += 1
        idx += 1


def fill_sliced(
    source_folder: Path,
    sliced_folder: Path,
    category: str,
    target: int,
    dry_run: bool,
    created_total: list[int],
) -> None:
    """Create _part_001 sliced variants of tracks in source_folder."""
    if not source_folder.exists():
        return

    sliced_folder.mkdir(parents=True, exist_ok=True)
    existing: set[str] = {
        f.name for f in sliced_folder.iterdir() if f.suffix == ".mp3"
    } if sliced_folder.exists() else set()

    sources: list[str] = [
        f.stem for f in source_folder.iterdir() if f.suffix == ".mp3"
    ][:target]

    for stem in sources:
        sliced_name = f"{stem}_part_001.mp3"
        if sliced_name not in existing:
            fpath = sliced_folder / sliced_name
            if dry_run:
                print(f"  WOULD CREATE: {fpath}")
            else:
                fpath.touch()
            existing.add(sliced_name)
            created_total[0] += 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Fill classified/ with faker tracks")
    parser.add_argument("--apply", action="store_true", help="Actually create files")
    parser.add_argument(
        "--root", default=str(CLASSIFIED_ROOT),
        help="Root directory (default: classified/)"
    )
    args = parser.parse_args()

    root = Path(args.root)
    dry_run = not args.apply
    mode = "DRY RUN" if dry_run else "APPLYING"
    print(f"=== Fill Classified ({mode}) ===\nRoot: {root}\n")

    if not root.exists():
        print(f"ERROR: {root} does not exist")
        sys.exit(1)

    created: list[int] = [0]

    # ── singles/Genre ───────────────────────────────────────────────
    genre_root = root / "singles" / "Genre"
    if genre_root.exists():
        print("── singles/Genre")
        for genre_dir in sorted(genre_root.iterdir()):
            if genre_dir.is_dir():
                fill_folder(genre_dir, genre_dir.name, GENRE_TARGET, dry_run, created)
        print()

    # ── singles/Mood ─────────────────────────────────────────────────
    mood_root = root / "singles" / "Mood"
    if mood_root.exists():
        print("── singles/Mood")
        for mood_dir in sorted(mood_root.iterdir()):
            if mood_dir.is_dir():
                fill_folder(mood_dir, mood_dir.name, MOOD_TARGET, dry_run, created)
        print()

    # ── singles/new (simulate incoming batch) ─────────────────────
    new_dir = root / "singles" / "new"
    print("── singles/new (incoming batch simulation)")
    fill_folder(new_dir, "new-batch", NEW_COUNT, dry_run, created)
    print()

    # ── singles/new-sliced ────────────────────────────────────────
    new_sliced_dir = root / "singles" / "new-sliced"
    print("── singles/new-sliced")
    fill_folder(new_sliced_dir, "new-sliced-batch", NEW_SLICED_COUNT, dry_run, created)
    print()

    # ── singles/sliced (cross-reference from Genre samples) ──────
    sliced_root = root / "singles" / "sliced"
    print("── singles/sliced (genre-sourced slices)")
    for genre_dir in sorted(genre_root.iterdir()):
        if genre_dir.is_dir():
            sliced_genre_dir = sliced_root / genre_dir.name
            fill_sliced(genre_dir, sliced_genre_dir, genre_dir.name,
                        SLICED_TARGET, dry_run, created)
    print()

    print(f"--- Summary ---")
    print(f"{'Created' if not dry_run else 'Would create'}: {created[0]} files")
    if dry_run:
        print("\nDRY RUN — use --apply to create.")


if __name__ == "__main__":
    main()
