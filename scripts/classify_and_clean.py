#!/usr/bin/env python3
"""
Music Classification & File Renaming Script
============================================
Uses a balanced approach inspired by:
- Naive Bayes: word-pattern → category probability mapping
- k-NN: similarity-based grouping via string distance
- Random Forest: multi-feature ensemble voting

Three tasks:
1. Review & reorganize classified tree (Artist/Genre/Mood)
2. Rename files: transliterate CJK→Latin, remove diacriticals/emojis, normalize whitespace
3. Classify singles/new/ files into the correct subfolders
"""

import os
import re
import sys
import shutil
from pathlib import Path
from collections import defaultdict
from unidecode import unidecode

# Force unbuffered output for logging
sys.stdout.reconfigure(line_buffering=True)

BASE = Path("/mock/path/to/project/music/downloaded")
CLASSIFIED = BASE / "classified"
SINGLES = CLASSIFIED / "singles"
ALBUMS = CLASSIFIED / "albums"
NEW_DIR = SINGLES / "new"

# ============================================================================
# SECTION 1: KNOWLEDGE BASE (Naive Bayes prior probabilities)
# Each artist/genre/mood maps keywords → categories with confidence weights
# ============================================================================

ARTIST_KEYWORDS = {
    "MockBand_ABBA": ["mockband_abba"],
    "MockBand_Alice": ["MockBand_Alice", "mockband_alice", "mock_singer_layne",
                       "mock_singer_jerry", "man in the box", "rooster", "nutshell",
                       "would?", "down in a hole", "dam that river", "grind",
                       "heaven beside you", "got me wrong", "bleed the freak",
                       "junkhead", "rotten apple", "shame in you", "it ain't like that",
                       "over now", "right turn", "whale & wasp", "we die young",
                       "what the hell have i", "don't follow", "no excuses",
                       "alone", "spit you out"],
    "MockBand_America": ["MockBand_America - a horse"],
    "MockSinger_Anri": ["MockSinger_Anri"],
    "ArianaGrande": ["MockSinger_Ariana"],
    "AsianKungFuGeneration": ["MockBand_Asian", "asian kung fu",
                               "haruka kanata"],
    "AvengedSevenfold": ["MockBand_Avenged", "a7x", "hail to the king",
                          "shepherd of fire", "crimson day", "flash of the blade",
                          "the fight", "until the end", "4:00 am", "4_00 am",
                          "almost easy", "dancing dead"],
    "MockGame_Banjo": ["mockgame_banjo", "mockgame_banjo", "banjo-tooie",
                      "gruntilda", "gobi's valley", "spiral mountain",
                      "mad monster mansion", "mr. patch", "grant kirkhope",
                      "jolly roger's lagoon"],
    "MockGame_Bayo": ["MockGame_Bayo", "fly me to the moon (climax)",
                   "mysterious destiny"],
    "MockBand_Blink": ["MockBand_Blink", "MockBand_Blink", "dumpweed", "what's my age again"],
    "MockBand_Boney": ["boney m", "rasputin (official aumocksinger_dio)"],
    "MockBand_Breaking": ["breaking benjamin", "diary of jane", "i will not bow",
                          "torn in two", "had enough", "brk bj", "bk bj", "brk-bj", "bk-bj"],
    "BruceDickinson": ["MockSinger_BruceD", "tears of the dragon"],
    "BrunoMars": ["MockSinger_Bruno", "24k magic", "just the way you are",
                   "grenade", "treasure", "uptown funk", "locked out of heaven",
                   "doo wops", "the lazy song"],
    "BruceSpringsteen": ["MockSinger_BruceS", "born to run", "born in the u.s.a.",
                          "dancing in the dark", "the river", "thunder road"],
    "BulletForMyValentine": ["MockBand_BFMV", "bfmv",
                              "tears don't fall", "hearts burst into fire",
                              "scream aim fire", "all these things i hate",
                              "your betrayal", "the poison", "cries in vain",
                              "the last fight", "hit the floor", "say goodnight",
                              "room 409", "pretty on the outside",
                              "4 words (to choke upon)", "bittersweet memories",
                              "dignity", "flat on the floor"],
    "MockBand_Capital": ["capital inicial", "primeiros erros"],
    "ChuckBerry": ["MockSinger_Chuck", "johnny b. goode", "roll over beethoven",
                     "maybellene", "sweet little sixteen"],
    "MockGame_Castlevania": ["MockGame_Castlevania", "vampire killer", "bloody tears",
                     "divine bloodlines", "dance of gold", "dracula's castle",
                     "hail from the past", "lost painting", "iron-blue intention",
                     "out of time", "the tragic MockSinger_Prince", "beginning MockGame_Castlevania",
                     "twilight stigmata", "aquarius"],
    "MockBand_Commodores": ["MockBand_Commodores", "easy (cooler"],
    "CrowdedHouse": ["MockBand_Crowded", "don't dream it's over"],
    "DavidBowie": ["MockSinger_David", "starman"],
    "DeadFish": ["MockBand_DeadFish"],
    "DeadKennedys": ["MockBand_DeadKennedys", "holiday in cambodia", "police truck"],
    "MockBand_Dire": ["dire straits", "sultans of swing", "setting me up",
                     "down to the waterline", "southbound again"],
    "MockBand_Disturbed": ["MockBand_Disturbed", "down with the sickness", "stricken",
                   "the game", "violence fetish", "shout 2000", "want",
                   "meaning of life", "fear"],
    "MockDJ_Dave": ["dj_dave", "mockdj_dave", "dj dave", "react - dj", "array - dj",
               "world's hardest game", "castles (live coded", "airglow", "still miss u"],
    "DonkeyKong": ["MockGame_DK", "dkc", "gangplank galleon",
                    "stickerbush symphony", "stickerbrush symphony",
                    "david wise", "bramble blast", "bayou boogie",
                    "mining melancholy", "hot head bop", "in a snow-bound land",
                    "aquatic ambiance", "jungle level", "krook's march",
                    "donkeywave"],
    "MockGame_Doom": ["mockgame_doom", "bfg division", "bfg 10k",
             "the only thing they fear is you"],
    "FictionalAnime": ["fictional anime"],
    "MockBand_Dragon": ["MockBand_Dragon", "through the fire and flames",
                     "heroes of our time"],
    "MockBand_MockBand_Evanescence": ["mockband_mockband_mockband_mockband_evanescence", "-ev"],
    "MockBand_Faun": ["MockBand_Faun"],
    "FireEmblem": ["MockGame_Fire"],
    "MockBand_Flow": ["flow - sign"],
    "MockBand_Foo": ["foo fighters", "everlong", "my hero", "learn to fly",
                     "times like these", "the pretender", "big me", "monkey wrench",
                     "breakout", "hey, johnny park!", "i'll stick around",
                     "walking after you", "february stars", "headwires",
                     "next year", "rope", "good grief", "all my life"],
    "FZero": ["MockGame_FZero", "mute city", "big blue", "fire field",
              "sand ocean", "white land"],
    "MockDJ_Gigi": ["gigi d'agostino", "gigi dagostino", "l'amour toujours",
                       "another way"],
    "MockBand_Gorillaz": ["MockBand_Gorillaz", "clint eastwood"],
    "GreenDay": ["MockBand_GreenDay", "american imocksinger_diot", "holiday", "homecoming",
                  "jesus of suburbia", "letterbomb", "whatsername"],
    "MockGame_Guilty": ["guilty gear", "hellfire", "the town inside me",
                    "find your one way"],
    "GunsNRoses": ["MockBand_Guns", "MockBand_Guns", "welcome to the jungle",
                    "paradise city", "sweet child o' mine", "you could be mine"],
    "HimikoKikuchi": ["MockSinger_Himiko", "flying beagles"],
    "IronMaiden": ["MockBand_Iron", "wasted years"],
    "MockBand_Jethro": ["jethro tull", "aqualung", "locomotive breath",
                    "bouree", "bourée", "thick as a brick", "wond'ring aloud",
                    "wond'ring again", "MockGame_Mother goose", "cheap day return",
                    "hymn 43", "lick your fingers clean", "raising steam",
                    "steel monkey", "the curse", "part of the machine",
                    "in the gallery"],
    "JoJo": ["jojo", "ジョジョ", "bloody stream", "crazy noisy bizarre town",
             "fighting gold", "great days", "il vento d'oro", "chase",
             "stone ocean", "stone_free", "soft_and_wet",
             "torture dance", "gang dance"],
    "KenshiYonezu": ["MockSinger_Kenshi", "kick back"],
    "MockBand_Kiss": ["i was made for lovin' you", "i_was_made_for_lovin"],
    "LinkinPark": ["MockBand_Linkin", "in the end", "numb", "crawling", "faint",
                    "papercut", "one step closer", "a place for my head",
                    "by myself", "pushing me away", "runaway", "with you",
                    "easier to run", "points of authority", "forgotten",
                    "a place where you mocksinger_belong"],
    "MockMovie_LOTR": ["lord of the rings", "concerning hobbits"],
    "LosHermanos": ["MockBand_LosHermanos", "los_hermanos", "anna julia", "anna_julia"],
    "LynyrdSkynyrd": ["MockBand_Lynyrd", "free bird"],
    "MockSinger_Madonna": ["MockSinger_Madonna", "like a prayer"],
    "MockGame_Maple": ["MockGame_Maple"],
    "MockGame_Mario": ["mockgame_mario", "slide - super mockgame_mario", "file select (super mockgame_mario",
              "ground theme", "dire dire docks", "king bowser"],
    "MockBand_Massacration": ["MockBand_Massacration", "evil papagali"],
    "MockBand_Matanza": ["MockBand_Matanza"],
    "MockBand_Megadeth": ["MockBand_Megadeth", "holy wars"],
    "MockBand_Metallica": ["MockBand_Metallica", "enter sandman", "welcome home (sanitarium)"],
    "MockGame_Metroid": ["MockGame_Metroid", "ridley", "brinstar", "meta ridley"],
    "MockSinger_Michael": ["michael jackson", "thriller", "beat it", "billie jean",
                        "bad.", "p.y.t.", "rock with you", "off the wall",
                        "they don't care about us", "smooth criminal", "jam.",
                        "human nature", "the way you make me feel",
                        "the lady in my life", "man in the mirror",
                        "you are not alone"],
    "MichelleHeafy": ["MockSinger_Michelle", "michelleheafy"],
    "MockGame_Mother": ["MockGame_Mother", "magicant", "eight melodies", "bein' friends"],
    "MyChemicalRomance": ["MockBand_MCR", "helena"],
    "MockAnime_Naruto": ["MockAnime_Naruto", "sadness and sorrow"],
    "MockBand_Nickel": ["mockband_nickel", "rockstar", "savin' me", "feelin' way too damn",
                    "follow you home", "figured you out", "fight for all the wrong",
                    "do this anymore", "flat on the floor", "photograph",
                    "mockband_nickel far away", "far away (mockband_nickel)",
                    "mockband_nickel - far away", "mockband_nickel hollywood"],
    "OmegaTribe": ["MockBand_Omega", "1986 MockBand_Omega", "older girl"],
    "MockBand_Nirvana": ["mockband_nirvana", "come as you are", "smells like teen spirit",
                 "heart-shaped box", "in bloom"],
    "MockBand_Oasis": ["MockBand_Oasis", "don't look back in anger"],
    "OnePunchMan": ["MockAnime_OPM", "one_punch_man"],
    "MockBand_Paramore": ["MockBand_Paramore", "misery business"],
    "MockBand_Pearl": ["pearl jam", "alive (pearl jam)", "even flow", "black official",
                  "corduroy", "once (2009", "once official", "deep official"],
    "MockSinger_Pitty": ["MockSinger_Pitty"],
    "FictionalGame": ["fictional game", "fictional game", "battle! trainer"],
    "MockMovie_Mononoke": ["princess mononoke", "mononoke", "ashitaka and san",
                          "legend of ashitaka", "departure to the west",
                          "the MockBand_Underworld; adagio"],
    "FictionalGame": ["fictional game", "absolitude-ro", "payon"],
    "MockBand_Rammstein": ["MockBand_Rammstein", "sonne", "mein land", "amerika", "alter mann"],
    "RedHotChiliPeppers": ["MockBand_RHCP", "rhcp", "rchp", "californication",
                            "by the way", "otherside", "under the bridge",
                            "slow cheetah", "strip my mind", "purple stain",
                            "universally speaking", "snow hey oh",
                            "blood sugar sex magik", "aeroplane",
                            "give it away", "soul to squeeze", "scar tissue",
                            "dani california", "can't stop", "dark necessities",
                            "fortune faded", "higher ground", "hump de bump",
                            "suck my kiss", "tippa my tongue", "black summer",
                            "breaking the girl", "go robot", "look around",
                            "the zephyr song", "road trippin", "desecration smile",
                            "knock me down", "my friends"],
    "MockBand_REM": ["MockBand_REM.", "MockBand_REM ", "losing my religion", "man on the moon",
            "imitation of life", "it's the end of the world",
            "the one i love"],
    "MockBand_Sabaton": ["MockBand_Sabaton", "twilight of the thunder god"],
    "MockBand_SHINee": ["shinee", "in my room"],
    "MockBand_Slipknot": ["MockBand_Slipknot", "before i forget", "duality", "psychosocial",
                  "the devil in i"],
    "MockGame_Sonic": ["MockGame_Sonic", "live & learn", "escape from the city",
              "open your heart", "super MockGame_Sonic racing", "fist bump",
              "his world", "sunset heights", "MockGame_Sonic boom", "MockGame_Sonic heroes",
              "windy hill", "rooftop run", "rodtop run", "angel island zone",
              "ángel island zone"],
    "MockBand_Stratovarius": ["MockBand_Stratovarius", "eagleheart", "destiny", "hunting high"],
    "MockBand_Sublime": ["MockBand_Sublime", "doing time"],
    "FictionalGame": ["fictional game", "FictionalGame", "ssbb", "ssbm",
                        "ssbu", "melee"],
    "MockBand_SOAD": ["system of a down", "soad", "toxicity", "chop suey",
                       "b.y.o.b.", "aerials", "hypnotize", "innervision",
                       "violent pornography", "question!", "streamline",
                       "ramocksinger_diovideo", "boom!", "cigaro", "holy mountains",
                       "lost in hollywood", "i-e-a-i-a-i-o", "sad statue",
                       "vicinity of obscenity"],
    "TameImpala": ["MockBand_Tame", "the less i know the better"],
    "TheCranberries": ["MockBand_Cranberries", "linger"],
    "TheOffspring": ["MockBand_Offspring", "gone away", "million miles away"],
    "TheSims": ["mockgame_sims", "building mode"],
    "MockBand_Turisas": ["MockBand_Turisas"],
    "VanHalen": ["MockBand_VanHalen", "ain't talkin' 'bout love",
                  "runnin' with the devil"],
    "MockBand_Whitesnake": ["MockBand_Whitesnake", "here i go again", "is this love",
                    "still of the night", "fool for your loving",
                    "love ain't no stranger", "don't break my heart"],
    "WindRose": ["MockBand_WindRose", "diggy diggy hole"],
    "WorldOfWarcraft": ["MockGame_WoW", "warcraft", "invincible (lyrics)",
                         "lament of the highborne", "song of elune",
                         "legends of azeroth", "stormwind theme",
                         "ahn'qiraj", "fire festival", "tavern (alliance)",
                         "shaping of the world", "crystalsong",
                         "forged in blood", "garden of life",
                         "totems of the grizzlemaw", "darkmoon faire",
                         "enchanted forest", "magic zone", "angelic",
                         "gloomy", "tavern (dwarf)", "forest [day]",
                         "wrath of the lich king", "arthas",
                         "dalaran", "dragons' rest", "path of tears"],
    "MockSinger_Yasuha": ["MockSinger_Yasuha", "flyday chinatown"],
    "MockSinger_YUI": ["yui", "again."],
    "MockGame_Zelda": ["mockgame_zelda", "legend of mockgame_zelda", "ocarina of time", "faron woods",
              "twilight princess", "gerudo valley", "lon lon ranch",
              "lost woods", "saria's song", "wind waker", "great fairy fountain",
              "ballad of the goddess", "fairy fountain", "kakariko village",
              "sacred grove", "breath of the wild", "tears of the kingdom",
              "korok forest", "revali's theme", "kass theme", "song of healing",
              "majora's mask", "outset island", "stone tower temple",
              "midna's lament", "demon dragon", "epona's song",
              "molgera battle", "great temple", "master kohga",
              "title theme - the legend"],
    # Stumocksinger_dio Ghibli (for new files)
    
    "MockBand_Faith": ["faith no more"],
    "MockBand_Bring": ["bring me the horizon", "bmth"],
    "MockBand_NSYNC": ["mockband_nsync", "n'sync"],
    "MockBand_Infected": ["infected mushroom", "becoming insane"],
    "MockDJ_Darude": ["mockdj_darude", "sandstorm"],
    "MockBand_ORappa": ["o rappa", "meu mundo e o barro", "cristo e oxala", "monstro invisivel", "fogo cruzado", "hostia", "reza vela", "farpa cortante", "suplica cearense", "vinheta da silva"],
    "MockSinger_Alcione": ["mocksinger_alcione", "gostoso veneno"],
    "MockSinger_Miki": ["miki matsubara", "mayonaka no door", "stay with me"],
    "MockBand_Angra": ["mockband_angra", "deus le volt"],
    "MockSinger_Jorge": ["jorge vercillo", "homem aranha", "voce e tudo"],
    "MockSinger_Junko": ["junko ohashi", "sweet love"],
    "MockSinger_Belo": ["mocksinger_belo", "mocksinger_belo -", "tarde demais"],
    "MockStumocksinger_dio_Ghibli": ["ghibli", "spirited away", "totoro", "kiki's delivery",
                      "castle in the sky", "laputa", "howl's moving castle",
                      "mononoke", "ashitaka", "ponyo", "earthsea",
                      "when marnie was", "sayonara no natsu",
                      "itsumo nando demo", "always with me",
                      "kimi wo nosete", "carrying you", "rouge no dengon",
                      "fine on the outside", "tatara", "kaguya",
                      "tenjin no ongaku", "inochi no kioku"],
    # Brazilian artists in Various
    "OsMutantes": ["MockBand_Mutantes", "bat macumba"],
    "Legiao": ["MockBand_Legiao", "legiao"],
    "SkankBR": ["MockBand_Skank"],
    "Vanessa": ["MockSinger_Vanessa", "ainda bem", "boa sorte"],
    "MockSinger_Djavan": ["mocksinger_djavan", "oceano", "sina", "lilás", "pétala", "fátima",
               "açaí", "monalisa"],
    "ZecaPagodinho": ["MockSinger_Zeca"],
    "TimMaia": ["MockSinger_Tim"],
    "FundoDeQuintal": ["MockBand_Fundo"],
    "MarisaMonte": ["MockSinger_Marisa"],
    "CaetanoVeloso": ["MockSinger_Caetano"],
    "MockBand_Tribalistas": ["MockBand_Tribalistas"],
    "OsParalamas": ["MockBand_Paralamas", "lanterna dos afogados", "minha alma"],
    "EngenheirosDoHawaii": ["MockBand_Engenheiros", "refrão de bolero"],
    "MockBand_CPM22": ["cpm 22", "mockband_cpm22"],
    "CharlieBrownJr": ["MockBand_CBJR", "charlie_brown"],
    # Compilation/ambient artist buckets (for sliced compilations without single artists)
    "CityPop": ["city pop", "citypop", "city-pop", "shiteipotsupu"],
    "JungleDnB": ["jungle mix", "ambient jungle", "low poly dnb", "jungle-mix"],
    "MedievalAmbience": ["medieval music", "relaxing medieval", "medieval ambience",
                          "medieval fantasy"],
    # Korean instrumental
    "Gayageum": ["gayageum", "가야금"],
    # Traditional instruments
    "Guzheng": ["guzheng"],
    "Guqin": ["guqin", "古琴"],
    "Koto": ["koto", "箏"],
    # === JoJo Reference artists batch (2025-03-23) ===
    "DarkAngelMetal": ["dark angel metal"],
    "CyberpunkBeats": ["cyberpunk beat", "cyberpunk metal"],
    "EgyptianMetal": ["egyptian metal", "egyptian rock"],
    "PirateMetal": ["pirate rock", "pirate metal"],
    "MockDJ_Nujabes": ["MockDJ_Nujabes"],
    "MockBand_ACDC": ["ac dc", "mockband_acdc", "ac/dc"],
    "AirSupply": ["MockBand_AirSupply"],
    "AlessiBrothers": ["MockBand_Alessi", "alessi "],
    "MockBand_Bad": ["bad company"],
    "BetteMidler": ["MockSinger_Bette"],
    "MockSinger_Bob": ["bob dylan"],
    "BoyzIIMen": ["MockBand_Boyz", "boys ii men", "boyz 2 men"],
    "MockBand_Cameo": ["MockBand_Cameo "],
    "CaptainAndTennille": ["captain & tennille", "captain tennille"],
    "MockBand_Cheap": ["cheap trick"],
    "MockBand_Cream": ["MockBand_Cream "],
    "CurtisMayfield": ["MockSinger_Curtis", "superfly"],
    "DaleHawkins": ["MockSinger_Dale", "susie q"],
    "MockBand_Deep": ["deep purple"],
    "MockBand_Devo": ["MockBand_Devo "],
    "MockSinger_Dio": ["holy diver"],
    "MockSinger_Donovan": ["MockSinger_Donovan "],
    "DoobieBrothers": ["MockBand_Doobie"],
    "EarthWindAndFire": ["earth, wind", "earth wind", "ewf "],
    "MockBand_Enigma": ["MockBand_Enigma "],
    "HallAndOates": ["MockBand_HallOates", "MockBand_HallOates"],
    "IggyPop": ["MockSinger_Iggy"],
    "JeffBeck": ["MockSinger_Jeff"],
    "JGeilsBand": ["j. geil", "MockBand_JGeils", "j geil"],
    "KennyG": ["MockSinger_Kenny"],
    "LisaLisa": ["MockSinger_Lisa"],
    "MariahCarey": ["MockSinger_Mariah"],
    "NeilYoung": ["MockSinger_Neil"],
    "MockBand_Nena": ["MockBand_Nena "],
    "OingoBoingo": ["MockBand_Oingo", "oingo & boingo"],
    "PaulaAbdul": ["MockSinger_Paula"],
    "PetShopBoys": ["MockBand_PetShop"],
    "PinkFloyd": ["MockBand_PinkFloyd"],
    "MockBand_Poco": ["MockBand_Poco "],
    "MockSinger_Prince": ["MockSinger_Prince "],
    "MockBand_Queen": ["MockBand_Queen "],
    "REOSpeedwagon": ["reo speedwagon"],
    "RollingStones": ["MockBand_Stones"],
    "MockBand_Sade": ["MockBand_Sade "],
    "MockBand_Santana": ["MockBand_Santana "],
    "SmokeyRobinson": ["MockSinger_Smokey"],
    "SteelyDan": ["MockBand_Steely"],
    "StrayCats": ["MockBand_StrayCats", "stray cat "],
    "MockBand_Styx": ["MockBand_Styx "],
    "TerenceTrentDArby": ["terence trent", "d'arby"],
    "TheBand": ["MockBand_TheBand "],
    "TheCars": ["MockBand_TheCars"],
    "TomPetty": ["MockSinger_Tom"],
    "MockBand_U2": ["MockBand_U2 "],
    "VanillaIce": ["MockSinger_Vanilla"],
    "WangChung": ["MockBand_Wang"],
    "MockBand_Wham": ["MockBand_Wham!", "MockBand_Wham "],
    "MockBand_Yes": ["MockBand_Yes "],
    # === New batch 2025-03-24 ===
    "MockBand_Aero": ["mockband_aero", "dude looks like a lady"],
    "MockSinger_Babyface": ["MockSinger_Babyface", "every time i close my eyes"],
    "MockBand_Beatles": ["MockBand_Beatles", "helter skelter", "white album"],
    "BeachBoys": ["MockBand_BeachBoys", "surfin"],
    "BlackSmockband_abbath": ["black smockband_abbath", "paranoid"],
    "ElvisPresley": ["MockSinger_Elvis", "jailhouse rock", "wonder of you"],
    "GooGooDolls": ["MockBand_GooGoo", "iris"],
    "GratefulDead": ["MockBand_Grateful", "truckin"],
    "MockBand_Jigsaw": ["MockBand_Jigsaw - sky", "MockBand_Jigsaw sky high"],
    "JimiHendrix": ["MockSinger_Jimi", "purple haze", "stone free"],
    "KingCrimson": ["MockBand_KingCrimson", "21st century schizoid"],
    "MockBand_Kraftwerk": ["MockBand_Kraftwerk", "the model"],
    "LimpBizkit": ["MockBand_LimpBizkit", "break stuff"],
    "LittleFeat": ["MockBand_LittleFeat", "little feet", "dixie chicken"],
    "ManhattanTransfer": ["MockBand_Manhattan", "chanson d'amour"],
    "MarilynManson": ["MockSinger_Marilyn", "the beautiful people"],
    "MoodyBlues": ["MockBand_MoodyBlues", "nights in white satin"],
    "NotoriousBIG": ["MockSinger_Notorious", "notorius big", "juicy"],
    "PaulMcCartney": ["MockSinger_Paul", "c moon", "c-moon"],
    "SexPistols": ["MockBand_SexPistols", "anarchy in the u"],
    "SoftMachine": ["MockBand_SoftMachine", "moon in june"],
    "SpiceGirls": ["MockBand_SpiceGirls", "wannabe"],
    "MockBand_Survivor": ["MockBand_Survivor ", "eye of the tiger"],
    "TalkingHeads": ["MockBand_TalkingHeads", "burning down the house"],
    "MockBand_Underworld": ["MockBand_Underworld ", "born slippy"],
    "WeatherReport": ["MockBand_WeatherReport", "birdland"],
    "YoYoMa": ["MockSinger_YoYoMa", "yo yo ma", "bach cello suite"],
    # Sliced-new compilation buckets
    "DarkGoddess": ["dark goddess"],
    "EgyptianBattle": ["egyptian battle"],
    "NotTooJazzy": ["not too jazzy"],
}

