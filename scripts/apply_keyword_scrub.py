#!/usr/bin/env python3
"""
apply_keyword_scrub.py  —  Second pass
=======================================
Replaces remaining real artist names, song titles, and copyrighted
keyword strings that the first pass (apply_fictional_names.py) missed.

The first pass handled PascalCase artist IDs and their text forms.
This pass handles:
  1. Remaining lowercase artist names used as classification keywords
  2. Song title keywords inside ARTIST_KEYWORDS / GENRE_KEYWORDS / MOOD_KEYWORDS
  3. Artist/song examples in moods-guide.json and gen_moods_checks.py
  4. Real person names (composers, performers) used as keywords

It does NOT touch genres, moods, instruments, or structural code.

Usage:
    python scripts/apply_keyword_scrub.py --dry-run
    python scripts/apply_keyword_scrub.py
"""
from __future__ import annotations
import hashlib
import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
THIS_SCRIPT = Path(__file__).resolve()
DRY_RUN = "--dry-run" in sys.argv

# ── directories / extensions to skip ──────────────────────────────
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

# ── deterministic fictional keyword ──────────────────────────────


def _fict_kw(original: str) -> str:
    """Produce Fictional-Kw-{8-char hash} from original string."""
    h = hashlib.md5(original.encode()).hexdigest()[:8]
    return f"Fictional-Kw-{h}"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# KNOWN REMAINING REAL ARTIST NAMES  (not PascalCase IDs)
