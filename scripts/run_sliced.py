#!/usr/bin/env python3
"""Process sliced-3 to classified/singles/sliced/{Artist,Genre,Mood}/. Single-run."""
import os, sys, shutil
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, "scripts")
from classify_and_clean import classify_file, clean_filename

SRC = Path("classified/singles/new/sliced-3")
DST = Path("classified/singles/sliced")
LOG = open("/tmp/sliced_final.log", "w", buffering=1)

def log(msg):
    LOG.write(msg + "\n")
    LOG.flush()

files = [f for f in SRC.rglob("*.mp3")]
log(f"START: {len(files)} files")

ok = err = skip = 0
for i, src in enumerate(files):
    fn = src.name
    try:
        new_fn = clean_filename(fn)
        cls = classify_file(fn)
        if "Various" in cls["artists"] or "Unclassified" in cls["genres"]:
            log(f"REJECT[{i}] {fn}: {cls}")
            err += 1
            continue
        base, ext = os.path.splitext(new_fn)
        for cat, items in [("Artist", cls["artists"]), ("Genre", cls["genres"]), ("Mood", cls["moods"])]:
            for item in items:
                td = DST / cat / item
                td.mkdir(parents=True, exist_ok=True)
                d = td / new_fn
                if d.exists() and d.stat().st_size == src.stat().st_size:
                    skip += 1
                    continue
                c = 1
                while d.exists():
                    d = td / f"{base}-dup{c}{ext}"
                    c += 1
                shutil.copy2(src, d)
        ok += 1
        if (i + 1) % 100 == 0:
            log(f"PROGRESS: {i+1}/{len(files)} ok={ok}")
    except Exception as e:
        log(f"ERROR[{i}] {fn}: {e}")
        import traceback; traceback.print_exc(file=LOG)
        err += 1

log(f"DONE: ok={ok} skip={skip} err={err}")
for cat in ["Artist", "Genre", "Mood"]:
    cd = DST / cat
    if cd.exists():
        af = [f for f in cd.rglob("*.mp3")]
        log(f"{cat}: {len(af)} total, {len({f.name for f in af})} unique")
LOG.close()
