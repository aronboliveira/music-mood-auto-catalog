import urllib.parse
import os

with open("xbel_mp3s.txt") as f:
    files = f.read().splitlines()

# Gather all current existing files
current_files = set()
for root, dirs, f in os.walk("classified"):
    for file in f:
        if file.endswith(".mp3"):
            current_files.add(file)

destroyed = []
for f in files:
    if f.startswith("file://"):
        path = urllib.parse.unquote(f[7:])
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
            if current_name.replace(".mp3", "") == sanitized_base:
                found = True
                break
        
        if not found:
            destroyed.append(base)

destroyed = list(set(destroyed))
print(f"Actually completely missing: {len(destroyed)}")
for d in sorted(destroyed):
    print(" -", d)