# These appear as lowercase keyword strings in genre/mood dicts.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXTRA_ARTIST_NAMES = [
    # Rock / Metal / Alternative
    "queen", "radiohead", "coldplay", "soundgarden", "led zeppelin",
    "judas priest", "genesis", "rush", "adele", "anthrax",
    "accept", "bob marley", "elvis", "stevie wonder", "james brown",
    "phil collins", "david wise", "david bowie", "jimi hendrix",
    "eric clapton", "johnny cash", "frank sinatra", "ray charles",
    "bob dylan", "three days grace", "killswitch engage", "blind guardian",
    "jerry cantrell", "layne staley", "chuck schuldiner", "eddie vedder",
    "cornell", "klaus meine", "hetfield", "dimebag", "corey taylor",
    "ozzy", "james hetfield", "kirk hammett", "lars ulrich",
    "dave mustaine", "bruce dickinson", "rob halford", "dio",
    "ronnie james dio", "ac-dc", "ac dc", "aliceinchains",
    "alice-in-chains", "grant kirkhope",
    # Brazilian / Latin
    "legiao urbana", "cbjr", "capital inicial",
    # Game/anime composers that weren't PascalCase IDs
    "koji kondo", "nobuo uematsu", "yoko shimomura",
    "david wise", "grant kirkhope", "hiroyuki sawano",
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# KNOWN REMAINING SONG TITLES  (used as keyword strings)
# Only the UNAMBIGUOUS ones ≥ 4 chars that clearly identify a song.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXTRA_SONG_TITLES = [
    # Long / distinctive titles
    "a place for my head", "smells like teen spirit", "come as you are",
    "enter sandman", "master of puppets", "welcome to the jungle",
    "sweet child o' mine", "bohemian rhapsody", "stairway to heaven",
    "through the fire and flames", "twilight of the thunder god",
    "shine on you crazy diamond", "the less i know the better",
    "every time i close my eyes", "it's the end of the world",
    "ain't talkin' 'bout love", "crazy noisy bizarre town",
    "don't look back in anger", "the way you make me feel",
    "they don't care about us", "the only thing they fear is you",
    "the only thing they fear", "all these things i hate",
    "fight for all the wrong", "smells like teen spirit",
    "down with the sickness", "dude looks like a lady",
    "hearts burst into fire", "love ain't no stranger",
    "runnin' with the devil", "blood sugar sex magik",
    "dark side of the moon", "don't dream it's over",
    "nights in white satin", "stickerbrush symphony",
    "stickerbush symphony", "vicinity of obscenity",
    "bittersweet memories", "pretty on the outside",
    "burning down the house",
    # Medium-length titles
    "before i forget", "bleed the freak", "come as you are",
    "dani california", "dancing queen", "mamma mia", "rasputin",
    "figured you out", "follow you home", "forged in blood",
    "here i go again", "man on the moon", "meaning of life",
    "misery business", "one step closer", "open your heart",
    "pushing me away", "smooth criminal", "the zephyr song",
    "tippa my tongue", "violence fetish", "your betrayal",
    "american idiot", "down in a hole", "dam that river",
    "february stars", "fool for your loving", "helter skelter",
    "holy mountains", "i will not bow", "il vento d'oro",
    "jailhouse rock", "man in the box", "the devil in i",
    "the last fight", "the one i love", "vampire killer",
    "bloody stream", "bramble blast", "cries in vain",
    "dance of gold", "diary of jane", "easier to run",
    "evil papagali", "fighting gold", "fortune faded",
    "higher ground", "hit the floor", "knock me down",
    "like a prayer", "monkey wrench", "paradise city",
    "path of tears", "rock with you", "say goodnight",
    "strip my mind", "the butterfly", "the lazy song",
    "the pretender", "torture dance", "until the end",
    "wonder of you", "black summer", "bloody tears",
    "carrying you", "dancing dead",
    "bfg division", "heart-shaped box",
    "don't follow", "losing my religion", "jesus of suburbia",
    "holiday in cambodia", "points of authority",
    "a place for my head", "dancing in the dark",
    "sweet little sixteen", "roll over beethoven",
    "iron-blue intention", "walking after you",
    "you could be mine", "working for the weekend",
    "sultans of swing", "southbound again", "setting me up",
    "tears of the dragon", "flash of the blade",
    "hail to the king", "shepherd of fire",
    "almost easy", "bat country", "thick as a brick",
    "times like these", "under the bridge",
    "tears don't fall", "what's my age again",
    "cheap day return", "bring me to life",
    "haruka kanata", "i gotta feeling", "three little birds",
    "californication", "dark necessities", "desecration smile",
    "breaking the girl", "soul to squeeze", "universally speaking",
    "snow hey oh", "the beautiful people", "all my life",
    "hey, johnny park!", "i'll stick around", "imitation of life",
    "locomotive breath", "lost in hollywood",
    "man in the mirror", "heaven beside you",
    "angry again", "fly on the wall", "hail from the past",
    "heroes of our time", "it ain't like that",
    "still of the night", "down to the waterline",
    "the tragic prince", "divine bloodlines",
    "violent pornography", "sugar", "toxicity", "aerials",
    "chop suey", "psychosocial", "duality", "holy wars",
    "numb", "crawling", "faint", "in the end",
    "rooster", "nutshell", "rockstar", "feelin' way too damn",
    "aces high", "anna julia", "primeiros erros",
    "ainda bem", "lanterna dos afogados", "palavras ao vento",
    "suplica cearense", "tarde de outubro",
    "depois da meia noite", "meu bem querer", "vinheta da silva",
    "gostoso veneno", "farpa cortante", "ancora te amo",
    "monstro invisivel", "meu mundo e o barro",
    "todas as noites", "cristo e oxala", "words ao vento",
    "johnny b. goode", "born in the u.s.a.",
    "24k magic", "just the way you are", "locked out of heaven",
    "zip-a-dee-doo-dah", "amazing grace", "bach cello suite",
    "adam lay ybounden", "clint eastwood",
    "eye of the tiger",
    # Fictional-Jozep / anime song refs
    "il vento d'oro", "fighting gold", "bloody stream",
    "crazy noisy bizarre town",
    # Clearly identifiable shorter titles
    "creep", "paranoid", "sandman",
    "closer", "photograph", "savin' me",
    "rockstar", "someday", "animals",
    "lick your fingers clean",
    "a whiter shade of pale",
    "yakety sax", "chanson d'amour",
    "l'amour toujours",
    "mayonaka no door",
    "flyday chinatown",
    "tenjin no ongaku",
    "rouge no dengon",
    "sayonara no natsu",
    "shiteipotsupu",
    "inochi no kioku",
    "itsumo nando demo",
    "kimi wo nosete",
    # Known album refs
    "dark side of the moon", "blood sugar sex magik",
    "...and justice", "and justice",
    "4 words (to choke upon)", "4:00 am", "4_00 am",
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Game / anime / franchise references (remaining lowercase keywords)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXTRA_GAME_ANIME_REFS = [
    "animal crossing", "ocarina of time", "breath of the wild",
    "twilight princess", "tears of the kingdom",
    "gerudo valley", "kakariko village", "lon lon ranch",
    "great fairy fountain", "fairy fountain", "stone tower temple",
    "ballad of the goddess", "song of healing", "outset island",
    "ganondorf", "hyrule", "majora's mask",
    "dracula's castle", "lost painting",
    "spiral mountain", "mad monster mansion",
    "gangplank galleon", "aquatic ambiance", "mining melancholy",
    "bramble blast", "in a snow-bound land", "krook's march",
    "stickerbush symphony", "stickerbrush symphony",
    "jolly roger's lagoon", "gobi's valley",
    "angel island zone", "dire dire docks",
    "escape from the city", "sunset heights",
    "world's hardest game",
    "wrath of the lich king", "legends of azeroth",
    "shaping of the world", "totems of the grizzlemaw",
    "lament of the highborne", "darkmoon faire",
    "stormwind theme", "ahn'qiraj",
    "dragon's rest",
    "legend of ashitaka", "ashitaka and san",
    "howl's moving castle", "kiki's delivery",
    "spirited away", "castle in the sky",
    "when marnie was", "fine on the outside",
    "molgera battle",
    "revali's theme", "midna's lament",
    "concerning hobbits",
    "ynis avalach", "departure to the west",
    "eight melodies",
    "digital devil",
    "beginning fictional-emeraldwarden",
    "mysterious destiny",
    "sadness and sorrow",
    "encrusted forest",
]

