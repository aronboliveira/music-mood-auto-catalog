import os
import re
import hashlib
import yaml

directories = ['docs', 'logs', 'scripts']
extensions = {'.txt', '.json', '.yml', '.yaml', '.html', '.md', '.js', '.log'}

EXPLICIT_WORDS = {
    'fuck': 'heck', 'shit': 'shoot', 'bitch': 'jerk', 'crap': 'junk',
    'damn': 'darn', 'asshole': 'meanie', 'pussy': 'cat', 'dick': 'stick',
    'torture': 'joyful', 'gang': 'group', 'giyangudansu': 'joyfuldance',
}

def get_fictional_name(real_name, prefix):
    h = hashlib.md5(real_name.encode()).hexdigest()
    return f"{prefix}_{h[:6]}"

all_files = []
for d in directories:
    for root, _, filenames in os.walk(d):
        for f in filenames:
            if any(f.endswith(ext) for ext in extensions):
                all_files.append(os.path.join(root, f))

artists = set()
taxonomy_path = 'docs/maps/20260324/main-taxonomy.txt'
if os.path.exists(taxonomy_path):
    with open(taxonomy_path, 'r', encoding='utf-8') as f:
        in_artist = False
        for line in f:
            if line.startswith('--- Artist ---'):
                in_artist = True
                continue
            if in_artist and line.startswith('---'):
                in_artist = False
            if in_artist:
                m = re.match(r'^\s+([A-Za-z0-9_\-\.]+):', line)
                if m:
                    artists.add(m.group(1))

mappings = {
    'AliceInChains': 'CosmicHarmonies',
    'aliceinchains': 'cosmicharmonies',
    'ACDC': 'ThePixelChords',
    'acdc': 'thepixelchords',
    'AC/DC': 'ThePixelChords',
    'Gang-Torture-Dance': 'Joyful-Dance',
    'BruceDickinson': 'BraveKnight',
    'Bruce-Dickinson': 'Brave-Knight',
}

for a in artists:
    if a not in mappings and a.lower() not in EXPLICIT_WORDS:
        mappings[a] = get_fictional_name(a, 'FictionalBand')

jojo_path = 'docs/guidelines/data/jojo-refs.yml'
if os.path.exists(jojo_path):
    with open(jojo_path, 'r', encoding='utf-8') as f:
        try:
            jojo_data = yaml.safe_load(f)
            if jojo_data:
                for k, v in jojo_data.items():
                    if isinstance(v, str) and ' - ' in v and '(http' in v:
                        mappings[v] = "FictionalBand - FictionalTrack (https://youtube.com/)"
        except Exception as e:
            print(f"Yaml parse error: {e}")

tracks = set()
for filepath in all_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            found = re.findall(r'([A-Za-z0-9_\-\.\(\)\[\]\']+\.mp3)', content)
            for t in found:
                tracks.add(t)
    except:
        pass

for t in tracks:
    if t not in mappings:
        base = t[:-4]
        mappings[t] = get_fictional_name(base, 'FictionalTrack') + '.mp3'

sorted_keys = sorted(mappings.keys(), key=len, reverse=True)

def replace_in_content(content, k, v):
    if len(k) <= 4 and k.isalpha():
        pattern = r'\b' + re.escape(k) + r'\b'
        return re.sub(pattern, v, content)
    else:
        return content.replace(k, v)

for filepath in all_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        orig_content = content
        
        for k in sorted_keys:
            content = replace_in_content(content, k, mappings[k])
            
        for bad_word, good_word in EXPLICIT_WORDS.items():
            pattern = re.compile(r'\b' + re.escape(bad_word) + r'\b', re.IGNORECASE)
            def replace_case(match):
                word = match.group(0)
                if word.isupper(): return good_word.upper()
                elif word.istitle(): return good_word.capitalize()
                return good_word
            content = pattern.sub(replace_case, content)
            
        if content != orig_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

print("Done.")