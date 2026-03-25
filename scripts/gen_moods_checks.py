#!/usr/bin/env python3
"""Generate docs/guidelines/moods-checks.html from track-mood data."""
import json, re, html, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Load data ────────────────────────────────────────────────────────────────
with open("/tmp/track_moods.json") as f:
    track_moods: dict[str, list[str]] = json.load(f)

with open(os.path.join(BASE, "docs/guidelines/moods.txt")) as f:
    ALL_MOODS = [line.strip() for line in f if line.strip()]

# ── Old→new mood migration map (for the 23→66 expansion) ────────────────────
# Tracks that were in removed moods get re-mapped:
OLD_TO_NEW = {
    "Gaming": ["Nostalgic", "Adventurous"],   # context→actual moods
    "Workout": ["Energetic", "Aggressive"],   # context→actual moods
    "Ambient": ["Serene", "Meditative"],
    "Party": ["Danceful", "Ecstatic"],
    "Cinematic": ["Awe-inspired", "Epic"],
}

# ── Keyword→mood heuristics for new moods ────────────────────────────────────
MOOD_KW = {
    "Adventurous": ["adventure", "quest", "journey", "dragon", "open your heart",
                     "escape from the city", "gerudo valley", "gangplank galleon",
                     "pirate", "MockGame_Sonic heroes", "fist bump", "open world"],
    "Aggressive": ["aggressive", "rage", "angry", "violent", "heavy",
                   "MockBand_Slipknot", "system of a down", "MockBand_Disturbed", "MockBand_Rammstein",
                   "MockBand_Megadeth", "toxicity", "chop suey", "before i forget",
                   "down with the sickness", "bfg division", "holy wars",
                   "sonne", "MockBand_DeadFish", "MockBand_DeadKennedys", "psychosocial",
                   "duality", "the only thing they fear"],
    "Anguished": ["anguish", "agony", "torment", "despair", "hurt",
                  "nutshell", "down in a hole", "black", "unforgiven",
                  "rooster", "would?", "rotten apple"],
    "Awe-inspired": ["awe", "granmocksinger_diose", "magnificent", "majestic",
                     "great gig in the sky", "zarathustra", "halo theme",
                     "liberi fatali", "one-winged angel"],
    "Bittersweet": ["bittersweet", "stickerbush", "to zanarkand",
                    "mining melancholy", "aquatic ambiance",
                    "in a snow-bound land", "theme of laura"],
    "Brooding": ["brooding", "brood", "simmering", "black hole sun",
                 "creep", "hotel california", "fade to black",
                 "the becoming", "heart-shaped box"],
    "Chaotic": ["chaotic", "chaos", "byob", "toxicity", "bohemian rhapsody",
                "psycho", "cat's foot", "prison song"],
    "Chill": ["chill", "lo-fi", "lofi", "mellow", "laid-back", "easy listening",
              "MockDJ_Nujabes", "city pop", "feather", "aruarian dance",
              "dire dire docks", "file select"],
    "Contemplative": ["contemplate", "ponder", "thinking", "breathe",
                      "time MockBand_PinkFloyd", "roundabout", "sound of silence",
                      "starry night", "vincent"],
    "Cozy": ["cozy", "warm", "home", "fireplace", "animal crossing",
             "lon lon ranch", "sunday morning", "here comes the sun",
             "coffee", "town theme"],
    "Danceful": ["dance", "disco", "club", "dancefloor", "get lucky",
                 "around the world", "september", "le freak",
                 "i gotta feeling", "dancing MockBand_Queen", "rasputin",
                 "eletrohits"],
    "Dark": ["dark", "sinister", "evil", "shadow", "mockgame_doom", "death",
             "vampire", "dracula", "gothic", "MockGame_Castlevania", "bloody tears",
             "cyberpunk", "dark angel", "mockband_mockband_mockband_evanescence", "the devil in i"],
    "Defiant": ["defiant", "we will rock you", "eye of the tiger",
                "we are the champions", "defy", "stand up",
                "overcome", "won't back down"],
    "Depressive": ["depress", "hopeless", "numb", "disintegration",
                   "adam's song", "how soon is now", "coma white",
                   "needle and the damage done"],
    "Desperate": ["desperate", "desperation", "in the end", "one step closer",
                  "numb encore", "running up that hill", "clocks",
                  "crawling", "breaking the habit"],
    "Determined": ["determined", "unstoppable", "harder better faster",
                   "lose yourself", "don't stop me now",
                   "won't back down", "eye of the tiger"],
    "Ecstatic": ["ecstatic", "euphoria", "euphoric", "don't stop me now",
                 "mr. brightside", "bohemian rhapsody",
                 "i feel good", "celebration"],
    "Emotional": ["emotional", "tears", "cry", "feel", "heart", "love",
                  "loss", "pearl jam", "MockBand_Alice", "linger",
                  "don't dream it's over", "billie jean",
                  "you are not alone", "midna's lament",
                  "tears of the dragon"],
    "Energetic": ["energetic", "fast", "power", "high energy",
                  "MockGame_Sonic", "MockBand_Dragon", "MockBand_Stratovarius",
                  "through the fire and flames", "live & learn",
                  "fist bump", "american imocksinger_diot", "duality",
                  "my hero", "the pretender", "MockBand_Sabaton",
                  "enter sandman", "MockBand_GreenDay"],
    "Epic": ["epic", "orchestral", "grand", "legendary",
             "ballad of the goddess", "great fairy fountain",
             "gerudo valley", "hail to the king", "shepherd of fire",
             "master of puppets", "twilight of the thunder god",
             "free bird", "mononoke", "stormwind"],
    "Ethereal": ["ethereal", "dreamy", "floating", "heavenly",
                 "fairy fountain", "song of healing", "korok forest",
                 "song of elune", "stickerbush symphony",
                 "aquatic ambiance", "spirited away", "totoro",
                 "ghibli", "castle in the sky", "always with me"],
    "Explosive": ["explosive", "explode", "blast", "battery",
                  "aces high", "enter sandman",
                  "smells like teen spirit", "bulls on parade"],
    "Focused": ["focused", "concentration", "precision",
                "march of the pigs", "logical song"],
    "Frenzy": ["frenzy", "frenetic", "blast beat", "shred",
               "painkiller", "tornado of souls", "eruption",
               "fury of the storm", "surfing with the alien"],
    "Furious": ["furious", "fury", "rage", "break stuff",
                "head like a hole", "killing in the name"],
    "Gritty": ["gritty", "grit", "raw", "blues rock", "dirty",
               "black dog", "whole lotta love", "seven nation army",
               "ball and biscuit", "superstition"],
    "Groovy": ["groovy", "groove", "funky", "funk", "soulful",
               "give it away", "superstition", "brick house",
               "higher ground", "fire", "MockBand_Commodores",
               "MockSinger_Tim", "MockBand_Fundo", "samba",
               "cant stop", "dani california"],
    "Hardworking": ["working", "worker", "labor", "grind",
                    "9 to 5", "blue collar", "working for the weekend"],
    "Heartbreak": ["heartbreak", "heartbroken", "broken heart",
                   "someone like you", "nothing compares",
                   "skinny love", "back to december",
                   "stay with me"],
    "Heroic": ["heroic", "hero", "Superman", "princes of the universe",
               "a change of seasons", "final countdown",
               "the imperial march"],
    "Hypnotic": ["hypnotic", "trance", "loop", "repetitive",
                 "music for airports", "autobahn", "trans-europe express",
                 "teardrop", "porcelain"],
    "Introspective": ["introspect", "think", "reflect", "quiet",
                      "alone", "self", "in the end", "crawling",
                      "nutshell", "losing my religion", "papercut",
                      "easier to run", "man in the mirror",
                      "wond'ring aloud", "thick as a brick"],
    "Jaded": ["jaded", "cynical", "disillusioned", "boulevard of broken dreams",
              "creep", "when i come around", "bitter"],
    "Joyful": ["joyful", "joy", "happy", "delight", "wonderful",
               "happy pharrell", "here comes the sun",
               "i wanna dance with somebody", "walking on sunshine",
               "lovely day"],
    "Lonely": ["lonely", "alone", "isolation", "isolated",
               "mad world", "eleanor rigby", "the stranger",
               "only nine inch nails"],
    "Macabre": ["macabre", "death", "decay", "grotesque",
                "danse macabre", "ghost love score", "for whom the bell tolls",
                "welcome home sanitarium", "grim grinning ghosts",
                "halloween"],
    "Meditative": ["meditative", "meditation", "zen", "yoga",
                   "spiegel im spiegel", "gymnop", "weightless",
                   "buddha"],
    "Melancholic": ["melanchol", "sad", "sorrow", "grief", "loss",
                    "blue", "tears", "pain", "nutshell",
                    "down in a hole", "rooster", "rotten apple",
                    "linger", "midna's lament", "song of healing",
                    "mining melancholy", "stickerbush symphony"],
    "Mysterious": ["mysterious", "mystery", "MockBand_Enigma", "secret",
                   "shadow", "hidden", "MockGame_Castlevania", "lost painting",
                   "stone tower temple", "majora's mask",
                   "dracula's castle", "twilight stigmata",
                   "sacred grove"],
    "Nostalgic": ["nostalg", "retro", "classic", "remember", "childhood",
                  "old school", "mockgame_zelda", "mockgame_mario", "MockGame_DK",
                  "mockgame_banjo", "fictional game", "mockcompany_nintendo",
                  "MockGame_Maple", "fictional game", "snes",
                  "n64", "lon lon ranch", "title theme",
                  "ocarina of time", "dire dire docks"],
    "Ominous": ["ominous", "forboding", "impending", "scarecrow",
                "premonition", "fear of the dark", "dread"],
    "Optimistic": ["optimistic", "hopeful", "promising",
                   "somewhere over the rainbow", "what a wonderful world",
                   "brand new day", "beautiful day",
                   "waiting on the world to change"],
    "Peaceful": ["peaceful", "peace", "calm", "idyllic", "pastoral",
                 "gentle", "safe", "fields of gold",
                 "lon lon ranch", "spring vivaldi",
                 "morning has broken"],
    "Playful": ["playful", "silly", "bouncy", "quirky",
                "bob-omb battlefield", "coconut mall",
                "yakety sax", "zip-a-dee-doo-dah", "goofy"],
    "Rebellious": ["rebel", "anarchy", "protest", "fight", "resist",
                   "system of a down", "MockBand_DeadKennedys", "MockBand_GreenDay",
                   "punk", "rage against", "american imocksinger_diot",
                   "holiday in cambodia", "police truck",
                   "the pretender", "MockBand_DeadFish", "MockBand_Matanza"],
    "Relaxed": ["relaxed", "relax", "easy going", "laid back",
                "banana pancakes", "better together", "jack johnson",
                "bob marley", "three little birds",
                "no woman no cry"],
    "Resigned": ["resigned", "accept", "let go", "yesterday MockBand_Beatles",
                 "sound of silence", "against the wind", "old man"],
    "Reverent": ["reverent", "sacred", "holy", "divine",
                 "ave maria", "o fortuna", "requiem",
                 "gregorian"],
    "Romantic": ["romantic", "love", "heart", "kiss", "together",
                 "sweetest", "you are not alone", "billie jean",
                 "the way you make me feel", "human nature",
                 "is this love", "sweet child", "l'amour toujours",
                 "like a prayer", "sweet love", "meu bem querer"],
    "Sad": ["sad", "sorrow", "crying", "tears in heaven",
            "everybody hurts", "with or without you",
            "wish you were here"],
    "Sensual": ["sensual", "seductive", "erotic", "let's get it on",
                "sexual healing", "wicked game", "earned it"],
    "Serene": ["serene", "tranquil", "still", "lullaby",
               "mockgame_zelda's lullaby", "sakura", "always with me",
               "itsumo nando demo", "carrying you", "kimi wo nosete",
               "fine on the outside", "guzheng", "guqin",
               "koto", "gayageum", "zither"],
    "Sleepy": ["sleepy", "sleep", "lullaby", "drowsy",
               "comptine", "weightless", "clair de lune"],
    "Soaring": ["soaring", "soar", "flying", "ascend",
                "don't stop believin", "separate ways",
                "open arms", "i believe i can fly",
                "defying gravity"],
    "Spiritual": ["spiritual", "transcend", "soul", "divine",
                  "koyaanisqatsi", "agnus dei", "hallelujah",
                  "amazing grace"],
    "StudyFocus": ["study", "focus", "concentrate", "lo-fi", "lofi",
                   "ambient", "MockDJ_Nujabes", "piano cover",
                   "great fairy fountain", "korok forest",
                   "dire dire docks", "file select",
                   "peaceful forest", "streamside", "city pop"],
    "Surreal": ["surreal", "psychedelic", "trippy",
                "lucy in the sky", "interstellar overdrive",
                "a whiter shade of pale", "echoes MockBand_PinkFloyd",
                "tomorrow never knows"],
    "Suspenseful": ["suspense", "tension", "build-up", "thriller",
                    "vampire killer", "dracula's castle",
                    "psycho", "mission impossible", "mockgame_doom e1m1",
                    "boss fight", "boss battle"],
    "Tender": ["tender", "gentle", "delicate", "blackbird",
               "norwegian wood", "wild horses", "father and son"],
    "Tense": ["tense", "anxiety", "anxious", "uneasy",
              "jaws", "in the hall of the mountain king",
              "closer nine inch nails"],
    "Triumphant": ["triumph", "victory", "glory", "win", "champion",
                   "heroes", "hail to the king", "live & learn",
                   "through the fire and flames", "my hero",
                   "learn to fly", "shepherd of fire",
                   "invincible", "eagleheart"],
    "Upbeat": ["upbeat", "happy", "joy", "fun", "bright",
               "cheerful", "mockband_abba", "dancing MockBand_Queen", "mamma mia",
               "off the wall", "rock with you", "beat it",
               "american imocksinger_diot", "paradise city", "MockGame_Sonic heroes",
               "all my life", "times like these", "monkey wrench"],
    "Vengeful": ["vengeful", "vengeance", "revenge", "retribution",
                 "the god that failed", "prison sex", "last resort"],
    "Whimsical": ["whimsical", "fanciful", "fairy tale",
                  "totoro", "arrietty", "caramell", "fraggle rock",
                  "ghibli"],
    "Wistful": ["wistful", "longing gently", "dust in the wind",
                "landslide", "river joni mitchell",
                "both sides now"],
    "Yearning": ["yearning", "yearn", "longing", "desire",
                 "can't help falling in love", "in your eyes",
                 "more than words", "everlong",
                 "i will always love you"],
}