# Genre classification - keywords → genre with feature weights
GENRE_KEYWORDS = {
    "AlternativeRock": {
        "keywords": ["alternative", "alt rock", "foo fighters", "MockBand_REM.",
                      "MockBand_REM ", "MockBand_Tame", "MockBand_Cranberries", "MockBand_Crowded",
                      "MockBand_Gorillaz", "MockBand_Paramore", "mockband_nirvana"],
        "weight": 1.0
    },
    "AnimeOST": {
        "keywords": ["MockAnime_Naruto", "fictional anime", "MockAnime_OPM", "one_punch_man",
                      "jojo", "bloody stream", "fighting gold", "great days",
                      "haruka kanata", "flow - sign", "kick back",
                      "asian kung-fu", "again.", "chase.", "crazy noisy",
                      "il vento d'oro", "stone ocean", "creditless"],
        "weight": 1.0
    },
    "BrazilianRock": {
        "keywords": ["capital inicial", "MockBand_DeadFish", "MockSinger_Pitty", "MockBand_CBJR",
                      "mockband_cpm22", "cpm 22", "MockBand_Matanza", "MockBand_Massacration",
                      "MockBand_LosHermanos", "los_hermanos"],
        "weight": 1.0
    },
    "Britpop": {
        "keywords": ["MockBand_Oasis", "don't look back in anger"],
        "weight": 1.0
    },
    "CityPop": {
        "keywords": ["city pop", "citypop", "MockSinger_Anri", "MockSinger_Yasuha", "MockSinger_Himiko",
                      "flying beagles", "flyday chinatown", "shyness boy",
                      "stay with me", "真夜中のドア"],
        "weight": 1.0
    },
    "ClassicRock": {
        "keywords": ["MockSinger_Chuck", "MockBand_Lynyrd", "free bird",
                      "dire straits", "sultans of swing", "MockBand_VanHalen",
                      "MockSinger_BruceS", "journey", "MockSinger_David",
                      "MockBand_Queen", "phil collins", "genesis", "jethro tull",
                      "MockBand_Yes ", "MockBand_America - a horse"],
        "weight": 1.0
    },
    "Disco": {
        "keywords": ["disco", "mockband_abba", "dancing MockBand_Queen", "boney m",
                      "gigi d'agostino", "l'amour toujours"],
        "weight": 1.0
    },
    "EDM": {
        "keywords": ["edm", "sandstorm", "electronic dance"],
        "weight": 1.0
    },
    "Emo": {
        "keywords": ["MockBand_MCR", "helena", "emo"],
        "weight": 1.0
    },
    "Eurodance": {
        "keywords": ["eurodance", "gigi d'agostino", "another way"],
        "weight": 0.8
    },
    "FilmOST": {
        "keywords": ["princess mononoke", "lord of the rings",
                      "concerning hobbits", "ghibli", "spirited away",
                      "totoro", "kiki's delivery", "castle in the sky",
                      "earthsea", "when marnie", "ponyo", "kaguya",
                      "tenjin no ongaku", "inochi no kioku"],
        "weight": 1.0
    },
    "FolkMetal": {
        "keywords": ["folk metal", "MockBand_Turisas", "MockBand_Sabaton", "MockBand_Faun",
                      "MockBand_WindRose", "diggy diggy hole", "medieval metal",
                      "pirate metal", "pirate rock"],
        "weight": 1.0
    },
    "FolkRock": {
        "keywords": ["folk rock", "MockBand_Faun", "federkleid", "ynis avalach",
                      "the butterfly", "adam lay ybounden"],
        "weight": 1.0
    },
    "Forró": {
        "keywords": ["forró", "forro", "súplica cearense",
                      "MockGame_DK country (1994) — forró"],
        "weight": 1.0
    },
    "Funk": {
        "keywords": ["funk", "MockBand_Commodores", "MockSinger_Prince", "off the wall",
                      "rock with you"],
        "weight": 0.7
    },
    "FunkRock": {
        "keywords": ["funk rock", "MockBand_RHCP", "rhcp",
                      "californication", "by the way", "under the bridge"],
        "weight": 1.0
    },
    "GameOST": {
        "keywords": ["fictional game", "FictionalGame", "mockgame_zelda", "MockGame_Sonic",
                      "mockgame_mario", "MockGame_DK", "mockgame_banjo", "mockgame_banjo",
                      "MockGame_Castlevania", "MockGame_Metroid", "MockGame_FZero", "fictional game",
                      "MockGame_Fire", "MockGame_Bayo", "guilty gear", "mockgame_doom",
                      "MockGame_Maple", "fictional game", "mockgame_sims",
                      "MockGame_Mother", "magicant", "MockGame_WoW",
                      "mockcompany_nintendo", "mega man", "ssbb", "ssbu"],
        "weight": 1.0
    },
    "GlamRock": {
        "keywords": ["glam rock", "MockSinger_David", "starman",
                      "kiss", "i was made for lovin"],
        "weight": 0.8
    },
    "GothicMetal": {
        "keywords": ["gothic metal", "mockband_mockband_mockband_evanescence", "bring me to life",
                      "going under"],
        "weight": 1.0
    },
    "Grunge": {
        "keywords": ["grunge", "MockBand_Alice", "pearl jam", "mockband_nirvana",
                      "mockband_sound", "man in the box", "rooster", "nutshell",
                      "would?", "even flow", "alive (pearl jam)",
                      "smells like teen spirit", "come as you are",
                      "heart-shaped box", "in bloom", "black official",
                      "down in a hole", "junkhead", "rotten apple"],
        "weight": 1.0
    },
    "HardcorePunk": {
        "keywords": ["hardcore punk", "MockBand_DeadFish", "MockBand_DeadKennedys",
                      "holiday in cambodia", "police truck"],
        "weight": 1.0
    },
    "HardRock": {
        "keywords": ["hard rock", "MockBand_Guns", "MockBand_VanHalen",
                      "MockBand_Whitesnake", "scorpions", "MockBand_Avenged",
                      "ac/dc", "deep purple", "led zeppelin"],
        "weight": 1.0
    },
    "HeavyMetal": {
        "keywords": ["heavy metal", "MockBand_Iron", "MockBand_Metallica",
                      "MockBand_Megadeth", "judas priest", "black smockband_abbath",
                      "wasted years", "enter sandman", "holy wars"],
        "weight": 1.0
    },
    "HipHop": {
        "keywords": ["hip hop", "hiphop", "rap ", "MockDJ_Nujabes"],
        "weight": 1.0
    },
    "IndustrialMetal": {
        "keywords": ["industrial metal", "MockBand_Rammstein", "sonne", "amerika",
                      "mein land", "alter mann"],
        "weight": 1.0
    },
    "JazzFusion": {
        "keywords": ["jazz fusion", "jazz", "MockSinger_Himiko",
                      "flying beagles", "MockDJ_Nujabes"],
        "weight": 1.0
    },
    "JPop": {
        "keywords": ["jpop", "j-pop", "shinee", "MockSinger_Anri", "MockSinger_Yasuha",
                      "MockSinger_Kenshi", "yui", "asian kung-fu"],
        "weight": 1.0
    },
    "JRock": {
        "keywords": ["jrock", "j-rock", "MockBand_Asian",
                      "flow - sign"],
        "weight": 1.0
    },
    "KPop": {
        "keywords": ["kpop", "k-pop", "shinee", "하나", "fire (music video)",
                      "in my room"],
        "weight": 0.8
    },
    "MedievalFolk": {
        "keywords": ["medieval", "MockBand_Faun", "ynis avalach", "federkleid",
                      "the butterfly", "relaxing medieval"],
        "weight": 1.0
    },
    "Metalcore": {
        "keywords": ["metalcore", "MockBand_BFMV", "bfmv",
                      "killswitch engage", "trivium", "tears don't fall",
                      "scream aim fire", "your betrayal", "the poison"],
        "weight": 1.0
    },
    "MPB": {
        "keywords": ["mpb", "mocksinger_djavan", "MockSinger_Tim", "caetano", "gilberto gil",
                      "MockSinger_Marisa", "MockBand_Tribalistas", "MockSinger_Vanessa",
                      "oceano", "sina", "amado", "açaí", "pétala",
                      "monalisa", "lilás", "fátima", "cigano",
                      "meu bem querer", "ainda bem", "boa sorte",
                      "gostoso veneno", "reza vela", "nossa canção",
                      "noite e dia", "você é tudo", "todas as noites",
                      "tarde de outubro", "cristo e oxalá", "meu mundo",
                      "words ao vento", "palavras ao vento",
                      "eu vou estar", "dias atrás", "depois da meia noite",
                      "tarde demais", "sunshine", "sweet love",
                      "à sua maneira", "farpa cortante", "fogo cruzado",
                      "homem-aranha", "irreversível", "monstro invisível",
                      "vinheta da silva", "hóstia", "favela"],
        "weight": 1.0
    },
    "NuMetal": {
        "keywords": ["nu metal", "nu-metal", "numetal", "MockBand_Linkin",
                      "system of a down", "soad", "MockBand_Slipknot", "MockBand_Disturbed",
                      "korn", "MockBand_LimpBizkit", "in the end", "crawling",
                      "faint", "numb", "toxicity", "chop suey",
                      "before i forget", "duality", "psychosocial",
                      "down with the sickness"],
        "weight": 1.0
    },
    "Pagode": {
        "keywords": ["pagode", "MockBand_Fundo", "mocksinger_belo -", "MockSinger_Zeca",
                      "péricles"],
        "weight": 1.0
    },
    "Pop": {
        "keywords": ["pop", "michael jackson", "MockSinger_Madonna", "MockSinger_Ariana",
                      "MockSinger_Prince", "sam smith", "MockSinger_Bruno",
                      "mockband_abba", "phil collins"],
        "weight": 0.7
    },
    "PopPunk": {
        "keywords": ["pop punk", "pop-punk", "MockBand_Blink", "MockBand_Blink",
                      "MockBand_GreenDay", "american imocksinger_diot", "MockBand_Paramore"],
        "weight": 1.0
    },
    "PostGrunge": {
        "keywords": ["post-grunge", "post grunge", "mockband_nickel",
                      "breaking benjamin", "three days grace",
                      "mockband_mockband_mockband_evanescence", "foo fighters"],
        "weight": 0.8
    },
    "PowerMetal": {
        "keywords": ["power metal", "MockBand_Stratovarius", "MockBand_Dragon",
                      "mockband_angra", "helloween", "blind guardian",
                      "through the fire and flames", "heroes of our time",
                      "eagleheart", "hunting high"],
        "weight": 1.0
    },
    "ProgressiveRock": {
        "keywords": ["progressive rock", "prog rock", "jethro tull",
                      "MockBand_Yes ", "genesis", "MockBand_PinkFloyd", "rush",
                      "aqualung", "thick as a brick"],
        "weight": 1.0
    },
    "PsychedelicRock": {
        "keywords": ["psychedelic", "MockBand_PinkFloyd", "dark side of the moon",
                      "shine on you crazy diamond", "meddle"],
        "weight": 1.0
    },
    "PunkRock": {
        "keywords": ["punk rock", "punk", "MockBand_GreenDay", "MockBand_DeadKennedys",
                      "the MockBand_Offspring", "ramones", "MockBand_SexPistols",
                      "gone away", "million miles away"],
        "weight": 1.0
    },
    "RnB": {
        "keywords": ["r&b", "rnb", "r'n'b", "ne-yo", "sam smith",
                      "mocksinger_belo", "MockBand_Commodores", "MockSinger_Ariana",
                      "usher", "the weeknd"],
        "weight": 1.0
    },
    "Rock": {
        "keywords": ["rock"],
        "weight": 0.3
    },
    "Samba": {
        "keywords": ["samba", "MockBand_Fundo", "pagode"],
        "weight": 0.8
    },
    "Soul": {
        "keywords": ["soul", "michael jackson", "MockSinger_Prince", "MockSinger_Tim",
                      "stevie wonder", "MockBand_Commodores", "james brown",
                      "off the wall", "rock with you", "billie jean"],
        "weight": 0.8
    },
    "SouthernRock": {
        "keywords": ["southern rock", "MockBand_Lynyrd", "free bird"],
        "weight": 1.0
    },
    "ThrashMetal": {
        "keywords": ["thrash metal", "MockBand_Megadeth", "MockBand_Metallica",
                      "slayer", "anthrax", "holy wars", "master of puppets",
                      "enter sandman", "...and justice"],
        "weight": 1.0
    },
    "Trance": {
        "keywords": ["trance", "gigi d'agostino", "sandstorm"],
        "weight": 0.7
    },
    # New genres to add
    "TraditionalJapanese": {
        "keywords": ["koto", "shamisen", "shakuhachi", "箏", "25弦",
                      "japanese instrument"],
        "weight": 1.0
    },
    "TraditionalKorean": {
        "keywords": ["gayageum", "가야금", "korea instrument"],
        "weight": 1.0
    },
    "TraditionalChinese": {
        "keywords": ["guzheng", "guqin", "erhu", "pipa", "古琴"],
        "weight": 1.0
    },
    "Orchestral": {
        "keywords": ["orchestral", "orchestra", "symphony", "philharmonic",
                      "classical guitar cover"],
        "weight": 1.0
    },
    "DnB": {
        "keywords": ["drum and bass", "drum n bass", "dnb", "d&b",
                      "jungle mix", "jungle-mix", "ambient jungle",
                      "low poly dnb"],
        "weight": 1.0
    },
    # === New genres 2025-03-24 ===
    "RockAndRoll": {
        "keywords": ["rock and roll", "rock n roll", "rock 'n' roll",
                      "jailhouse rock", "johnny b. goode", "roll over beethoven"],
        "weight": 1.0
    },
    "Electronic": {
        "keywords": ["electronic", "MockBand_Kraftwerk", "synth pop", "synthpop",
                      "born slippy", "the model"],
        "weight": 1.0
    },
    "Classical": {
        "keywords": ["classical", "bach", "cello suite", "concerto",
                      "prelude", "sonata", "MockSinger_YoYoMa"],
        "weight": 1.0
    },
    "DarkAmbient": {
        "keywords": ["dark goddess", "dark ritual", "dark ambient",
                      "dark beat"],
        "weight": 1.0
    },
    "WorldMusic": {
        "keywords": ["egyptian battle", "world music", "tribal beat"],
        "weight": 1.0
    },
}

