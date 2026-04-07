import sys
import os
import shutil
from pathlib import Path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from classify_and_clean import classify_file, clean_filename, ensure_dir  # noqa: E402


def process_new_files():
    new_dir = Path("classified/singles/new")
    root = Path("classified/singles")

    if not new_dir.exists():
        print(f"Directory {new_dir} does not exist.")
        return

    files_processed = 0
    errors = 0

    # We will track processed files to remove them later
    processed_paths = []

    for fn in os.listdir(new_dir):
        if not fn.endswith(".mp3"):
            continue

        src = new_dir / fn
        try:
            # 1. Clean the filename
            new_fn = clean_filename(fn)

            # 2. Re-classify
            cls = classify_file(fn)

            # 3. Create a unique identifier to avoid infinite name loops on duplicates
            base, ext = os.path.splitext(new_fn)

            destinations = []

            # 4. Determine destinations across Artist, Genre, Mood
            for category, items in [("Artist", cls["artists"]), ("Genre", cls["genres"]), ("Mood", cls["moods"])]:
                for item in items:
                    target_dir = root / category / item
                    ensure_dir(target_dir)

                    dst_path = target_dir / new_fn
                    counter = 1
                    while dst_path.exists():
                        # Only increase counter if it's not the exact same file content / size
                        # A better check is if the file size is identical we can skip copying to avoid bloating
                        if os.path.getsize(src) == os.path.getsize(dst_path):
                            break
                        dst_path = target_dir / f"{base}-{counter}{ext}"
                        counter += 1

                    if not dst_path.exists():
                        destinations.append(dst_path)

            # 5. Execute copies
            for dst in destinations:
                shutil.copy2(src, dst)
                print(f"Copied {fn} -> {dst}")

            processed_paths.append(src)
            files_processed += 1

        except Exception as e:
            print(f"Error processing {fn}: {e}")
            errors += 1

    # 6. Cleanup
    for src in processed_paths:
        os.remove(src)

    print("\nBatch processing complete!")
    print(f"Successfully processed and removed: {files_processed} files.")
    print(f"Errors encountered: {errors}")


if __name__ == "__main__":
    process_new_files()
