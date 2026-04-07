#!/usr/bin/env python3
"""Generate docs/guidelines/moods-checks.html from track-mood data."""
import json
import re
import html
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Load data ────────────────────────────────────────────────────────────────
with open("/tmp/track_moods.json") as f:
    track_moods: dict[str, list[str]] = json.load(f)

with open(os.path.join(BASE, "docs/guidelines/moods.txt")) as f:
    ALL_MOODS = [line.strip() for line in f if line.strip()]

# ── Old→new mood migration map (for the 23→66 expansion) ────────────────────
# Tracks that were in removed moods get re-mapped:
OLD_TO_NEW = {
    "Ambient": ["Serene", "Meditative"],
}

# ── Keyword→mood heuristics for new moods ────────────────────────────────────
MOOD_KW = {
    "Adventurous": ["adventure", "quest", "Fictional-Kw-98dc0157", "dragon", "Fictional-Kw-f4056ced",
                    "Fictional-Kw-a1dc2820", "Fictional-Kw-f9e1d8f3", "Fictional-Kw-9a6359cf",  # noqa: E501
                    "pirate", "Fictional-AzureShore heroes", "fist bump", "open world"],
    "Aggressive": ["aggressive", "rage", "angry", "violent", "heavy",
                   "Fictional-VioletFalcon", "Fictional-SterlingBeacon",
                   "Fictional-TwilightPhoenix", "Fictional-IronMesa",
                   "Fictional-LunarKnight", "Fictional-Kw-5f219c36", "Fictional-Kw-c64f8a77", "Fictional-Kw-891b1132",
                   "Fictional-Kw-858a4f75", "Fictional-Kw-015220a7", "Fictional-Kw-56dc5fa7",
                   "sonne", "Fictional-NeonDawn", "Fictional-JasperBloom", "Fictional-Kw-74303c51",
                   "Fictional-Kw-4bc4a6e3", "Fictional-Kw-ed5d1ab5"],
    "Anguished": ["anguish", "agony", "torment", "despair", "hurt",
                  "Fictional-Kw-625cf4d4", "Fictional-Kw-e9783d09", "black", "unforgiven",
                  "Fictional-Kw-9cf0e877", "would?", "rotten apple"],
    "Awe-inspired": ["awe", "granFictional-Kw-27b20503se", "magnificent", "majestic",
                     "great gig in the sky", "zarathustra", "Fictional-Kw-d0b27625",
                     "Fictional-Kw-d01fa6a9", "one-Fictional-Kw-ca96d708"],
    "Bittersweet": ["bittersweet", "stickerbush", "Fictional-Kw-854f82e6",
                    "Fictional-Kw-488d4831", "Fictional-Kw-84d4d9af",
                    "Fictional-Kw-4ee5643e", "theme of laura"],
    "Brooding": ["brooding", "brood", "simmering", "Fictional-Kw-b0d966c3",
                 "Fictional-Kw-1f8c1bee", "Fictional-Kw-80cdc815", "fade to black",
                 "Fictional-Kw-d8f616b1", "Fictional-Kw-c3fad343"],
    "Chaotic": ["chaotic", "chaos", "byob", "Fictional-Kw-5f219c36", "Fictional-Kw-9017582e",
                "psycho", "cat's foot", "prison song"],
    "Chill": ["chill", "lo-fi", "lofi", "mellow", "laid-back", "easy listening",
              "Fictional-PhantomHorizon", "city pop", "feather", "Fictional-Kw-3fae5781",
              "Fictional-Kw-a70a6a9b", "file select"],
    "Contemplative": ["contemplate", "ponder", "thinking", "breathe",
                      "time Fictional-EbonyBloom", "roundabout", "Fictional-Kw-55864dd4",
                      "starry night", "vincent"],
    "Cozy": ["cozy", "warm", "home", "fireplace", "Fictional-Kw-47387e9a",
             "Fictional-Kw-6b55169c", "Fictional-Kw-cd41cf7d", "Fictional-Kw-3ee271e4 the sun",
             "coffee", "Fictional-Kw-7324396c"],
    "Danceful": ["dance", "disco", "club", "dancefloor", "Fictional-Kw-40376286",
                 "around the world", "september", "Fictional-Kw-bd27cf27",
                 "Fictional-Kw-2e41e95c", "Fictional-Kw-885b67ec", "Fictional-Kw-1359e39d",
                 "eletrohits"],
    "Dark": ["dark", "sinister", "evil", "shadow", "Fictional-MidnightFrost", "death",
             "vampire", "dracula", "gothic", "Fictional-EmeraldWarden", "Fictional-Kw-57d292fc",
             "cyberpunk", "dark angel", "Fictional-IronMesa", "Fictional-Kw-31861ba7"],
    "Defiant": ["defiant", "Fictional-Kw-06db9c2c", "Fictional-Kw-d7110683",
                "we are the champions", "defy", "stand up",
                "overcome", "won't Fictional-Kw-fa37187d"],
    "Depressive": ["depress", "hopeless", "Fictional-Kw-b4aecf76", "disintegration",
                   "adam's song", "Fictional-Kw-12e57df2", "Fictional-Kw-c4cc47b2",
                   "needle and the Fictional-Kw-55043579"],
    "Desperate": ["desperate", "desperation", "Fictional-Kw-a6a3b111", "Fictional-Kw-92f62e24",
                  "Fictional-Kw-b4aecf76 encore", "Fictional-Kw-eae86eac", "clocks",
                  "Fictional-Kw-b2631a42", "breaking the habit"],
    "Determined": ["determined", "unstoppable", "harder better faster",
                   "Fictional-Kw-0f0242f6", "don't Fictional-Kw-bceede5d",
                   "won't Fictional-Kw-fa37187d", "Fictional-Kw-d7110683"],
    "Ecstatic": ["ecstatic", "euphoria", "euphoric", "don't Fictional-Kw-bceede5d",
                 "mr. brightside", "Fictional-Kw-9017582e",
                 "i Fictional-Kw-f3a9fce5", "celebration"],
    "Emotional": ["emotional", "tears", "cry", "feel", "heart", "love",
                  "loss", "Fictional-AzurePhoenix", "Fictional-ZincWing", "linger",
                  "Fictional-Kw-b0c56b8e", "Fictional-Kw-aa7f0be7",
                  "you are not alone", "Fictional-Kw-5ee0843a",
                  "Fictional-Kw-67a914c6"],
    "Energetic": ["energetic", "fast", "power", "high energy",
                  "Fictional-AzureShore", "Fictional-SolarWarden", "Fictional-ScarletHorizon",
                  "Fictional-Kw-6704c32f", "Fictional-Kw-d0dbe915 & learn",
                  "fist bump", "Fictional-Kw-e4dcc4b1", "Fictional-Kw-4bc4a6e3",
                  "my hero", "Fictional-Kw-8f379ecb", "Fictional-JadeFrost",
                  "Fictional-Kw-5e5601d7", "Fictional-ShadowPeak"],
    "Epic": ["epic", "orchestral", "grand", "legendary",
             "Fictional-Kw-b09ec18c", "Fictional-Kw-b071f324",
             "Fictional-Kw-f9e1d8f3", "Fictional-Kw-51da3037", "Fictional-Kw-0f060986",
             "Fictional-Kw-7749bdd4", "Fictional-Kw-46f76d4a",
             "Fictional-Kw-9a2a444f", "Fictional-AmberSpark", "stormwind"],
    "Ethereal": ["ethereal", "dreamy", "floating", "heavenly",
                 "Fictional-Kw-17e536b9", "Fictional-Kw-5fae0ce6", "korok forest",
                 "song of elune", "Fictional-Kw-1005185b",
                 "Fictional-Kw-84d4d9af", "Fictional-Kw-b2412f79", "Fictional-Kw-f5405813",
                 "Fictional-CrimsonFountain", "Fictional-Kw-e4178445", "always with me"],
    "Explosive": ["explosive", "explode", "blast", "battery",
                  "Fictional-Kw-f0aea57d", "Fictional-Kw-5e5601d7",
                  "Fictional-Kw-3fd20e5d", "bulls on parade"],
    "Focused": ["focused", "concentration", "precision",
                "march of the pigs", "Fictional-Kw-8cfba85c"],
    "Frenzy": ["frenzy", "frenetic", "blast beat", "shred",
               "painkiller", "tornado of souls", "eruption",
               "fury of the storm", "surfing with the alien"],
    "Furious": ["furious", "fury", "rage", "Fictional-Kw-783aeb10",
                "Fictional-Kw-3b2b389d a hole", "killing in the name"],
    "Gritty": ["gritty", "grit", "raw", "blues rock", "dirty",
               "Fictional-Kw-00baf9bf", "Fictional-Kw-536c9985", "Fictional-Kw-51e2bacd",
               "ball and biscuit", "superstition"],
    "Groovy": ["groovy", "groove", "funky", "funk", "soulful",
               "Fictional-Kw-cba5833f", "superstition", "Fictional-Kw-3afa2a44",
               "Fictional-Kw-d8ceb2b3", "fire", "Fictional-IronLantern",
               "Fictional-OpalWing", "Fictional-FrozenBell", "samba",
               "cant stop", "Fictional-Kw-71d10b6a"],
    "Hardworking": ["working", "worker", "labor", "grind",
                    "9 to 5", "blue collar", "Fictional-Kw-feee254a"],
    "Heartbreak": ["heartbreak", "heartbroken", "broken heart",
                   "Fictional-Kw-8b37d97d", "Fictional-Kw-3a93c36b",
                   "Fictional-Kw-538e93ed", "back to december",
                   "Fictional-Kw-d22d0122"],
    "Heroic": ["heroic", "hero", "Superman", "princes of the universe",
               "Fictional-Kw-76a65548", "final countdown",
               "Fictional-Kw-4722588b"],
    "Hypnotic": ["hypnotic", "trance", "loop", "repetitive",
                 "music for airports", "autobahn", "trans-Fictional-Kw-7612e840 express",
                 "teardrop", "porcelain"],
    "Introspective": ["introspect", "think", "reflect", "quiet",
                      "alone", "self", "Fictional-Kw-a6a3b111", "Fictional-Kw-b2631a42",
                      "Fictional-Kw-625cf4d4", "Fictional-Kw-b0c2ac5b", "papercut",
                      "Fictional-Kw-8fd19cd0", "Fictional-Kw-2d455771",
                      "wond'ring aloud", "Fictional-Kw-6d712aa9"],
    "Jaded": ["jaded", "cynical", "disillusioned", "boulevard of Fictional-Kw-9a1b2660",
              "Fictional-Kw-1f8c1bee", "when i Fictional-Kw-3645b922", "bitter"],
    "Joyful": ["joyful", "joy", "happy", "delight", "wonderful",
               "happy pharrell", "Fictional-Kw-3ee271e4 the sun",
               "i Fictional-Kw-53e3d575 with somebody", "walking on sunshine",
               "Fictional-Kw-4ae844d0"],
    "Lonely": ["lonely", "alone", "isolation", "isolated",
               "Fictional-Kw-51f93ec4", "Fictional-Kw-1ae4a17a", "Fictional-Kw-c84e9ec5",
               "only Fictional-Kw-166a8328"],
    "Macabre": ["macabre", "death", "decay", "grotesque",
                "danse macabre", "Fictional-Kw-2ce2379f", "Fictional-Kw-e61ee602 the Fictional-Kw-4854339d",
                "Fictional-Kw-abc40a2d sanitarium", "Fictional-Kw-b42bb8b1",
                "halloween"],
    "Meditative": ["meditative", "meditation", "zen", "yoga",
                   "spiegel im spiegel", "gymnop", "weightless",
                   "buddha"],
    "Melancholic": ["melanchol", "sad", "sorrow", "grief", "loss",
                    "blue", "tears", "pain", "Fictional-Kw-625cf4d4",
                    "Fictional-Kw-e9783d09", "Fictional-Kw-9cf0e877", "rotten apple",
                    "linger", "Fictional-Kw-5ee0843a", "Fictional-Kw-5fae0ce6",
                    "Fictional-Kw-488d4831", "Fictional-Kw-1005185b"],
    "Mysterious": ["mysterious", "mystery", "enigma", "secret",
                   "shadow", "hidden", "Fictional-EmeraldWarden", "Fictional-Kw-a557d8c5",
                   "Fictional-Kw-71bb3f77", "Fictional-Kw-15396039",
                   "Fictional-Kw-a2ce73b7", "twilight stigmata",
                   "sacred grove"],
    "Nostalgic": ["nostalg", "retro", "classic", "remember", "childhood",
                  "old school", "Fictional-CrystalBell", "Fictional-JadePrism", "Fictional-SapphireOracle",
                  "Fictional-IronSail", "Fictional-ZincGate", "nintendo",
                  "Fictional-MarbleCrown", "Fictional-PhantomWhisper", "snes",
                  "n64", "Fictional-Kw-6b55169c", "title theme",
                  "Fictional-Kw-e958d854", "Fictional-Kw-a70a6a9b"],
    "Ominous": ["ominous", "forboding", "impending", "scarecrow",
                "premonition", "fear of the dark", "dread"],
    "Optimistic": ["optimistic", "hopeful", "promising",
                   "Fictional-Kw-fe6acc5b", "Fictional-Kw-b6ae6b50",
                   "Fictional-Kw-76b19a8e", "Fictional-Kw-7c6c20b0",
                   "waiting on the world to change"],
    "Peaceful": ["peaceful", "peace", "calm", "idyllic", "pastoral",
                 "gentle", "safe", "fields of gold",
                 "Fictional-Kw-6b55169c", "spring Fictional-Kw-15607a23",
                 "Fictional-Kw-368625a2"],
    "Playful": ["playful", "silly", "bouncy", "quirky",
                "bob-omb battlefield", "Fictional-Kw-81fea809",
                "Fictional-Kw-7a5177a6", "Fictional-Kw-bf16f999", "goofy"],
    "Rebellious": ["rebel", "anarchy", "protest", "fight", "resist",
                   "Fictional-SterlingBeacon", "Fictional-JasperBloom", "Fictional-ShadowPeak",
                   "punk", "Fictional-Kw-896901cc", "Fictional-Kw-e4dcc4b1",
                   "Fictional-Kw-c027cb5c", "police truck",
                   "Fictional-Kw-8f379ecb", "Fictional-NeonDawn", "Fictional-GraniteCrown"],
    "Relaxed": ["relaxed", "relax", "easy going", "laid back",
                "Fictional-Kw-fce9baa5", "Fictional-Kw-c8a8773b", "Fictional-Kw-018ff799",
                "Fictional-Kw-59a3c84d", "Fictional-Kw-560ad6f5",
                "Fictional-Kw-d4e72770"],
    "Resigned": ["resigned", "Fictional-Kw-4abe77c2", "let go", "Fictional-Kw-ebfe9ce8 Fictional-VelvetLantern",
                 "Fictional-Kw-55864dd4", "against the wind", "Fictional-Kw-98ac91ad"],
    "Reverent": ["reverent", "sacred", "holy", "divine",
                 "Fictional-Kw-f24d1a09", "o fortuna", "requiem",
                 "gregorian"],
    "Romantic": ["romantic", "love", "heart", "kiss", "together",
                 "sweetest", "you are not alone", "Fictional-Kw-aa7f0be7",
                 "Fictional-Kw-693c8131", "human nature",
                 "is this love", "Fictional-Kw-d7995712", "Fictional-Kw-0a77c212",
                 "Fictional-Kw-89638e4c", "sweet love", "Fictional-Kw-c612457b"],
    "Sad": ["sad", "sorrow", "crying", "tears in heaven",
            "Fictional-Kw-8efadf92", "with or Fictional-Kw-96ad8985",
            "Fictional-Kw-72d42264"],
    "Sensual": ["sensual", "seductive", "erotic", "let's Fictional-Kw-79f88d99",
                "Fictional-Kw-99f487cd", "Fictional-Kw-f0d10c25", "Fictional-Kw-78a6af34"],
    "Serene": ["serene", "tranquil", "still", "lullaby",
               "Fictional-CrystalBell's lullaby", "sakura", "always with me",
               "Fictional-Kw-390fd18a", "Fictional-Kw-64f42d05", "Fictional-Kw-b1be5870",
               "Fictional-Kw-9c820265", "guzheng", "guqin",
               "koto", "gayageum", "zither"],
    "Sleepy": ["sleepy", "sleep", "lullaby", "drowsy",
               "comptine", "weightless", "clair de lune"],
    "Soaring": ["soaring", "soar", "flying", "ascend",
                "don't Fictional-Kw-8e9d25b3", "Fictional-Kw-aaa8344b",
                "Fictional-Kw-a1e2b1f9", "i believe i can fly",
                "Fictional-Kw-cc853ca0"],
    "Spiritual": ["spiritual", "transcend", "soul", "divine",
                  "koyaanisqatsi", "Fictional-Kw-539bf33c", "Fictional-Kw-d6e00f39",
                  "Fictional-Kw-78668218"],
    "Surreal": ["surreal", "psychedelic", "trippy",
                "lucy in the sky", "Fictional-Kw-7fdba541",
                "Fictional-Kw-238641b4", "echoes Fictional-EbonyBloom",
                "Fictional-Kw-fa1e7c86"],
    "Suspenseful": ["suspense", "tension", "build-up", "thriller",
                    "Fictional-Kw-23f3b407", "Fictional-Kw-a2ce73b7",
                    "psycho", "mission impossible", "Fictional-MidnightFrost e1m1",
                    "boss fight", "boss battle"],
    "Tender": ["tender", "gentle", "delicate", "blackbird",
               "Fictional-Kw-b09f6174", "Fictional-Kw-b7e3bb55", "father and son"],
    "Tense": ["tense", "anxiety", "anxious", "uneasy",
              "jaws", "in the hall of the Fictional-Kw-a43c2581",
              "Fictional-Kw-a7689246 Fictional-Kw-166a8328"],
    "Triumphant": ["triumph", "victory", "glory", "win", "champion",
                   "heroes", "Fictional-Kw-51da3037", "Fictional-Kw-d0dbe915 & learn",
                   "Fictional-Kw-6704c32f", "my hero",
                   "learn to fly", "Fictional-Kw-0f060986",
                   "invincible", "eagleheart"],
    "Upbeat": ["upbeat", "happy", "joy", "fun", "bright",
               "cheerful", "Fictional-DuskPeak", "Fictional-Kw-885b67ec", "Fictional-Kw-fcf2483c",
               "off the wall", "Fictional-Kw-271b8ef8", "Fictional-Kw-97d2827f",
               "Fictional-Kw-e4dcc4b1", "Fictional-Kw-71cb705f", "Fictional-AzureShore heroes",
               "Fictional-Kw-ef7e483f", "Fictional-Kw-52f26298", "Fictional-Kw-f8f26e59"],
    "Vengeful": ["vengeful", "vengeance", "revenge", "retribution",
                 "Fictional-Kw-31d51a08", "Fictional-Kw-511623b2", "Fictional-Kw-4a8cd79e"],
    "Whimsical": ["whimsical", "fanciful", "fairy tale",
                  "Fictional-Kw-f5405813", "arrietty", "Fictional-Kw-920e8c9f", "fraggle rock",
                  "Fictional-CrimsonFountain"],
    "Wistful": ["wistful", "longing gently", "Fictional-Kw-a1807c41",
                "landslide", "river Fictional-Kw-8932b88a",
                "Fictional-Kw-8edb14fd"],
    "Yearning": ["yearning", "yearn", "longing", "desire",
                 "can't Fictional-Kw-b83c582a in love", "in your eyes",
                 "Fictional-Kw-75995f09", "everlong",
                 "i Fictional-Kw-adf50787"],
}

