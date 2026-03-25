import os, shutil
from pathlib import Path

files = {
    "*.mp3": ("MockBand_Capital", "BrazilianRock"),
    "*.mp3": ("MockBand_ORappa", "BrazilianRock"),
    "*.mp3": ("MockDJ_Dave", "EDM"),
    "*.mp3": ("MockGame_Zelda", "GameOST")
}

for d_type, d_name in [("Artist", "Various"), ("Genre", "Unclassified")]:
    src_dir = Path(f"classified/singles/{d_type}/{d_name}")
    if src_dir.exists():
        for fn in os.listdir(src_dir):
            if fn in files:
                artist, genre = files[fn]
                dest_val = artist if d_type == "Artist" else genre
                dest_dir = Path("classified/singles") / d_type / dest_val
                dest_dir.mkdir(parents=True, exist_ok=True)
                
                src_path = src_dir / fn
                dst_path = dest_dir / fn
                
                if not dst_path.exists():
                    shutil.move(str(src_path), str(dst_path))
                else:
                    os.remove(str(src_path))
        
        try:
            os.rmdir(str(src_dir))
            print(f"Deleted {src_dir}")
        except Exception as e:
            print(f"Could not delete {src_dir}: {e}")
