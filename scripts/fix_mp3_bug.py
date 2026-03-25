import os
import re

dir_path = "scripts"
pattern = re.compile(r'FictionalBand - rock-song-[a-f0-9]{6}\.mp3')
count = 0
for filename in os.listdir(dir_path):
    if filename.endswith(".py"):
        filepath = os.path.join(dir_path, filename)
        with open(filepath, "r") as f:
            content = f.read()
        
        new_content, n = pattern.subn('.mp3', content)
        if n > 0:
            with open(filepath, "w") as f:
                f.write(new_content)
            count += n

print(f"Replaced {count} instances.")
