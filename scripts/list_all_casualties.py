import urllib.parse
import re

with open("xbel_mp3s.txt") as f:
    files = f.read().splitlines()

for f in files:
    if f.startswith("file://"):
        path = urllib.parse.unquote(f[7:])
        base = path.split("/")[-1]
        
        # Apply the exact sanitization rule that was used to place them in classified
        sanitized = base.replace(" ", "-").replace("_", "-")
        while "--" in sanitized:
            sanitized = sanitized.replace("--", "-")
            
        if re.search(r'-[1-9]\.mp3$', sanitized):
            print(base)

