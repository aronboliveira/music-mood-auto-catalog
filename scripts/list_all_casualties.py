import urllib.parse
import re

with open("xbel_mp3s.txt") as fh:
    files: list[str] = fh.read().splitlines()

for line in files:
    if line.startswith("file://"):
        path: str = urllib.parse.unquote(line[7:])
        base = path.split("/")[-1]

        # Apply the exact sanitization rule that was used to place them in classified
        sanitized = base.replace(" ", "-").replace("_", "-")
        while "--" in sanitized:
            sanitized = sanitized.replace("--", "-")

        if re.search(r'-[1-9]\.mp3$', sanitized):
            print(base)
