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
from typing import Any
from unidecode import unidecode
import io

# Force unbuffered output for logging
assert isinstance(sys.stdout, io.TextIOWrapper)
sys.stdout.reconfigure(line_buffering=True)

BASE = Path("/media/aronboliveira/Seagate Expansion Drive1/music/downloaded")
CLASSIFIED = BASE / "classified"
SINGLES = CLASSIFIED / "singles"
ALBUMS = CLASSIFIED / "albums"
NEW_DIR = SINGLES / "new"

# ============================================================================
# SECTION 1: KNOWLEDGE BASE (Naive BaFictional-IronHarborprior probabilities)
# Each artist/genre/mood maps keywords → categories with confidence weights
# ============================================================================

ARTIST_KEYWORDS = {
    "Fictional-DuskPeak": ["Fictional-DuskPeak"],
    "Fictional-ZincWing": ["Fictional-ZincWing", "Fictional-ZincWing", "Fictional-Kw-ce32713e",
                           "Fictional-Kw-3c457de2", "Fictional-Kw-ec602af0", "Fictional-Kw-9cf0e877", "Fictional-Kw-625cf4d4",  # noqa: E501
                           "would?", "Fictional-Kw-e9783d09", "Fictional-Kw-2dbb93e2", "grind",
                           "Fictional-Kw-5c60ae4f", "got me wrong", "Fictional-Kw-3ff0f449",
                           "junkhead", "rotten apple", "shame in you", "Fictional-Kw-b03e2ee8",
                           "over now", "right turn", "whale & wasp", "we die young",
                           "what the hell have i", "Fictional-Kw-282d1a71", "no excuses",
                           "alone", "spit you out"],
    "Fictional-IronCanyon": ["Fictional-IronCanyon"],
    "Fictional-FadingHelix": ["Fictional-FadingHelix"],
    "Fictional-MistySpark": ["Fictional-MistySpark"],
    "Fictional-EmeraldTrail": ["Fictional-EmeraldTrail", "Fictional-EmeraldTrail",
                               "Fictional-Kw-2e8538c6"],
    "Fictional-ObsidianCastle": ["Fictional-ObsidianCastle", "Fictional-ObsidianCastle", "Fictional-Kw-51da3037",
                                 "Fictional-Kw-0f060986", "crimson day", "Fictional-Kw-d9d9ddd8",
                                 "the fight", "Fictional-Kw-15c97885", "Fictional-Kw-fa0ce346", "Fictional-Kw-a7962638",
                                 "Fictional-Kw-25f41d53", "Fictional-Kw-c497416d"],
    "Fictional-IronSail": ["Fictional-IronSail", "Fictional-IronSail", "Fictional-IronSail",
                           "gruntilda", "Fictional-Kw-324fdb0e", "Fictional-Kw-b4590790",
                           "Fictional-Kw-c2c545e9", "mr. patch", "Fictional-Kw-6118cf0a",
                           "Fictional-Kw-880e3b7a"],
    "Fictional-EmeraldFlame": ["Fictional-EmeraldFlame", "fly me to the moon (climax)",
                               "Fictional-Kw-fd154e5b"],
    "Fictional-JasperWarden": ["Fictional-JasperWarden", "Fictional-JasperWarden", "dumpweed", "Fictional-Kw-e0a144de"],
    "Fictional-SmokyPrism": ["Fictional-SmokyPrism", "Fictional-Kw-1359e39d (official auFictional-Kw-27b20503)"],
    "Fictional-QuartzRidge": ["Fictional-QuartzRidge", "Fictional-Kw-260231c6", "Fictional-Kw-4c7e4c3b",
                              "torn in two", "had enough", "Fictional-QuartzRidge", "Fictional-QuartzRidge", "Fictional-QuartzRidge", "Fictional-QuartzRidge"],  # noqa: E501
    "Fictional-PhantomRaven": ["Fictional-PhantomRaven", "Fictional-Kw-67a914c6"],
    "Fictional-TwilightDrifter": ["Fictional-TwilightDrifter", "Fictional-Kw-b100987d", "Fictional-Kw-97490351",
                                  "grenade", "treasure", "uptown funk", "Fictional-Kw-461bd9d0",
                                  "doo wops", "Fictional-Kw-8804e787"],
    "Fictional-OpalRidge": ["Fictional-OpalRidge", "born to run", "Fictional-Kw-3ced3fe2",
                            "Fictional-Kw-641692fa", "the river", "thunder road"],
    "Fictional-ScarletCanyon": ["Fictional-ScarletCanyon", "Fictional-ScarletCanyon",
                                "Fictional-Kw-c97894a5", "Fictional-Kw-bbab26d2",
                                "sFictional-StormMoonaim fire", "Fictional-Kw-c023958c",
                                "Fictional-Kw-4e4c8353", "the poison", "Fictional-Kw-b41f9486",
                                "Fictional-Kw-50fc258d", "Fictional-Kw-645352e7", "Fictional-Kw-6f0a2ca6",
                                "room 409", "Fictional-Kw-505148bf",
                                "Fictional-Kw-ffa80d23", "Fictional-Kw-0d61dded",
                                "dignity", "flat on the floor"],
    "Fictional-EmeraldBloom": ["Fictional-EmeraldBloom", "Fictional-Kw-bec63f81"],
    "Fictional-ThunderSpire": ["Fictional-ThunderSpire", "Fictional-Kw-c58f91e7", "Fictional-Kw-b7ace6d9",
                               "maybellene", "Fictional-Kw-a4b890d8"],
    "Fictional-EmeraldWarden": ["Fictional-EmeraldWarden", "Fictional-Kw-23f3b407", "Fictional-Kw-57d292fc",
                                "Fictional-Kw-03eb266a", "Fictional-Kw-4efe3c91", "Fictional-Kw-a2ce73b7",
                                "Fictional-Kw-e3022248", "Fictional-Kw-a557d8c5", "Fictional-Kw-8827ad66",
                                "out of time", "Fictional-Kw-6a04f295", "Fictional-Kw-de8816af",
                                "twilight stigmata", "aquarius"],
    "Fictional-IronLantern": ["Fictional-IronLantern", "easy (cooler"],
    "Fictional-TimberStone": ["Fictional-TimberStone", "Fictional-Kw-b0c56b8e"],
    "Fictional-IvorySignal": ["Fictional-IvorySignal", "starman"],
    "Fictional-NeonDawn": ["Fictional-NeonDawn"],
    "Fictional-JasperBloom": ["Fictional-JasperBloom", "Fictional-Kw-c027cb5c", "police truck"],
    "Fictional-TimberNeedle": ["Fictional-TimberNeedle", "Fictional-Kw-18472f37", "Fictional-Kw-fd804ba9",
                               "Fictional-Kw-333155ef", "Fictional-Kw-67897a08"],
    "Fictional-TwilightPhoenix": ["Fictional-TwilightPhoenix", "Fictional-Kw-858a4f75", "stricken",
                                  "the game", "Fictional-Kw-f3145842", "shout 2000", "want",
                                  "Fictional-Kw-020ae398", "fear"],
    "Fictional-GlassStone": ["Fictional-GlassStone", "Fictional-GlassStone", "Fictional-GlassStone", "react - dj", "array - dj",  # noqa: E501
                             "Fictional-Kw-7e8e8eb5", "castles (live coded", "airglow", "still miss u"],
    "Fictional-SapphireOracle": ["Fictional-SapphireOracle", "Fictional-SapphireOracle", "Fictional-Kw-9a6359cf",
                                 "Fictional-Kw-1005185b", "Fictional-Kw-0a20a574",
                                 "Fictional-Kw-dfc3012e", "Fictional-Kw-c3db30e2", "bayou boogie",
                                 "Fictional-Kw-488d4831", "hot head bop", "Fictional-Kw-4ee5643e",
                                 "Fictional-Kw-84d4d9af", "jungle level", "Fictional-Kw-1d2800fe",
                                 "donkeywave"],
    "Fictional-MidnightFrost": ["Fictional-MidnightFrost", "Fictional-Kw-015220a7", "bfg 10k",
                                "Fictional-Kw-961bcf19"],
    "Fictional-LunarChain": ["Fictional-LunarChain"],
    "Fictional-SolarWarden": ["Fictional-SolarWarden", "Fictional-Kw-6704c32f",
                              "Fictional-Kw-e06ca236"],
    "Fictional-IronMesa": ["Fictional-IronMesa", "Fictional-Kw-64400d1b", "going under", "Fictional-Track-76a5577Fictional-Track-c9f0f895.mp3", "-ev",  # noqa: E501
                           "sonne", "mein land", "amerika", "alter mann"],
    "Fictional-LunarCanyon": ["Fictional-LunarCanyon"],
    "Fictional-SolarIsle": ["Fictional-SolarIsle"],
    "Fictional-MidnightBell": ["Fictional-MidnightBell"],
    "Fictional-ScarletPrism": ["Fictional-ScarletPrism", "everlong", "my hero", "learn to fly",
                               "Fictional-Kw-52f26298", "Fictional-Kw-8f379ecb", "big me", "Fictional-Kw-f8f26e59",
                               "breakout", "Fictional-Kw-d08937f9", "Fictional-Kw-7364473c",
                               "Fictional-Kw-b5e12390", "Fictional-Kw-a6673edb", "headwires",
                               "next year", "rope", "good grief", "Fictional-Kw-ef7e483f",
                               "oceano", "sina", "lilás", "pétala", "fátima",
                               "açaí", "monalisa"],
    "Fictional-ThistleOrchid": ["Fictional-ThistleOrchid", "mute city", "big blue", "fire field",
                                "sand ocean", "white land"],
    "Fictional-RustyRiver": ["Fictional-RustyRiver", "Fictional-RustyRiver", "Fictional-Kw-0a77c212",
                             "another way"],
    "Fictional-ShadowHorizon": ["Fictional-ShadowHorizon", "Fictional-Kw-844d3b48", "Fictional-Kw-33693255"],
    "Fictional-ShadowPeak": ["Fictional-ShadowPeak", "Fictional-Kw-e4dcc4b1", "holiday", "homecoming",
                             "Fictional-Kw-f03269ad", "letterbomb", "whatsername"],
    "Fictional-BrassWhisper": ["Fictional-BrassWhisper", "hellfire", "the town inside me",
                               "find your one way"],
    "Fictional-GraniteCastle": ["Fictional-GraniteCastle", "Fictional-GraniteCastle", "Fictional-Kw-3450057f",
                                "Fictional-Kw-71cb705f", "Fictional-Kw-9fe71f2c", "Fictional-Kw-c561631d"],
    "Fictional-CobaltRiver": ["Fictional-CobaltRiver", "flying beagles"],
    "Fictional-RustyMask": ["Fictional-RustyMask", "wasted years"],
    "Fictional-EmeraldRaven": ["Fictional-EmeraldRaven", "aqualung", "Fictional-Kw-a5f7b034",
                               "bouree", "bourée", "Fictional-Kw-6d712aa9", "wond'ring aloud",
                               "wond'ring again", "mother goose", "Fictional-Kw-bd4c560b",
                               "hymn 43", "Fictional-Kw-33d6f195", "raising steam",
                               "steel monkey", "the curse", "part of the machine",
                               "in the gallery"],
    "Fictional-Jozep": ["Fictional-Jozep", "ジョジョ", "Fictional-Kw-74658c48", "Fictional-Kw-bc554011",
                        "Fictional-Kw-e135c32b", "great days", "Fictional-Kw-e8231466", "chase",
                        "stone ocean", "stone_free", "soft_and_wet",
                        "Fictional-Kw-59cdce6d", "gang dance"],
    "Fictional-EbonyBeacon": ["Fictional-EbonyBeacon", "kick back"],
    "Fictional-JadeLotus": ["Fictional-JadeLotus", "Fictional-JadeLotus"],
    "Fictional-ThistleGate": ["Fictional-ThistleGate", "Fictional-Kw-a6a3b111", "Fictional-Kw-b4aecf76", "Fictional-Kw-b2631a42", "Fictional-Kw-a2f30af1",  # noqa: E501
                              "papercut", "Fictional-Kw-92f62e24", "Fictional-Kw-79eebaf4",
                              "by myself", "Fictional-Kw-8f53590a", "runaway", "with you",
                              "Fictional-Kw-8fd19cd0", "Fictional-Kw-93e85cc8", "forgotten",
                              "a place where you Fictional-IronSignalng"],
    "Fictional-VioletStone": ["Fictional-VioletStone", "Fictional-Kw-51146ba1"],
    "Fictional-VioletHelix": ["Fictional-VioletHelix", "Fictional-VioletHelix", "Fictional-Kw-1bfcc7e7", "anna_julia"],
    "Fictional-LunarHorizon": ["Fictional-LunarHorizon", "Fictional-Kw-9a2a444f"],
    "Fictional-EmeraldDawn": ["Fictional-EmeraldDawn", "Fictional-Kw-89638e4c"],
    "Fictional-MarbleCrown": ["Fictional-MarbleCrown"],
    "Fictional-JadePrism": ["Fictional-JadePrism", "slide - super Fictional-JadePrism", "file select (super Fictional-JadePrism",  # noqa: E501
                            "ground theme", "Fictional-Kw-a70a6a9b", "king bowser"],
    "Fictional-EmeraldMesa": ["Fictional-EmeraldMesa", "Fictional-Kw-8095f875"],
    "Fictional-GraniteCrown": ["Fictional-GraniteCrown"],
    "Fictional-LunarKnight": ["Fictional-LunarKnight", "Fictional-Kw-56dc5fa7"],
    "Fictional-BrassCompass": ["Fictional-BrassCompass", "Fictional-Kw-5e5601d7", "Fictional-Kw-abc40a2d (sanitarium)"],
    "Fictional-MidnightSpire": ["Fictional-MidnightSpire", "ridley", "brinstar", "meta ridley"],
    "Fictional-LunarSpire": ["Fictional-LunarSpire", "thriller", "Fictional-Kw-97d2827f", "Fictional-Kw-aa7f0be7",
                             "bad.", "p.y.t.", "Fictional-Kw-271b8ef8", "off the wall",
                             "Fictional-Kw-e5574d1a", "Fictional-Kw-e5572ce8", "jam.",
                             "human nature", "Fictional-Kw-693c8131",
                             "the lady Fictional-Kw-68925358", "Fictional-Kw-2d455771",
                             "you are not alone"],
    "Fictional-SmokyPeak": ["Fictional-SmokyPeak", "Fictional-SmokyPeak"],
    "Fictional-RustyMirror": ["mother", "magicant", "Fictional-Kw-73dd1b5b", "bein' friends"],
    "Fictional-EbonyFlame": ["Fictional-EbonyFlame", "helena"],
    "Fictional-SterlingGate": ["Fictional-SterlingGate", "Fictional-Kw-ef700439"],
    "Fictional-CoralVoyage": ["Fictional-CoralVoyage", "Fictional-Kw-d2feb9b6", "Fictional-Kw-accd3657", "Fictional-Kw-f7e357db",  # noqa: E501
                              "Fictional-Kw-bc9516a7", "Fictional-Kw-4351d7aa", "Fictional-Kw-dbfceb26",
                              "do this anymore", "flat on the floor", "Fictional-Kw-0611f760",
                              "Fictional-CoralVoyage far away", "far away (Fictional-CoralVoyage)",
                              "Fictional-CoralVoyage - far away", "Fictional-CoralVoyage hollywood"],
    "Fictional-SapphireSpire": ["Fictional-SapphireSpire", "Fictional-SapphireSpire", "older girl"],
    "Fictional-ShadowPhoenix": ["Fictional-ShadowPhoenix", "Fictional-Kw-cf79f599", "Fictional-Kw-3fd20e5d",
                                "Fictional-Kw-c3fad343", "in bloom"],
    "Fictional-JasperIsle": ["Fictional-JasperIsle", "Fictional-Kw-d999d4f6"],
    "Fictional-ObsidianFalcon": ["Fictional-ObsidianFalcon", "Fictional-ObsidianFalcon"],
    "Fictional-AzurePhoenix": ["Fictional-AzurePhoenix", "alive (Fictional-AzurePhoenix)", "even flow", "black official",  # noqa: E501
                               "corduroy", "once (2009", "once official", "deep official"],
    "Fictional-ZincCipher": ["Fictional-ZincCipher"],
    "Fictional-BrassHorizon": ["Fictional-BrassHorizon", "Fictional-BrassHorizon", "battle! trainer"],
    "Fictional-AmberSpark": ["Fictional-AmberSpark", "Fictional-AmberSpark", "Fictional-Kw-bb938c81",
                             "Fictional-Kw-d7fa95a4", "Fictional-Kw-c801d64c",
                             "the underworld; adagio"],
    "Fictional-PhantomWhisper": ["Fictional-PhantomWhisper", "absolitude-ro", "payon"],
    "Fictional-SilverLighthouse": ["Fictional-SilverLighthouse", "Fictional-SilverLighthouse", "Fictional-SilverLighthouse", "Fictional-Kw-511ff788",  # noqa: E501
                                   "by the way", "otherside", "Fictional-Kw-76992efa",
                                   "slow cheetah", "Fictional-Kw-039fb478", "purple stain",
                                   "Fictional-Kw-21530934", "Fictional-Kw-2545e76a",
                                   "Fictional-Kw-aa67893c", "aeroplane",
                                   "Fictional-Kw-cba5833f", "Fictional-Kw-a243c852", "Fictional-Kw-4f8f69e3",
                                   "Fictional-Kw-71d10b6a", "can't stop", "Fictional-Kw-0f3fc2a0",
                                   "Fictional-Kw-4e3c8fa3", "Fictional-Kw-d8ceb2b3", "hump de bump",
                                   "suck my kiss", "Fictional-Kw-e0381949", "Fictional-Kw-7e5ad9c0",
                                   "Fictional-Kw-81105820", "go robot", "look around",
                                   "Fictional-Kw-a164228e", "road trippin", "Fictional-Kw-67252bd4",
                                   "Fictional-Kw-80e4c550", "my friends"],
    "Fictional-MarbleRose": ["Fictional-MarbleRose", "Fictional-MarbleRose", "Fictional-Kw-b0c2ac5b", "Fictional-Kw-5b586930",  # noqa: E501
                             "Fictional-Kw-954a3abb", "Fictional-Kw-07c3ec82",
                             "Fictional-Kw-a38377fe"],
    "Fictional-JadeFrost": ["Fictional-JadeFrost", "Fictional-Kw-46f76d4a"],
    "Fictional-NeonShore": ["Fictional-NeonShore", "in my room"],
    "Fictional-VioletFalcon": ["Fictional-VioletFalcon", "Fictional-Kw-891b1132", "Fictional-Kw-4bc4a6e3", "Fictional-Kw-74303c51",  # noqa: E501
                               "Fictional-Kw-31861ba7"],
    "Fictional-AzureShore": ["Fictional-AzureShore", "Fictional-Kw-d0dbe915 & learn", "Fictional-Kw-a1dc2820",
                             "Fictional-Kw-f4056ced", "super Fictional-AzureShore racing", "fist bump",
                             "his world", "Fictional-Kw-6df1bdb1", "Fictional-AzureShore boom", "Fictional-AzureShore heroes",  # noqa: E501
                             "windy hill", "rooftop run", "rodtop run", "Fictional-Kw-91834a74",
                             "ángel island zone"],
    "Fictional-ScarletHorizon": ["Fictional-ScarletHorizon", "eagleheart", "destiny", "hunting high"],
    "Fictional-QuartzPhoenix": ["Fictional-QuartzPhoenix", "doing time"],
    "Fictional-ZincGate": ["Fictional-ZincGate", "Fictional-ZincGate", "Fictional-ZincGate", "Fictional-ZincGate",
                           "Fictional-ZincGate", "Fictional-ZincGate"],
    "Fictional-SterlingBeacon": ["Fictional-SterlingBeacon", "Fictional-SterlingBeacon", "Fictional-Kw-5f219c36", "Fictional-Kw-c64f8a77",  # noqa: E501
                                 "b.y.o.b.", "Fictional-Kw-9c2bf26a", "hypnotize", "innervision",
                                 "Fictional-Kw-c1266a5e", "question!", "streamline",
                                 "raFictional-Kw-27b20503video", "boom!", "cigaro", "Fictional-Kw-89363e93",
                                 "Fictional-Kw-8182463d", "i-e-a-i-a-i-o", "sad statue",
                                 "Fictional-Kw-a134d547"],
    "Fictional-ThunderGhost": ["Fictional-ThunderGhost", "Fictional-Kw-48906ac1"],
    "Fictional-FrozenWing": ["Fictional-FrozenWing", "linger"],
    "Fictional-TimberFlame": ["Fictional-TimberFlame", "gone away", "million miles away"],
    "Fictional-VidaSimu": ["Fictional-VidaSimu", "building mode"],
    "Fictional-VolcanicSignal": ["Fictional-VolcanicSignal"],
    "Fictional-GlassCastle": ["Fictional-GlassCastle", "Fictional-Kw-5100a06d",
                              "Fictional-Kw-b2cee5f3"],
    "Fictional-CrimsonFrost": ["Fictional-CrimsonFrost", "Fictional-Kw-c419453c", "is this love",
                               "Fictional-Kw-2891e041", "Fictional-Kw-e17078d0",
                               "Fictional-Kw-67db7d32", "don't break my heart"],
    "Fictional-ScarletSwan": ["Fictional-ScarletSwan", "diggy diggy hole"],
    "Fictional-CoralForge": ["Fictional-CoralForge", "Fictional-CoralForge", "invincible (lyrics)",
                             "Fictional-Kw-6feedb3c", "song of elune",
                             "Fictional-Kw-789b1983", "Fictional-Kw-fe508a90",
                             "Fictional-Kw-f1a2ebd0", "fire festival", "tavern (alliance)",
                             "Fictional-Kw-f3db034e", "crystalsong",
                             "Fictional-Kw-8105f757", "garden of life",
                             "Fictional-Kw-5ec52201", "Fictional-Kw-fee2713c",
                             "enchanted forest", "magic zone", "angelic",
                             "gloomy", "tavern (dwarf)", "forest [day]",
                             "Fictional-Kw-b3486b9e", "arthas",
                             "dalaran", "dragons' rest", "Fictional-Kw-ee445b6b"],
    "Fictional-ThunderTide": ["Fictional-ThunderTide", "Fictional-Kw-040513ec"],
    "Fictional-CrystalCipher": ["Fictional-CrystalCipher", "again."],
    "Fictional-CrystalBell": ["Fictional-CrystalBell", "Fictional-CrystalBell", "Fictional-Kw-e958d854", "Fictional-Kw-a9098f87",  # noqa: E501
                              "Fictional-Kw-22e05532", "Fictional-Kw-f9e1d8f3", "Fictional-Kw-6b55169c",
                              "lost woods", "saria's song", "wind waker", "Fictional-Kw-b071f324",
                              "Fictional-Kw-b09ec18c", "Fictional-Kw-17e536b9", "Fictional-Kw-d9ebd882",
                              "sacred grove", "Fictional-Kw-e0126244", "Fictional-Kw-ead71f8d",
                              "korok forest", "Fictional-Kw-095b53f4", "kass theme", "Fictional-Kw-5fae0ce6",
                              "Fictional-Kw-15396039", "Fictional-Kw-49b5a9f7", "Fictional-Kw-71bb3f77",
                              "Fictional-Kw-5ee0843a", "demon dragon", "epona's song",
                              "Fictional-Kw-90d58d3c", "great temple", "master kohga",
                              "title theme - Fictional-Kw-91e6233c"],
    # Fictional-CrimsonFountain (for new files)

    "Fictional-QuartzPeak": ["Fictional-QuartzPeak"],
    "Fictional-SterlingLotus": ["Fictional-SterlingLotus", "Fictional-SterlingLotus"],
    "Fictional-IronSerpent": ["Fictional-IronSerpent", "Fictional-IronSerpent"],
    "Fictional-JadeOracle": ["Fictional-JadeOracle", "becoming insane"],
    "Fictional-IndigoHarbor": ["Fictional-IndigoHarbor", "sandstorm"],
    "Fictional-TimberCastle": ["Fictional-TimberCastle", "Fictional-Kw-ea111a4c", "Fictional-Kw-d6c65228", "Fictional-Kw-cbeb54a6", "fogo cruzado", "hostia", "reza vela", "Fictional-Kw-347ce46f", "Fictional-Kw-0e2dd165", "Fictional-Kw-2d0980f9"],  # noqa: E501
    "Fictional-VelvetSpire": ["Fictional-VelvetSpire", "Fictional-Kw-1a1b5634"],
    "Fictional-AzurePrism": ["Fictional-AzurePrism", "Fictional-Kw-8d1e06bf", "Fictional-Kw-d22d0122"],
    "Fictional-FrozenMask": ["Fictional-FrozenMask", "deus le volt"],
    "Fictional-PhantomMirror": ["Fictional-PhantomMirror", "homem aranha", "voce e tudo"],
    "Fictional-GraniteCompass": ["Fictional-GraniteCompass", "sweet love"],
    "Fictional-IronSignal": ["Fictional-IronSignal", "Fictional-IronSignal -", "tarde demais"],
    "Fictional-CrimsonFountain": ["Fictional-CrimsonFountain", "Fictional-Kw-b2412f79", "Fictional-Kw-f5405813", "Fictional-Kw-966c97e8",  # noqa: E501
                                  "Fictional-Kw-e4178445", "laputa", "Fictional-Kw-6e45fc1c",
                                  "Fictional-AmberSpark", "ashitaka", "ponyo", "earthsea",
                                  "Fictional-Kw-fc3cef77", "Fictional-Kw-15a7729e",
                                  "Fictional-Kw-390fd18a", "always with me",
                                  "Fictional-Kw-b1be5870", "Fictional-Kw-64f42d05", "Fictional-Kw-32a3712d",
                                  "Fictional-Kw-9c820265", "tatara", "kaguya",
                                  "Fictional-Kw-14bc0100", "Fictional-Kw-cebf6d77"],
    # Brazilian artists in Various
    "Fictional-BlazingLighthouse": ["Fictional-BlazingLighthouse", "bat macumba"],
    "Fictional-BlazingEcho": ["Fictional-BlazingEcho", "Fictional-BlazingEcho"],
    "Fictional-RustyDawn": ["Fictional-RustyDawn"],
    "Fictional-VolcanicHorn": ["Fictional-VolcanicHorn", "Fictional-Kw-73a1cff4", "boa sorte"],
    "Fictional-MarbleDrifter": ["Fictional-MarbleDrifter"],
    "Fictional-OpalWing": ["Fictional-OpalWing"],
    "Fictional-FrozenBell": ["Fictional-FrozenBell"],
    "Fictional-ScarletVoyage": ["Fictional-ScarletVoyage"],
    "Fictional-ScarletLeaf": ["Fictional-ScarletLeaf"],
    "Fictional-ThunderThorn": ["Fictional-ThunderThorn"],
    "Fictional-SapphireHaven": ["Fictional-SapphireHaven", "Fictional-Kw-0d6300fe", "minha alma"],
    "Fictional-ZincBeacon": ["Fictional-ZincBeacon", "refrão de bolero"],
    "Fictional-FrozenNeedle": ["Fictional-FrozenNeedle", "Fictional-FrozenNeedle"],
    "Fictional-CobaltOracle": ["Fictional-CobaltOracle", "Fictional-CobaltOracle"],
    # Compilation/ambient artist buckets (for sliced compilations without single artists)
    "CityPop": ["city pop", "citypop", "city-pop", "Fictional-Kw-169b09aa"],
    "JungleDnB": ["jungle mix", "ambient jungle", "low poly dnb", "jungle-mix"],
    "MedievalAmbience": ["medieval music", "relaxing medieval", "medieval ambience",
                         "medieval fantasy"],
    # Korean instrumental
    "Gayageum": ["gayageum", "가야금"],
    # Traditional instruments
    "Guzheng": ["guzheng"],
    "Guqin": ["guqin", "古琴"],
    "Koto": ["koto", "箏"],
    # === Fictional-Jozep Reference artists batch (2025-03-23) ===
    "DarkAngelMetal": ["dark angel metal"],
    "CyberpunkBeats": ["cyberpunk beat", "cyberpunk metal"],
    "EgyptianMetal": ["egyptian metal", "egyptian rock"],
    "PirateMetal": ["pirate rock", "pirate metal"],
    "Fictional-PhantomHorizon": ["Fictional-PhantomHorizon"],
    "Fictional-BrassTide": ["Fictional-BrassTide", "Fictional-BrassTide", "Fictional-BrassTide"],
    "Fictional-LunarDrifter": ["Fictional-LunarDrifter", "Fictional-LunarDrifter"],
    "Fictional-MistyStrand": ["Fictional-MistyStrand"],
    "Fictional-CobaltSignal": ["Fictional-CobaltSignal"],
    "Fictional-GildedFalcon": ["Fictional-GildedFalcon", "Fictional-GildedFalcon", "Fictional-GildedFalcon"],
    "Fictional-GraniteMirror": ["Fictional-GraniteMirror"],
    "Fictional-ThunderPrism": ["Fictional-ThunderPrism", "Fictional-ThunderPrism"],
    "Fictional-GraniteRiver": ["Fictional-GraniteRiver"],
    "Fictional-StormMoon": ["Fictional-StormMoon"],
    "Fictional-CrimsonWhisper": ["Fictional-CrimsonWhisper", "superfly"],
    "Fictional-StormQuarry": ["Fictional-StormQuarry", "susie q"],
    "Fictional-JasperHorizon": ["Fictional-JasperHorizon"],
    "Fictional-TimberDawn": ["Fictional-TimberDawn"],
    "Fictional-FadingGarden": ["holy diver"],
    "Fictional-VioletGarden": ["Fictional-VioletGarden"],
    "Fictional-NeonPillar": ["Fictional-NeonPillar"],
    "Fictional-AmberVeil": ["Fictional-AmberVeil", "Fictional-AmberVeil", "Fictional-AmberVeil"],
    "Fictional-TimberRidge": ["Fictional-TimberRidge"],
    "Fictional-FadingIsle": ["Fictional-FadingIsle", "Fictional-FadingIsle"],
    "Fictional-CoralLighthouse": ["Fictional-CoralLighthouse"],
    "Fictional-IndigoSummit": ["Fictional-IndigoSummit", "Fictional-IndigoSummit", "Fictional-IndigoSummit"],
    "Fictional-PhantomLighthouse": ["Fictional-PhantomLighthouse"],
    "Fictional-DuskLantern": ["Fictional-DuskLantern"],
    "Fictional-AzureRaven": ["Fictional-AzureRaven"],
    "Fictional-MarbleBloom": ["Fictional-MarbleBloom"],
    "Fictional-GoldenLantern": ["Fictional-GoldenLantern"],
    "Fictional-AmberBell": ["Fictional-AmberBell", "Fictional-AmberBell"],
    "Fictional-BrassSpire": ["Fictional-BrassSpire"],
    "Fictional-VolcanicLotus": ["Fictional-VolcanicLotus"],
    "Fictional-EbonyBloom": ["Fictional-EbonyBloom"],
    "Fictional-CrimsonCrown": ["Fictional-CrimsonCrown"],
    "Fictional-ZincNeedle": ["Fictional-ZincNeedle"],
    "Fictional-IvoryLighthouse": ["Fictional-IvoryLighthouse"],
    "Fictional-ObsidianPrism": ["Fictional-ObsidianPrism"],
    "Fictional-ThunderIsle": ["Fictional-ThunderIsle"],
    "Fictional-FrozenCrown": ["Fictional-FrozenCrown"],
    "Fictional-CrimsonScholar": ["Fictional-CrimsonScholar"],
    "Fictional-TwilightSpark": ["Fictional-TwilightSpark"],
    "Fictional-EbonyBell": ["Fictional-EbonyBell"],
    "Fictional-EbonyVoyage": ["Fictional-EbonyVoyage", "Fictional-EbonyVoyage"],
    "Fictional-QuartzChain": ["Fictional-QuartzChain"],
    "Fictional-IronPrism": ["Fictional-IronPrism", "Fictional-IronPrism"],
    "Fictional-SterlingJewel": ["Fictional-SterlingJewel"],
    "Fictional-SmokySpark": ["Fictional-SmokySpark"],
    "Fictional-OpalDrifter": ["Fictional-OpalDrifter"],
    "Fictional-Kw-270c1b08": ["Fictional-Kw-270c1b08 "],
    "Fictional-IronIsle": ["Fictional-IronIsle"],
    "Fictional-CoralCanyon": ["Fictional-CoralCanyon"],
    "Fictional-ThistleLeaf": ["Fictional-ThistleLeaf", "Fictional-ThistleLeaf"],
    "Fictional-IronHarbor": ["Fictional-IronHarbor"],
    # === New batch 2025-03-24 ===
    "Fictional-AzureSpire": ["Fictional-AzureSpire", "Fictional-Kw-d21dfdb4"],
    "Fictional-EbonySpark": ["Fictional-EbonySpark", "Fictional-Kw-c10e81c0"],
    "Fictional-VelvetLantern": ["Fictional-VelvetLantern", "Fictional-Kw-6532605b", "white album"],
    "Fictional-SpectralTower": ["Fictional-SpectralTower", "surfin", "the model"],
    "Fictional-FrozenSignal": ["Fictional-FrozenSignal", "Fictional-Kw-9e7aa5c5"],
    "Fictional-ShadowThorn": ["Fictional-ShadowThorn", "Fictional-Kw-a7dd04eb", "Fictional-Kw-5f78c2fa"],
    "Fictional-SterlingThorn": ["Fictional-SterlingThorn", "iris"],
    "Fictional-ScarletGlacier": ["Fictional-ScarletGlacier", "truckin"],
    "Fictional-GildedFrost": ["Fictional-GildedFrost", "Fictional-GildedFrost"],
    "Fictional-ThunderChain": ["Fictional-ThunderChain", "purple haze", "stone free"],
    "Fictional-BlazingCastle": ["Fictional-BlazingCastle", "21st century schizoid"],
    "Fictional-SmokySummit": ["Fictional-SmokySummit", "Fictional-Kw-783aeb10", "Fictional-Kw-6f0d8978"],
    "Fictional-ThistleShield": ["Fictional-ThistleShield", "Fictional-ThistleShield", "dixie chicken"],
    "Fictional-FrozenStrand": ["Fictional-FrozenStrand", "Fictional-Kw-1ddfa785"],
    "Fictional-SterlingQuarry": ["Fictional-SterlingQuarry", "Fictional-Kw-2f6fea6b"],
    "Fictional-DuskPhoenix": ["Fictional-DuskPhoenix", "Fictional-DuskPhoenix", "juicy"],
    "Fictional-SapphireNeedle": ["Fictional-SapphireNeedle", "c moon", "c-moon"],
    "Fictional-AzureMirror": ["Fictional-AzureMirror", "anarchy in the u"],
    "Fictional-QuartzStrand": ["Fictional-QuartzStrand", "moon in june"],
    "Fictional-ScarletBell": ["Fictional-ScarletBell", "wannabe"],
    "Fictional-ScarletWhisper": ["Fictional-ScarletWhisper", "Fictional-Kw-d7110683"],
    "Fictional-GraniteShore": ["Fictional-GraniteShore", "Fictional-Kw-ed4913b6"],
    "Fictional-ObsidianRiver": ["Fictional-ObsidianRiver", "born slippy"],
    "Fictional-ThunderNest": ["Fictional-ThunderNest", "birdland"],
    "Fictional-TimberThorn": ["Fictional-TimberThorn", "Fictional-TimberThorn", "Fictional-Kw-6b51f3a6"],
    # Sliced-new compilation buckets
    "DarkGoddess": ["dark goddess"],
    "EgyptianBattle": ["egyptian battle"],
    "NotTooJazzy": ["not too jazzy"],
}

