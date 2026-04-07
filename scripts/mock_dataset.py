import os
import shutil
import random
import subprocess
import json
import types
try:
    import yaml
except ImportError:
    yaml: types.ModuleType | None = None  # type: ignore[no-redef]

random.seed(42)

BASE_DIR = '/home/mockuser/Desktop/programming/py/music-algorithm'


def clear_directory(path):
    if os.path.exists(path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
    os.makedirs(path, exist_ok=True)


dirs_to_clear = ['singles', 'albums', 'classified']
for d in dirs_to_clear:
    clear_directory(os.path.join(BASE_DIR, d))

artists = ["Neon Whispers", "The Pixel Chords", "Cybernetic Dreams", "Acoustic Mirage", "Quantum Beats"]
genres = {
    "synthwave": ["Energetic", "Groovy", "Nostalgic"],
    "calm": ["Peaceful", "Serene", "Relaxed"],
    "rock": ["Rebellious", "Aggressive", "Gritty"],
    "pagode": ["Joyful", "Playful", "Upbeat"],
    "ambient": ["Ethereal", "Hypnotic", "Meditative"]
}

singles_dir = os.path.join(BASE_DIR, 'singles')
albums_dir = os.path.join(BASE_DIR, 'albums')


def generate_mp3(filepath, duration):
    cmd = [
        'ffmpeg', '-y', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo',
        '-t', str(duration), '-q:a', '9', '-acodec', 'libmp3lame', filepath
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


singles_files: list[dict[str, str | int]] = []
for i in range(1, 26):
    artist = random.choice(artists)
    genre = random.choice(list(genres.keys()))
    filename = f"{artist} - {genre}-song-{i}.mp3"
    filepath = os.path.join(singles_dir, filename)
    duration = random.randint(60, 180)  # 1 to 3 mins
    generate_mp3(filepath, duration)
    singles_files.append({"filename": filename, "artist": artist, "genre": genre,
                         "path": filepath, "size": os.path.getsize(filepath)})

albums_files: list[dict[str, str | int]] = []
for i in range(1, 9):
    artist = random.choice(artists)
    genre = random.choice(list(genres.keys()))
    filename = f"{artist} - {genre}-album-{i}.mp3"
    filepath = os.path.join(albums_dir, filename)
    duration = random.randint(600, 1800)  # 10 to 30 mins
    generate_mp3(filepath, duration)
    albums_files.append({"filename": filename, "artist": artist, "genre": genre,
                        "path": filepath, "size": os.path.getsize(filepath)})

classified_dir = os.path.join(BASE_DIR, 'classified')


def classify_files(files_list, source_type):
    for f in files_list:
        artist = f['artist']
        genre = f['genre']
        filename = f['filename']
        src_path = f['path']

        artist_dir = os.path.join(classified_dir, source_type, 'Artist', artist)
        os.makedirs(artist_dir, exist_ok=True)
        shutil.copy2(src_path, os.path.join(artist_dir, filename))

        genre_dir = os.path.join(classified_dir, source_type, 'Genre', genre)
        os.makedirs(genre_dir, exist_ok=True)
        shutil.copy2(src_path, os.path.join(genre_dir, filename))

        moods = genres[genre]
        for mood in moods:
            mood_dir = os.path.join(classified_dir, source_type, 'Mood', mood)
            os.makedirs(mood_dir, exist_ok=True)
            shutil.copy2(src_path, os.path.join(mood_dir, filename))


classify_files(singles_files, 'singles')
classify_files(albums_files, 'albums')

maps_dir_20260324 = os.path.join(BASE_DIR, 'docs', 'maps', '20260324')
os.makedirs(maps_dir_20260324, exist_ok=True)

main_taxonomy = []
for root, dirs, files in os.walk(classified_dir):
    level = root.replace(classified_dir, '').count(os.sep)
    indent = ' ' * 4 * level
    if root != classified_dir:
        main_taxonomy.append(f"{indent}{os.path.basename(root)}/")
    else:
        main_taxonomy.append("classified/")
    subindent = ' ' * 4 * (level + 1)
    for fname in files:
        main_taxonomy.append(f"{subindent}{fname}")

with open(os.path.join(maps_dir_20260324, 'main-taxonomy.txt'), 'w') as fh:
    fh.write("\n".join(main_taxonomy))

with open(os.path.join(maps_dir_20260324, 'sliced-taxonomy.txt'), 'w') as fh:
    fh.write("No slices in mock dataset.\n")

with open(os.path.join(maps_dir_20260324, 'track-mods.txt'), 'w') as fh:
    fh.write("Mock dataset generation complete. No track mods required.\n")

mock_track_moods: dict[str, dict[str, object]] = {}
for entry in singles_files + albums_files:
    mock_track_moods[str(entry['filename'])] = {
        "artist": entry['artist'],
        "genre": entry['genre'],
        "moods": genres[str(entry['genre'])]
    }
with open(os.path.join(maps_dir_20260324, 'track-moods.json'), 'w') as fh:
    json.dump(mock_track_moods, fh, indent=2)

with open(os.path.join(maps_dir_20260324, 'track-moods.html'), 'w') as fh:
    fh.write("<html><body><h1>Mock Dataset Moods</h1><p>Replace with actual visualization if needed.</p></body></html>")


def build_tree_dict(path: str) -> dict[str, object]:
    tree: dict[str, object] = {}
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            tree[item + '/'] = build_tree_dict(item_path)
        else:
            tree[item] = os.path.getsize(item_path)
    return tree


mock_tree = build_tree_dict(classified_dir)

maps_base = os.path.join(BASE_DIR, 'docs', 'maps')
for root, _, files in os.walk(maps_base):
    for fname in files:
        if fname.endswith('.json') and fname != 'track-moods.json':
            with open(os.path.join(root, fname), 'w') as json_file:
                json.dump(mock_tree, json_file, indent=2)
        elif fname.endswith('.yml') or fname.endswith('.yaml'):
            if yaml:
                with open(os.path.join(root, fname), 'w') as yml_file:
                    yaml.dump(mock_tree, yml_file, default_flow_style=False)
            else:
                with open(os.path.join(root, fname), 'w') as yml_file:
                    yml_file.write("# Mock tree (yaml library not found)\n")

readme_mock_path = os.path.join(BASE_DIR, 'README-mock.md')
with open(readme_mock_path, 'w') as fh:
    fh.write(
        "# Mock Dataset\n\nThis dataset is a mock generation for public"
        " demonstration. The real files have been removed to avoid"
        " copyrighted or inappropriate names/content. Fictional artists,"
        " genres, and auFictional-Kw-27b20503 files have been"
        " deterministically generated.\n"
    )

tech_overview_path = os.path.join(BASE_DIR, 'docs', 'specifications', 'technical-overview.md')
if os.path.exists(tech_overview_path):
    with open(tech_overview_path, 'r') as fh:
        content: str = fh.read()
    if "MOCK DATASET" not in content:
        with open(tech_overview_path, 'w') as fh:
            fh.write("**NOTE: THIS PROJECT IS CURRENTLY USING A MOCK DATASET FOR PUBLIC DEMONSTRATION.**\n\n" + content)

print("Mock dataset generated successfully.")