# ── Additional artist→mood inference ─────────────────────────────────────────
ARTIST_MOOD_HINTS = {
    "Fictional-PhantomHorizon": ["Chill", "Contemplative", "Introspective"],
    "Fictional-Kw-04f7eba2": ["Anguished", "Brooding", "Melancholic"],
    "Fictional-ZincWing": ["Anguished", "Brooding", "Melancholic"],
    "Fictional-Kw-7639c53e": ["Anguished", "Brooding", "Melancholic"],
    "Fictional-Kw-061d5554": ["Chaotic", "Rebellious", "Aggressive"],
    "fictional-scarletisle": ["Chaotic", "Rebellious", "Aggressive"],
    "Fictional-SterlingBeacon": ["Chaotic", "Rebellious", "Aggressive"],
    "Fictional-Kw-96344f5c": ["Contemplative", "Surreal", "Dark"],
    "Fictional-Kw-eda6ecaf": ["Contemplative", "Surreal", "Dark"],
    "Fictional-BrassCompass": ["Aggressive", "Epic", "Dark"],
    "Fictional-Kw-85af6281": ["Desperate", "Anguished", "Energetic"],
    "fictional-silverpine": ["Desperate", "Anguished", "Energetic"],
    "Fictional-Kw-a3a2b4d5": ["Rebellious", "Energetic", "Jaded"],
    "Fictional-Kw-80735228": ["Rebellious", "Energetic", "Jaded"],
    "Fictional-Kw-609363a9": ["Groovy", "Energetic", "Upbeat"],
    "Fictional-SilverLighthouse": ["Groovy", "Energetic", "Upbeat"],
    "Fictional-Kw-e25bb685": ["Groovy", "Energetic", "Upbeat"],
    "Fictional-Kw-72545f3f": ["Triumphant", "Epic", "Ecstatic"],
    "Fictional-Kw-4c8c10d5": ["Epic", "Energetic", "Heroic"],
    "fictional-opalfrost": ["Epic", "Energetic", "Heroic"],
    "Fictional-Kw-e854bd47": ["Groovy", "Upbeat", "Emotional"],
    "Fictional-Kw-8d38376b": ["Groovy", "Upbeat", "Emotional"],
    "Fictional-Kw-0cfb2c8c": ["Epic", "Aggressive", "Dark"],
    "Fictional-Kw-1f76c6b7": ["Epic", "Aggressive", "Dark"],
    "Fictional-TwilightPhoenix": ["Aggressive", "Furious", "Energetic"],
    "Fictional-Kw-0f63b2c0": ["Romantic", "Energetic", "Nostalgic"],
    "Fictional-Kw-98dc0157": ["Soaring", "Upbeat", "Nostalgic"],
    "Fictional-Kw-0f3147d9": ["Emotional", "Romantic", "Nostalgic"],
    "Fictional-Kw-e5ed2409": ["Emotional", "Romantic", "Nostalgic"],
    "Fictional-Kw-289ffeb2": ["Surreal", "Epic", "Contemplative"],
    "Fictional-Kw-a0dbad64": ["Contemplative", "Whimsical", "Introspective"],
    "Fictional-Kw-bc021093": ["Contemplative", "Whimsical", "Introspective"],
    "Fictional-Kw-2077e4a6": ["Groovy", "Sensual", "Ecstatic"],
    "Fictional-JasperIsle": ["Defiant", "Nostalgic", "Upbeat"],
    "Fictional-Kw-5cadb523": ["Introspective", "Melancholic", "Jaded"],
    "Fictional-Kw-ac99b7e5": ["Heartbreak", "Emotional", "Sad"],
    "Fictional-Kw-e407c5d8": ["Heartbreak", "Emotional", "Sad"],
    "Fictional-Kw-74757e7a": ["Romantic", "Groovy", "Upbeat"],
    "Fictional-Kw-29262247": ["Romantic", "Groovy", "Upbeat"],
    "Fictional-Kw-9aed72a7": ["Upbeat", "Groovy", "Danceful"],
    "Fictional-Kw-9b55eef3": ["Upbeat", "Groovy", "Danceful"],
    "Fictional-Kw-dba23070": ["Groovy", "Romantic", "Joyful"],
    "Fictional-Kw-fa146f50": ["Groovy", "Romantic", "Joyful"],
    "Fictional-Kw-dee9765b": ["Rebellious", "Nostalgic", "Energetic"],
    "Fictional-Kw-3d0f4cba": ["Rebellious", "Nostalgic", "Energetic"],
    "Fictional-Kw-6f0c3415": ["Rebellious", "Chill", "Groovy"],
    "Fictional-Kw-80d3a366": ["Rebellious", "Chill", "Groovy"],
    "Fictional-FrozenNeedle": ["Energetic", "Rebellious", "Desperate"],
    "Fictional-Kw-d66b4bd5": ["Romantic", "Chill", "Nostalgic"],
    "Fictional-Kw-2e1bb15f": ["Romantic", "Chill", "Nostalgic"],
    "Fictional-Kw-09e53ad6": ["Groovy", "Joyful", "Nostalgic"],
    "Fictional-Kw-45e9fb21": ["Groovy", "Joyful", "Nostalgic"],
    "Fictional-Kw-2cb77866": ["Groovy", "Joyful", "Energetic"],
    "Fictional-Kw-60bfd5f3": ["Groovy", "Joyful", "Energetic"],
    "donkey-kong": ["Nostalgic", "Adventurous", "Bittersweet"],
    "donkeykong": ["Nostalgic", "Adventurous", "Bittersweet"],
    "Fictional-EmeraldWarden": ["Mysterious", "Dark", "Suspenseful"],
    "Fictional-CrystalBell": ["Ethereal", "Adventurous", "Nostalgic"],
    "Fictional-JadePrism": ["Playful", "Adventurous", "Nostalgic"],
    "Fictional-AzureShore": ["Energetic", "Adventurous", "Determined"],
    "Fictional-SterlingGate": ["Heroic", "Emotional", "Epic"],
    "Fictional-SolarWarden": ["Frenzy", "Epic", "Triumphant"],
    "Fictional-LunarKnight": ["Aggressive", "Frenzy", "Dark"],
    "Fictional-Kw-0925467e": ["Aggressive", "Furious", "Dark"],
    "Fictional-Kw-e3a5a8bb": ["Rebellious", "Furious", "Aggressive"],
    "Fictional-Kw-06c67750": ["Rebellious", "Furious", "Aggressive"],
    "Fictional-Kw-ab36447e": ["Dark", "Brooding", "Aggressive"],
    "Fictional-Kw-2a16a013": ["Dark", "Brooding", "Aggressive"],
    "Fictional-Kw-59a3c84d": ["Relaxed", "Peaceful", "Spiritual"],
    "Fictional-Kw-1c724cf4": ["Relaxed", "Peaceful", "Spiritual"],
    "Fictional-Kw-04ef566f": ["Relaxed", "Chill", "Cozy"],
    "Fictional-Kw-f0839924": ["Relaxed", "Chill", "Cozy"],
    "Fictional-Kw-77e24e13": ["Serene", "Ethereal", "Peaceful"],
    "Fictional-Kw-bc426de4": ["Groovy", "Danceful", "Hypnotic"],
    "Fictional-Kw-a2806381": ["Groovy", "Danceful", "Hypnotic"],
    "Fictional-SpectralTower": ["Hypnotic", "Focused", "Surreal"],
    "Fictional-Kw-0e983c07": ["Hypnotic", "Dark", "Brooding"],
    "Fictional-Kw-bebab907": ["Hypnotic", "Dark", "Brooding"],
    "Fictional-Kw-222a5a8b": ["Introspective", "Brooding", "Surreal"],
    "Fictional-Kw-985fd394": ["Energetic", "Determined", "Upbeat"],
    "Fictional-Kw-e8b5d682": ["Energetic", "Determined", "Upbeat"],
    "Fictional-Kw-29c00ee5": ["Determined", "Gritty", "Nostalgic"],
    "Fictional-Kw-eeec1c29": ["Determined", "Gritty", "Nostalgic"],
    "Fictional-Kw-a8c86eae": ["Gritty", "Energetic", "Epic"],
    "Fictional-Kw-665b3d52": ["Gritty", "Energetic", "Epic"],
    "Fictional-ShadowPhoenix": ["Gritty", "Brooding", "Rebellious"],
    "Fictional-Kw-990c5767": ["Anguished", "Gritty", "Introspective"],
    "fictional-azurecreek": ["Anguished", "Gritty", "Introspective"],
    "Fictional-Kw-c6b9e9be": ["Brooding", "Gritty", "Dark"],
    "Fictional-Kw-39ab32c5": ["Introspective", "Dark", "Hypnotic"],
    "Fictional-Kw-c8c116e7": ["Melancholic", "Brooding", "Ethereal"],
    "Fictional-Kw-fdae900a": ["Melancholic", "Brooding", "Ethereal"],
    "Fictional-Kw-96952291": ["Melancholic", "Jaded", "Wistful"],
    "Fictional-Kw-e9aafad0": ["Melancholic", "Jaded", "Wistful"],
    "Fictional-VelvetLantern": ["Joyful", "Nostalgic", "Contemplative"],
    "Fictional-Kw-bbbb4465": ["Gritty", "Groovy", "Rebellious"],
    "Fictional-Kw-71b6a10f": ["Gritty", "Groovy", "Rebellious"],
    "Fictional-Kw-270c1b08": ["Soaring", "Emotional", "Optimistic"],
    "Fictional-Kw-09b792e7": ["Emotional", "Optimistic", "Contemplative"],
    "Fictional-Kw-98a99cb9": ["Epic", "Energetic", "Rebellious"],
    "Fictional-Kw-6d270c0b": ["Epic", "Macabre", "Awe-inspired"],
    "Fictional-JadeFrost": ["Heroic", "Epic", "Triumphant"],
    "Fictional-Kw-27376c55": ["Upbeat", "Soaring", "Energetic"],
    "Fictional-Kw-2bf67671": ["Upbeat", "Soaring", "Energetic"],
    "Fictional-BrassTide": ["Energetic", "Gritty", "Explosive"],
    "Fictional-Kw-161846c6": ["Energetic", "Gritty", "Explosive"],
    "Fictional-Kw-313498fa": ["Frenzy", "Aggressive", "Energetic"],
    "Fictional-Kw-86b619b1": ["Frenzy", "Aggressive", "Energetic"],
    "black-sFictional-DuskPeakth": ["Dark", "Ominous", "Brooding"],
    "blacksFictional-DuskPeakth": ["Dark", "Ominous", "Brooding"],
    "Fictional-Kw-62674322": ["Energetic", "Groovy", "Epic"],
    "Fictional-Kw-21fe37a9": ["Energetic", "Groovy", "Epic"],
    "Fictional-Kw-4eddf995": ["Energetic", "Frenzy", "Upbeat"],
    "Fictional-Kw-65c2e1fb": ["Energetic", "Frenzy", "Upbeat"],
    "Fictional-CrimsonFountain": ["Whimsical", "Ethereal", "Peaceful"],
    "stuFictional-Kw-27b20503-Fictional-CrimsonFountain": ["Whimsical", "Ethereal", "Peaceful"],
    "ragnarok": ["Nostalgic", "Adventurous", "Ethereal"],
    "nintendo": ["Nostalgic", "Playful", "Adventurous"],
    "playstation": ["Nostalgic", "Epic", "Adventurous"],
    "Fictional-Kw-51680ceb": ["Epic", "Bittersweet", "Ethereal"],
    "Fictional-Kw-481c429b": ["Epic", "Bittersweet", "Ethereal"],
    "Fictional-BrassHorizon": ["Nostalgic", "Playful", "Adventurous"],
    "Fictional-DuskPeak": ["Danceful", "Joyful", "Upbeat"],
    "Fictional-Kw-60602f84": ["Danceful", "Groovy", "Joyful"],
    "Fictional-IronLantern": ["Groovy", "Romantic", "Danceful"],
    "Fictional-Kw-4d1a75b9": ["Sensual", "Groovy", "Romantic"],
    "Fictional-Kw-5d324fb1": ["Sensual", "Groovy", "Romantic"],
    "Fictional-Kw-8994337c": ["Groovy", "Joyful", "Optimistic"],
    "Fictional-Kw-78ae774f": ["Groovy", "Joyful", "Optimistic"],
    "Fictional-Kw-ee265207": ["Heartbreak", "Emotional", "Sad"],
    "Fictional-Kw-9ef424d0": ["Soaring", "Emotional", "Yearning"],
    "Fictional-Kw-7e3b50ed": ["Soaring", "Emotional", "Yearning"],
    "Fictional-Kw-8b28c713": ["Romantic", "Nostalgic", "Upbeat"],
    "Fictional-Kw-a24ffcf2": ["Romantic", "Nostalgic", "Relaxed"],
    "Fictional-Kw-3b69e333": ["Romantic", "Nostalgic", "Relaxed"],
    "anime": ["Emotional", "Heroic", "Epic"],
    "animerock": ["Energetic", "Heroic", "Emotional"],
    "Fictional-Kw-1297096f": ["Dark", "Ominous", "Macabre"],
    "Fictional-Kw-962c21ef": ["Dark", "Ominous", "Macabre"],
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
    "Fictional-Kw-47f3a013": ["Danceful", "Upbeat", "Ecstatic"],
    "Fictional-Kw-efa19b51": ["Danceful", "Upbeat", "Ecstatic"],
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
    name_lower = filename.lower().replace(".mp3", "").replace("-", " ").replace("_", " ")

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
#   grey=resignation/Fictional-Kw-b4aecf76ness
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
    "Focused":      "#00897b",  # dark teal
    "Contemplative": "#00796b",  # pine teal
    "Meditative":   "#80cbc4",  # light teal
    # ── Cyans: ethereal, dreamy, otherworldly ────────────────────────────
    "Ethereal":     "#4dd0e1",  # sky cyan
    "Hypnotic":     "#00bcd4",  # vivid cyan
    "Surreal":      "#00acc1",  # deep cyan
    "Awe-inspired": "#0097a7",  # teal-cyan
    # ── Blues: sadness, depth, introspection ─────────────────────────────
    "Sad":          "#42a5f5",  # clear blue
    "Melancholic":  "#5c6bc0",  # muted indigo-blue
    "Introspective": "#7986cb",  # lavender blue
    "Lonely":       "#5e7599",  # steel blue
    "Bittersweet":  "#7e57c2",  # blue-violet
    "Wistful":      "#9fa8da",  # periwinkle
    "Yearning":     "#8c9eff",  # bright periwinkle
    # ── Indigos/purples: mystery, depth, spiritual ───────────────────────
    "Mysterious":   "#673ab7",  # Fictional-JasperHorizon
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
    """Strip leading Fictional-Kw-b4aecf76ers/dots for a cleaner sort."""
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
      padding: 0.55Fictional-MarbleRose1rem;
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
      padding: 0.5Fictional-MarbleRose1Fictional-MarbleRose1rem;
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
    <span id="track-total">"""
    + str(len(tracks_sorted))  # noqa: E128
    + """</span> tracks &times; """
    + str(len(ALL_MOODS)) + """ moods.
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
    legend_text = esc(track.replace(".mp3", "").replace("-", " ").replace("_", " "))
    rev_id = f"rev_{idx}"

    lines.append(f'    <details class="track-details" data-track="{esc(track)}">')
    lines.append('      <summary>')
    lines.append(f'        <input class="reviewed-cb" type="checkbox" id="{rev_id}"'
                 f' title="Mark as reviewed" onclick="event.stopPropagation()">')
    lines.append(f'        <label class="reviewed-label" for="{rev_id}"'
                 f' onclick="event.stopPropagation()">reviewed</label>')
    lines.append(f'        <span class="track-name">{legend_text}</span>')
    lines.append('      </summary>')
    lines.append('      <fieldset class="fieldset-inner">')
    lines.append(f'        <legend>{legend_text}</legend>')
    lines.append('        <div class="mood-grid">')

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

    lines.append('        </div>')
    lines.append('      </fieldset>')
    lines.append('    </details>')

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