# ── Additional artist→mood inference ─────────────────────────────────────────
ARTIST_MOOD_HINTS = {
    "MockDJ_Nujabes": ["Chill", "Contemplative", "Introspective"],
    "alice-in-chains": ["Anguished", "Brooding", "Melancholic"],
    "mockband_alice": ["Anguished", "Brooding", "Melancholic"],
    "mockband_alice": ["Anguished", "Brooding", "Melancholic"],
    "system-of-a-down": ["Chaotic", "Rebellious", "Aggressive"],
    "mockband_soad": ["Chaotic", "Rebellious", "Aggressive"],
    "soad": ["Chaotic", "Rebellious", "Aggressive"],
    "pink-floyd": ["Contemplative", "Surreal", "Dark"],
    "pinkfloyd": ["Contemplative", "Surreal", "Dark"],
    "MockBand_Metallica": ["Aggressive", "Epic", "Dark"],
    "linkin-park": ["Desperate", "Anguished", "Energetic"],
    "linkinpark": ["Desperate", "Anguished", "Energetic"],
    "green-day": ["Rebellious", "Energetic", "Jaded"],
    "greenday": ["Rebellious", "Energetic", "Jaded"],
    "red-hot-chili-peppers": ["Groovy", "Energetic", "Upbeat"],
    "rhcp": ["Groovy", "Energetic", "Upbeat"],
    "redhotchilipeppers": ["Groovy", "Energetic", "Upbeat"],
    "MockBand_Queen": ["Triumphant", "Epic", "Ecstatic"],
    "iron-maiden": ["Epic", "Energetic", "Heroic"],
    "ironmaiden": ["Epic", "Energetic", "Heroic"],
    "michael-jackson": ["Groovy", "Upbeat", "Emotional"],
    "mocksinger_michael": ["Groovy", "Upbeat", "Emotional"],
    "avenged-sevenfold": ["Epic", "Aggressive", "Dark"],
    "avengedsevenfold": ["Epic", "Aggressive", "Dark"],
    "MockBand_Disturbed": ["Aggressive", "Furious", "Energetic"],
    "scorpions": ["Romantic", "Energetic", "Nostalgic"],
    "journey": ["Soaring", "Upbeat", "Nostalgic"],
    "phil-collins": ["Emotional", "Romantic", "Nostalgic"],
    "philcollins": ["Emotional", "Romantic", "Nostalgic"],
    "genesis": ["Surreal", "Epic", "Contemplative"],
    "jethro-tull": ["Contemplative", "Whimsical", "Introspective"],
    "mockband_jethro": ["Contemplative", "Whimsical", "Introspective"],
    "MockSinger_Prince": ["Groovy", "Sensual", "Ecstatic"],
    "MockBand_Oasis": ["Defiant", "Nostalgic", "Upbeat"],
    "MockBand_REM": ["Introspective", "Melancholic", "Jaded"],
    "sam-smith": ["Heartbreak", "Emotional", "Sad"],
    "samsmith": ["Heartbreak", "Emotional", "Sad"],
    "ne-yo": ["Romantic", "Groovy", "Upbeat"],
    "neyo": ["Romantic", "Groovy", "Upbeat"],
    "bruno-mars": ["Upbeat", "Groovy", "Danceful"],
    "brunomars": ["Upbeat", "Groovy", "Danceful"],
    "tim-maia": ["Groovy", "Romantic", "Joyful"],
    "timmaia": ["Groovy", "Romantic", "Joyful"],
    "capital-inicial": ["Rebellious", "Nostalgic", "Energetic"],
    "mockband_capital": ["Rebellious", "Nostalgic", "Energetic"],
    "charlie-brown-jr": ["Rebellious", "Chill", "Groovy"],
    "charliebrownjr": ["Rebellious", "Chill", "Groovy"],
    "mockband_cpm22": ["Energetic", "Rebellious", "Desperate"],
    "ls-jack": ["Romantic", "Chill", "Nostalgic"],
    "lsjack": ["Romantic", "Chill", "Nostalgic"],
    "fundo-de-quintal": ["Groovy", "Joyful", "Nostalgic"],
    "fundodequintal": ["Groovy", "Joyful", "Nostalgic"],
    "chuck-berry": ["Groovy", "Joyful", "Energetic"],
    "chuckberry": ["Groovy", "Joyful", "Energetic"],
    "MockGame_DK": ["Nostalgic", "Adventurous", "Bittersweet"],
    "donkeykong": ["Nostalgic", "Adventurous", "Bittersweet"],
    "MockGame_Castlevania": ["Mysterious", "Dark", "Suspenseful"],
    "mockgame_zelda": ["Ethereal", "Adventurous", "Nostalgic"],
    "mockgame_mario": ["Playful", "Adventurous", "Nostalgic"],
    "MockGame_Sonic": ["Energetic", "Adventurous", "Determined"],
    "MockAnime_Naruto": ["Heroic", "Emotional", "Epic"],
    "MockBand_Dragon": ["Frenzy", "Epic", "Triumphant"],
    "MockBand_Megadeth": ["Aggressive", "Frenzy", "Dark"],
    "slayer": ["Aggressive", "Furious", "Dark"],
    "rage-against": ["Rebellious", "Furious", "Aggressive"],
    "rageagainst": ["Rebellious", "Furious", "Aggressive"],
    "nine-inch-nails": ["Dark", "Brooding", "Aggressive"],
    "nin": ["Dark", "Brooding", "Aggressive"],
    "bob-marley": ["Relaxed", "Peaceful", "Spiritual"],
    "bobmarley": ["Relaxed", "Peaceful", "Spiritual"],
    "jack-johnson": ["Relaxed", "Chill", "Cozy"],
    "jackjohnson": ["Relaxed", "Chill", "Cozy"],
    "enya": ["Serene", "Ethereal", "Peaceful"],
    "daft-punk": ["Groovy", "Danceful", "Hypnotic"],
    "daftpunk": ["Groovy", "Danceful", "Hypnotic"],
    "MockBand_Kraftwerk": ["Hypnotic", "Focused", "Surreal"],
    "massive-attack": ["Hypnotic", "Dark", "Brooding"],
    "massiveattack": ["Hypnotic", "Dark", "Brooding"],
    "ramocksinger_diohead": ["Introspective", "Brooding", "Surreal"],
    "foo-fighters": ["Energetic", "Determined", "Upbeat"],
    "mockband_foo": ["Energetic", "Determined", "Upbeat"],
    "bruce-springsteen": ["Determined", "Gritty", "Nostalgic"],
    "brucespringsteen": ["Determined", "Gritty", "Nostalgic"],
    "led-zeppelin": ["Gritty", "Energetic", "Epic"],
    "ledzeppelin": ["Gritty", "Energetic", "Epic"],
    "mockband_nirvana": ["Gritty", "Brooding", "Rebellious"],
    "pearl-jam": ["Anguished", "Gritty", "Introspective"],
    "mockband_pearl": ["Anguished", "Gritty", "Introspective"],
    "mockband_sound": ["Brooding", "Gritty", "Dark"],
    "tool": ["Introspective", "Dark", "Hypnotic"],
    "the-cure": ["Melancholic", "Brooding", "Ethereal"],
    "thecure": ["Melancholic", "Brooding", "Ethereal"],
    "the-smiths": ["Melancholic", "Jaded", "Wistful"],
    "thesmiths": ["Melancholic", "Jaded", "Wistful"],
    "MockBand_Beatles": ["Joyful", "Nostalgic", "Contemplative"],
    "rolling-stones": ["Gritty", "Groovy", "Rebellious"],
    "rollingstones": ["Gritty", "Groovy", "Rebellious"],
    "MockBand_U2": ["Soaring", "Emotional", "Optimistic"],
    "coldplay": ["Emotional", "Optimistic", "Contemplative"],
    "muse": ["Epic", "Energetic", "Rebellious"],
    "nightwish": ["Epic", "Macabre", "Awe-inspired"],
    "MockBand_Sabaton": ["Heroic", "Epic", "Triumphant"],
    "bon-jovi": ["Upbeat", "Soaring", "Energetic"],
    "bonjovi": ["Upbeat", "Soaring", "Energetic"],
    "mockband_acdc": ["Energetic", "Gritty", "Explosive"],
    "ac-dc": ["Energetic", "Gritty", "Explosive"],
    "judas-priest": ["Frenzy", "Aggressive", "Energetic"],
    "judaspriest": ["Frenzy", "Aggressive", "Energetic"],
    "black-smockband_abbath": ["Dark", "Ominous", "Brooding"],
    "blacksmockband_abbath": ["Dark", "Ominous", "Brooding"],
    "deep-purple": ["Energetic", "Groovy", "Epic"],
    "mockband_deep": ["Energetic", "Groovy", "Epic"],
    "van-halen": ["Energetic", "Frenzy", "Upbeat"],
    "vanhalen": ["Energetic", "Frenzy", "Upbeat"],
    "ghibli": ["Whimsical", "Ethereal", "Peaceful"],
    "stumocksinger_dio-ghibli": ["Whimsical", "Ethereal", "Peaceful"],
    "FictionalGame2": ["Nostalgic", "Adventurous", "Ethereal"],
    "mockcompany_nintendo": ["Nostalgic", "Playful", "Adventurous"],
    "playstation": ["Nostalgic", "Epic", "Adventurous"],
    "final-fantasy": ["Epic", "Bittersweet", "Ethereal"],
    "finalfantasy": ["Epic", "Bittersweet", "Ethereal"],
    "fictional game": ["Nostalgic", "Playful", "Adventurous"],
    "mockband_abba": ["Danceful", "Joyful", "Upbeat"],
    "earth-wind": ["Danceful", "Groovy", "Joyful"],
    "MockBand_Commodores": ["Groovy", "Romantic", "Danceful"],
    "marvin-gaye": ["Sensual", "Groovy", "Romantic"],
    "marvingaye": ["Sensual", "Groovy", "Romantic"],
    "stevie-wonder": ["Groovy", "Joyful", "Optimistic"],
    "steviewonder": ["Groovy", "Joyful", "Optimistic"],
    "adele": ["Heartbreak", "Emotional", "Sad"],
    "whitney-houston": ["Soaring", "Emotional", "Yearning"],
    "whitneyhouston": ["Soaring", "Emotional", "Yearning"],
    "elvis": ["Romantic", "Nostalgic", "Upbeat"],
    "frank-sinatra": ["Romantic", "Nostalgic", "Relaxed"],
    "franksinatra": ["Romantic", "Nostalgic", "Relaxed"],
    "anime": ["Emotional", "Heroic", "Epic"],
    "animerock": ["Energetic", "Heroic", "Emotional"],
    "darkgoddess": ["Dark", "Ominous", "Macabre"],
    "dark-goddess": ["Dark", "Ominous", "Macabre"],
    "egyptianbattle": ["Epic", "Suspenseful", "Mysterious"],
    "egyptian-battle": ["Epic", "Suspenseful", "Mysterious"],
    "egyptianmetal": ["Epic", "Aggressive", "Mysterious"],
    "egyptian-metal": ["Epic", "Aggressive", "Mysterious"],
    "piratemetal": ["Adventurous", "Energetic", "Groovy"],
    "pirate-metal": ["Adventurous", "Energetic", "Groovy"],
    "medievalambience": ["Mysterious", "Serene", "Peaceful"],
    "medieval-ambience": ["Mysterious", "Serene", "Peaceful"],
    "cyberpunk": ["Dark", "Energetic", "Gritty"],
    "cyberpunkbeats": ["Dark", "Energetic", "Gritty"],
    "numetal": ["Aggressive", "Energetic", "Gritty"],
    "nu-metal": ["Aggressive", "Energetic", "Gritty"],
    "shibuya": ["Chill", "Groovy", "Nostalgic"],
    "nottoo-jazzy": ["Chill", "Groovy", "Relaxed"],
    "nottoojazzy": ["Chill", "Groovy", "Relaxed"],
    "summereletrohits": ["Danceful", "Upbeat", "Ecstatic"],
    "summer-eletrohits": ["Danceful", "Upbeat", "Ecstatic"],
    "donkeykongforro": ["Groovy", "Nostalgic", "Playful"],
    "donkeykongsoul": ["Groovy", "Nostalgic", "Bittersweet"],
}

