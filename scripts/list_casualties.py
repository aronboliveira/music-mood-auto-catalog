import urllib.parse
import re

with open("xbel_mp3s.txt") as fh:
    files: list[str] = fh.read().splitlines()

casualties: list[str] = []
for line in files:
    if line.startswith("file://"):
        path: str = urllib.parse.unquote(line[7:])
        base = path.split("/")[-1]

        # Determine if the base name after spaces replaced by dashes ends in -digit
        # e.g., "Building Mode
        # Fictional-Track-c4ca423Fictional-Track-c9f0f895.mp3" ->
        # "Fictional-Track-d182d04Fictional-Track-c9f0f895.mp3"
        sanitized = base.replace(" ", "-").replace("_", "-")
        if re.search(r'-[1-9]\.mp3$', sanitized):
            casualties.append(base)

for c in sorted(list(set(casualties))):
    print(c)
