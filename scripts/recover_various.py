import os
import shutil
from pathlib import Path

root = Path("classified/singles")
artist_dir = root / "Artist"
genre_dir = root / "Genre"

# Get all filenames currently across ALL Artist directories
existing_in_artist = set()
if artist_dir.exists():
    for d, _, files in os.walk(artist_dir):
        for f in files:
            if f.endswith(".mp3"):
                existing_in_artist.add(f)

# Find any file in Genre that lacks an Artist counterpart
various_dir = artist_dir / "Various"
various_dir.mkdir(parents=True, exist_ok=True)

recovered_count = 0
if genre_dir.exists():
    for d, _, files in os.walk(genre_dir):
        for f in files:
            if f.endswith(".mp3") and f not in existing_in_artist:
                src = os.path.join(d, f)
                dst = various_dir / f
                if not dst.exists():
                    shutil.copy2(src, dst)
                    existing_in_artist.add(f)
                    recovered_count += 1
                    print(f"Recovered to Various: {f}")

print(f"Total recovered: {recovered_count}")
