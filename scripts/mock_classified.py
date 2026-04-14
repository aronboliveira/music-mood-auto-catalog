#!/usr/bin/env python3
"""
mock_classified.py
==================
Populate the classified/ directory tree with fictional placeholder tracks
to demonstrate the classification system's folder structure.

Each single appears in all three dimensions: Artist, Genre, and Mood.
Albums appear under Artist only.

All names use the Fictional-* prefix — no real artist/track names.

Usage:
    python scripts/mock_classified.py           # create tree + faker tracks
    python scripts/mock_classified.py --dry-run  # preview only
"""
from __future__ import annotations

import hashlib
import random
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLASSIFIED = PROJECT_ROOT / "classified"
DRY_RUN = "--dry-run" in sys.argv
random.seed(42)  # Deterministic

# ── Fictional name generators ──────────────────────────────────────────────

_ADJ = [
    "Amber", "Azure", "Blazing", "Brass", "Cobalt", "Coral", "Crimson",
    "Crystal", "Dusk", "Ebony", "Emerald", "Fading", "Frozen", "Gilded",
    "Glass", "Golden", "Granite", "Hollow", "Indigo", "Iron", "Ivory",
    "Jade", "Jasper", "Lunar", "Marble", "Midnight", "Misty", "Neon",
    "Obsidian", "Opal", "Phantom", "Quartz", "Rusty", "Sapphire",
    "Scarlet", "Shadow", "Silver", "Smoky", "Solar", "Spectral",
    "Sterling", "Storm", "Thistle", "Thunder", "Timber", "Twilight",
    "Velvet", "Violet", "Volcanic", "Zinc",
]
_NOUN = [
    "Arrow", "Beacon", "Bell", "Bloom", "Canyon", "Castle", "Chain",
    "Cipher", "Compass", "Crown", "Dawn", "Drifter", "Echo", "Falcon",
    "Flame", "Forge", "Fountain", "Frost", "Garden", "Gate", "Ghost",
    "Glacier", "Harbor", "Haven", "Helix", "Horn", "Horizon", "Isle",
    "Jewel", "Knight", "Lantern", "Leaf", "Lighthouse", "Lotus", "Mask",
    "Mesa", "Mirror", "Moon", "Needle", "Nest", "Oracle", "Orchid",
    "Peak", "Phoenix", "Pillar", "Prism", "Quarry", "Raven", "Ridge",
    "River", "Rose", "Sail", "Scholar", "Serpent", "Shield", "Shore",
    "Signal", "Spark", "Spire", "Stone", "Strand", "Summit", "Swan",
    "Thorn", "Tide", "Tower", "Trail", "Veil", "Vine", "Voyage",
    "Warden", "Whisper", "Wing",
]

GENRES = [
    "AlternativeRock", "AnimeOST", "BrazilianRock", "Britpop", "CityPop",
    "ClassicRock", "Classical", "DarkAmbient", "Disco", "DnB", "EDM",
    "Electronic", "Emo", "Eurodance", "FilmOST", "FolkMetal", "FolkRock",
    "Forró", "Funk", "FunkRock", "GameOST", "GlamRock", "GothicMetal",
    "Grunge", "HardRock", "HardcorePunk", "HeavyMetal", "HipHop",
    "IndustrialMetal", "JRock", "JPop", "JazzFusion", "KPop",
    "MedievalFolk", "Metalcore", "MPB", "NuMetal", "Orchestral", "Pagode",
    "Pop", "PopPunk", "PostGrunge", "PowerMetal", "ProgressiveRock",
    "PsychedelicRock", "PunkRock", "RnB", "Rock", "RockAndRoll", "Samba",
    "Soul", "SouthernRock", "ThrashMetal", "Trance", "TraditionalChinese",
    "TraditionalJapanese", "TraditionalKorean", "WorldMusic",
]