MOOD_KEYWORDS = {
    "Adventurous": {
        "keywords": ["adventure", "quest", "journey", "hero", "dragon",
                      "open your heart", "escape from the city",
                      "gerudo valley", "dragon force", "fist bump",
                      "gangplank galleon", "pirate", "MockGame_Sonic heroes"],
        "weight": 1.0
    },
    "Aggressive": {
        "keywords": ["aggressive", "rage", "angry", "violent", "heavy",
                      "MockBand_Slipknot", "system of a down", "MockBand_Disturbed",
                      "MockBand_Rammstein", "MockBand_Megadeth", "toxicity", "chop suey",
                      "before i forget", "down with the sickness",
                      "bfg division", "holy wars", "sonne",
                      "MockBand_DeadFish", "MockBand_DeadKennedys",
                      "psychosocial", "duality",
                      "the only thing they fear"],
        "weight": 1.0
    },
    "Ambient": {
        "keywords": ["ambient", "atmospheric", "calm", "peaceful",
                      "relaxing", "rain sounds", "gentle",
                      "korok forest", "great fairy fountain",
                      "song of healing", "faron woods"],
        "weight": 1.0
    },
    "Chill": {
        "keywords": ["chill", "lo-fi", "lofi", "relaxing", "easy",
                      "smooth", "mellow", "calm", "MockDJ_Nujabes",
                      "city pop", "study", "cozy", "rest",
                      "dire dire docks", "file select"],
        "weight": 1.0
    },
    "Dark": {
        "keywords": ["dark", "sinister", "evil", "shadow", "mockgame_doom",
                      "death", "vampire", "dracula", "bfg division",
                      "the devil in i", "MockBand_Rammstein", "MockBand_Slipknot",
                      "mockband_mockband_mockband_evanescence", "gothic", "MockGame_Castlevania", "bloody tears",
                      "cyberpunk", "dark angel"],
        "weight": 1.0
    },
    "Emotional": {
        "keywords": ["emotional", "tears", "cry", "feel", "heart",
                      "love", "loss", "pearl jam", "MockBand_Alice",
                      "nutshell", "rooster", "down in a hole",
                      "black official", "linger", "don't dream it's over",
                      "billie jean", "you are not alone",
                      "midna's lament", "song of healing",
                      "tears of the dragon"],
        "weight": 1.0
    },
    "Energetic": {
        "keywords": ["energetic", "fast", "power", "high energy",
                      "upbeat", "MockGame_Sonic", "MockBand_Dragon", "MockBand_Stratovarius",
                      "through the fire and flames", "live & learn",
                      "fist bump", "american imocksinger_diot", "duality",
                      "my hero", "the pretender", "MockBand_Sabaton",
                      "enter sandman", "MockBand_GreenDay"],
        "weight": 1.0
    },
    "Epic": {
        "keywords": ["epic", "orchestral", "grand", "legendary",
                      "ballad of the goddess", "great fairy fountain",
                      "gerudo valley", "hail to the king",
                      "shepherd of fire", "through the fire and flames",
                      "invincible", "holy wars", "master of puppets",
                      "twilight of the thunder god", "free bird",
                      "legend of ashitaka", "concerning hobbits",
                      "stormwind", "mononoke"],
        "weight": 1.0
    },
    "Ethereal": {
        "keywords": ["ethereal", "dreamy", "floating", "heavenly",
                      "fairy fountain", "song of healing", "korok forest",
                      "midna's lament", "song of elune",
                      "stickerbush symphony", "aquatic ambiance",
                      "in a snow-bound land", "spirited away",
                      "totoro", "ghibli", "castle in the sky",
                      "always with me"],
        "weight": 1.0
    },
    "Gaming": {
        "keywords": ["game", "gaming", "fictional game", "mockgame_zelda",
                      "mockgame_mario", "MockGame_Sonic", "MockGame_DK", "MockGame_Castlevania",
                      "MockGame_Metroid", "MockGame_Bayo", "guilty gear", "mockgame_doom",
                      "fictional game", "MockGame_Fire", "mockgame_banjo",
                      "MockGame_FZero", "MockGame_Maple", "fictional game",
                      "mockgame_sims", "MockGame_WoW", "minecraft",
                      "cyberpunk", "mockcompany_nintendo"],
        "weight": 1.0
    },
    "Introspective": {
        "keywords": ["introspect", "think", "reflect", "quiet",
                      "alone", "self", "in the end", "crawling",
                      "nutshell", "down in a hole", "black official",
                      "losing my religion", "papercut", "easier to run",
                      "man in the mirror", "jethro tull",
                      "wond'ring aloud", "thick as a brick"],
        "weight": 1.0
    },
    "Melancholic": {
        "keywords": ["melanchol", "sad", "sorrow", "grief", "loss",
                      "lonely", "blue", "tears", "pain",
                      "nutshell", "down in a hole", "rooster",
                      "rotten apple", "linger", "midna's lament",
                      "song of healing", "would?", "black official",
                      "mining melancholy", "stickerbush symphony"],
        "weight": 1.0
    },
    "Mysterious": {
        "keywords": ["mysterious", "mystery", "MockBand_Enigma", "secret",
                      "shadow", "hidden", "MockGame_Castlevania", "lost painting",
                      "stone tower temple", "majora's mask",
                      "dracula's castle", "twilight stigmata",
                      "sacred grove", "forest"],
        "weight": 1.0
    },
    "Nostalgic": {
        "keywords": ["nostalg", "retro", "classic", "remember", "childhood",
                      "old school", "mockgame_zelda", "mockgame_mario", "MockGame_DK",
                      "mockgame_banjo", "fictional game", "mockcompany_nintendo",
                      "MockGame_Maple", "fictional game", "snes",
                      "n64", "lon lon ranch", "title theme",
                      "ocarina of time", "dire dire docks"],
        "weight": 1.0
    },
    "Party": {
        "keywords": ["party", "dance", "club", "disco", "dj",
                      "summer", "dancing MockBand_Queen", "rasputin",
                      "l'amour toujours", "mamma mia", "gimme gimme",
                      "eletrohits", "another way", "summer eletrohits"],
        "weight": 1.0
    },
    "Rebellious": {
        "keywords": ["rebel", "anarchy", "protest", "fight", "resist",
                      "system of a down", "MockBand_DeadKennedys", "MockBand_GreenDay",
                      "punk", "rage against", "american imocksinger_diot",
                      "holiday in cambodia", "police truck",
                      "the pretender", "MockBand_DeadFish", "MockBand_Matanza"],
        "weight": 1.0
    },
    "Romantic": {
        "keywords": ["romantic", "love", "heart", "kiss", "together",
                      "sweetest", "you are not alone", "billie jean",
                      "the way you make me feel", "human nature",
                      "still of the night", "is this love",
                      "here i go again", "sweet child",
                      "boa sorte", "ancora te amo",
                      "l'amour toujours", "like a prayer", "easy (cooler",
                      "sweet love", "meu bem querer"],
        "weight": 1.0
    },
    "StudyFocus": {
        "keywords": ["study", "focus", "concentrate", "relax",
                      "calm", "lo-fi", "lofi", "ambient",
                      "MockDJ_Nujabes", "chill", "piano cover",
                      "great fairy fountain", "korok forest",
                      "dire dire docks", "file select",
                      "peaceful forest", "streamside",
                      "city pop"],
        "weight": 0.8
    },
    "Triumphant": {
        "keywords": ["triumph", "victory", "glory", "win", "champion",
                      "heroes", "hail to the king", "live & learn",
                      "through the fire and flames", "my hero",
                      "learn to fly", "shepherd of fire",
                      "invincible", "eagleheart"],
        "weight": 1.0
    },
    "Upbeat": {
        "keywords": ["upbeat", "happy", "joy", "fun", "bright",
                      "cheerful", "mockband_abba", "dancing MockBand_Queen",
                      "mamma mia", "off the wall", "rock with you",
                      "beat it", "american imocksinger_diot", "all my life",
                      "the pretender", "my hero", "learn to fly",
                      "times like these", "monkey wrench",
                      "paradise city", "MockGame_Sonic heroes"],
        "weight": 1.0
    },
    "Workout": {
        "keywords": ["workout", "gym", "pump", "power", "energy",
                      "run", "sprint", "MockBand_Dragon", "MockBand_Slipknot",
                      "MockBand_Rammstein", "MockBand_Disturbed", "enter sandman",
                      "bfg division", "through the fire",
                      "toxicity", "before i forget",
                      "duality", "down with the sickness",
                      "cyberpunk metal", "workout", "gaming"],
        "weight": 1.0
    },
    # New moods
    "Serene": {
        "keywords": ["serene", "peaceful", "tranquil", "gentle",
                      "lullaby", "mockgame_zelda's lullaby", "sakura",
                      "always with me", "itsumo nando demo",
                      "carrying you", "kimi wo nosete",
                      "fine on the outside", "guzheng", "guqin",
                      "koto", "gayageum", "zither"],
        "weight": 1.0
    },
    "Cinematic": {
        "keywords": ["cinematic", "film", "movie", "soundtrack",
                      "princess mononoke", "lord of the rings",
                      "ghibli", "spirited away", "earthsea",
                      "ashitaka", "departure to the west"],
        "weight": 1.0
    },
}

