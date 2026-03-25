import os
import json

songs = []
for f in os.listdir("classified/singles/Artist/Various"):
    if f.endswith(".mp3"):
        songs.append(f)
songs.sort()
print(json.dumps(songs, indent=2))
