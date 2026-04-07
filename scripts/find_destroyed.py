import urllib.parse
import os

with open("xbel_mp3s.txt") as fh:
    files: list[str] = fh.read().splitlines()

# Gather all current existing files
current_files: set[str] = set()
for root, dirs, dir_files in os.walk("classified"):
    for file in dir_files:
        if file.endswith(".mp3"):
            current_files.add(file)

destroyed: list[str] = []
for line in files:
    if line.startswith("file://"):
        path: str = urllib.parse.unquote(line[7:])
        base = os.path.basename(path)
        # Apply standard sanitization to see what the name would be now
        sanitized = base.replace(" ", "-").replace("_", "-")
        # remove multiple dashes
        while "--" in sanitized:
            sanitized = sanitized.replace("--", "-")

        # Check if this sanitized basename exists in the current system
        found = False
        for current_name in current_files:
            # We do a loose match or exact match
            if (sanitized.lower() == current_name.lower()
                    or current_name.lower().startswith(
                        sanitized.lower().replace(".mp3", ""))):
                found = True
                break

        if not found:
            destroyed.append(base)

destroyed = list(set(destroyed))
print(f"Actually completely missing: {len(destroyed)}")
for d in sorted(destroyed):
    print(" -", d)