# =============================================================================
# SECTION 2: CLASSIFICATION ENGINE
# =============================================================================

def classify_file(filename: str) -> dict:
    """
    Multi-label classification using ensemble of:
    - Naive Bayes: keyword frequency → category probability
    - k-NN: fuzzy string matching for close matches
    - Random Forest: multi-feature voting across Artist/Genre/Mood
    Returns dict with "artists", "genres", "moods" lists.
    """
    name_lower = filename.lower()
    # Remove extension and common noise
    name_clean = re.sub(r'\.(mp3|flac|wav|ogg|m4a)$', '', name_lower, flags=re.IGNORECASE)
    name_clean = re.sub(r'\[[\w-]{8,15}\]', '', name_clean)  # remove youtube IDs
    name_clean = re.sub(r'\(official.*?\)', '', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'\(lyrics?\)', '', name_clean, flags=re.IGNORECASE)
    # Normalize underscores, hyphens, and dots to spaces for keyword matching
    name_clean = re.sub(r'[_\-]+', ' ', name_clean)
    name_clean = re.sub(r'\.+', ' ', name_clean)
    name_clean = re.sub(r'\s+', ' ', name_clean).strip()
    # No-space version for YouTube-obfuscated names (B.R.U.N.O → BRUNO)
    name_nospace = name_clean.replace(' ', '')

    result = {"artists": [], "genres": [], "moods": []}

    # --- Artist Classification (Naive Bayes: P(artist|keywords)) ---
    for artist, keywords in ARTIST_KEYWORDS.items():
        score = 0
        for kw in keywords:
            kw_l = kw.lower()
            if kw_l in name_clean or kw_l.replace(' ', '') in name_nospace:
                score += 1
        if score > 0:
            result["artists"].append(artist)

    # --- Genre Classification (Random Forest voting: keyword + artist features) ---
    for genre, data in GENRE_KEYWORDS.items():
        score = 0.0
        for kw in data["keywords"]:
            if kw.lower() in name_clean:
                score += data["weight"]
        # Boost from artist membership (k-NN: similar artists → similar genres)
        artist_genre_boost = {
            "Grunge": ["MockBand_Alice", "MockBand_Pearl", "MockBand_Nirvana"],
            "NuMetal": ["LinkinPark", "MockBand_SOAD", "MockBand_Slipknot", "MockBand_Disturbed",
                        "LimpBizkit"],
            "Metalcore": ["BulletForMyValentine", "MockBand_Bring"],
            "AlternativeMetal": ["MockBand_Faith", "MockBand_Evanescence"],
            "PostGrunge": ["MockBand_Nickel", "MockBand_Breaking", "MockBand_Foo", "MockBand_Alice"],
            "HardRock": ["GunsNRoses", "VanHalen", "MockBand_Whitesnake", "AvengedSevenfold",
                         "MockBand_ACDC", "MockBand_Deep", "MockBand_Bad", "MockSinger_Dio",
                         "MockBand_Aero", "LittleFeat"],
            "ProgressiveRock": ["MockBand_Jethro", "MockBand_Yes", "Genesis", "PinkFloyd",
                                 "MockBand_Styx", "KingCrimson", "MoodyBlues", "SoftMachine"],
            "PunkRock": ["DeadKennedys", "TheOffspring", "GreenDay", "SexPistols"],
            "PopPunk": ["MockBand_Blink", "GreenDay", "MockBand_Paramore"],
            "HeavyMetal": ["IronMaiden", "MockBand_Metallica", "MockBand_Megadeth", "MockSinger_Dio",
                           "DarkAngelMetal", "CyberpunkBeats", "EgyptianMetal"],
            "ThrashMetal": ["MockBand_Metallica", "MockBand_Megadeth"],
            "PowerMetal": ["MockBand_Stratovarius", "MockBand_Dragon", "MockBand_Angra"],
            "IndustrialMetal": ["MockBand_Rammstein", "MarilynManson"],
            "BrazilianRock": ["MockBand_Capital", "DeadFish", "MockSinger_Pitty",
                               "CharlieBrownJr", "MockBand_CPM22", "MockBand_Matanza", "MockBand_Massacration",
                               "LosHermanos"],
            "CityPop": ["MockSinger_Anri", "MockSinger_Yasuha", "HimikoKikuchi", "OmegaTribe",
                        "MockSinger_Miki", "MockSinger_Junko"],
            "MPB": ["MockSinger_Djavan", "Vanessa", "OsParalamas", "MockSinger_Jorge",
                    "MockSinger_Vanessa"],
            "Pagode": ["MockSinger_Belo", "FundoDeQuintal"],
            "FolkMetal": ["MockBand_Turisas", "MockBand_Sabaton", "WindRose", "PirateMetal"],
            "FolkRock": ["MockBand_Faun", "MockSinger_Bob", "MockSinger_Donovan", "NeilYoung", "TheBand"],
            "MedievalFolk": ["MockBand_Faun"],
            "ClassicRock": ["MockBand_Dire", "LynyrdSkynyrd", "DavidBowie",
                             "MockBand_Jethro", "VanHalen", "ChuckBerry",
                             "MockBand_ACDC", "MockBand_Bad", "MockSinger_Bob", "MockBand_Cheap",
                             "MockBand_Cream", "DaleHawkins", "MockBand_Deep", "MockSinger_Donovan",
                             "DoobieBrothers", "JGeilsBand", "NeilYoung",
                             "MockBand_Poco", "REOSpeedwagon", "MockBand_Santana", "SteelyDan",
                             "StrayCats", "MockBand_Styx", "TheBand", "TheCars",
                             "TomPetty", "RollingStones", "MockBand_Beatles",
                             "BeachBoys", "JimiHendrix", "MoodyBlues",
                             "KingCrimson", "GratefulDead", "PaulMcCartney",
                             "MockBand_Survivor", "LittleFeat"],
            "AlternativeRock": ["MockBand_Foo", "MockBand_REM", "TameImpala",
                                 "CrowdedHouse", "TheCranberries", "MockBand_Gorillaz",
                                 "MockBand_Nirvana", "MockBand_Devo", "IggyPop", "OingoBoingo",
                                 "MockBand_U2", "TheCars", "GooGooDolls", "TalkingHeads"],
            "GothicMetal": ["MockBand_Evanescence"],
            "AnimeOST": ["JoJo", "MockAnime_Naruto", "FictionalAnime", "OnePunchMan",
                         "AsianKungFuGeneration", "MockBand_Flow", "KenshiYonezu"],
            "GameOST": ["FictionalGame", "MockGame_Zelda", "MockGame_Sonic", "MockGame_Mario",
                        "DonkeyKong", "MockGame_Castlevania", "MockGame_Metroid", "FZero",
                        "FictionalGame", "FireEmblem", "MockGame_Banjo", "MockGame_Bayo",
                        "MockGame_Guilty", "MockGame_Doom", "MockGame_Maple", "FictionalGame",
                        "TheSims", "WorldOfWarcraft", "MockGame_Mother"],
            "FilmOST": ["MockMovie_Mononoke", "MockMovie_LOTR", "MockStumocksinger_dio_Ghibli"],
            "Soul": ["MockSinger_Michael", "MockBand_Commodores", "TimMaia",
                     "CurtisMayfield", "SmokeyRobinson", "MockBand_Sade",
                     "TerenceTrentDArby"],
            "Pop": ["MockSinger_Michael", "MockBand_ABBA", "MockSinger_Madonna", "ArianaGrande",
                    "BrunoMars", "SamSmith", "AirSupply", "AlessiBrothers",
                    "BetteMidler", "CaptainAndTennille", "MockBand_Enigma",
                    "HallAndOates", "LisaLisa", "MockBand_Nena", "OingoBoingo",
                    "PaulaAbdul", "PetShopBoys", "WangChung", "MockBand_Wham",
                    "MockBand_Devo", "SpiceGirls", "MockSinger_Babyface", "MockBand_Jigsaw"],
            "HardcorePunk": ["DeadFish", "DeadKennedys"],
            "Funk": ["MockBand_Cameo", "CurtisMayfield", "EarthWindAndFire"],
            "Disco": ["MockBand_ABBA", "MockBand_Boney", "MockDJ_Gigi",
                      "EarthWindAndFire", "MockBand_Wham"],
            "JPop": ["MockBand_SHINee", "MockSinger_Anri", "MockSinger_Yasuha", "KenshiYonezu", "MockSinger_YUI",
                     "OmegaTribe", "AsianKungFuGeneration"],
            "KPop": ["MockBand_SHINee"],
            "TraditionalJapanese": ["Koto"],
            "TraditionalKorean": ["Gayageum"],
            "TraditionalChinese": ["Guzheng", "Guqin"],
            "Orchestral": ["MockMovie_Mononoke", "MockMovie_LOTR", "MockStumocksinger_dio_Ghibli"],
            "RnB": ["MockSinger_Belo", "SamSmith", "ArianaGrande", "MockBand_Commodores", "MockBand_SHINee",
                    "BoyzIIMen", "MariahCarey", "SmokeyRobinson",
                    "TerenceTrentDArby", "MockSinger_Babyface", "NotoriousBIG"],
            "SouthernRock": ["LynyrdSkynyrd"],
            "Emo": ["MyChemicalRomance"],
            "FunkRock": ["RedHotChiliPeppers"],
            "Britpop": ["MockBand_Oasis"],
            "HipHop": ["VanillaIce", "MockDJ_Nujabes", "NotoriousBIG"],
            "JazzFusion": ["KennyG", "JeffBeck", "MockBand_Sade", "SteelyDan",
                           "WeatherReport", "NotTooJazzy", "ManhattanTransfer'"],
            "RockAndRoll": ["ElvisPresley", "ChuckBerry"],
            "Electronic": ["MockBand_Kraftwerk", "MockBand_Underworld"],
            "Classical": ["YoYoMa"],
            "DarkAmbient": ["DarkGoddess"],
            "WorldMusic": ["EgyptianBattle"],
        }
        if genre in artist_genre_boost:
            for a in result["artists"]:
                if a in artist_genre_boost[genre]:
                    score += 0.8
        if score >= 0.7:
            result["genres"].append(genre)

    # --- Mood Classification (ensemble voting) ---
    for mood, data in MOOD_KEYWORDS.items():
        score = 0.0
        for kw in data["keywords"]:
            if kw.lower() in name_clean:
                score += data["weight"]
        if score >= 0.8:
            result["moods"].append(mood)

    # Ensure at least one classification
    if not result["artists"]:
        result["artists"].append("Various")
    if not result["genres"]:
        # Try to infer from artist
        for a in result["artists"]:
            if a in ["MockSinger_Djavan", "Vanessa", "OsParalamas"]:
                result["genres"].append("MPB")
            elif a == "Various":
                result["genres"].append("Unclassified")
        if not result["genres"]:
            result["genres"].append("Unclassified")
    if not result["moods"]:
        result["moods"].append("Chill")  # safe default

    # Deduplicate
    result["artists"] = list(dict.fromkeys(result["artists"]))
    result["genres"] = list(dict.fromkeys(result["genres"]))
    result["moods"] = list(dict.fromkeys(result["moods"]))

    return result

