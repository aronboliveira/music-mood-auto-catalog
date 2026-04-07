import urllib.parse
import os

with open("xbel_mp3s.txt") as fh:
    files: list[str] = fh.read().splitlines()

missing: list[str] = []
for line in files:
    if line.startswith("file://"):
        path: str = urllib.parse.unquote(line[7:])
        if not os.path.exists(path):
            # Try to see if it matched standard sanitization in classified
            sanitized_name = os.path.basename(path).replace(" ", "-").replace("_", "-")
            # We can't know exactly where it was moved, but we know it was deleted if we can't find it
            missing.append(path)

print(f"Out of {len(files)} historical files, {len(missing)} paths are missing from their original locations")
with open("missing_from_xbel.txt", "w") as out:
    for m in missing:
        out.write(m + "\n")
