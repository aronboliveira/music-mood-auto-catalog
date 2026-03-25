#!/usr/bin/env python3
"""
Process sliced tracks from classified/singles/new/sliced-3/
into the isolated taxonomy at classified/singles/sliced/{Artist,Genre,Mood}/.

Walks all subdirectories of sliced-3, classifies each mp3 by filename,
copies to every matching Artist/Genre/Mood subfolder.
Rejects "Various" and "Unclassified" (banned per SOP).
"""
import os
import sys
import shutil
import time
from pathlib import Path

# Unbuffered stdout for log reliability
sys.stdout.reconfigure(line_buffering=True)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from classify_and_clean import classify_file, clean_filename

SRC_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("classified/singles/new/sliced-3")
DST_ROOT = Path("classified/singles/sliced")


def process():
    if not SRC_DIR.exists():
        print(f"Source directory {SRC_DIR} does not exist.")
        return

    # Collect all mp3s recursively
    files = [f for f in SRC_DIR.rglob("*.mp3")]
    print(f"Found {len(files)} mp3 files in {SRC_DIR}")

    processed = 0
    skipped = 0
    errors = []

    for src in files:
        fn = src.name
        try:
            new_fn = clean_filename(fn)
            cls = classify_file(fn)

            if "Various" in cls["artists"] or "Unclassified" in cls["genres"]:
                print(f"  REJECT: {fn} -> {cls}")
                errors.append((fn, cls))
                continue

            base, ext = os.path.splitext(new_fn)

            for category, items in [
                ("Artist", cls["artists"]),
                ("Genre", cls["genres"]),
                ("Mood", cls["moods"]),
            ]:
                for item in items:
                    target_dir = DST_ROOT / category / item
                    target_dir.mkdir(parents=True, exist_ok=True)
                    dst = target_dir / new_fn

                    # Skip exact duplicate (same name + same size)
                    if dst.exists() and os.path.getsize(src) == os.path.getsize(dst):
                        skipped += 1
                        continue

                    # Handle name collision with different content
                    counter = 1
                    while dst.exists():
                        dst = target_dir / f"{base}-dup{counter}{ext}"
                        counter += 1

                    for attempt in range(3):
                        try:
                            shutil.copy(src, dst)
                            break
                        except OSError as copy_err:
                            if attempt < 2:
                                time.sleep(2)
                            else:
                                raise copy_err

            processed += 1
            if processed % 25 == 0:
                print(f"  progress: {processed}/{len(files)} source files")
        except Exception as e:
            print(f"  ERROR: {fn}: {e}")
            errors.append((fn, str(e)))

    print(f"\nProcessed: {processed} | Skipped dups: {skipped} | Errors: {len(errors)}")
    if errors:
        print("Rejected/errored files:")
        for fn, info in errors:
            print(f"  {fn}: {info}")

    # Verification: count unique basenames per category
    print("\n--- Verification ---")
    for cat in ["Artist", "Genre", "Mood"]:
        cat_dir = DST_ROOT / cat
        if cat_dir.exists():
            all_files = [f for f in cat_dir.rglob("*.mp3")]
            basenames = {f.name for f in all_files}
            print(f"{cat}: {len(all_files)} total files, {len(basenames)} unique basenames")


if __name__ == "__main__":
    process()