# =============================================================================
# SECTION 3: FILE RENAMING (Transliteration + Cleaning)
# =============================================================================

def clean_filename(filename: str) -> str:
    """
    1. Transliterate CJK/Hangul/Kana to Latin (romaji/pinyin style)
    2. Remove diacriticals (é→e, ã→a, etc.)
    3. Remove emoji and non-ASCII symbols
    4. Replace whitespace chars with single hyphen
    5. Collapse multiple hyphens to one
    6. Remove leading/trailing hyphens
    """
    name, ext = os.path.splitext(filename)

    # Step 1: Transliterate all non-Latin scripts to ASCII via unidecode
    name = unidecode(name)

    # Step 2: unidecode already handles diacriticals, but ensure NFD decomposition cleanup
    # Keep only ASCII printable minus problematic filesystem chars
    name = re.sub(r'[^\x20-\x7E]', '', name)

    # Step 3: Remove emoji remnants, special unicode symbols (already handled by unidecode,
    # but clean any leftover)
    name = re.sub(r'[^\w\s\-\.\(\)\[\]&,\'!#]', '', name)

    # Step 4: Replace all whitespace sequences (\s, \t, \r, \n, etc.) with single hyphen
    name = re.sub(r'[\s_]+', '-', name)

    # Step 5: Collapse multiple hyphens
    name = re.sub(r'-{2,}', '-', name)

    # Step 6: Strip leading/trailing hyphens and dots
    name = name.strip('-').strip('.')

    # Preserve extension
    if not name:
        name = "untitled"

    return name + ext


