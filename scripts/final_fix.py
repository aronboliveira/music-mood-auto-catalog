import os
import shutil
from pathlib import Path

files = {
    "Fictional-Track-cfb8c580.mp3": ("Fictional-EmeraldBloom", "BrazilianRock"),
    "Fictional-Track-8fc20faFictional-Track-8f14e45f.mp3": ("Fictional-TimberCastle", "BrazilianRock"),
    "Fictional-Track-b211b1ed.mp3": ("Fictional-GlassStone", "EDM"),
    "Fictional-Track-4c61d92Fictional-Track-a87ff679.mp3": ("Fictional-CrystalBell", "GameOST")
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
