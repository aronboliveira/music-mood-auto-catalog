import os
import shutil
import fnmatch
from pathlib import Path

patterns = {
    "*.mp3": ("MockBand_Faith", "AlternativeMetal"),
    "*.mp3": ("MockBand_Faith", "AlternativeMetal"),
    "*.mp3": ("MockBand_Breaking", "PostGrunge"),
    "*.mp3": ("MockBand_Breaking", "PostGrunge"),
    "*.mp3": ("MockBand_Bring", "Metalcore"),
    "*.mp3": ("MockBand_Bring", "Metalcore"),
    "*.mp3": ("MockBand_Evanescence", "AlternativeMetal"),
    "*.mp3": ("MockBand_NSYNC", "Pop"),
    "*.mp3": ("MockBand_Nickel", "PostGrunge"),
    "*.mp3": ("MockBand_SOAD", "NuMetal"),
    "*.mp3": ("MockBand_Foo", "AlternativeRock"),
    "*.mp3": ("MockDJ_Dave", "EDM"),
    "*.mp3": ("MockBand_Infected", "EDM"),
    "*.mp3": ("MockDJ_Darude", "EDM"),
    "*.mp3": ("MockBand_ORappa", "BrazilianRock"),
    "*.mp3": ("MockBand_ORappa", "BrazilianRock"),
    "*.mp3": ("MockBand_ORappa", "BrazilianRock"),
    "*.mp3": ("MockBand_ORappa", "BrazilianRock"),
    "*.mp3": ("MockBand_ORappa", "BrazilianRock"),
    "*.mp3": ("MockBand_ORappa", "BrazilianRock"),
    "*.mp3": ("MockBand_ORappa", "BrazilianRock"),
    "*.mp3": ("MockBand_ORappa", "BrazilianRock"),
    "*.mp3": ("MockBand_ORappa", "BrazilianRock"),
    "*.mp3": ("MockBand_Capital", "BrazilianRock"),
    "*.mp3": ("MockBand_Capital", "BrazilianRock"),
    "*.mp3": ("MockBand_Capital", "BrazilianRock"),
    "*.mp3": ("MockBand_Capital", "BrazilianRock"),
    "*.mp3": ("MockBand_Capital", "BrazilianRock"),
    "*.mp3": ("MockBand_Capital", "BrazilianRock"),
    "*.mp3": ("MockBand_Capital", "BrazilianRock"),
    "*.mp3": ("MockSinger_Alcione", "Samba"),
    "*.mp3": ("MockSinger_Djavan", "MPB"),
    "*.mp3": ("MockSinger_Djavan", "MPB"),
    "*.mp3": ("MockGame_Zelda", "GameOST"),
    "*.mp3": ("MockStumocksinger_dio_Ghibli", "AnimeOST"),
    "*.mp3": ("MockStumocksinger_dio_Ghibli", "AnimeOST"),
    "*.mp3": ("MockSinger_Miki", "CityPop"),
    "*.mp3": ("MockBand_CPM22", "BrazilianRock"),
    "*.mp3": ("MockBand_CPM22", "BrazilianRock"),
    "*.mp3": ("MockBand_CPM22", "BrazilianRock"),
    "*.mp3": ("MockBand_CPM22", "BrazilianRock"),
    "*.mp3": ("MockBand_CPM22", "BrazilianRock"),
    "*.mp3": ("MockSinger_Vanessa", "MPB"),
    "*.mp3": ("MockSinger_Vanessa", "MPB"),
    "*.mp3": ("MockBand_Angra", "PowerMetal"),
    "*.mp3": ("MockSinger_Jorge", "MPB"),
    "*.mp3": ("MockSinger_Jorge", "MPB"),
    "*.mp3": ("MockSinger_Junko", "CityPop"),
    "*.mp3": ("MockSinger_Belo", "Pagode"),
    "*.mp3": ("MockBand_Alice", "Grunge")
}

def move_from_dir(src_dir, dest_type):
    if not os.path.exists(src_dir):
        return
    for fn in list(os.listdir(src_dir)):
        if not fn.endswith(".mp3"):
            continue
        
        matched = False
        for pat, (artist, genre) in patterns.items():
            if fnmatch.fnmatch(fn, pat):
                dest_val = artist if dest_type == "Artist" else genre
                dest_dir = Path("classified/singles") / dest_type / dest_val
                dest_dir.mkdir(parents=True, exist_ok=True)
                
                src_path = os.path.join(src_dir, fn)
                dst_path = dest_dir / fn
                
                if not dst_path.exists():
                    shutil.move(src_path, dst_path)
                else:
                    os.remove(src_path)
                matched = True
                print(f"Matched {fn} -> {dest_val}")
                break
                
        if not matched:
            print(f"WARNING: No pattern matched for {fn} in {src_dir}")

move_from_dir("classified/singles/Artist/Various", "Artist")
move_from_dir("classified/singles/Genre/Unclassified", "Genre")

# Cleanup directories
try:
    os.rmdir("classified/singles/Artist/Various")
    print("Deleted Artist/Various")
except Exception as e:
    print("Artist/Various not empty or missing", e)

try:
    os.rmdir("classified/singles/Genre/Unclassified")
    print("Deleted Genre/Unclassified")
except Exception as e:
    print("Genre/Unclassified not empty or missing", e)