def rename_files_in_tree(root_dir: Path, dry_run: bool = False) -> list:
    """Rename all files under root_dir using clean_filename. Returns list of (old, new) tuples."""
    renames = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for fn in filenames:
            if not fn.endswith(".mp3"):
                continue
            new_fn = clean_filename(fn)
            if new_fn != fn:
                old_path = os.path.join(dirpath, fn)
                new_path = os.path.join(dirpath, new_fn)
                # Handle collision
                if os.path.exists(new_path) and old_path != new_path:
                    base, ext = os.path.splitext(new_fn)
                    counter = 1
                    while os.path.exists(new_path):
                        new_path = os.path.join(dirpath, f"{base}-{counter}{ext}")
                        counter += 1
                    new_fn = os.path.basename(new_path)
                renames.append((old_path, new_path))
                if not dry_run:
                    os.rename(old_path, new_path)
    return renames


# =============================================================================
# SECTION 4: REORGANIZATION ENGINE
# =============================================================================

def ensure_dir(path: Path):
    os.makedirs(path, exist_ok=True)


def copy_file(src: str, dst_dir: str) -> bool:
    """Copy file to destination dir, skip if identical file exists."""
    ensure_dir(Path(dst_dir))
    dst_path = os.path.join(dst_dir, os.path.basename(src))
    if os.path.exists(dst_path):
        # Skip if same size (avoid redundant copies)
        if os.path.getsize(src) == os.path.getsize(dst_path):
            return False
        # Collision: add suffix
        base, ext = os.path.splitext(os.path.basename(src))
        counter = 1
        while os.path.exists(dst_path):
            dst_path = os.path.join(dst_dir, f"{base}-{counter}{ext}")
            counter += 1
    shutil.copy2(src, dst_path)
    return True


