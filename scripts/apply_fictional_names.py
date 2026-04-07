#!/usr/bin/env python3
"""
apply_fictional_names.py
========================
Mass-replace every real artist name, track title, and album reference
across ALL workspace files with deterministic Fictional-* names.

Rules
-----
- Genres stay real  (AlternativeRock, Grunge, MPB, …)
- Moods  stay real  (Melancholic, Aggressive, Chill, …)
- Instrument names stay real (Gayageum, Guzheng, Guqin, Koto)
- Genre-label compilation buckets stay real
  (CityPop, JungleDnB, MedievalAmbience, DarkAngelMetal, …)
- Everything else (artist names, game/anime franchises,
  track titles, album names, keyword strings) → Fictional-*

Usage
-----
    python scripts/apply_fictional_names.py --dry-run     # preview
    python scripts/apply_fictional_names.py               # apply
    python scripts/apply_fictional_names.py --dump-map     # print mapping JSON
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════

PROJECT_ROOT = Path(__file__).resolve().parent.parent
THIS_SCRIPT = Path(__file__).resolve()

# File extensions to process
TEXT_EXTS = {
    ".py", ".json", ".yaml", ".yml", ".txt", ".md",
    ".csv", ".cfg", ".ini", ".toml", ".sh", ".bat",
    ".js", ".html", ".css", ".log",
}

# Also match compound extensions like .py.bak.20260323


def _is_processable(fpath):
    """Return True if fpath has a processable extension (including .bak compound)."""
    if fpath.suffix in TEXT_EXTS:
        return True
    # Handle compound extensions: e.g. .py.bak.20260323
    suffixes = fpath.suffixes  # e.g. ['.py', '.bak', '.20260323']
    return any(s in TEXT_EXTS for s in suffixes)


# Directories/files to skip
SKIP_DIRS = {".git", ".venv", "__pycache__", "node_modules"}


def _iter_project_files():
    """Walk project tree, skipping .venv / .git / etc."""
    for dirpath, dirnames, filenames in os.walk(PROJECT_ROOT):
        # Prune skipped dirs IN-PLACE so os.walk won't descend
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            yield Path(dirpath) / fn

# ══════════════════════════════════════════════════════════════════════════════
# KEEP-AS-IS LISTS  (not copyrighted / genre descriptors / instruments)
# ══════════════════════════════════════════════════════════════════════════════


KEEP_REAL_ARTIST_IDS = {
    # Genre / style compilation labels used as artist buckets
    "CityPop", "JungleDnB", "MedievalAmbience",
    "DarkAngelMetal", "CyberpunkBeats", "EgyptianMetal",
    "PirateMetal", "EgyptianBattle", "DarkGoddess", "NotTooJazzy",
    # Generic instruments
    "Gayageum", "Guzheng", "Guqin", "Koto",
}

# ══════════════════════════════════════════════════════════════════════════════
# FICTIONAL ARTIST NAME GENERATOR
# ══════════════════════════════════════════════════════════════════════════════

_ADJ = [
    "Amber", "Azure", "Blazing", "Brass", "Cobalt", "Coral", "Crimson",
    "Crystal", "Dusk", "Ebony", "Emerald", "Fading", "Frozen", "Gilded",
    "Glass", "Golden", "Granite", "Hollow", "Indigo", "Iron", "Ivory",
    "Jade", "Jasper", "Lunar", "Marble", "Midnight", "Misty", "Neon",
    "Obsidian", "Opal", "Phantom", "Quartz", "Rusty", "Sapphire",
    "Scarlet", "Shadow", "Silver", "Smoky", "Solar", "Spectral",
    "Sterling", "Storm", "Thistle", "Thunder", "Timber", "Twilight",
    "Velvet", "Violet", "Volcanic", "Zinc",
]

_NOUN = [
    "Arrow", "Beacon", "Bell", "Bloom", "Canyon", "Castle", "Chain",
    "Cipher", "Compass", "Crown", "Dawn", "Drifter", "Echo", "Falcon",
    "Flame", "Forge", "Fountain", "Frost", "Garden", "Gate", "Ghost",
    "Glacier", "Harbor", "Haven", "Helix", "Horn", "Horizon", "Isle",
    "Jewel", "Knight", "Lantern", "Leaf", "Lighthouse", "Lotus", "Mask",
    "Mesa", "Mirror", "Moon", "Needle", "Nest", "Oracle", "Orchid",
    "Peak", "Phoenix", "Pillar", "Prism", "Quarry", "Raven", "Ridge",
    "River", "Rose", "Sail", "Scholar", "Serpent", "Shield", "Shore",
    "Signal", "Spark", "Spire", "Stone", "Strand", "Summit", "Swan",
    "Thorn", "Tide", "Tower", "Trail", "Veil", "Vine", "Voyage",
    "Warden", "Whisper", "Wing",
]


def _hash_int(s: str) -> int:
    return int(hashlib.md5(s.encode("utf-8")).hexdigest(), 16)


def make_fictional_artist(real_name: str) -> str:
    """Deterministic: same input → same output, always."""
    h = _hash_int(real_name)
    adj = _ADJ[h % len(_ADJ)]
    noun = _NOUN[(h >> 8) % len(_NOUN)]
    return f"Fictional-{adj}{noun}"


def make_fictional_track(real_filename: str) -> str:
    """
    Turn a real mp3 filename into Fictional-Track-<6hex>.mp3
    preserving any _part_NNN suffix for sliced tracks.
    """
    stem, ext = os.path.splitext(real_filename)
    # Preserve part suffixes: _part_000, _part_001, etc.
    part_match = re.search(r"(_part_\d{3})$", stem)
    part_suffix = part_match.group(1) if part_match else ""
    base = stem[: -len(part_suffix)] if part_suffix else stem
    h = hashlib.md5(base.encode("utf-8")).hexdigest()[:8]
    return f"Fictional-Track-{h}{part_suffix}{ext}"


# ══════════════════════════════════════════════════════════════════════════════
# MASTER ARTIST LIST — every PascalCase artist ID from classify_and_clean.py
# ══════════════════════════════════════════════════════════════════════════════

ALL_ARTIST_IDS = [
    "ABBA", "ACDC", "Aerosmith", "AirSupply", "Alcione", "AlessiBrothers",
    "AliceInChains", "America", "Angra", "Anri", "ArianaGrande",
    "AsianKungFuGeneration", "AvengedSevenfold", "Babyface", "BadCompany",
    "BanjoKazooie", "Bayonetta", "BeachBoys", "Beatles", "Belo",
    "BetteMidler", "BlackSabbath", "Blink182", "BobDylan", "BoneyM",
    "BoyzIIMen", "BreakingBenjamin", "BringMeTheHorizon", "BruceDickinson",
    "BruceSpringsteen", "BrunoMars", "BulletForMyValentine", "CPM22",
    "CaetanoVeloso", "Cameo", "CapitalInicial", "CaptainAndTennille",
    "Castlevania", "CharlieBrownJr", "CheapTrick", "ChuckBerry",
    "Commodores", "Cream", "CrowdedHouse", "CurtisMayfield",
    "DJDave", "DOOM", "DaleHawkins", "Darude", "DavidBowie", "DeadFish",
    "DeadKennedys", "DeepPurple", "Devo", "Dio", "DireStraits", "Disturbed",
    "Djavan", "DonkeyKong", "Donovan", "DoobieBrothers", "DragonBall",
    "DragonForce", "EarthWindAndFire", "ElvisPresley",
    "EngenheirosDoHawaii", "Enigma", "Evanescence", "FLOW", "FZero",
    "FaithNoMore", "Faun", "FireEmblem", "FooFighters", "FundoDeQuintal",
    "GigiDAgostino", "GooGooDolls", "Gorillaz", "GratefulDead", "GreenDay",
    "GuiltyGear", "GunsNRoses", "HallAndOates", "HimikoKikuchi", "IggyPop",
    "InfectedMushroom", "IronMaiden", "JGeilsBand", "JeffBeck", "JethroTull",
    "Jigsaw", "JimiHendrix", "Fictional-Jozep", "JorgeVercillo", "JunkoOhashi", "KISS",
    "KennyG", "KenshiYonezu", "KingCrimson", "Kraftwerk", "Legiao",
    "LimpBizkit", "LinkinPark", "LisaLisa", "LittleFeat", "LordOfTheRings",
    "LosHermanos", "LynyrdSkynyrd", "Madonna", "ManhattanTransfer",
    "MapleStory", "MariahCarey", "MarilynManson", "Mario", "MarisaMonte",
    "Massacration", "Matanza", "Megadeth", "Metallica", "Metroid",
    "MichaelJackson", "MichelleHeafy", "MikiMatsubara", "MoodyBlues",
    "Mother", "MyChemicalRomance", "NSYNC", "Naruto", "NeilYoung", "Nena",
    "Nickelback", "Nirvana", "NotoriousBIG", "Nujabes", "ORappa", "Oasis",
    "OingoBoingo", "OmegaTribe", "OnePunchMan", "OsMutantes", "OsParalamas",
    "Paramore", "PaulMcCartney", "PaulaAbdul", "PearlJam", "PetShopBoys",
    "PinkFloyd", "Pitty", "Poco", "Pokemon", "Prince", "PrincessMononoke",
    "Queen", "REM", "REOSpeedwagon", "RagnarokOnline", "Rammstein",
    "RedHotChiliPeppers", "RollingStones", "SHINee", "Sabaton", "Sade",
    "Santana", "SexPistols", "SkankBR", "Slipknot", "SmokeyRobinson",
    "SoftMachine", "Sonic", "SpiceGirls", "SteelyDan", "Stratovarius",
    "StrayCats", "StudioGhibli", "Styx", "Sublime", "SuperSmashBros",
    "Survivor", "SystemOfADown", "TalkingHeads", "TameImpala",
    "TerenceTrentDArby", "TheBand", "TheCars", "TheCranberries",
    "TheOffspring", "TheSims", "TimMaia", "TomPetty", "Tribalistas",
    "Turisas", "U2", "Underworld", "VanHalen", "Vanessa", "VanessaDaMata",
    "VanillaIce", "WangChung", "WeatherReport", "Wham", "Whitesnake",
    "WindRose", "WorldOfWarcraft", "YUI", "Yasuha", "Yes", "YoYoMa",
    "ZecaPagodinho", "Zelda",
]

# ══════════════════════════════════════════════════════════════════════════════
# ARTIST KEYWORD → SPACED / HYPHENATED FORMS
# Maps artist PascalCase ID to common textual forms that appear in code/data
# ══════════════════════════════════════════════════════════════════════════════

ARTIST_TEXT_FORMS: dict[str, list[str]] = {
    "ABBA": ["abba"],
    "ACDC": ["ac dc", "acdc", "ac/dc", "AC/DC"],
    "Aerosmith": ["aerosmith", "Aerosmith"],
    "AirSupply": ["air supply", "Air Supply"],
    "Alcione": ["alcione", "Alcione"],
    "AlessiBrothers": ["alessi brothers", "alessi ", "Alessi Brothers", "Alessi"],
    "AliceInChains": ["alice in chains", "alice_in_chains", "Alice-In-Chains", "Alice in Chains"],
    "America": ["america - a horse", "America - A Horse"],
    "Angra": ["angra", "Angra"],
    "Anri": ["anri", "Anri"],
    "ArianaGrande": ["ariana grande", "Ariana Grande"],
    "AsianKungFuGeneration": ["asian kung-fu generation", "asian kung fu",
                              "Asian Kung-Fu Generation"],
    "AvengedSevenfold": ["avenged sevenfold", "a7x", "Avenged Sevenfold", "A7X"],
    "Babyface": ["babyface", "Babyface", "Baby Face"],
    "BadCompany": ["bad company", "Bad Company"],
    "BanjoKazooie": ["banjo-kazooie", "banjo kazooie", "banjo-tooie",
                     "Banjo-Kazooie", "Banjo Kazooie"],
    "Bayonetta": ["bayonetta", "Bayonetta"],
    "BeachBoys": ["beach boys", "Beach Boys", "Beach Boy"],
    "Beatles": ["beatles", "Beatles", "The Beatles"],
    "Belo": ["belo", "Belo"],
    "BetteMidler": ["bette midler", "Bette Midler", "Midler"],
    "BlackSabbath": ["black sabbath", "Black Sabbath"],
    "Blink182": ["blink-182", "blink 182", "Blink-182", "blink182"],
    "BobDylan": ["bob dylan", "Bob Dylan"],
    "BoneyM": ["boney m", "Boney M"],
    "BoyzIIMen": ["boyz ii men", "boys ii men", "boyz 2 men",
                  "Boyz II Men", "Boy II Man"],
    "BreakingBenjamin": ["breaking benjamin", "Breaking Benjamin",
                         "brk bj", "bk bj", "brk-bj", "bk-bj"],
    "BringMeTheHorizon": ["bring me the horizon", "bmth",
                          "Bring-Me-The-Horizon", "Bring Me The Horizon"],
    "BruceDickinson": ["bruce dickinson", "Bruce Dickinson", "Bruce-Dickinson",
                       "Brave-Knight", "BraveKnight"],
    "BruceSpringsteen": ["bruce springsteen", "Bruce Springsteen"],
    "BrunoMars": ["bruno mars", "Bruno Mars"],
    "BulletForMyValentine": ["bullet for my valentine", "bfmv",
                             "Bullet For My Valentine", "BFMV"],
    "CPM22": ["cpm 22", "cpm22", "CPM 22"],
    "CaetanoVeloso": ["caetano veloso", "Caetano Veloso"],
    "Cameo": ["cameo ", "Cameo"],
    "CapitalInicial": ["capital inicial", "Capital Inicial", "Capital-Inicial"],
    "CaptainAndTennille": ["captain & tennille", "captain tennille",
                           "Captain & Tennille", "Captain Tennille"],
    "Castlevania": ["castlevania", "Castlevania"],
    "CharlieBrownJr": ["charlie brown jr", "charlie_brown",
                       "Charlie Brown Jr", "Charlie-Brown-Jr"],
    "CheapTrick": ["cheap trick", "Cheap Trick"],
    "ChuckBerry": ["chuck berry", "Chuck Berry"],
    "Commodores": ["commodores", "Commodores"],
    "Cream": ["cream ", "Cream"],
    "CrowdedHouse": ["crowded house", "Crowded House"],
    "CurtisMayfield": ["curtis mayfield", "Curtis Mayfield"],
    "DJDave": ["dj_dave", "djdave", "dj dave", "DJ Dave", "DJDave", "DJ-Dave"],
    "DOOM": ["doom", "DOOM"],
    "DaleHawkins": ["dale hawkins", "Dale Hawkins"],
    "Darude": ["darude", "Darude"],
    "DavidBowie": ["david bowie", "David Bowie"],
    "DeadFish": ["dead fish", "Dead Fish"],
    "DeadKennedys": ["dead kennedys", "Dead Kennedys"],
    "DeepPurple": ["deep purple", "Deep Purple"],
    "Devo": ["devo ", "Devo"],
    "Dio": ["Dio"],
    "DireStraits": ["dire straits", "Dire Straits"],
    "Disturbed": ["disturbed", "Disturbed"],
    "Djavan": ["djavan", "Djavan"],
    "DonkeyKong": ["donkey kong", "Donkey Kong", "DonkeyKong", "dkc", "DKC"],
    "Donovan": ["donovan ", "Donovan"],
    "DoobieBrothers": ["doobie brothers", "Doobie Brothers"],
    "DragonBall": ["dragon ball", "Dragon Ball"],
    "DragonForce": ["dragonforce", "DragonForce"],
    "EarthWindAndFire": ["earth, wind", "earth wind", "ewf ",
                         "Earth, Wind & Fire", "Earth Wind and Fire"],
    "ElvisPresley": ["elvis presley", "Elvis Presley"],
    "EngenheirosDoHawaii": ["engenheiros do hawaii", "Engenheiros do Hawaii"],
    "Enigma": ["enigma ", "Enigma"],
    "Evanescence": ["evanescence", "Evanescence"],
    "FLOW": ["flow - sign", "FLOW"],
    "FZero": ["f-zero", "F-Zero", "FZero"],
    "FaithNoMore": ["faith no more", "Faith No More", "faith-no-more",
                    "Faith-No-More"],
    "Faun": ["faun", "Faun"],
    "FireEmblem": ["fire emblem", "Fire Emblem"],
    "FooFighters": ["foo fighters", "Foo Fighters", "Foo-Fighters"],
    "FundoDeQuintal": ["fundo de quintal", "Fundo de Quintal"],
    "GigiDAgostino": ["gigi d'agostino", "gigi dagostino",
                      "Gigi D'Agostino"],
    "GooGooDolls": ["goo goo dolls", "Goo Goo Dolls"],
    "Gorillaz": ["gorillaz", "Gorillaz"],
    "GratefulDead": ["grateful dead", "Grateful Dead", "The Grateful Dead"],
    "GreenDay": ["green day", "Green Day"],
    "GuiltyGear": ["guilty gear", "Guilty Gear"],
    "GunsNRoses": ["guns n' roses", "guns n roses", "Guns N' Roses",
                   "Guns N Roses"],
    "HallAndOates": ["hall & oates", "hall and oates", "Hall & Oates"],
    "HimikoKikuchi": ["himiko kikuchi", "Himiko Kikuchi"],
    "IggyPop": ["iggy pop", "Iggy Pop", "Iggy"],
    "InfectedMushroom": ["infected mushroom", "Infected Mushroom",
                         "Infected-Mushroom"],
    "IronMaiden": ["iron maiden", "Iron Maiden"],
    "JGeilsBand": ["j. geil", "j. geils", "j geil",
                   "J. Geils Band", "J. Geil"],
    "JeffBeck": ["jeff beck", "Jeff Beck", "Wired Beck"],
    "JethroTull": ["jethro tull", "Jethro Tull"],
    "Jigsaw": ["jigsaw - sky", "jigsaw sky high", "Jigsaw"],
    "JimiHendrix": ["jimi hendrix", "Jimi Hendrix"],
    "Fictional-Jozep": ["jojo", "Fictional-Jozep"],
    "JorgeVercillo": ["jorge vercillo", "Jorge Vercillo", "Jorge-Vercillo"],
    "JunkoOhashi": ["junko ohashi", "Junko Ohashi", "Junko-Ohashi"],
    "KISS": ["i was made for lovin' you", "i_was_made_for_lovin",
             "Kiss", "KISS"],
    "KennyG": ["kenny g", "Kenny G"],
    "KenshiYonezu": ["kenshi yonezu", "Kenshi Yonezu"],
    "KingCrimson": ["king crimson", "King Crimson"],
    "Kraftwerk": ["kraftwerk", "Kraftwerk", "Kraft Werk"],
    "Legiao": ["legião urbana", "legiao", "Legião Urbana", "Legiao"],
    "LimpBizkit": ["limp bizkit", "Limp Bizkit"],
    "LinkinPark": ["linkin park", "Linkin Park"],
    "LisaLisa": ["lisa lisa", "Lisa Lisa"],
    "LittleFeat": ["little feat", "little feet", "Little Feat"],
    "LordOfTheRings": ["lord of the rings", "Lord of the Rings"],
    "LosHermanos": ["los hermanos", "los_hermanos", "Los Hermanos"],
    "LynyrdSkynyrd": ["lynyrd skynyrd", "Lynyrd Skynyrd"],
    "Madonna": ["madonna", "Madonna"],
    "ManhattanTransfer": ["manhattan transfer", "Manhattan Transfer"],
    "MapleStory": ["maplestory", "MapleStory"],
    "MariahCarey": ["mariah carey", "Mariah Carey", "Mariah"],
    "MarilynManson": ["marilyn manson", "Marilyn Manson"],
    "Mario": ["mario", "Mario"],
    "MarisaMonte": ["marisa monte", "Marisa Monte"],
    "Massacration": ["massacration", "Massacration"],
    "Matanza": ["matanza", "Matanza"],
    "Megadeth": ["megadeth", "Megadeth"],
    "Metallica": ["metallica", "Metallica"],
    "Metroid": ["metroid", "Metroid"],
    "MichaelJackson": ["michael jackson", "Michael Jackson"],
    "MichelleHeafy": ["michelle heafy", "michelleheafy",
                      "Michelle Heafy", "MichelleHeafy"],
    "MikiMatsubara": ["miki matsubara", "Miki Matsubara", "Miki-Matsubara"],
    "MoodyBlues": ["moody blues", "Moody Blues", "The Moody Blues"],
    "Mother": ["Mother"],
    "MyChemicalRomance": ["my chemical romance", "My Chemical Romance"],
    "NSYNC": ["nsync", "n'sync", "NSYNC", "N'Sync"],
    "Naruto": ["naruto", "Naruto"],
    "NeilYoung": ["neil young", "Neil Young"],
    "Nena": ["nena ", "Nena"],
    "Nickelback": ["nickelback", "Nickelback"],
    "Nirvana": ["nirvana", "Nirvana"],
    "NotoriousBIG": ["notorious big", "notorius big", "Notorious B.I.G."],
    "Nujabes": ["nujabes", "Nujabes"],
    "ORappa": ["o rappa", "O Rappa", "O-Rappa", "ORappa"],
    "Oasis": ["oasis", "Oasis"],
    "OingoBoingo": ["oingo boingo", "oingo & boingo",
                    "Oingo Boingo", "Oingo & Boingo"],
    "OmegaTribe": ["omega tribe", "1986 omega tribe", "Omega Tribe"],
    "OnePunchMan": ["one punch man", "one_punch_man", "One Punch Man"],
    "OsMutantes": ["os mutantes", "Os Mutantes"],
    "OsParalamas": ["paralamas", "Paralamas", "Os Paralamas"],
    "Paramore": ["paramore", "Paramore"],
    "PaulMcCartney": ["paul mccartney", "Paul McCartney"],
    "PaulaAbdul": ["paula abdul", "Paula Abdul"],
    "PearlJam": ["pearl jam", "Pearl Jam"],
    "PetShopBoys": ["pet shop boys", "Pet Shop Boys", "Pet Shop"],
    "PinkFloyd": ["pink floyd", "Pink Floyd"],
    "Pitty": ["pitty", "Pitty"],
    "Poco": ["poco ", "Poco"],
    "Pokemon": ["pokémon", "pokemon", "Pokémon", "Pokemon"],
    "Prince": ["prince ", "Prince"],
    "PrincessMononoke": ["princess mononoke", "mononoke",
                         "Princess Mononoke"],
    "Queen": ["queen ", "Queen"],
    "REM": ["r.e.m.", "rem ", "R.E.M.", "REM"],
    "REOSpeedwagon": ["reo speedwagon", "REO Speedwagon"],
    "RagnarokOnline": ["ragnarok online", "Ragnarok Online"],
    "Rammstein": ["rammstein", "Rammstein"],
    "RedHotChiliPeppers": ["red hot chili peppers", "rhcp", "rchp",
                           "Red Hot Chili Peppers", "RHCP",
                           "Red Hot Chili Pepper"],
    "RollingStones": ["rolling stones", "Rolling Stones", "The Rolling Stones"],
    "SHINee": ["shinee", "SHINee"],
    "Sabaton": ["sabaton", "Sabaton"],
    "Sade": ["sade ", "Sade"],
    "Santana": ["santana ", "Santana"],
    "SexPistols": ["sex pistols", "Sex Pistols"],
    "SkankBR": ["skank", "Skank"],
    "Slipknot": ["slipknot", "Slipknot"],
    "SmokeyRobinson": ["smokey robinson", "Smokey Robinson"],
    "SoftMachine": ["soft machine", "Soft Machine"],
    "Sonic": ["sonic", "Sonic"],
    "SpiceGirls": ["spice girls", "Spice Girls", "Spice Girl"],
    "SteelyDan": ["steely dan", "Steely Dan"],
    "Stratovarius": ["stratovarius", "Stratovarius"],
    "StrayCats": ["stray cats", "stray cat ", "Stray Cats", "Stray Cat"],
    "StudioGhibli": ["ghibli", "Studio Ghibli", "Studio-Ghibli", "Ghibli"],
    "Styx": ["styx ", "Styx", "Father Styx"],
    "Sublime": ["sublime", "Sublime"],
    "SuperSmashBros": ["super smash bros", "smash bros", "ssbb", "ssbm",
                       "ssbu", "Super Smash Bros", "Smash Bros", "melee"],
    "Survivor": ["survivor ", "Survivor"],
    "SystemOfADown": ["system of a down", "soad", "System of a Down",
                      "System-Of-A-Down", "SOAD"],
    "TalkingHeads": ["talking heads", "Talking Heads"],
    "TameImpala": ["tame impala", "Tame Impala"],
    "TerenceTrentDArby": ["terence trent", "d'arby", "Terence Trent D'Arby",
                          "Daniel J. D'Arby"],
    "TheBand": ["the band ", "The Band"],
    "TheCars": ["the cars", "The Cars"],
    "TheCranberries": ["cranberries", "Cranberries", "The Cranberries"],
    "TheOffspring": ["offspring", "Offspring", "The Offspring"],
    "TheSims": ["the fictional-vidasimu", "The Fictional-VidaSimu"],
    "TimMaia": ["tim maia", "Tim Maia"],
    "TomPetty": ["tom petty", "Tom Petty", "Tonpetty"],
    "Tribalistas": ["tribalistas", "Tribalistas"],
    "Turisas": ["turisas", "Turisas"],
    "U2": ["u2 ", "U2"],
    "Underworld": ["underworld ", "Underworld", "Under World"],
    "VanHalen": ["van halen", "Van Halen"],
    "Vanessa": ["vanessa da mata", "Vanessa Da Mata", "Vanessa-Da-Mata"],
    "VanessaDaMata": ["vanessa da mata", "Vanessa da Mata"],
    "VanillaIce": ["vanilla ice", "Vanilla Ice"],
    "WangChung": ["wang chung", "Wang Chung"],
    "WeatherReport": ["weather report", "Weather Report"],
    "Wham": ["wham!", "wham ", "Wham!", "Wham"],
    "Whitesnake": ["whitesnake", "Whitesnake"],
    "WindRose": ["wind rose", "Wind Rose"],
    "WorldOfWarcraft": ["world of warcraft", "warcraft",
                        "World of Warcraft", "Warcraft"],
    "YUI": ["yui", "YUI"],
    "Yasuha": ["yasuha", "Yasuha"],
    "Yes": ["yes ", "Yes"],
    "YoYoMa": ["yo-yo ma", "yo yo ma", "Yo-Yo Ma"],
    "ZecaPagodinho": ["zeca pagodinho", "Zeca Pagodinho"],
    "Zelda": ["zelda", "Zelda", "legend of zelda"],
}


# ══════════════════════════════════════════════════════════════════════════════
# BUILD MASTER REPLACEMENT TABLE
# ══════════════════════════════════════════════════════════════════════════════

def build_artist_map() -> dict[str, str]:
    """PascalCase artist ID → Fictional-* name."""
    m: dict[str, str] = {}
    for aid in ALL_ARTIST_IDS:
        if aid in KEEP_REAL_ARTIST_IDS:
            continue
        m[aid] = make_fictional_artist(aid)
    return m


def build_artist_text_map(artist_map: dict[str, str]) -> dict[str, str]:
    """
    All textual/spaced/hyphenated forms of artist names → their fictional
    equivalent in matching case style.
    """
    result: dict[str, str] = {}
    for aid, forms in ARTIST_TEXT_FORMS.items():
        if aid in KEEP_REAL_ARTIST_IDS:
            continue
        fictional = artist_map.get(aid)
        if not fictional:
            continue
        # The PascalCase form is already handled in artist_map.
        # Generate a spaced/hyphenated version for text forms.
        # "Fictional-AmberBeacon" → "Fictional-Amber Beacon" (spaced),
        #                          "Fictional-Amber-Beacon" (hyphenated)
        # Just replace with the PascalCase form in all cases for consistency.
        for form in forms:
            if form not in result:
                result[form] = fictional
    return result


def build_track_map_from_jsons() -> dict[str, str]:
    """Scan all track-moods JSON files and generate fictional track names."""
    m: dict[str, str] = {}
    patterns = [
        "docs/maps/*/track-moods*.json",
        "docs/maps/*/classified_singles_tree*.json",
    ]
    for pat in patterns:
        import glob
        for fpath in glob.glob(str(PROJECT_ROOT / pat)):
            try:
                with open(fpath) as f:
                    data = json.load(f)
            except Exception:
                continue
            _walk_json_keys(data, m)

    # Also scan other files for .mp3 references
    for fpath in _iter_project_files():
        if _is_processable(fpath) and fpath.is_file():
            if fpath.resolve() == THIS_SCRIPT:
                continue
            try:
                content = fpath.read_text(encoding="utf-8")
            except Exception:
                continue
            # Find all *.mp3 references
            for match in re.finditer(r'[\w\[\]\(\).,\'!#\-]+\.mp3', content):
                fn = match.group(0)
                if fn not in m and not fn.startswith("Fictional-"):
                    m[fn] = make_fictional_track(fn)
    return m


def _walk_json_keys(obj, m: dict[str, str]):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str) and k.endswith(".mp3"):
                if k not in m and not k.startswith("Fictional-"):
                    m[k] = make_fictional_track(k)
            _walk_json_keys(v, m)
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, str) and item.endswith(".mp3"):
                if item not in m and not item.startswith("Fictional-"):
                    m[item] = make_fictional_track(item)
            elif isinstance(item, (dict, list)):
                _walk_json_keys(item, m)


def build_full_replacement_table() -> list[tuple[str, str]]:
    """
    Build the master replacement table.
    Returns list of (old, new) sorted longest-first.
    """
    pairs: dict[str, str] = {}

    # 1. Artist PascalCase IDs
    artist_map = build_artist_map()
    for k, v in artist_map.items():
        pairs[k] = v

    # 2. Artist text forms (spaced, hyphenated, etc.)
    text_map = build_artist_text_map(artist_map)
    for k, v in text_map.items():
        pairs[k] = v

    # 3. Track filenames from JSONs
    track_map = build_track_map_from_jsons()
    for k, v in track_map.items():
        pairs[k] = v

    # Filter out entries where key == value or key is empty or too short (< 3 chars)
    # to avoid replacing generic short words
    filtered = {}
    for k, v in pairs.items():
        if k == v or len(k.strip()) < 3:
            continue
        if k.strip() in {"the", "The", "and", "And", "for", "For", "not"}:
            continue
        filtered[k] = v

    # Sort longest-first to avoid partial matches
    table = sorted(filtered.items(), key=lambda t: len(t[0]), reverse=True)
    return table


# ══════════════════════════════════════════════════════════════════════════════
# FILE PROCESSING
# ══════════════════════════════════════════════════════════════════════════════

def transform(content: str, table: list[tuple[str, str]]) -> str:
    """Apply all replacements to content string."""
    for old, new in table:
        content = content.replace(old, new)
    return content


def process_json_file(
    fpath: Path,
    table: list[tuple[str, str]],
    track_map: dict[str, str],
    dry_run: bool,
) -> bool:
    """
    Special handling for JSON files: replace both keys and values.
    Returns True if file was modified.
    """
    try:
        with open(fpath, encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return False

    original_text = json.dumps(data, ensure_ascii=False, indent=2)

    # For track-moods files: replace the dict keys (mp3 filenames)
    if isinstance(data, dict):
        new_data: dict[str, object] = {}
        for k, v in data.items():
            new_k: str = str(track_map.get(k, k) if k.endswith(".mp3") else k)
            # Also apply general text replacements to keys
            new_k = transform(new_k, table)
            # Apply text replacements to values
            new_v: object
            if isinstance(v, str):
                new_v = transform(v, table)
            elif isinstance(v, list):
                new_v = v  # mood labels stay as-is
            else:
                new_v = v
            new_data[new_k] = new_v
        data = new_data

    new_text = json.dumps(data, ensure_ascii=False, indent=2)

    # Also apply string replacements to the whole JSON text
    # (catches artist names in values, nested structures, etc.)
    new_text = transform(new_text, table)

    if new_text != original_text:
        if dry_run:
            print(f"  [DRY-RUN] Would modify: {fpath}")
        else:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_text + "\n")
            print(f"  [MODIFIED] {fpath}")
        return True
    return False


def process_text_file(
    fpath: Path,
    table: list[tuple[str, str]],
    dry_run: bool,
) -> bool:
    """Process a generic text file. Returns True if modified."""
    try:
        original = fpath.read_text(encoding="utf-8")
    except (UnicodeDecodeError, PermissionError):
        return False

    result = transform(original, table)
    if result != original:
        if dry_run:
            print(f"  [DRY-RUN] Would modify: {fpath}")
        else:
            fpath.write_text(result, encoding="utf-8")
            print(f"  [MODIFIED] {fpath}")
        return True
    return False


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    dry_run = "--dry-run" in sys.argv
    dump_map = "--dump-map" in sys.argv

    print("=" * 70)
    print("  FICTIONAL NAME REPLACEMENT TOOL")
    print(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print("=" * 70)

    # Build mappings
    print("\n[1/4] Building artist mapping...")
    artist_map = build_artist_map()
    print(f"  {len(artist_map)} artist identifiers mapped")

    print("[2/4] Building artist text-form mapping...")
    text_map = build_artist_text_map(artist_map)
    print(f"  {len(text_map)} text forms mapped")

    print("[3/4] Scanning for track filenames...")
    track_map = build_track_map_from_jsons()
    print(f"  {len(track_map)} track filenames mapped")

    print("[4/4] Building full replacement table...")
    table = build_full_replacement_table()
    print(f"  {len(table)} total replacement rules (sorted longest-first)")

    if dump_map:
        # Output the mapping as JSON for review
        mapping = {
            "artists": {k: v for k, v in sorted(artist_map.items())},
            "tracks_sample": dict(list(sorted(track_map.items()))[:50]),
            "total_tracks": len(track_map),
            "total_rules": len(table),
        }
        print(json.dumps(mapping, indent=2, ensure_ascii=False))
        return

    # Process all files
    print(f"\n--- Processing files in {PROJECT_ROOT} ---")
    modified = 0
    scanned = 0

    for fpath in sorted(_iter_project_files()):
        if not fpath.is_file():
            continue
        if not _is_processable(fpath):
            continue
        if fpath.resolve() == THIS_SCRIPT:
            continue

        scanned += 1

        if fpath.suffix == ".json":
            if process_json_file(fpath, table, track_map, dry_run):
                modified += 1
        else:
            if process_text_file(fpath, table, dry_run):
                modified += 1

    print("\n--- Summary ---")
    print(f"  Files scanned:  {scanned}")
    print(f"  Files modified: {modified}")
    if dry_run:
        print("  (DRY RUN — no files were actually changed)")
    print("\nDone.")


if __name__ == "__main__":
    main()
