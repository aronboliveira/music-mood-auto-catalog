import os
import shutil
import fnmatch
from pathlib import Path

patterns = {
    "*Fictional-Track-6c600ed9.mp3": ("Fictional-QuartzPeak", "AlternativeMetal"),
    "Fictional-QuartzPeak*.mp3": ("Fictional-QuartzPeak", "AlternativeMetal"),
    "*Fictional-Track-b054d42Fictional-Track-e4da3b7f.mp3": ("Fictional-QuartzRidge", "PostGrunge"),
    "*Fictional-Track-093c90cFictional-Track-eccbc87e.mp3": ("Fictional-QuartzRidge", "PostGrunge"),
    "Fictional-SterlingLotus*.mp3": ("Fictional-SterlingLotus", "Metalcore"),
    "Fictional-Track-e8b2faaa.mp3": ("Fictional-SterlingLotus", "Metalcore"),
    "*Fictional-Track-76a5577Fictional-Track-c9f0f895.mp3": ("Fictional-IronMesa", "AlternativeMetal"),
    "Fictional-IronSerpent*.mp3": ("Fictional-IronSerpent", "Pop"),
    "Because-of-You*.mp3": ("Fictional-CoralVoyage", "PostGrunge"),
    "Fictional-Track-dcfafcbFictional-Track-a87ff679.mp3": ("Fictional-SterlingBeacon", "NuMetal"),
    "Fictional-Track-509e089Fictional-Track-e4da3b7f.mp3": ("Fictional-ScarletPrism", "AlternativeRock"),
    "Fictional-Track-20448b5Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3": ("Fictional-GlassStone", "EDM"),
    "Fictional-Track-465f02ec.mp3": ("Fictional-JadeOracle", "EDM"),
    "Fictional-Track-cb1d02ce.mp3": ("Fictional-IndigoHarbor", "EDM"),
    "Fictional-Track-940f223Fictional-Track-a87ff679.mp3": ("Fictional-TimberCastle", "BrazilianRock"),
    "Fictional-Track-a7a716cFictional-Track-c9f0f895.mp3": ("Fictional-TimberCastle", "BrazilianRock"),
    "Fictional-Track-24c9ba60.mp3": ("Fictional-TimberCastle", "BrazilianRock"),
    "Fictional-Track-02275a4e.mp3": ("Fictional-TimberCastle", "BrazilianRock"),
    "Fictional-Track-3e1d66c9.mp3": ("Fictional-TimberCastle", "BrazilianRock"),
    "Fictional-Track-f7587d70.mp3": ("Fictional-TimberCastle", "BrazilianRock"),
    "Fictional-Track-eedff66e.mp3": ("Fictional-TimberCastle", "BrazilianRock"),
    "Fictional-Track-9398bafFictional-Track-1679091c.mp3": ("Fictional-TimberCastle", "BrazilianRock"),
    "Fictional-Track-b2332a3d.mp3": ("Fictional-TimberCastle", "BrazilianRock"),
    "Fogo-*.mp3": ("Fictional-EmeraldBloom", "BrazilianRock"),
    "A-Sua-Maneira*.mp3": ("Fictional-EmeraldBloom", "BrazilianRock"),
    "O-Passageiro*.mp3": ("Fictional-EmeraldBloom", "BrazilianRock"),
    "Noite-e-Dia*.mp3": ("Fictional-EmeraldBloom", "BrazilianRock"),
    "Fictional-Kw-5bf11d51*.mp3": ("Fictional-EmeraldBloom", "BrazilianRock"),
    "Fictional-Kw-75c11c8b*.mp3": ("Fictional-EmeraldBloom", "BrazilianRock"),
    "Fictional-Kw-aff601f7*.mp3": ("Fictional-EmeraldBloom", "BrazilianRock"),
    "Fictional-Track-c8f75b0Fictional-Track-eccbc87e.mp3": ("Fictional-VelvetSpire", "Samba"),
    "Fictional-Track-522cc4cFictional-Track-eccbc87e.mp3": ("Fictional-ScarletPrism", "MPB"),
    "Fictional-Track-2a4e0beFictional-Track-c81e728d.mp3": ("Fictional-ScarletPrism", "MPB"),
    "Hylian-ensemble*.mp3": ("Fictional-CrystalBell", "GameOST"),
    "Fictional-Kw-e4178445*.mp3": ("Fictional-CrimsonFountain", "AnimeOST"),
    "O-Conto-da-Fictional-ZincNeedlesa-kaguya*.mp3": ("Fictional-CrimsonFountain", "AnimeOST"),
    "Fictional-Track-c0f4308Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3": ("Fictional-AzurePrism", "CityPop"),
    "Dias-Atras*.mp3": ("Fictional-FrozenNeedle", "BrazilianRock"),
    "Regina-Let*.mp3": ("Fictional-FrozenNeedle", "BrazilianRock"),
    "Irreversivel*.mp3": ("Fictional-FrozenNeedle", "BrazilianRock"),
    "Fictional-Kw-31e2e4d0*.mp3": ("Fictional-FrozenNeedle", "BrazilianRock"),
    "Game-Over*.mp3": ("Fictional-FrozenNeedle", "BrazilianRock"),
    "Amado*.mp3": ("Fictional-ScarletPrism", "MPB"),
    "Fictional-Track-aa6503ce.mp3": ("Fictional-ScarletPrism", "MPB"),
    "Fictional-Track-872f27da.mp3": ("Fictional-FrozenMask", "PowerMetal"),
    "Fictional-Track-6a5dc9bb.mp3": ("Fictional-PhantomMirror", "MPB"),
    "Fictional-Track-fa210e2a.mp3": ("Fictional-PhantomMirror", "MPB"),
    "Fictional-Track-e411283e.mp3": ("Fictional-GraniteCompass", "CityPop"),
    "Fictional-Track-2aa8b86f.mp3": ("Fictional-IronSignal", "Pagode"),
    "Fictional-Track-230d3b2Fictional-Track-a87ff679.mp3": ("Fictional-ZincWing", "Grunge")
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