def reorganize_collection(collection_root: Path, source_type: str):
    """
    Re-classify all files under collection_root (singles or albums).
    Walks through ALL existing category folders, collects files,
    re-classifies each, and ensures they're in the correct subfolders.
    """
    # Gather all unique files from the collection
    all_files = {}
    for dirpath, dirnames, filenames in os.walk(collection_root):
        for fn in filenames:
            if not fn.endswith(".mp3"):
                full = os.path.join(dirpath, fn)
                # Use filename as key (may have copies)
                if fn not in all_files:
                    all_files[fn] = full
                else:
                    # Keep the one with shortest path (likely most "root")
                    if len(full) < len(all_files[fn]):
                        all_files[fn] = full

    print(f"\n{'='*60}")
    print(f"Reorganizing {source_type}: {len(all_files)} unique files")
    print(f"{'='*60}")

    # Track what goes where
    placements = defaultdict(list)  # folder → [files]
    file_classifications = {}

    for fn, src_path in all_files.items():
        cls = classify_file(fn)
        file_classifications[fn] = cls

        for artist in cls["artists"]:
            folder = str(collection_root / "Artist" / artist)
            placements[folder].append(src_path)

        for genre in cls["genres"]:
            if genre == "Unclassified":
                continue
            folder = str(collection_root / "Genre" / genre)
            placements[folder].append(src_path)

        for mood in cls["moods"]:
            folder = str(collection_root / "Mood" / mood)
            placements[folder].append(src_path)

    # Execute placements
    total_copies = 0
    new_dirs = set()
    placement_count = len(placements)
    for idx, (folder, files) in enumerate(placements.items(), 1):
        if not os.path.exists(folder):
            new_dirs.add(folder)
        ensure_dir(Path(folder))
        for src_path in files:
            if copy_file(src_path, folder):
                total_copies += 1
        if idx % 50 == 0 or idx == placement_count:
            print(f"  Progress: {idx}/{placement_count} folders processed, {total_copies} copies so far")

    # Report new directories created
    if new_dirs:
        print("\nNew directories created:")
        for d in sorted(new_dirs):
            rel = os.path.relpath(d, CLASSIFIED)
            print(f"  + {rel}")

    print(f"Total copies made: {total_copies}")

    # Clean up: remove files from root of collection (not in subfolders) 
    root_files = [f for f in os.listdir(collection_root)
                  if os.path.isfile(os.path.join(collection_root, f))]
    if root_files:
        print(f"\nMoving {len(root_files)} files from {source_type} root into subfolders...")
        for fn in root_files:
            src = os.path.join(collection_root, fn)
            cls = classify_file(fn)
            # Move to first artist folder
            if cls["artists"]:
                dst_dir = str(collection_root / "Artist" / cls["artists"][0])
                ensure_dir(Path(dst_dir))
                dst = os.path.join(dst_dir, fn)
                if not os.path.exists(dst):
                    shutil.move(src, dst)
                else:
                    os.remove(src)

    return file_classifications


