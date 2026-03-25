#!/usr/bin/env python3
"""One-shot: copy TheSims tracks to Genre/GameOST + correct Mood folders."""
import shutil
from pathlib import Path

BASE = Path("/mock/path/to/project/music/downloaded")
SRC  = BASE / "classified/singles/Artist/TheSims"
GENRE     = BASE / "classified/singles/Genre/GameOST"
STUDYFOCUS = BASE / "classified/singles/Mood/StudyFocus"
UPBEAT    = BASE / "classified/singles/Mood/Upbeat"
NOSTALGIC = BASE / "classified/singles/Mood/Nostalgic"

STUDY_FILES = {
    "*.mp3",
    "*.mp3",
    "*.mp3",
    "*.mp3",
    "*.mp3",
    "*.mp3",
    "*.mp3",
    "*.mp3",
    "MockGame_Sims\".mp3",
    "*.mp3",
}

UPBEAT_FILES = {
    "*.mp3",
    "*.mp3",
    "*.mp3",
    "*.mp3",
    "*.mp3",
    "*.mp3",
    "*.mp3",
    "*.mp3",
    "*.mp3",
    "*.mp3",
    "*.mp3",
    "01 - It\".mp3",
    "MockGame_Sims\".mp3",
    "MockGame_Sims\".mp3",
    "MockGame_Sims\".mp3",
}

NOSTALGIC_FILES = {
    "MockGame_Sims\".mp3",
}


def safe_copy(src: Path, dst_dir: Path):
    dst = dst_dir / src.name
    if dst.exists():
        print(f"  skip (exists): {dst.name}")
        return
    shutil.copy2(src, dst)
    print(f"  copied: {src.name} -> {dst_dir.name}/")


errors = []
for mp3 in list(SRC.rglob("*.mp3")):
    try:
        safe_copy(mp3, GENRE)
    except Exception as e:
        errors.append((mp3.name, "GameOST", str(e)))

    mood_dir = None
    if mp3.name in STUDY_FILES:
        mood_dir = STUDYFOCUS
    elif mp3.name in UPBEAT_FILES:
        mood_dir = UPBEAT
    elif mp3.name in NOSTALGIC_FILES:
        mood_dir = NOSTALGIC

    if mood_dir:
        try:
            safe_copy(mp3, mood_dir)
        except Exception as e:
            errors.append((mp3.name, mood_dir.name, str(e)))

print("\n=== summary ===")
print(f"GameOST:    {len(list(GENRE.glob('*Sims*')))} / 26")
print(f"StudyFocus: {len([f for f in STUDYFOCUS.iterdir() if 'Sims' in f.name or 'Test' in f.name])} / 10")
print(f"Upbeat:     {len(list(UPBEAT.glob('*Sims*')))} / 15")
print(f"Nostalgic:  {len(list(NOSTALGIC.glob('*Sims*')))} / 1")
if errors:
    print("\n=== errors ===")
    for name, dest, msg in errors:
        print(f"  {name} -> {dest}: {msg}")