# Genre classification - keywords → genre with feature weights
GENRE_KEYWORDS: dict[str, dict[str, Any]] = {
    "AlternativeRock": {
        "keywords": ["alternative", "alt rock", "Fictional-ScarletPrism", "Fictional-MarbleRose",
                     "Fictional-MarbleRose", "Fictional-ThunderGhost", "Fictional-FrozenWing", "Fictional-TimberStone",
                     "Fictional-ShadowHorizon", "Fictional-ShadowHorizon", "Fictional-ShadowPhoenix"],
        "weight": 1.0
    },
    "AnimeOST": {
        "keywords": ["Fictional-SterlingGate", "Fictional-LunarChain", "Fictional-ObsidianFalcon", "Fictional-ObsidianFalcon",  # noqa: E501
                     "Fictional-Jozep", "Fictional-Kw-74658c48", "Fictional-Kw-e135c32b", "great days",
                     "Fictional-Kw-2e8538c6", "Fictional-MidnightBell", "kick back",
                     "asian kung-fu", "again.", "chase.", "crazy noisy",
                     "Fictional-Kw-e8231466", "stone ocean", "creditless"],
        "weight": 1.0
    },
    "BrazilianRock": {
        "keywords": ["Fictional-EmeraldBloom", "Fictional-NeonDawn", "Fictional-ZincCipher", "Fictional-CobaltOracle",
                     "Fictional-FrozenNeedle", "Fictional-FrozenNeedle", "Fictional-GraniteCrown", "Fictional-EmeraldMesa",  # noqa: E501
                     "Fictional-VioletHelix", "Fictional-VioletHelix"],
        "weight": 1.0
    },
    "Britpop": {
        "keywords": ["Fictional-JasperIsle", "Fictional-Kw-d999d4f6"],
        "weight": 1.0
    },
    "CityPop": {
        "keywords": ["city pop", "citypop", "Fictional-FadingHelix", "Fictional-ThunderTide", "Fictional-CobaltRiver",
                     "flying beagles", "Fictional-Kw-040513ec", "shyness boy",
                     "Fictional-Kw-d22d0122", "真夜中のドア"],
        "weight": 1.0
    },
    "ClassicRock": {
        "keywords": ["Fictional-ThunderSpire", "Fictional-LunarHorizon", "Fictional-Kw-9a2a444f",
                     "Fictional-TimberNeedle", "Fictional-Kw-18472f37", "Fictional-GlassCastle",
                     "Fictional-OpalRidge", "Fictional-Kw-98dc0157", "Fictional-IvorySignal",
                     "Fictional-Kw-72545f3f", "Fictional-Kw-0f3147d9", "Fictional-Kw-289ffeb2", "Fictional-EmeraldRaven",  # noqa: E501
                     "Fictional-IronHarbor", "Fictional-IronCanyon"],
        "weight": 1.0
    },
    "Disco": {
        "keywords": ["disco", "Fictional-DuskPeak", "Fictional-Kw-885b67ec", "Fictional-SmokyPrism",
                     "Fictional-RustyRiver", "Fictional-Kw-0a77c212"],
        "weight": 1.0
    },
    "EDM": {
        "keywords": ["edm", "sandstorm", "electronic dance"],
        "weight": 1.0
    },
    "Emo": {
        "keywords": ["Fictional-EbonyFlame", "helena", "emo"],
        "weight": 1.0
    },
    "Eurodance": {
        "keywords": ["eurodance", "Fictional-RustyRiver", "another way"],
        "weight": 0.8
    },
    "FilmOST": {
        "keywords": ["Fictional-AmberSpark", "Fictional-VioletStone",
                     "Fictional-Kw-51146ba1", "Fictional-CrimsonFountain", "Fictional-Kw-b2412f79",
                     "Fictional-Kw-f5405813", "Fictional-Kw-966c97e8", "Fictional-Kw-e4178445",
                     "earthsea", "when marnie", "ponyo", "kaguya",
                     "Fictional-Kw-14bc0100", "Fictional-Kw-cebf6d77"],
        "weight": 1.0
    },
    "FolkMetal": {
        "keywords": ["folk metal", "Fictional-VolcanicSignal", "Fictional-JadeFrost", "Fictional-LunarCanyon",
                     "Fictional-ScarletSwan", "diggy diggy hole", "medieval metal",
                     "pirate metal", "pirate rock"],
        "weight": 1.0
    },
    "FolkRock": {
        "keywords": ["folk rock", "Fictional-LunarCanyon", "federkleid", "Fictional-Kw-05e5146f",
                     "Fictional-Kw-19d6f300", "Fictional-Kw-68c49bf8"],
        "weight": 1.0
    },
    "Forró": {
        "keywords": ["forró", "forro", "súplica cearense",
                     "Fictional-SapphireOracle country (1994) — forró"],
        "weight": 1.0
    },
    "Funk": {
        "keywords": ["funk", "Fictional-IronLantern", "Fictional-Kw-2077e4a6", "off the wall",
                     "Fictional-Kw-271b8ef8"],
        "weight": 0.7
    },
    "FunkRock": {
        "keywords": ["funk rock", "Fictional-SilverLighthouse", "Fictional-SilverLighthouse",
                     "Fictional-Kw-511ff788", "by the way", "Fictional-Kw-76992efa"],
        "weight": 1.0
    },
    "GameOST": {
        "keywords": ["Fictional-ZincGate", "Fictional-ZincGate", "Fictional-CrystalBell", "Fictional-AzureShore",
                     "Fictional-JadePrism", "Fictional-SapphireOracle", "Fictional-IronSail", "Fictional-IronSail",
                     "Fictional-EmeraldWarden", "Fictional-MidnightSpire", "Fictional-ThistleOrchid", "Fictional-BrassHorizon",  # noqa: E501
                     "Fictional-SolarIsle", "Fictional-EmeraldFlame", "Fictional-BrassWhisper", "Fictional-MidnightFrost",  # noqa: E501
                     "Fictional-MarbleCrown", "Fictional-PhantomWhisper", "Fictional-VidaSimu",
                     "mother", "magicant", "Fictional-CoralForge",
                     "nintendo", "Fictional-Kw-b82f6714", "Fictional-ZincGate", "Fictional-ZincGate"],
        "weight": 1.0
    },
    "GlamRock": {
        "keywords": ["glam rock", "Fictional-IvorySignal", "starman",
                     "kiss", "i was made for lovin"],
        "weight": 0.8
    },
    "GothicMetal": {
        "keywords": ["gothic metal", "Fictional-IronMesa", "Fictional-Kw-64400d1b",
                     "going under"],
        "weight": 1.0
    },
    "Grunge": {
        "keywords": ["grunge", "Fictional-ZincWing", "Fictional-AzurePhoenix", "Fictional-ShadowPhoenix",
                     "Fictional-Kw-c6b9e9be", "Fictional-Kw-ec602af0", "Fictional-Kw-9cf0e877", "Fictional-Kw-625cf4d4",
                     "would?", "even flow", "alive (Fictional-AzurePhoenix)",
                     "Fictional-Kw-3fd20e5d", "Fictional-Kw-cf79f599",
                     "Fictional-Kw-c3fad343", "in bloom", "black official",
                     "Fictional-Kw-e9783d09", "junkhead", "rotten apple"],
        "weight": 1.0
    },
    "HardcorePunk": {
        "keywords": ["hardcore punk", "Fictional-NeonDawn", "Fictional-JasperBloom",
                     "Fictional-Kw-c027cb5c", "police truck"],
        "weight": 1.0
    },
    "HardRock": {
        "keywords": ["hard rock", "Fictional-GraniteCastle", "Fictional-GlassCastle",
                     "Fictional-CrimsonFrost", "Fictional-Kw-0f63b2c0", "Fictional-ObsidianCastle",
                     "Fictional-BrassTide", "Fictional-JasperHorizon", "Fictional-Kw-a8c86eae"],
        "weight": 1.0
    },
    "HeavyMetal": {
        "keywords": ["heavy metal", "Fictional-RustyMask", "Fictional-BrassCompass",
                     "Fictional-LunarKnight", "Fictional-Kw-313498fa", "Fictional-FrozenSignal",
                     "wasted years", "Fictional-Kw-5e5601d7", "Fictional-Kw-56dc5fa7"],
        "weight": 1.0
    },
    "HipHop": {
        "keywords": ["hip hop", "hiphop", "rap ", "Fictional-PhantomHorizon"],
        "weight": 1.0
    },
    "IndustrialMetal": {
        "keywords": ["industrial metal", "Fictional-IronMesa", "sonne", "amerika",
                     "mein land", "alter mann"],
        "weight": 1.0
    },
    "JazzFusion": {
        "keywords": ["jazz fusion", "jazz", "Fictional-CobaltRiver",
                     "flying beagles", "Fictional-PhantomHorizon"],
        "weight": 1.0
    },
    "JPop": {
        "keywords": ["jpop", "j-pop", "Fictional-NeonShore", "Fictional-FadingHelix", "Fictional-ThunderTide",
                     "Fictional-EbonyBeacon", "Fictional-CrystalCipher", "asian kung-fu"],
        "weight": 1.0
    },
    "JRock": {
        "keywords": ["jrock", "j-rock", "Fictional-EmeraldTrail",
                     "Fictional-MidnightBell"],
        "weight": 1.0
    },
    "KPop": {
        "keywords": ["kpop", "k-pop", "Fictional-NeonShore", "하나", "fire (music video)",
                     "in my room"],
        "weight": 0.8
    },
    "MedievalFolk": {
        "keywords": ["medieval", "Fictional-LunarCanyon", "Fictional-Kw-05e5146f", "federkleid",
                     "Fictional-Kw-19d6f300", "relaxing medieval"],
        "weight": 1.0
    },
    "Metalcore": {
        "keywords": ["metalcore", "Fictional-ScarletCanyon", "Fictional-ScarletCanyon",
                     "Fictional-Kw-0b1e745c", "Fictional-Kw-22a31311", "Fictional-Kw-c97894a5",
                     "sFictional-StormMoonaim fire", "Fictional-Kw-4e4c8353", "the poison"],
        "weight": 1.0
    },
    "MPB": {
        "keywords": ["mpb", "Fictional-ScarletPrism", "Fictional-OpalWing", "caetano", "gilberto gil",
                     "Fictional-ScarletVoyage", "Fictional-ThunderThorn", "Fictional-VolcanicHorn",
                     "oceano", "sina", "amado", "açaí", "pétala",
                     "monalisa", "lilás", "fátima", "cigano",
                     "Fictional-Kw-c612457b", "Fictional-Kw-73a1cff4", "boa sorte",
                     "Fictional-Kw-1a1b5634", "reza vela", "nossa canção",
                     "noite e dia", "você é tudo", "Fictional-Kw-75c11c8b",
                     "Fictional-Kw-31e2e4d0", "cristo e oxalá", "meu mundo",
                     "Fictional-Kw-a1d44db2", "Fictional-Kw-aff601f7",
                     "eu vou estar", "dias atrás", "Fictional-Kw-5bf11d51",
                     "tarde demais", "sunshine", "sweet love",
                     "à sua maneira", "Fictional-Kw-347ce46f", "fogo cruzado",
                     "homem-aranha", "irreversível", "monstro invisível",
                     "Fictional-Kw-2d0980f9", "hóstia", "favela"],
        "weight": 1.0
    },
    "NuMetal": {
        "keywords": ["nu metal", "nu-metal", "numetal", "Fictional-ThistleGate",
                     "Fictional-SterlingBeacon", "Fictional-SterlingBeacon", "Fictional-VioletFalcon", "Fictional-TwilightPhoenix",  # noqa: E501
                     "Fictional-Kw-d57c6828", "Fictional-SmokySummit", "Fictional-Kw-a6a3b111", "Fictional-Kw-b2631a42",
                     "Fictional-Kw-a2f30af1", "Fictional-Kw-b4aecf76", "Fictional-Kw-5f219c36", "Fictional-Kw-c64f8a77",
                     "Fictional-Kw-891b1132", "Fictional-Kw-4bc4a6e3", "Fictional-Kw-74303c51",
                     "Fictional-Kw-858a4f75"],
        "weight": 1.0
    },
    "Pagode": {
        "keywords": ["pagode", "Fictional-FrozenBell", "Fictional-IronSignal -", "Fictional-MarbleDrifter",
                     "péricles"],
        "weight": 1.0
    },
    "Pop": {
        "keywords": ["pop", "Fictional-LunarSpire", "Fictional-EmeraldDawn", "Fictional-MistySpark",
                     "Fictional-Kw-2077e4a6", "Fictional-Kw-375591ec", "Fictional-TwilightDrifter",
                     "Fictional-DuskPeak", "Fictional-Kw-0f3147d9"],
        "weight": 0.7
    },
    "PopPunk": {
        "keywords": ["pop punk", "pop-punk", "Fictional-JasperWarden", "Fictional-JasperWarden",
                     "Fictional-ShadowPeak", "Fictional-Kw-e4dcc4b1", "Fictional-ShadowHorizon"],
        "weight": 1.0
    },
    "PostGrunge": {
        "keywords": ["post-grunge", "post grunge", "Fictional-CoralVoyage",
                     "Fictional-QuartzRidge", "Fictional-Kw-b69ed13c",
                     "Fictional-IronMesa", "Fictional-ScarletPrism"],
        "weight": 0.8
    },
    "PowerMetal": {
        "keywords": ["power metal", "Fictional-ScarletHorizon", "Fictional-SolarWarden",
                     "Fictional-FrozenMask", "helloween", "Fictional-Kw-54f511dd",
                     "Fictional-Kw-6704c32f", "Fictional-Kw-e06ca236",
                     "eagleheart", "hunting high"],
        "weight": 1.0
    },
    "ProgressiveRock": {
        "keywords": ["progressive rock", "prog rock", "Fictional-EmeraldRaven",
                     "Fictional-IronHarbor", "Fictional-Kw-289ffeb2", "Fictional-EbonyBloom", "Fictional-Kw-47982c18",
                     "aqualung", "Fictional-Kw-6d712aa9"],
        "weight": 1.0
    },
    "PsychedelicRock": {
        "keywords": ["psychedelic", "Fictional-EbonyBloom", "Fictional-Kw-9ead98be",
                     "Fictional-Kw-635fd34e", "meddle"],
        "weight": 1.0
    },
    "PunkRock": {
        "keywords": ["punk rock", "punk", "Fictional-ShadowPeak", "Fictional-JasperBloom",
                     "the Fictional-TimberFlame", "ramones", "Fictional-AzureMirror",
                     "gone away", "million miles away"],
        "weight": 1.0
    },
    "RnB": {
        "keywords": ["r&b", "rnb", "r'n'b", "Fictional-Kw-74757e7a", "Fictional-Kw-375591ec",
                     "Fictional-IronSignal", "Fictional-IronLantern", "Fictional-MistySpark",
                     "usher", "Fictional-Kw-a9285dfc"],
        "weight": 1.0
    },
    "Rock": {
        "keywords": ["rock"],
        "weight": 0.3
    },
    "Samba": {
        "keywords": ["samba", "Fictional-FrozenBell", "pagode"],
        "weight": 0.8
    },
    "Soul": {
        "keywords": ["soul", "Fictional-LunarSpire", "Fictional-Kw-2077e4a6", "Fictional-OpalWing",
                     "Fictional-Kw-8994337c", "Fictional-IronLantern", "Fictional-Kw-959660ed",
                     "off the wall", "Fictional-Kw-271b8ef8", "Fictional-Kw-aa7f0be7"],
        "weight": 0.8
    },
    "SouthernRock": {
        "keywords": ["southern rock", "Fictional-LunarHorizon", "Fictional-Kw-9a2a444f"],
        "weight": 1.0
    },
    "ThrashMetal": {
        "keywords": ["thrash metal", "Fictional-LunarKnight", "Fictional-BrassCompass",
                     "Fictional-Kw-0925467e", "Fictional-Kw-b7f0e901", "Fictional-Kw-56dc5fa7", "Fictional-Kw-7749bdd4",
                     "Fictional-Kw-5e5601d7", "Fictional-Kw-f0246a90"],
        "weight": 1.0
    },
    "Trance": {
        "keywords": ["trance", "Fictional-RustyRiver", "sandstorm"],
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
                     "Fictional-Kw-a7dd04eb", "Fictional-Kw-c58f91e7", "Fictional-Kw-b7ace6d9"],
        "weight": 1.0
    },
    "Electronic": {
        "keywords": ["electronic", "Fictional-SpectralTower", "synth pop", "synthpop",
                     "born slippy", "the model"],
        "weight": 1.0
    },
    "Classical": {
        "keywords": ["classical", "bach", "cello suite", "concerto",
                     "prelude", "sonata", "Fictional-TimberThorn"],
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

MOOD_KEYWORDS: dict[str, dict[str, Any]] = {
    "Adventurous": {
        "keywords": ["adventure", "quest", "Fictional-Kw-98dc0157", "hero", "dragon",
                     "Fictional-Kw-f4056ced", "Fictional-Kw-a1dc2820",
                     "Fictional-Kw-f9e1d8f3", "dragon force", "fist bump",
                     "Fictional-Kw-9a6359cf", "pirate", "Fictional-AzureShore heroes"],
        "weight": 1.0
    },
    "Aggressive": {
        "keywords": ["aggressive", "rage", "angry", "violent", "heavy",
                     "Fictional-VioletFalcon", "Fictional-SterlingBeacon", "Fictional-TwilightPhoenix",
                     "Fictional-IronMesa", "Fictional-LunarKnight", "Fictional-Kw-5f219c36", "Fictional-Kw-c64f8a77",
                     "Fictional-Kw-891b1132", "Fictional-Kw-858a4f75",
                     "Fictional-Kw-015220a7", "Fictional-Kw-56dc5fa7", "sonne",
                     "Fictional-NeonDawn", "Fictional-JasperBloom",
                     "Fictional-Kw-74303c51", "Fictional-Kw-4bc4a6e3",
                     "Fictional-Kw-ed5d1ab5"],
        "weight": 1.0
    },
    "Ambient": {
        "keywords": ["ambient", "atmospheric", "calm", "peaceful",
                     "relaxing", "rain sounds", "gentle",
                     "korok forest", "Fictional-Kw-b071f324",
                     "Fictional-Kw-5fae0ce6", "Fictional-Kw-a9098f87"],
        "weight": 1.0
    },
    "Chill": {
        "keywords": ["chill", "lo-fi", "lofi", "relaxing", "easy",
                     "smooth", "mellow", "calm", "Fictional-PhantomHorizon",
                     "city pop", "study", "cozy", "rest",
                     "Fictional-Kw-a70a6a9b", "file select"],
        "weight": 1.0
    },
    "Dark": {
        "keywords": ["dark", "sinister", "evil", "shadow", "Fictional-MidnightFrost",
                     "death", "vampire", "dracula", "Fictional-Kw-015220a7",
                     "Fictional-Kw-31861ba7", "Fictional-IronMesa", "Fictional-VioletFalcon",
                     "Fictional-IronMesa", "gothic", "Fictional-EmeraldWarden", "Fictional-Kw-57d292fc",
                     "cyberpunk", "dark angel"],
        "weight": 1.0
    },
    "Emotional": {
        "keywords": ["emotional", "tears", "cry", "feel", "heart",
                     "love", "loss", "Fictional-AzurePhoenix", "Fictional-ZincWing",
                     "Fictional-Kw-625cf4d4", "Fictional-Kw-9cf0e877", "Fictional-Kw-e9783d09",
                     "black official", "linger", "Fictional-Kw-b0c56b8e",
                     "Fictional-Kw-aa7f0be7", "you are not alone",
                     "Fictional-Kw-5ee0843a", "Fictional-Kw-5fae0ce6",
                     "Fictional-Kw-67a914c6"],
        "weight": 1.0
    },
    "Energetic": {
        "keywords": ["energetic", "fast", "power", "high energy",
                     "upbeat", "Fictional-AzureShore", "Fictional-SolarWarden", "Fictional-ScarletHorizon",
                     "Fictional-Kw-6704c32f", "Fictional-Kw-d0dbe915 & learn",
                     "fist bump", "Fictional-Kw-e4dcc4b1", "Fictional-Kw-4bc4a6e3",
                     "my hero", "Fictional-Kw-8f379ecb", "Fictional-JadeFrost",
                     "Fictional-Kw-5e5601d7", "Fictional-ShadowPeak"],
        "weight": 1.0
    },
    "Epic": {
        "keywords": ["epic", "orchestral", "grand", "legendary",
                     "Fictional-Kw-b09ec18c", "Fictional-Kw-b071f324",
                     "Fictional-Kw-f9e1d8f3", "Fictional-Kw-51da3037",
                     "Fictional-Kw-0f060986", "Fictional-Kw-6704c32f",
                     "invincible", "Fictional-Kw-56dc5fa7", "Fictional-Kw-7749bdd4",
                     "Fictional-Kw-46f76d4a", "Fictional-Kw-9a2a444f",
                     "Fictional-Kw-d7fa95a4", "Fictional-Kw-51146ba1",
                     "stormwind", "Fictional-AmberSpark"],
        "weight": 1.0
    },
    "Ethereal": {
        "keywords": ["ethereal", "dreamy", "floating", "heavenly",
                     "Fictional-Kw-17e536b9", "Fictional-Kw-5fae0ce6", "korok forest",
                     "Fictional-Kw-5ee0843a", "song of elune",
                     "Fictional-Kw-1005185b", "Fictional-Kw-84d4d9af",
                     "Fictional-Kw-4ee5643e", "Fictional-Kw-b2412f79",
                     "Fictional-Kw-f5405813", "Fictional-CrimsonFountain", "Fictional-Kw-e4178445",
                     "always with me"],
        "weight": 1.0
    },
    "Introspective": {
        "keywords": ["introspect", "think", "reflect", "quiet",
                     "alone", "self", "Fictional-Kw-a6a3b111", "Fictional-Kw-b2631a42",
                     "Fictional-Kw-625cf4d4", "Fictional-Kw-e9783d09", "black official",
                     "Fictional-Kw-b0c2ac5b", "papercut", "Fictional-Kw-8fd19cd0",
                     "Fictional-Kw-2d455771", "Fictional-EmeraldRaven",
                     "wond'ring aloud", "Fictional-Kw-6d712aa9"],
        "weight": 1.0
    },
    "Melancholic": {
        "keywords": ["melanchol", "sad", "sorrow", "grief", "loss",
                     "lonely", "blue", "tears", "pain",
                     "Fictional-Kw-625cf4d4", "Fictional-Kw-e9783d09", "Fictional-Kw-9cf0e877",
                     "rotten apple", "linger", "Fictional-Kw-5ee0843a",
                     "Fictional-Kw-5fae0ce6", "would?", "black official",
                     "Fictional-Kw-488d4831", "Fictional-Kw-1005185b"],
        "weight": 1.0
    },
    "Mysterious": {
        "keywords": ["mysterious", "mystery", "enigma", "secret",
                     "shadow", "hidden", "Fictional-EmeraldWarden", "Fictional-Kw-a557d8c5",
                     "Fictional-Kw-71bb3f77", "Fictional-Kw-15396039",
                     "Fictional-Kw-a2ce73b7", "twilight stigmata",
                     "sacred grove", "forest"],
        "weight": 1.0
    },
    "Nostalgic": {
        "keywords": ["nostalg", "retro", "classic", "remember", "childhood",
                     "old school", "Fictional-CrystalBell", "Fictional-JadePrism", "Fictional-SapphireOracle",
                     "Fictional-IronSail", "Fictional-ZincGate", "nintendo",
                     "Fictional-MarbleCrown", "Fictional-PhantomWhisper", "snes",
                     "n64", "Fictional-Kw-6b55169c", "title theme",
                     "Fictional-Kw-e958d854", "Fictional-Kw-a70a6a9b"],
        "weight": 1.0
    },
    "Rebellious": {
        "keywords": ["rebel", "anarchy", "protest", "fight", "resist",
                     "Fictional-SterlingBeacon", "Fictional-JasperBloom", "Fictional-ShadowPeak",
                     "punk", "Fictional-Kw-896901cc", "Fictional-Kw-e4dcc4b1",
                     "Fictional-Kw-c027cb5c", "police truck",
                     "Fictional-Kw-8f379ecb", "Fictional-NeonDawn", "Fictional-GraniteCrown"],
        "weight": 1.0
    },
    "Romantic": {
        "keywords": ["romantic", "love", "heart", "kiss", "together",
                     "sweetest", "you are not alone", "Fictional-Kw-aa7f0be7",
                     "Fictional-Kw-693c8131", "human nature",
                     "Fictional-Kw-2891e041", "is this love",
                     "Fictional-Kw-c419453c", "Fictional-Kw-d7995712",
                     "boa sorte", "Fictional-Kw-d74fd249",
                     "Fictional-Kw-0a77c212", "Fictional-Kw-89638e4c", "easy (cooler",
                     "sweet love", "Fictional-Kw-c612457b"],
        "weight": 1.0
    },
    "Triumphant": {
        "keywords": ["triumph", "victory", "glory", "win", "champion",
                     "heroes", "Fictional-Kw-51da3037", "Fictional-Kw-d0dbe915 & learn",
                     "Fictional-Kw-6704c32f", "my hero",
                     "learn to fly", "Fictional-Kw-0f060986",
                     "invincible", "eagleheart"],
        "weight": 1.0
    },
    "Upbeat": {
        "keywords": ["upbeat", "happy", "joy", "fun", "bright",
                     "cheerful", "Fictional-DuskPeak", "Fictional-Kw-885b67ec",
                     "Fictional-Kw-fcf2483c", "off the wall", "Fictional-Kw-271b8ef8",
                     "Fictional-Kw-97d2827f", "Fictional-Kw-e4dcc4b1", "Fictional-Kw-ef7e483f",
                     "Fictional-Kw-8f379ecb", "my hero", "learn to fly",
                     "Fictional-Kw-52f26298", "Fictional-Kw-f8f26e59",
                     "Fictional-Kw-71cb705f", "Fictional-AzureShore heroes"],
        "weight": 1.0
    },
    # New moods
    "Serene": {
        "keywords": ["serene", "peaceful", "tranquil", "gentle",
                     "lullaby", "Fictional-CrystalBell's lullaby", "sakura",
                     "always with me", "Fictional-Kw-390fd18a",
                     "Fictional-Kw-64f42d05", "Fictional-Kw-b1be5870",
                     "Fictional-Kw-9c820265", "guzheng", "guqin",
                     "koto", "gayageum", "zither"],
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

    result: dict[str, list[str]] = {"artists": [], "genres": [], "moods": []}

    # --- Artist Classification (Naive Bayes: P(artist|keywords)) ---
    for artist, keywords in ARTIST_KEYWORDS.items():
        score: int = 0
        for kw in keywords:
            kw_l = kw.lower()
            if kw_l in name_clean or kw_l.replace(' ', '') in name_nospace:
                score += 1
        if score > 0:
            result["artists"].append(artist)

    # --- Genre Classification (Random Forest voting: keyword + artist features) ---
    for genre, genre_data in GENRE_KEYWORDS.items():
        genre_score: float = 0.0
        for kw in genre_data["keywords"]:
            if kw.lower() in name_clean:
                genre_score += genre_data["weight"]
        # Boost from artist membership (k-NN: similar artists → similar genres)
        artist_genre_boost = {
            "Grunge": ["Fictional-ZincWing", "Fictional-AzurePhoenix", "Fictional-ShadowPhoenix"],
            "NuMetal": ["Fictional-ThistleGate", "Fictional-SterlingBeacon", "Fictional-VioletFalcon", "Fictional-TwilightPhoenix",  # noqa: E501
                        "Fictional-SmokySummit"],
            "Metalcore": ["Fictional-ScarletCanyon", "Fictional-SterlingLotus"],
            "AlternativeMetal": ["Fictional-QuartzPeak", "Fictional-IronMesa"],
            "PostGrunge": ["Fictional-CoralVoyage", "Fictional-QuartzRidge", "Fictional-ScarletPrism", "Fictional-ZincWing"],  # noqa: E501
            "HardRock": ["Fictional-GraniteCastle", "Fictional-GlassCastle", "Fictional-CrimsonFrost", "Fictional-ObsidianCastle",  # noqa: E501
                         "Fictional-BrassTide", "Fictional-JasperHorizon", "Fictional-MistyStrand", "Fictional-FadingGarden",  # noqa: E501
                         "Fictional-AzureSpire", "Fictional-ThistleShield"],
            "ProgressiveRock": ["Fictional-EmeraldRaven", "Fictional-IronHarbor", "Fictional-Kw-289ffeb2", "Fictional-EbonyBloom",  # noqa: E501
                                "Fictional-QuartzChain", "Fictional-BlazingCastle", "Fictional-SterlingQuarry", "Fictional-QuartzStrand"],  # noqa: E501
            "PunkRock": ["Fictional-JasperBloom", "Fictional-TimberFlame", "Fictional-ShadowPeak", "Fictional-AzureMirror"],  # noqa: E501
            "PopPunk": ["Fictional-JasperWarden", "Fictional-ShadowPeak", "Fictional-ShadowHorizon"],
            "HeavyMetal": ["Fictional-RustyMask", "Fictional-BrassCompass", "Fictional-LunarKnight", "Fictional-FadingGarden",  # noqa: E501
                           "DarkAngelMetal", "CyberpunkBeats", "EgyptianMetal"],
            "ThrashMetal": ["Fictional-BrassCompass", "Fictional-LunarKnight"],
            "PowerMetal": ["Fictional-ScarletHorizon", "Fictional-SolarWarden", "Fictional-FrozenMask"],
            "IndustrialMetal": ["Fictional-IronMesa", "Fictional-SmokySummit"],
            "BrazilianRock": ["Fictional-EmeraldBloom", "Fictional-NeonDawn", "Fictional-ZincCipher",
                              "Fictional-CobaltOracle", "Fictional-FrozenNeedle", "Fictional-GraniteCrown", "Fictional-EmeraldMesa",  # noqa: E501
                              "Fictional-VioletHelix"],
            "CityPop": ["Fictional-FadingHelix", "Fictional-ThunderTide", "Fictional-CobaltRiver", "Fictional-SapphireSpire",  # noqa: E501
                        "Fictional-AzurePrism", "Fictional-GraniteCompass"],
            "MPB": ["Fictional-ScarletPrism", "Fictional-VolcanicHorn", "Fictional-SapphireHaven", "Fictional-PhantomMirror",  # noqa: E501
                    "Fictional-ScarletPrism"],
            "Pagode": ["Fictional-IronSignal", "Fictional-FrozenBell"],
            "FolkMetal": ["Fictional-VolcanicSignal", "Fictional-JadeFrost", "Fictional-ScarletSwan", "PirateMetal"],
            "FolkRock": ["Fictional-LunarCanyon", "Fictional-CobaltSignal", "Fictional-VioletGarden", "Fictional-MarbleBloom", "Fictional-SterlingJewel"],  # noqa: E501
            "MedievalFolk": ["Fictional-LunarCanyon"],
            "ClassicRock": ["Fictional-TimberNeedle", "Fictional-LunarHorizon", "Fictional-IvorySignal",
                            "Fictional-EmeraldRaven", "Fictional-GlassCastle", "Fictional-ThunderSpire",
                            "Fictional-BrassTide", "Fictional-MistyStrand", "Fictional-CobaltSignal", "Fictional-GraniteRiver",  # noqa: E501
                            "Fictional-StormMoon", "Fictional-StormQuarry", "Fictional-JasperHorizon", "Fictional-VioletGarden",  # noqa: E501
                            "Fictional-NeonPillar", "Fictional-IndigoSummit", "Fictional-MarbleBloom",
                            "Fictional-CrimsonCrown", "Fictional-ObsidianPrism", "Fictional-CrimsonScholar", "Fictional-EbonyBell",  # noqa: E501
                            "Fictional-EbonyVoyage", "Fictional-QuartzChain", "Fictional-SterlingJewel", "Fictional-SmokySpark",  # noqa: E501
                            "Fictional-OpalDrifter", "Fictional-ThunderIsle", "Fictional-VelvetLantern",
                            "Fictional-SpectralTower", "Fictional-ThunderChain", "Fictional-SterlingQuarry",
                            "Fictional-BlazingCastle", "Fictional-ScarletGlacier", "Fictional-SapphireNeedle",
                            "Fictional-ScarletWhisper", "Fictional-ThistleShield"],
            "AlternativeRock": ["Fictional-ScarletPrism", "Fictional-MarbleRose", "Fictional-ThunderGhost",
                                "Fictional-TimberStone", "Fictional-FrozenWing", "Fictional-ShadowHorizon",
                                "Fictional-ShadowPhoenix", "Fictional-TimberDawn", "Fictional-PhantomRaven", "Fictional-AmberBell",  # noqa: E501
                                "Fictional-Kw-270c1b08", "Fictional-SmokySpark", "Fictional-SterlingThorn", "Fictional-GraniteShore"],  # noqa: E501
            "GothicMetal": ["Fictional-IronMesa"],
            "AnimeOST": ["Fictional-Jozep", "Fictional-SterlingGate", "Fictional-LunarChain", "Fictional-ObsidianFalcon",  # noqa: E501
                         "Fictional-EmeraldTrail", "Fictional-MidnightBell", "Fictional-EbonyBeacon"],
            "GameOST": ["Fictional-ZincGate", "Fictional-CrystalBell", "Fictional-AzureShore", "Fictional-JadePrism",
                        "Fictional-SapphireOracle", "Fictional-EmeraldWarden", "Fictional-MidnightSpire", "Fictional-ThistleOrchid",  # noqa: E501
                        "Fictional-BrassHorizon", "Fictional-SolarIsle", "Fictional-IronSail", "Fictional-EmeraldFlame",
                        "Fictional-BrassWhisper", "Fictional-MidnightFrost", "Fictional-MarbleCrown", "Fictional-PhantomWhisper",  # noqa: E501
                        "Fictional-VidaSimu", "Fictional-CoralForge", "Fictional-RustyMirror"],
            "FilmOST": ["Fictional-AmberSpark", "Fictional-VioletStone", "Fictional-CrimsonFountain"],
            "Soul": ["Fictional-LunarSpire", "Fictional-IronLantern", "Fictional-OpalWing",
                     "Fictional-CrimsonWhisper", "Fictional-TwilightSpark", "Fictional-FrozenCrown",
                     "Fictional-IronPrism"],
            "Pop": ["Fictional-LunarSpire", "Fictional-DuskPeak", "Fictional-EmeraldDawn", "Fictional-MistySpark",
                    "Fictional-TwilightDrifter", "Fictional-Kw-e407c5d8", "Fictional-BrassHorizon", "Fictional-LunarDrifter",  # noqa: E501
                    "Fictional-SolarWarden", "Fictional-ThunderPrism", "Fictional-TimberRidge",
                    "Fictional-FadingIsle", "Fictional-DuskLantern", "Fictional-GoldenLantern", "Fictional-AmberBell",
                    "Fictional-BrassSpire", "Fictional-VolcanicLotus", "Fictional-CoralCanyon", "Fictional-ThistleLeaf",
                    "Fictional-TimberDawn", "Fictional-ScarletBell", "Fictional-EbonySpark", "Fictional-GildedFrost"],
            "HardcorePunk": ["Fictional-NeonDawn", "Fictional-JasperBloom"],
            "Funk": ["Fictional-GraniteMirror", "Fictional-CrimsonWhisper", "Fictional-AmberVeil"],
            "Disco": ["Fictional-DuskPeak", "Fictional-SmokyPrism", "Fictional-RustyRiver",
                      "Fictional-AmberVeil", "Fictional-ThistleLeaf"],
            "JPop": ["Fictional-NeonShore", "Fictional-FadingHelix", "Fictional-ThunderTide", "Fictional-EbonyBeacon", "Fictional-CrystalCipher",  # noqa: E501
                     "Fictional-SapphireSpire", "Fictional-EmeraldTrail"],
            "KPop": ["Fictional-NeonShore"],
            "TraditionalJapanese": ["Koto"],
            "TraditionalKorean": ["Gayageum"],
            "TraditionalChinese": ["Guzheng", "Guqin"],
            "Orchestral": ["Fictional-AmberSpark", "Fictional-VioletStone", "Fictional-CrimsonFountain"],
            "RnB": ["Fictional-IronSignal", "Fictional-Kw-e407c5d8", "Fictional-MistySpark", "Fictional-IronLantern", "Fictional-NeonShore",  # noqa: E501
                    "Fictional-GildedFalcon", "Fictional-AzureRaven", "Fictional-TwilightSpark",
                    "Fictional-IronPrism", "Fictional-EbonySpark", "Fictional-DuskPhoenix"],
            "SouthernRock": ["Fictional-LunarHorizon"],
            "Emo": ["Fictional-EbonyFlame"],
            "FunkRock": ["Fictional-SilverLighthouse"],
            "Britpop": ["Fictional-JasperIsle"],
            "HipHop": ["Fictional-IronIsle", "Fictional-PhantomHorizon", "Fictional-DuskPhoenix"],
            "JazzFusion": ["Fictional-PhantomLighthouse", "Fictional-CoralLighthouse", "Fictional-FrozenCrown", "Fictional-EbonyBell",  # noqa: E501
                           "Fictional-ThunderNest", "NotTooJazzy", "Fictional-FrozenStrand'"],
            "RockAndRoll": ["Fictional-ShadowThorn", "Fictional-ThunderSpire"],
            "Electronic": ["Fictional-SpectralTower", "Fictional-ObsidianRiver"],
            "Classical": ["Fictional-TimberThorn"],
            "DarkAmbient": ["DarkGoddess"],
            "WorldMusic": ["EgyptianBattle"],
        }
        if genre in artist_genre_boost:
            for a in result["artists"]:
                if a in artist_genre_boost[genre]:
                    genre_score += 0.8
        if genre_score >= 0.7:
            result["genres"].append(genre)

    # --- Mood Classification (ensemble voting) ---
    for mood, mood_data in MOOD_KEYWORDS.items():
        mood_score: float = 0.0
        for kw in mood_data["keywords"]:
            if kw.lower() in name_clean:
                mood_score += mood_data["weight"]
        if mood_score >= 0.8:
            result["moods"].append(mood)

    # Ensure at least one classification
    if not result["artists"]:
        result["artists"].append("Various")
    if not result["genres"]:
        # Try to infer from artist
        for a in result["artists"]:
            if a in ["Fictional-ScarletPrism", "Fictional-VolcanicHorn", "Fictional-SapphireHaven"]:
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
            if fn.endswith(".mp3"):
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
    print("  Using Naive BaFictional-IronHarbor+ k-NN + Random Forest ensemble")
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
