#!/usr/bin/env python3
"""
apply_third_pass.py  —  Third pass
====================================
Catches remaining real artist/song references that slipped through
the first two passes:
  - Artist names in HTML track labels (e.g., "Blink 182 All The Small Things")
  - Song titles appearing without artist prefix
  - Performer names (e.g., "Magdalena Pedarnig")
  - Various case/spacing variants

Uses the same deterministic Fictional-Kw-{hash} naming as pass 2.

Usage:
    python scripts/apply_third_pass.py --dry-run
    python scripts/apply_third_pass.py
"""
from __future__ import annotations
import hashlib
import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
THIS_SCRIPT = Path(__file__).resolve()
SCRIPT2 = PROJECT_ROOT / "scripts" / "apply_keyword_scrub.py"
SCRIPT1 = PROJECT_ROOT / "scripts" / "apply_fictional_names.py"
DRY_RUN = "--dry-run" in sys.argv

SKIP_DIRS = {".venv", ".git", "node_modules", "__pycache__", ".mypy_cache"}
TEXT_EXTS = {
    ".py", ".json", ".yaml", ".yml", ".txt", ".md",
    ".csv", ".cfg", ".ini", ".toml", ".sh", ".bat",
    ".js", ".html", ".css", ".log",
}


def _is_processable(fpath: Path) -> bool:
    if fpath.suffix in TEXT_EXTS:
        return True
    return any(s in TEXT_EXTS for s in fpath.suffixes)