MOODS = [
    "Adventurous", "Aggressive", "Anguished", "Awe-inspired", "Bittersweet",
    "Brooding", "Chaotic", "Chill", "Contemplative", "Cozy", "Danceful",
    "Dark", "Defiant", "Depressive", "Desperate", "Determined", "Ecstatic",
    "Emotional", "Energetic", "Epic", "Ethereal", "Explosive", "Focused",
    "Frenzy", "Furious", "Gritty", "Groovy", "Hardworking", "Heartbreak",
    "Heroic", "Hypnotic", "Introspective", "Jaded", "Joyful", "Lonely",
    "Macabre", "Meditative", "Melancholic", "Mysterious", "Nostalgic",
    "Ominous", "Optimistic", "Peaceful", "Playful", "Rebellious", "Relaxed",
    "Resigned", "Reverent", "Romantic", "Sad", "Sensual", "Serene",
    "Sleepy", "Soaring", "Spiritual", "Surreal", "Suspenseful", "Tender",
    "Tense", "Triumphant", "Upbeat", "Vengeful", "Whimsical", "Wistful",
    "Yearning",
]


def _make_artist(seed: int) -> str:
    adj = _ADJ[seed % len(_ADJ)]
    noun = _NOUN[(seed >> 8) % len(_NOUN)]
    return f"Fictional-{adj}{noun}"


def _make_track_name(seed: int) -> str:
    h = hashlib.md5(str(seed).encode()).hexdigest()[:8]
    return f"Fictional-Track-{h}.mp3"


def _mkdir(p: Path) -> None:
    if DRY_RUN:
        print(f"  mkdir {p}")
    else:
        p.mkdir(parents=True, exist_ok=True)


def _touch(p: Path) -> None:
    if DRY_RUN:
        print(f"  touch {p}")
    else:
        p.parent.mkdir(parents=True, exist_ok=True)
        if not p.exists():
            p.touch()


def main() -> None:
    if DRY_RUN:
        print("=== DRY RUN ===\n")

    singles = CLASSIFIED / "singles"
    albums = CLASSIFIED / "albums"

    # ── 1. Create all mood folders ──
    print("Creating Mood folders...")
    for mood in MOODS:
        _mkdir(singles / "Mood" / mood)

    # ── 2. Create all genre folders ──
    print("Creating Genre folders...")
    for genre in GENRES:
        _mkdir(singles / "Genre" / genre)

    # ── 3. Create utility folders ──
    for d in ["new", "new-sliced", "sliced"]:
        _mkdir(singles / d)
    _mkdir(albums / "Artist")
    _mkdir(albums / "etc")

    # ── 4. Generate fictional artists + tracks ──
    # ~40 artists, each with 3-8 tracks, distributed across Genre & Mood
    print("Generating fictional tracks...")
    num_artists = 40
    track_counter = 1000
    total_tracks = 0

    for i in range(num_artists):
        artist = _make_artist(i * 37 + 7)
        num_tracks = random.randint(3, 8)

        # Pick a primary genre and 1–3 moods for this artist
        artist_genre = GENRES[i % len(GENRES)]
        artist_moods = random.sample(MOODS, k=min(random.randint(1, 3), len(MOODS)))

        # Artist folder under singles/Artists/
        artist_dir = singles / "Artists" / artist
        _mkdir(artist_dir)

        for t in range(num_tracks):
            track_name = _make_track_name(track_counter)
            track_counter += 1

            # Place in Artist/
            _touch(artist_dir / track_name)

            # Place in Genre/
            _touch(singles / "Genre" / artist_genre / track_name)

            # Place in each assigned mood
            pool = list(set(artist_moods + random.sample(MOODS, k=random.randint(0, 2))))
            track_moods = random.sample(pool, k=min(random.randint(1, 4), len(pool)))
            for mood in set(track_moods):
                _touch(singles / "Mood" / mood / track_name)

            total_tracks += 1

        # Also create an album entry for every 3rd artist
        if i % 3 == 0:
            album_dir = albums / "Artist" / artist
            _mkdir(album_dir)
            album_name = f"Fictional-Album-{hashlib.md5(artist.encode()).hexdigest()[:6]}"
            album_folder = album_dir / album_name
            _mkdir(album_folder)
            for t in range(random.randint(8, 14)):
                _touch(album_folder / _make_track_name(track_counter))
                track_counter += 1

    # ── 5. Add some tracks to sliced/ ──
    print("Adding sliced examples...")
    sliced_dir = singles / "sliced"
    for i in range(10):
        base = _make_track_name(9000 + i).replace(".mp3", "")
        for part in range(3):
            _touch(sliced_dir / f"{base}_part_{part:03d}.mp3")

    print(f"\nDone. {total_tracks} singles across {num_artists} artists.")
    if DRY_RUN:
        print("(Dry run — nothing written to disk.)")


if __name__ == "__main__":
    main()