# ── Migration: old moods → new moods ─────────────────────────────────────────
def migrate_old_moods(moods: list[str]) -> set[str]:
    """Convert old 23-mood assignments into the new 66-mood vocabulary."""
    result = set()
    for m in moods:
        if m in OLD_TO_NEW:
            result.update(OLD_TO_NEW[m])
        elif m in ALL_MOODS:
            result.add(m)
        # else: mood no longer exists, drop it
    return result

def classify_track(filename: str, existing_moods: list[str]) -> list[str]:
    """Assign moods to a track based on filename keywords + existing moods."""
    fn = track.replace(".mp3", "").replace("-", " ").replace("_", " ")

    # Start with migrated existing moods
    assigned = migrate_old_moods(existing_moods)

    # Keyword matching against the new 66-mood taxonomy
    for mood, keywords in MOOD_KW.items():
        for kw in keywords:
            if kw.lower() in name_lower:
                assigned.add(mood)
                break

    # Artist-based hints
    for artist_pattern, moods in ARTIST_MOOD_HINTS.items():
        if artist_pattern.lower() in name_lower:
            for m in moods:
                assigned.add(m)
            break  # take first artist match

    # If nothing matched, give it Chill as fallback
    if not assigned:
        assigned.add("Chill")

    # Filter to only valid mood names and sort
    valid = sorted([m for m in assigned if m in ALL_MOODS])
    return valid

