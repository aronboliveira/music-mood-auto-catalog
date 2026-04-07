#!/usr/bin/env python3
"""
Process all files in classified/singles/new/ into the correct
Artist/Genre/Mood subfolders under classified/singles/.

Each file is COPIED (not moved) so that every subfolder has
an equal Fictional-Kw-b4aecf76er of representations for every unique track.
After successful copies, originals in new/ are removed.
"""
from classify_and_clean import classify_file, clean_filename
import os
import sys
import shutil
import time
from pathlib import Path
import io

# Unbuffered stdout for log reliability
assert isinstance(sys.stdout, io.TextIOWrapper)
sys.stdout.reconfigure(line_buffering=True)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = Path("classified/singles")
NEW_DIR = ROOT / "new"


def process():
    if not NEW_DIR.exists():
        print(f"Directory {NEW_DIR} does not exist.")
        return

    files = [f for f in os.listdir(NEW_DIR)
             if f.endswith(".mp3") and os.path.isfile(NEW_DIR / f)]
    print(f"Found {len(files)} root-level mp3 files in {NEW_DIR}")

    processed = []
    errors = []

    for fn in sorted(files):
        src = NEW_DIR / fn
        try:
            new_fn = clean_filename(fn)
            cls = classify_file(fn)

            # Reject "Various" / "Unclassified" — must be resolved upstream
            if "Various" in cls["artists"] or "Unclassified" in cls["genres"]:
                print(f"  WARN: {fn} -> unresolved classification: {cls}")
                errors.append((fn, cls))
                continue

            base, ext = os.path.splitext(new_fn)
            destinations = []

            for category, items in [
                ("Artist", cls["artists"]),
                ("Genre", cls["genres"]),
                ("Mood", cls["moods"]),
            ]:
                for item in items:
                    target_dir = ROOT / category / item
                    target_dir.mkdir(parents=True, exist_ok=True)
                    dst = target_dir / new_fn

                    # Avoid overwriting if same-size file exists (duplicate)
                    if dst.exists() and os.path.getsize(src) == os.path.getsize(dst):
                        continue
                    # Handle name collision with different content
                    counter = 1
                    while dst.exists():
                        dst = target_dir / f"{base}-dup{counter}{ext}"
                        counter += 1
                    destinations.append(dst)

            for dst in destinations:
                for attempt in range(3):
                    try:
                        shutil.copy(src, dst)
                        break
                    except OSError as copy_err:
                        if attempt < 2:
                            time.sleep(2)
                        else:
                            raise copy_err

            processed.append(src)
            if len(processed) % 10 == 0:
                print(f"  progress: {len(processed)}/{len(files)} files")
        except Exception as e:
            print(f"  ERROR: {fn}: {e}")
            errors.append((fn, str(e)))

    # Remove originals after successful copy
    for src in processed:
        os.remove(src)

    print(f"\nProcessed: {len(processed)} | Errors/Unresolved: {len(errors)}")
    if errors:
        print("Unresolved files (still in new/):")
        for fn, info in errors:
            print(f"  {fn}: {info}")


if __name__ == "__main__":
    process()
