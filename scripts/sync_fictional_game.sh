#!/bin/bash
set -e

SMASH_DIR="classified/singles/Artist/FictionalGame"
mkdir -p "$SMASH_DIR"

declare -A FRANCHISES=(
    ["Zelda"]="Zelda|Gerudo|Kass|Goddess"
    ["Mario"]="Mario"
    ["BanjoKazooie"]="Banjo"
    ["Castlevania"]="Castlevania"
    ["Sonic"]="Sonic"
    ["DonkeyKong"]="Donkey Kong|DKC|Gangplank"
    ["Metroid"]="Metroid|Ridley|Brinstar"
    ["FictionalGame"]="FictionalGame"
    ["Bayonetta"]="Bayonetta"
    ["FZero"]="F-Zero|Mute City|Big Blue|Sand Ocean"
)

# 1. Any file with 'Smash' in any Artist folder, copy to FictionalGame
find classified/singles/Artist/FictionalBand - rock-song-449d87.mp3" | grep -v "/FictionalGame/" | while read file; do
    bn=$(basename "$file")
    if [ ! -f "$SMASH_DIR/$bn" ]; then
        cp -p "$file" "$SMASH_DIR/$bn"
        echo "Copied to FictionalGame: $bn"
    fi
done

# 2. Any file in FictionalGame that belongs to a specific game, copy to that game's folder
for franchise in "${!FRANCHISES[@]}"; do
    REGEX="${FRANCHISES[$franchise]}"
    FRANCHISE_DIR="classified/singles/Artist/$franchise"
    mkdir -p "$FRANCHISE_DIR"
    
FictionalBand - rock-song-908a80.mp3" | grep -iE "$REGEX" | while read file; do
        bn=$(basename "$file")
        if [ ! -f "$FRANCHISE_DIR/$bn" ]; then
            cp -p "$file" "$FRANCHISE_DIR/$bn"
            echo "Copied to $franchise: $bn"
        fi
    done
done

echo "FictionalGame / Franchise Sync Complete."