# ── Mood color mapping (color psychology) ────────────────────────────────────
# Each mood gets an accent-color for its native checkbox.
# Families: red=anger/aggression, orange=energy/fire, yellow=joy/optimism,
#   green=peace/nature, teal=calm/focus, cyan=ethereal/dreamy,
#   blue=sadness/introspection, indigo=mystery/depth, purple=spiritual/surreal,
#   pink=love/romance, magenta=sensual/ecstatic, brown=grit/earth,
#   grey=resignation/numbness
MOOD_COLORS: dict[str, str] = {
    # ── Reds: anger, violence, hostility ─────────────────────────────────
    "Aggressive":   "#e53935",  # strong red
    "Furious":      "#c62828",  # deep red
    "Vengeful":     "#b71c1c",  # dark crimson
    "Chaotic":      "#d32f2f",  # hot red
    "Explosive":    "#ff1744",  # neon red
    # ── Orange-reds: dark energy, dread ──────────────────────────────────
    "Dark":         "#bf360c",  # burnt orange-red
    "Macabre":      "#8d2c0e",  # dried-blood
    "Ominous":      "#a1350f",  # smoked ember
    "Tense":        "#d84315",  # warning orange
    "Suspenseful":  "#e64a19",  # hot amber
    # ── Oranges: energy, drive, power ────────────────────────────────────
    "Energetic":    "#f57c00",  # vivid orange
    "Frenzy":       "#ef6c00",  # deep orange
    "Determined":   "#fb8c00",  # amber
    "Defiant":      "#ff9800",  # standard orange
    "Hardworking":  "#c77a20",  # muted gold
    # ── Yellows: joy, optimism, fun ──────────────────────────────────────
    "Joyful":       "#fdd835",  # bright yellow
    "Ecstatic":     "#ffeb3b",  # lemon
    "Optimistic":   "#fbc02d",  # warm yellow
    "Upbeat":       "#ffe082",  # soft gold
    "Playful":      "#fff176",  # light yellow
    "Whimsical":    "#dce775",  # yellow-lime
    # ── Greens: peace, nature, calm, safety ──────────────────────────────
    "Peaceful":     "#66bb6a",  # garden green
    "Serene":       "#81c784",  # pale sage
    "Relaxed":      "#a5d6a7",  # mint
    "Cozy":         "#c8e6c9",  # soft green
    "Sleepy":       "#b2dfdb",  # seafoam
    # ── Teals: focus, clarity, coolness ──────────────────────────────────
    "Chill":        "#4db6ac",  # chill teal
    "StudyFocus":   "#26a69a",  # deep teal
    "Focused":      "#00897b",  # dark teal
    "Contemplative":"#00796b",  # pine teal
    "Meditative":   "#80cbc4",  # light teal
    # ── Cyans: ethereal, dreamy, otherworldly ────────────────────────────
    "Ethereal":     "#4dd0e1",  # sky cyan
    "Hypnotic":     "#00bcd4",  # vivid cyan
    "Surreal":      "#00acc1",  # deep cyan
    "Awe-inspired": "#0097a7",  # teal-cyan
    # ── Blues: sadness, depth, introspection ─────────────────────────────
    "Sad":          "#42a5f5",  # clear blue
    "Melancholic":  "#5c6bc0",  # muted indigo-blue
    "Introspective":"#7986cb",  # lavender blue
    "Lonely":       "#5e7599",  # steel blue
    "Bittersweet":  "#7e57c2",  # blue-violet
    "Wistful":      "#9fa8da",  # periwinkle
    "Yearning":     "#8c9eff",  # bright periwinkle
    # ── Indigos/purples: mystery, depth, spiritual ───────────────────────
    "Mysterious":   "#673ab7",  # deep purple
    "Brooding":     "#4a148c",  # dark purple
    "Depressive":   "#37286e",  # midnight indigo
    "Anguished":    "#6a1b9a",  # dark violet
    "Jaded":        "#78628e",  # dusty mauve
    "Resigned":     "#9e9e9e",  # neutral grey
    # ── Magentas/pinks: love, romance, sensuality ────────────────────────
    "Romantic":     "#ec407a",  # rose pink
    "Sensual":      "#d81b60",  # deep pink
    "Tender":       "#f48fb1",  # soft pink
    "Heartbreak":   "#ad1457",  # dark rose
    # ── Warm emotional tones ─────────────────────────────────────────────
    "Emotional":    "#ce93d8",  # orchid
    "Desperate":    "#ab47bc",  # bright purple
    "Soaring":      "#29b6f6",  # sky blue
    "Heroic":       "#ffa726",  # hero gold
    "Triumphant":   "#ffca28",  # gold
    "Rebellious":   "#ff7043",  # punk orange-red
    # ── Browns/earth: gritty, raw ────────────────────────────────────────
    "Gritty":       "#8d6e63",  # earth brown
    "Groovy":       "#ff8a65",  # warm coral
    "Danceful":     "#ff80ab",  # dance pink
    # ── Greens/golds: adventure, epic ────────────────────────────────────
    "Adventurous":  "#26c6da",  # adventure cyan
    "Epic":         "#ffc107",  # epic gold
    "Nostalgic":    "#ffcc80",  # sepia
    "Spiritual":    "#b39ddb",  # amethyst
    "Reverent":     "#9575cd",  # soft purple
}
# Fallback for any mood missing a mapping
DEFAULT_MOOD_COLOR = "#90a4ae"  # blue-grey

