import os
import re
import hashlib
import yaml

directories = ['docs', 'logs', 'scripts']
extensions = {'.txt', '.json', '.yml', '.yaml', '.html', '.md', '.js', '.log'}

EXPLICIT_WORDS: dict[str, str] = {
    'fuck': 'heck', 'shit': 'shoot', 'bitch': 'jerk', 'crap': 'junk',
    'damn': 'darn', 'asshole': 'meanie', 'pussy': 'cat', 'dick': 'stick',
    'torture': 'joyful', 'gang': 'group', 'giyangudansu': 'joyfuldance',
}


def get_fictional_name(real_name: str, prefix: str) -> str:
    h: str = hashlib.md5(real_name.encode()).hexdigest()
    return f"{prefix}_{h[:6]}"


all_files: list[str] = []
for d in directories:
    for root, _, filenames in os.walk(d):
        for fname in filenames:
            if any(fname.endswith(ext) for ext in extensions):
                all_files.append(os.path.join(root, fname))

artists: set[str] = set()
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

mappings: dict[str, str] = {
    'Fictional-ZincWing': 'CosmicHarmonies',
    'Fictional-Kw-7639c53e': 'cosmicharmonies',
    'Fictional-BrassTide': 'ThePixelChords',
    'Gang-Fictional-Kw-59cdce6d': 'Joyful-Dance',
    'Fictional-PhantomRaven': 'Fictional-PhantomRaven',
}

for a in artists:
    if a not in mappings and a.lower() not in EXPLICIT_WORDS:
        mappings[a] = get_fictional_name(a, 'FictionalBand')

jozep_path = 'docs/guidelines/data/jozep-refs.yml'
if os.path.exists(jozep_path):
    with open(jozep_path, 'r', encoding='utf-8') as f:
        try:
            jozep_data = yaml.safe_load(f)
            if jozep_data:
                for k, v in jozep_data.items():
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
    except Exception:
        pass

for t in tracks:
    if t not in mappings:
        base = t[:-4]
        mappings[t] = get_fictional_name(base, 'FictionalTrack') + '.mp3'

sorted_keys: list[str] = sorted(mappings.keys(), key=len, reverse=True)


def replace_in_content(content: str, k: str, v: str) -> str:
    if len(k) <= 4 and k.isalpha():
        pattern: str = r'\b' + re.escape(k) + r'\b'
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

            def replace_case(match: re.Match[str]) -> str:
                word: str = match.group(0)
                if word.isupper():
                    return good_word.upper()
                elif word.istitle():
                    return good_word.capitalize()
                return good_word

            content = pattern.sub(replace_case, content)

        if content != orig_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

print("Done.")