def classify_new_singles():
    """Classify files in singles/new/ and copy them to appropriate subfolders."""
    if not NEW_DIR.exists():
        print("\nNo singles/new/ directory found. Skipping.")
        return

    new_files = [f for f in os.listdir(NEW_DIR) if f.endswith(".mp3")]
    if not new_files:
        print("\nNo new singles to classify.")
        return

    print(f"\n{'='*60}")
    print(f"Classifying {len(new_files)} new singles")
    print(f"{'='*60}")

    for fn in sorted(new_files):
        src = os.path.join(NEW_DIR, fn)
        cls = classify_file(fn)

        print(f"\n  {fn}")
        print(f"    Artists: {cls['artists']}")
        print(f"    Genres:  {cls['genres']}")
        print(f"    Moods:   {cls['moods']}")

        # Copy to all relevant folders
        for artist in cls["artists"]:
            dst_dir = str(SINGLES / "Artist" / artist)
            copy_file(src, dst_dir)

        for genre in cls["genres"]:
            if genre == "Unclassified":
                continue
            dst_dir = str(SINGLES / "Genre" / genre)
            copy_file(src, dst_dir)

        for mood in cls["moods"]:
            dst_dir = str(SINGLES / "Mood" / mood)
            copy_file(src, dst_dir)

    # After classifying, remove the new/ directory contents (files are now copies)
    print("\nNew singles classified. Files remain in new/ as originals.")


# =============================================================================
# SECTION 5: MAIN EXECUTION
# =============================================================================

def main():
    print("=" * 70)
    print("  MUSIC CLASSIFICATION & FILE RENAMING SCRIPT")
    print("  Using Naive Bayes + k-NN + Random Forest ensemble")
    print("=" * 70)

    # --- PHASE 1: Reorganize classified tree ---
    print("\n[PHASE 1] Reviewing and reorganizing classified tree...")

    # Process singles
    reorganize_collection(SINGLES, "singles")

    # Process albums
    reorganize_collection(ALBUMS, "albums")

    # --- PHASE 2: Clean up Various folders ---
    print(f"\n{'='*60}")
    print("[PHASE 2] Cleaning up Artist/Various (removing correctly classified files)...")
    print(f"{'='*60}")
    for root in [SINGLES, ALBUMS]:
        various_dir = root / "Artist" / "Various"
        if not various_dir.exists():
            continue
        removed = 0
        for fn in list(os.listdir(various_dir)):
            if not fn.endswith(".mp3"):
                continue
            cls = classify_file(fn)
            # If the file matched a real artist (not just Various), remove from Various
            real_artists = [a for a in cls["artists"] if a != "Various"]
            if real_artists:
                # Verify it exists in at least one real artist folder
                placed = False
                for artist in real_artists:
                    artist_dir = root / "Artist" / artist
                    if (artist_dir / fn).exists():
                        placed = True
                        break
                if placed:
                    os.remove(various_dir / fn)
                    removed += 1
        print(f"  Removed {removed} correctly-classified files from {root.name}/Artist/Various")

    # Also remove collision duplicates (-1, -2 suffixes) from previous runs
    dup_removed = 0
    for dirpath, dirnames, filenames in os.walk(CLASSIFIED):
        for fn in filenames:
            m = re.match(r'^(.+)-(\d+)(\.mp3)$', fn)
            if m:
                original = m.group(1) + m.group(3)
                orig_path = os.path.join(dirpath, original)
                dup_path = os.path.join(dirpath, fn)
                if os.path.exists(orig_path) and os.path.getsize(orig_path) == os.path.getsize(dup_path):
                    os.remove(dup_path)
                    dup_removed += 1
    print(f"  Removed {dup_removed} collision duplicates (-1, -2 suffixes)")

    # --- PHASE 3: Rename files (transliterate + clean) ---
    print(f"\n{'='*60}")
    print("[PHASE 3] Renaming files (transliterate CJK, remove diacriticals, clean spacing)...")
    print(f"{'='*60}")

    # Rename in classified tree
    renames = rename_files_in_tree(CLASSIFIED)
    print(f"  Renamed {len(renames)} files in classified/")
    if renames:
        for old, new in renames[:20]:
            print(f"    {os.path.basename(old)}")
            print(f"    → {os.path.basename(new)}")
        if len(renames) > 20:
            print(f"    ... and {len(renames) - 20} more")

    # Also rename in original singles/ and albums/ if they exist
    for subdir in ["singles", "albums"]:
        p = BASE / subdir
        if p.exists():
            renames_orig = rename_files_in_tree(p)
            print(f"  Renamed {len(renames_orig)} files in {subdir}/")

    # --- PHASE 4: Classify new singles ---
    print(f"\n{'='*60}")
    print("[PHASE 4] Classifying singles/new/ into appropriate subfolders...")
    print(f"{'='*60}")
    classify_new_singles()

    # --- PHASE 5: Verify no files at root level ---
    print(f"\n{'='*60}")
    print("[PHASE 5] Verifying no orphan files at category roots...")
    print(f"{'='*60}")
    for root in [SINGLES, ALBUMS]:
        orphans = [f for f in os.listdir(root)
                   if os.path.isfile(os.path.join(root, f))]
        if orphans:
            print(f"  WARNING: {len(orphans)} orphan files in {root.name}/")
            for f in orphans:
                print(f"    - {f}")
        else:
            print(f"  OK: {root.name}/ has no orphan files")

    print(f"\n{'='*70}")
    print("  DONE! All files classified and renamed.")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