def get_mood_color(mood: str) -> str:
    return MOOD_COLORS.get(mood, DEFAULT_MOOD_COLOR)

# ── Generate HTML ────────────────────────────────────────────────────────────
def esc(s: str) -> str:
    return html.escape(s, quote=True)

def track_sort_key(name: str) -> str:
    """Strip leading numbers/dots for a cleaner sort."""
    return re.sub(r'^[\d.\-\s]+', '', name).lower()

tracks_sorted = sorted(track_moods.keys(), key=track_sort_key)

# Build the HTML
lines: list[str] = []
lines.append("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mood Assignments — Track Checker</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        rel="stylesheet"
        integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YcnS/1f0MQJkLV8wPZLhYb8WNTTEP2GzAHs"
        crossorigin="anonymous">
  <style>
    body { background: #121212; color: #e0e0e0; }
    details.track-details {
      border: 1px solid #333;
      border-radius: 8px;
      margin-bottom: 0.6rem;
      background: #1a1a1a;
    }
    details.track-details[open] {
      border-color: #555;
    }
    details.track-details summary {
      padding: 0.55rem 1rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 0.75rem;
      user-select: none;
      border-radius: 8px;
      list-style: none;
    }
    details.track-details summary::-webkit-details-marker { display: none; }
    details.track-details summary::before {
      content: '▶';
      font-size: 0.65rem;
      color: #888;
      transition: transform 0.15s ease;
      flex-shrink: 0;
    }
    details.track-details[open] > summary::before {
      transform: rotate(90deg);
    }
    details.track-details summary:hover { background: #242424; }
    .track-name {
      font-size: 0.93rem;
      font-weight: 600;
      color: #90caf9;
      flex: 1;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .reviewed-cb {
      width: 1.5rem;
      height: 1.5rem;
      accent-color: #4caf50;
      cursor: pointer;
      flex-shrink: 0;
    }
    .reviewed-label {
      font-size: 0.72rem;
      color: #888;
      cursor: pointer;
      flex-shrink: 0;
      white-space: nowrap;
    }
    details.track-details:has(.reviewed-cb:checked) {
      border-color: #4caf50;
    }
    details.track-details:has(.reviewed-cb:checked) .track-name {
      color: #81c784;
    }
    details.track-details:has(.reviewed-cb:checked) .reviewed-label {
      color: #66bb6a;
    }
    .fieldset-inner {
      padding: 0.5rem 1rem 1rem;
    }
    .fieldset-inner legend { display: none; }
    .mood-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(165px, 1fr));
      gap: 3px 14px;
    }
    .form-check-label {
      font-size: 0.82rem;
      cursor: pointer;
      transition: color 0.12s;
    }
    .form-check-input { cursor: pointer; }
    .form-check-input:checked + .form-check-label { font-weight: 600; }
    #cta-bar {
      position: sticky;
      bottom: 0;
      background: #1e1e1e;
      border-top: 2px solid #333;
      padding: 1rem;
      z-index: 100;
    }
    #search-bar { background: #222; color: #e0e0e0; border: 1px solid #444; }
    #search-bar::placeholder { color: #888; }
    .track-count { color: #999; font-size: 0.8rem; }
    details.track-details.d-none { display: none !important; }
    .progress-bar-custom {
      height: 6px; border-radius: 3px; background: #333; overflow: hidden;
    }
    .progress-bar-custom > div {
      height: 100%; background: #4caf50; transition: width 0.3s;
    }
  </style>
</head>
<body>
<main class="container-fluid py-3">
  <h1 class="h4 mb-1">Mood Assignments — Track Checker</h1>
  <p class="text-secondary mb-3">
    <span id="track-total">""" + str(len(tracks_sorted)) + """</span> tracks &times; """ + str(len(ALL_MOODS)) + """ moods.
    Pre-checked boxes = current assignment. Edit as needed, then export.
  </p>

  <div class="row mb-3 align-items-center">
    <div class="col-md-5">
      <input type="search" id="search-bar" class="form-control"
             placeholder="Filter tracks by name…" autocomplete="off">
    </div>
    <div class="col-md-3 d-flex align-items-center gap-2">
      <span class="track-count" id="visible-count">Showing all</span>
    </div>
    <div class="col-md-4">
      <div class="d-flex align-items-center gap-2">
        <span class="track-count">Reviewed:</span>
        <span class="track-count" id="reviewed-count">0 / """ + str(len(tracks_sorted)) + """</span>
        <div class="progress-bar-custom flex-grow-1"><div id="reviewed-bar" style="width:0%"></div></div>
      </div>
    </div>
  </div>

  <form id="moods-form">
""")

for idx, track in enumerate(tracks_sorted):
    assigned = classify_track(track, track_moods[track])
    fn = track.replace(".mp3", "").replace("-", " ").replace("_", " ")
    rev_id = f"rev_{idx}"

    lines.append(f'    <details class="track-details" data-track="{esc(track)}">')
    lines.append(f'      <summary>')
    lines.append(f'        <input class="reviewed-cb" type="checkbox" id="{rev_id}"'
                 f' title="Mark as reviewed" onclick="event.stopPropagation()">')
    lines.append(f'        <label class="reviewed-label" for="{rev_id}"'
                 f' onclick="event.stopPropagation()">reviewed</label>')
    lines.append(f'        <span class="track-name">{legend_text}</span>')
    lines.append(f'      </summary>')
    lines.append(f'      <fieldset class="fieldset-inner">')
    lines.append(f'        <legend>{legend_text}</legend>')
    lines.append(f'        <div class="mood-grid">')

    for mood in ALL_MOODS:
        cb_id = f"cb_{idx}_{mood}"
        checked = " checked" if mood in assigned else ""
        color = get_mood_color(mood)
        lines.append(
            f'          <div class="form-check">'
            f'<input class="form-check-input" type="checkbox"'
            f' name="{esc(track)}" value="{esc(mood)}"'
            f' id="{cb_id}" style="accent-color:{color}"{checked}>'
            f'<label class="form-check-label" for="{cb_id}"'
            f' style="color:{color}">{esc(mood)}</label>'
            f'</div>'
        )

    lines.append(f'        </div>')
    lines.append(f'      </fieldset>')
    lines.append(f'    </details>')

lines.append("""
    <fieldset id="cta-bar">
      <legend class="visually-hidden">Actions</legend>
      <div class="btn-group" role="group">
        <button type="button" class="btn btn-primary" id="btn-export-json">
          Export JSON
        </button>
        <button type="button" class="btn btn-outline-light" id="btn-copy-clipboard">
          Copy to Clipboard (YAML)
        </button>
      </div>
      <span class="ms-3 text-secondary" id="status-msg"></span>
    </fieldset>
  </form>
</main>

<script>
(function () {
  const form = document.getElementById('moods-form');
  const searchBar = document.getElementById('search-bar');
  const visibleCount = document.getElementById('visible-count');
  const statusMsg = document.getElementById('status-msg');
  const details = document.querySelectorAll('.track-details');
  const reviewedCountEl = document.getElementById('reviewed-count');
  const reviewedBar = document.getElementById('reviewed-bar');
  const totalTracks = details.length;

  // ── Reviewed counter ────────────────────────────────────────────────────
  function updateReviewedCount() {
    const n = document.querySelectorAll('.reviewed-cb:checked').length;
    reviewedCountEl.textContent = `${n} / ${totalTracks}`;
    reviewedBar.style.width = `${(n / totalTracks * 100).toFixed(1)}%`;
  }
  document.querySelectorAll('.reviewed-cb').forEach(cb => {
    cb.addEventListener('change', updateReviewedCount);
  });

  // ── Search / filter ─────────────────────────────────────────────────────
  searchBar.addEventListener('input', function () {
    const q = this.value.trim().toLowerCase();
    let shown = 0;
    details.forEach(d => {
      const name = (d.dataset.track || '').toLowerCase();
      const match = !q || name.includes(q);
      d.classList.toggle('d-none', !match);
      if (match) shown++;
    });
    visibleCount.textContent = q ? `Showing ${shown} of ${totalTracks}` : 'Showing all';
  });

  // ── Collect form data (only mood checkboxes, not reviewed) ──────────────
  function collectData() {
    const result = {};
    details.forEach(d => {
      const track = d.dataset.track;
      const checked = d.querySelectorAll('.fieldset-inner input[type=checkbox]:checked');
      const moods = Array.from(checked).map(cb => cb.value);
      if (moods.length > 0) result[track] = moods;
    });
    return result;
  }

  // ── Export JSON ─────────────────────────────────────────────────────────
  document.getElementById('btn-export-json').addEventListener('click', function () {
    const data = collectData();
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'track-moods.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    statusMsg.textContent = 'JSON exported ✓';
    setTimeout(() => statusMsg.textContent = '', 3000);
  });

  // ── Copy YAML-like text to clipboard ────────────────────────────────────
  document.getElementById('btn-copy-clipboard').addEventListener('click', function () {
    const data = collectData();
    const yamlLines = Object.entries(data)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([track, moods]) => track + ':\\n  - ' + moods.join('\\n  - '))
      .join('\\n');
    navigator.clipboard.writeText(yamlLines).then(() => {
      statusMsg.textContent = 'Copied to clipboard ✓';
      setTimeout(() => statusMsg.textContent = '', 3000);
    }).catch(() => {
      statusMsg.textContent = 'Clipboard access denied';
    });
  });
})();
</script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
        crossorigin="anonymous"></script>
</body>
</html>
""")

output_path = os.path.join(BASE, "docs/guidelines/moods-checks.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Written {output_path}")
print(f"  Tracks: {len(tracks_sorted)}")
print(f"  Moods:  {len(ALL_MOODS)}")
print(f"  Checkboxes: {len(tracks_sorted) * len(ALL_MOODS)}")
