import urllib.parse
import re

with open("xbel_mp3s.txt") as f:
    files = f.read().splitlines()

casualties = []
for f in files:
    if f.startswith("file://"):
        path = urllib.parse.unquote(f[7:])
        base = path.split("/")[-1]
        
        # Determine if the base name after spaces replaced by dashes ends in -digit
        sanitized = base.replace(" ", "-").replace("_", "-")
        if re.search(r'-[1-9]\.mp3$', sanitized):
            casualties.append(base)

for c in sorted(list(set(casualties))):
    print(c)