# ── Strings to NEVER replace (genre, mood, instrument, common English) ──
KEEP_STRINGS = {
    # Genres / subgenres / styles
    "rock", "metal", "pop", "jazz", "blues", "funk", "soul", "reggae",
    "punk", "grunge", "classical", "ambient", "electronic", "techno",
    "house", "trance", "hip hop", "hip-hop", "rap", "country", "folk",
    "disco", "ska", "swing", "bossa", "samba", "mpb", "indie",
    "alternative", "progressive", "industrial", "cyberpunk", "lo-fi",
    "lofi", "darkwave", "synthwave", "vaporwave", "chillwave",
    "post punk", "post rock", "post grunge", "nu metal", "doom metal",
    "death metal", "black metal", "power metal", "speed metal",
    "thrash metal", "heavy metal", "glam metal", "hair metal",
    "progressive rock", "progressive metal", "industrial metal",
    "southern rock", "hard rock", "soft rock", "classic rock",
    "alt rock", "garage rock", "psychedelic", "acoustic",
    "drum and bass", "world music", "new wave", "new age",
    "christian", "gospel", "praise", "worship", "spiritual",
    "medieval", "celtic", "arabic", "asian", "japanese", "korean",
    "chinese", "indian", "african", "latin", "brazilian",
    "animerock", "anime", "game ost", "ost",
    # Moods / emotions
    "aggressive", "melancholic", "cheerful", "peaceful", "dark",
    "bright", "energetic", "calm", "nostalgic", "romantic",
    "triumphant", "epic", "brooding", "gritty", "dreamy",
    "ethereal", "introspective", "anguish", "angelic", "anxiety",
    "anxious", "bittersweet", "blissful", "contemplative",
    "defiant", "dramatic", "ecstatic", "euphoric", "fierce",
    "frantic", "gentle", "gloomy", "haunting", "hopeful",
    "intense", "joyful", "manic", "mysterious", "optimistic",
    "ominous", "passionate", "playful", "rebellious", "reflective",
    "resentful", "restless", "serene", "somber", "solemn",
    "tender", "tragic", "turbulent", "upbeat", "vengeful",
    "wistful", "yearn", "yearning", "wonderful", "whimsical",
    # Common English words that should never be replaced
    "adventure", "again", "alone", "beautiful", "broken", "burning",
    "change", "crazy", "dead", "devil", "dragon", "dream", "endless",
    "eternal", "fallen", "fire", "forgotten", "freedom", "garden",
    "glory", "gold", "heaven", "hero", "home", "hope", "king",
    "knight", "legend", "light", "lost", "love", "maiden", "mirror",
    "monster", "mountain", "night", "ocean", "pain", "paradise",
    "phantom", "prayer", "rain", "shadow", "silence", "silver",
    "sky", "snow", "song", "spirit", "storm", "sun", "sword",
    "tears", "temple", "thunder", "tower", "twilight", "war",
    "warrior", "water", "wild", "wind", "winter", "wolf", "world",
    "agony", "anarchy", "anonymous", "aeroplane", "airglow",
    "amado", "another way", "working", "worker", "yoga", "zither",
    # Structural/code
    "utf-8", "keywords", "weight", "boost", "name", "path", "key",
    "value", "type", "albums", "singles", "classified",
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# BUILD REPLACEMENT TABLE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def build_keyword_table() -> dict[str, str]:
    table: dict[str, str] = {}

    # Add extra artist names
    for name in EXTRA_ARTIST_NAMES:
        name = name.strip().lower()
        if name and name not in KEEP_STRINGS:
            if name not in table:
                table[name] = _fict_kw(name)

    # Add song titles
    for title in EXTRA_SONG_TITLES:
        title = title.strip().lower()
        if title and title not in KEEP_STRINGS:
            if title not in table:
                table[title] = _fict_kw(title)

    # Add game/anime refs
    for ref in EXTRA_GAME_ANIME_REFS:
        ref = ref.strip().lower()
        if ref and ref not in KEEP_STRINGS:
            if ref not in table:
                table[ref] = _fict_kw(ref)

    # Also add title-case and original-case variants
    extra = {}
    for k, v in list(table.items()):
        # Title Case
        tc = k.title()
        if tc not in table and tc.lower() not in KEEP_STRINGS:
            extra[tc] = v
        # As-typed (preserve original casing from the source lists)
        # First-letter caps
        fc = k[0].upper() + k[1:] if k else k
        if fc not in table and fc not in extra:
            extra[fc] = v
        # ALL CAPS for short names
        uc = k.upper()
        if len(k) <= 20 and uc not in table and uc not in extra:
            extra[uc] = v
        # Hyphenated
        hyp = k.replace(" ", "-")
        if hyp != k and hyp not in table and hyp not in extra:
            extra[hyp] = v
        hyp_tc = hyp.title()
        if hyp_tc not in table and hyp_tc not in extra:
            extra[hyp_tc] = v

    table.update(extra)

    # Sort longest-first to avoid partial matches
    return dict(sorted(table.items(), key=lambda x: -len(x[0])))


def build_keyword_index(table: dict[str, str]):
    """Build a fast lookup structure: list of (lowercase_key, replacement) sorted longest-first."""
    entries = []
    seen = set()
    for k, v in table.items():
        low = k.lower()
        if low not in seen:
            seen.add(low)
            entries.append((low, v))
    entries.sort(key=lambda x: -len(x[0]))
    return entries


def process_file(fpath: Path, entries: list, dry_run: bool) -> bool:
    """Replace keyword occurrences in a text file. Returns True if modified."""
    try:
        content = fpath.read_text(encoding="utf-8")
    except Exception:
        return False

    content_lower = content.lower()

    # First pass: find which keywords are present in this file
    present = [(kw, repl) for kw, repl in entries if kw in content_lower]
    if not present:
        return False

    # Apply replacements longest-first using case-insensitive regex
    new_content = content
    for kw, repl in present:
        new_content = re.sub(re.escape(kw), repl, new_content, flags=re.IGNORECASE)

    if new_content != content:
        if dry_run:
            print(f"  [DRY-RUN] Would modify: {fpath}")
        else:
            fpath.write_text(new_content, encoding="utf-8")
            print(f"  [MODIFIED] {fpath}")
        return True
    return False


def main():
    mode = "DRY RUN" if DRY_RUN else "LIVE"
    print("=" * 70)
    print("  KEYWORD SCRUB (second pass)")
    print(f"  Mode: {mode}")
    print("=" * 70)
    print()

    print("[1/2] Building keyword replacement table...")
    table = build_keyword_table()
    print(f"  {len(table)} keyword replacement rules")
    print("  Building index...")
    entries = build_keyword_index(table)
    print(f"  {len(entries)} unique lowercase entries")
    print()

    print(f"[2/2] Processing files in {PROJECT_ROOT}")
    scanned = 0
    modified = 0

    for fpath in sorted(_iter_project_files()):
        if not fpath.is_file():
            continue
        if not _is_processable(fpath):
            continue
        if fpath.resolve() == THIS_SCRIPT:
            continue
        # Also skip the first-pass script
        if fpath.name == "apply_fictional_names.py":
            continue

        scanned += 1
        if process_file(fpath, entries, DRY_RUN):
            modified += 1

    print("\n--- Summary ---")
    print(f"  Files scanned:  {scanned}")
    print(f"  Files modified: {modified}")
    if DRY_RUN:
        print("  (DRY RUN — no files were actually changed)")
    print("\nDone.")


if __name__ == "__main__":
    main()
