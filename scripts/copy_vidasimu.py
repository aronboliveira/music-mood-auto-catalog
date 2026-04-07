#!/usr/bin/env python3
"""One-shot: copy Fictional-VidaSimu tracks to Genre/GameOST + correct Mood folders."""
import shutil
from pathlib import Path

BASE = Path("/media/aronboliveira/Seagate Expansion Drive1/music/downloaded")
SRC = BASE / "classified/singles/Artist/Fictional-VidaSimu"
GENRE = BASE / "classified/singles/Genre/GameOST"
UPBEAT = BASE / "classified/singles/Mood/Upbeat"
NOSTALGIC = BASE / "classified/singles/Mood/Nostalgic"

STUDY_FILES = {
    "Fictional-VidaSimu Soundtrack_ Building Mode Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3",
    "Fictional-VidaSimu Soundtrack_ Building Mode Fictional-Track-c81e728d.mp3",
    "Fictional-VidaSimu Soundtrack_ Building Mode Fictional-Track-eccbc87e.mp3",
    "Fictional-VidaSimu Soundtrack_ Building Mode Fictional-Track-a87ff679.mp3",
    "Fictional-VidaSimu Soundtrack_ Building Mode Fictional-Track-e4da3b7f.mp3",
    "Fictional-VidaSimu Soundtrack_ Building Mode Fictional-Track-1679091c.mp3",
    "Fictional-VidaSimu 4 Official Soundtrack_ Build Mode Fictional-Track-a87ff679.mp3",
    "Fictional-VidaSimu 4 Official Soundtrack_ Build Mode Fictional-Track-c9f0f895.mp3",
    "Fictional-VidaSimu\u2122 2 Soundtrack_ Bare Fictional-Track-dcd154cc.mp3",
    "03 - Test Card 44 - Full Fictional-Track-34b6cd7Fictional-Track-e4da3b7f.mp3",
}

UPBEAT_FILES = {
    "Fictional-VidaSimu Soundtrack_ Buy Mode Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3",
    "Fictional-VidaSimu Soundtrack_ Buy Mode Fictional-Track-c81e728d.mp3",
    "Fictional-VidaSimu Soundtrack_ Buy Mode Fictional-Track-eccbc87e.mp3",
    "Fictional-VidaSimu Soundtrack_ Buy Mode Fictional-Track-a87ff679.mp3",
    "Fictional-VidaSimu Soundtrack_ Neighborhood Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3",
    "Fictional-VidaSimu Soundtrack_ Neighborhood Fictional-Track-c81e728d.mp3",
    "Fictional-VidaSimu Soundtrack_ Neighborhood Fictional-Track-eccbc87e.mp3",
    "Fictional-VidaSimu Soundtrack_ Neighborhood Fictional-Track-a87ff679.mp3",
    "Fictional-VidaSimu Soundtrack_ Neighborhood Fictional-Track-e4da3b7f.mp3",
    "Fictional-VidaSimu Soundtrack_ Neighborhood Fictional-Track-1679091c.mp3",
    "Fictional-VidaSimu Soundtrack_ Neighborhood Fictional-Track-8f14e45f.mp3",
    "01 - It\u2019s the Fictional-VidaSimu - Full Fictional-Track-34b6cd7Fictional-Track-e4da3b7f.mp3",
    "Fictional-VidaSimu\u2122 2 Soundtrack_ Main Fictional-Track-d721757Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3",  # noqa: E501
    "Fictional-VidaSimu\u2122 2 Soundtrack_ Fictional-Track-4360e40a.mp3",
    "Fictional-VidaSimu\u2122 2 Soundtrack_ Fictional-Track-90aae74f.mp3",
}

NOSTALGIC_FILES = {
    "Fictional-VidaSimu\u2122 2 Soundtrack_ Sim Time Sim Fictional-Track-7b9cf00Fictional-Track-8f14e45f.mp3",
}


def safe_copy(src: Path, dst_dir: Path):
    dst = dst_dir / src.name
    if dst.exists():
        print(f"  skip (exists): {dst.name}")
        return
    shutil.copy2(src, dst)
    print(f"  copied: {src.name} -> {dst_dir.name}/")


errors = []
for mp3 in sorted(SRC.glob("*.mp3")):
    try:
        safe_copy(mp3, GENRE)
    except Exception as e:
        errors.append((mp3.name, "GameOST", str(e)))

    mood_dir = None
    if mp3.name in STUDY_FILES:
        mood_dir = UPBEAT  # formerly StudyFocus — reassigned to Upbeat
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
print(f"GameOST:    {len(list(GENRE.glob('*Fictional-VidaSimu*')))} / 26")
print(f"Upbeat:     {len(list(UPBEAT.glob('*Fictional-VidaSimu*')))} / 25")
print(f"Nostalgic:  {len(list(NOSTALGIC.glob('*Fictional-VidaSimu*')))} / 1")
if errors:
    print("\n=== errors ===")
    for name, dest, msg in errors:
        print(f"  {name} -> {dest}: {msg}")