def _iter_project_files():
    for dirpath, dirnames, filenames in os.walk(PROJECT_ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            yield Path(dirpath) / fn


def _fict_kw(original: str) -> str:
    h = hashlib.md5(original.encode()).hexdigest()[:8]
    return f"Fictional-Kw-{h}"

# ━━━━━━━━━━━━━━━━━━━━━━ REPLACEMENTS ━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Each tuple: (pattern_string, replacement)
# Patterns are matched case-insensitively with word boundaries where safe.
# Longer patterns first to prevent partial matches.


ARTIST_NAMES = [
    # Multi-word (longest first)
    "Avenged Sevenfold",
    "Ariana Grande",
    "Bright Eyes",
    "Bruno Mars",
    "Bryan Adams",
    "Bill Bruford",
    "Bill Withers",
    "Billy Joel",
    "Bob Seger",
    "Brian Eno",
    "Belle & Sebastian",
    "Bernard Herrmann",
    "Bon Iver",
    "Bon Jovi",
    "Bruce Springsteen",
    "Carl Orff",
    "Cat Stevens",
    "Capital Inicial",
    "Charlie Brown Jr",
    "Chris Isaak",
    "Chuck Berry",
    "Claude Debussy",
    "Daft Punk",
    "Deep Purple",
    "Dolly Parton",
    "Don Gibson",
    "Don Henley",
    "Don McLean",
    "Dream Theater",
    "Édith Piaf",
    "Ed Sheeran",
    "Electric Light Orchestra",
    "Emerson, Lake & Palmer",
    "Eric Whitacre",
    "Erik Satie",
    "Etta James",
    "Fleetwood Mac",
    "Foo Fighters",
    "Frank Sinatra",
    "Frankie Valli",
    "Fundo de Quintal",
    "Gary Jules",
    "Green Day",
    "Holland K Smith",
    "Iron Maiden",
    "Israel Kamakawiwoʻole",
    "Israel Kamakawiwo'ole",
    "Jack Johnson",
    "Jethro Tull",
    "Joe Satriani",
    "John Mayer",
    "John Williams",
    "Joni Mitchell",
    "Judas Priest",
    "Kate Bush",
    "Katrina and the Waves",
    "King Crimson",
    "Klaus Badelt",
    "Lady Gaga",
    "Lalo Schifrin",
    "Led Zeppelin",
    "Leonard Cohen",
    "Leon Bridges",
    "Linkin Park",
    "Loggins & Messina",
    "Louis Armstrong",
    "Ludovico Einaudi",
    "Magdalena Pedarnig",
    "Manchester Orchestra",
    "Marconi Union",
    "Mark Ronson",
    "Maroon 5",
    "Martin O'Donnell",
    "Marvin Gaye",
    "Massive Attack",
    "Max Richter",
    "Michael Jackson",
    "Mike Oldfield",
    "Miles Davis",
    "Nat King Cole",
    "Nine Inch Nails",
    "Of Monsters and Men",
    "Papa Roach",
    "Pearl Jam",
    "Peter Gabriel",
    "Pharrell Williams",
    "Phil Collins",
    "Philip Glass",
    "Pink Floyd",
    "Rage Against",
    "Red Hot Chili Peppers",
    "Richard Strauss",
    "R. Kelly",
    "Rolling Stones",
    "Saint-Saëns",
    "Sam Smith",
    "Samuel Barber",
    "Simon & Garfunkel",
    "Sinéad O'Connor",
    "Stevie Wonder",
    "Suzi Quatro",
    "System of a Down",
    "Taylor Swift",
    "Tears for Fears",
    "The Cure",
    "The Killers",
    "The O'Jays",
    "The Prodigy",
    "The Smiths",
    "The Weeknd",
    "The White Stripes",
    "Tim Maia",
    "Two Steps from Hell",
    "T. Rex",
    "Van Halen",
    "Whitney Houston",
    "Yann Tiersen",
    "ZZ Top",
    # Two-word or specific forms
    "Amy Winehouse",
    "Aphex Twin",
    "Arvo Pärt",
    "Blink 182",
    "Blink-182",
    "Blink182",
    "Bob Marley",
    "Bright Eyes",
    # Single-word (need \b boundaries)
    "ABBA",
    "Akon",
    "Beethoven",
    "Caramell",
    "Chic",
    "Debussy",
    "Disney",
    "Duffy",
    "Eagles",
    "ELO",
    "Eminem",
    "Enya",
    "Europe",
    "Evanescence",
    "Extreme",
    "Gorillaz",
    "Grieg",
    "Hawkwind",
    "Jay-Z",
    "Journey",
    "Kansas",
    "Korn",
    "Live",
    "Megadeth",
    "Mineral",
    "Moby",
    "Mozart",
    "Muse",
    "Nightwish",
    "Normani",
    "Oasis",
    "Outkast",
    "Passenger",
    "Perfume",
    "Prince",
    "Rammstein",
    "Rainbow",
    "Ratt",
    "Rihanna",
    "Sabaton",
    "Schubert",
    "Scorpions",
    "Slayer",
    "Sting",
    "Stratovarius",
    "Supertramp",
    "Surface",
    "Tool",
    "Trivium",
    "Tycho",
    "U2",
    "Vivaldi",
    "SpongeBob",
]

SONG_TITLES = [
    "Somewhere Over the Rainbow",
    "Sharp Dressed Man",
    "Scar Tissue",
    "Purple Rain",
    "Hotel California",
    "Sound of Silence",
    "The Sound of Silence",
    "Orinoco Flow",
    "californication",
    "under the bridge",
    "somewhere over the rainbow",
    "what a wonderful world",
]

# Additional performer/artist names not in ARTIST_NAMES above
EXTRA_PERFORMERS = [
    "Israel Kamakawiwoʻole",
    "Israel Kamakawiwo'ole",
    "Joe Satriani",
]

# Concatenated / hyphenated artist forms as dict keys in gen_moods_checks.py
CONCAT_ARTIST_FORMS = [
    "avenged-sevenfold", "avengedsevenfold",
    "bobmarley", "bob-marley",
    "bon-jovi", "bonjovi",
    "bruce-springsteen", "brucespringsteen",
    "bruno-mars", "brunomars",
    "capitalinicial", "capital-inicial",
    "charlie-brown-jr", "charliebrownjr",
    "chuck-berry", "chuckberry",
    "daft-punk", "daftpunk",
    "deep-purple", "deeppurple",
    "foo-fighters", "foofighters",
    "franksinatra", "frank-sinatra",
    "fundo-de-quintal", "fundodequintal",
    "green-day", "greenday",
    "iron-maiden", "ironmaiden",
    "jack-johnson", "jackjohnson",
    "jethro-tull", "jethrotull",
    "judaspriest", "judas-priest",
    "ledzeppelin", "led-zeppelin",
    "linkin-park", "linkinpark",
    "ls-jack", "lsjack",
    "marvin-gaye", "marvingaye",
    "massive-attack", "massiveattack",
    "michael-jackson", "michaeljackson",
    "ne-yo", "neyo",
    "nine-inch-nails",
    "pearl-jam", "pearljam",
    "philcollins", "phil-collins",
    "pink-floyd", "pinkfloyd",
    "rage-against", "rageagainst",
    "red-hot-chili-peppers", "redhotchilipeppers",
    "rolling-stones", "rollingstones",
    "sam-smith", "samsmith",
    "steviewonder", "stevie-wonder",
    "summer-eletrohits", "summereletrohits",
    "system-of-a-down", "systemofadown",
    "the-cure", "thecure",
    "the-smiths", "thesmiths",
    "tim-maia", "timmaia",
    "van-halen", "vanhalen",
    "whitney-houston", "whitneyhouston",
]

# Common English words that happen to be band names — skip globally
# "tool", "death", "sleep", "rush", "yes", "genesis", "venom", "exodus"
# These are only replaced in targeted file-specific fixes below.


def build_replacements():
    """Build list of (compiled_regex, replacement_string) tuples."""
    rules = []
    # Combine all entries
    all_entries = []
    for name in ARTIST_NAMES:
        all_entries.append(name)
    for title in SONG_TITLES:
        all_entries.append(title)
    for perf in EXTRA_PERFORMERS:
        all_entries.append(perf)
    for concat in CONCAT_ARTIST_FORMS:
        all_entries.append(concat)

    # Deduplicate (case-insensitive)
    seen = set()
    deduped = []
    for e in all_entries:
        key = e.lower()
        if key not in seen:
            seen.add(key)
            deduped.append(e)

    # Sort longest first
    deduped.sort(key=lambda x: -len(x))

    # Ambiguous single words that are also common English — skip global replacement
    # Only match these in music-reference contexts (after – or as dict key)
    AMBIGUOUS = {"live", "can", "nin", "rem", "elo", "chic", "ratt",
                 "surface", "tool", "extreme", "mineral", "disney",
                 "europe", "perfume"}

    for entry in deduped:
        repl = _fict_kw(entry.lower().strip())
        escaped = re.escape(entry)
        if entry.lower() in AMBIGUOUS:
            # Only match in music-reference contexts: "Artist - Song" or dict key
            # or in moods-guide.json examples
            pattern = rf'(?:(?<=– )|(?<=")|(?<=: "))\b{escaped}\b'
        else:
            pattern = rf'\b{escaped}\b'
        # Store the raw keyword for pre-filtering (not the full regex)
        rules.append((re.compile(pattern, re.IGNORECASE), repl, entry.lower()))

    return rules


def process_file(fpath: Path, rules):
    """Apply all replacement rules to a file. Returns True if modified."""
    if fpath.resolve() in (THIS_SCRIPT.resolve(), SCRIPT1.resolve(), SCRIPT2.resolve()):
        return False
    if not _is_processable(fpath):
        return False
    try:
        content = fpath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return False

    original = content
    content_lower = content.lower()

    # Pre-filter: only apply rules whose keywords appear in the file
    for regex, repl, raw_kw in rules:
        if raw_kw not in content_lower:
            continue
        content = regex.sub(repl, content)

    if content != original:
        if not DRY_RUN:
            fpath.write_text(content, encoding="utf-8")
        return True
    return False


def fix_targeted_dict_keys():
    """Targeted fix: replace ambiguous band names when used as dict keys."""
    fpath = PROJECT_ROOT / "scripts" / "gen_moods_checks.py"
    if not fpath.exists():
        return False
    content = fpath.read_text(encoding="utf-8", errors="replace")
    original = content

    # Ambiguous words that are band names when used as dict keys
    ambiguous_bands = ["tool", "journey", "kansas", "europe", "extreme",
                       "prince", "rainbow", "live", "nin", "rem", "u2",
                       "enya"]
    for band in ambiguous_bands:
        repl = _fict_kw(band)
        content = re.sub(
            rf'"{re.escape(band)}"(\s*:\s*\[)',
            f'"{repl}"\\1',
            content
        )

    if content != original:
        if not DRY_RUN:
            fpath.write_text(content, encoding="utf-8")
        return True
    return False


def main():
    rules = build_replacements()
    print(f"Third pass: {len(rules)} replacement rules")
    print(f"Mode: {'DRY RUN' if DRY_RUN else 'APPLY'}")
    print()

    scanned = 0
    modified = 0
    modified_files = []

    for fpath in _iter_project_files():
        if not _is_processable(fpath):
            continue
        scanned += 1
        if process_file(fpath, rules):
            modified += 1
            modified_files.append(str(fpath.relative_to(PROJECT_ROOT)))

    # Targeted fixes
    if fix_targeted_dict_keys():
        modified += 1
        modified_files.append("scripts/gen_moods_checks.py (targeted dict keys)")

    print(f"Scanned {scanned} files, modified {modified}")
    if modified_files:
        print("\nModified files:")
        for f in sorted(modified_files):
            print(f"  {f}")


if __name__ == "__main__":
    main()
