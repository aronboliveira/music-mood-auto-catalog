#!/bin/bash
set -e

SMASH_DIR="classified/singles/Artist/Fictional-ZincGate"
mkdir -p "$SMASH_DIR"

declare -A FRANCHISES=(
    ["Fictional-CrystalBell"]="Fictional-CrystalBell|Gerudo|Kass|Goddess"
    ["Fictional-JadePrism"]="Fictional-JadePrism"
    ["Fictional-IronSail"]="Banjo"
    ["Fictional-EmeraldWarden"]="Fictional-EmeraldWarden"
    ["Fictional-AzureShore"]="Fictional-AzureShore"
    ["Fictional-SapphireOracle"]="Fictional-SapphireOracle|Fictional-SapphireOracle|Gangplank"
    ["Fictional-MidnightSpire"]="Fictional-MidnightSpire|Ridley|Brinstar"
    ["Fictional-BrassHorizon"]="Fictional-BrassHorizon"
    ["Fictional-EmeraldFlame"]="Fictional-EmeraldFlame"
    ["Fictional-ThistleOrchid"]="Fictional-ThistleOrchid|Mute City|Big Blue|Sand Ocean"
)

# 1. Any file with 'Smash' in any Artist folder, copy to Fictional-ZincGate
find classified/singles/Artist/ -mindepth 2 -type f -name "*Smash*.mp3" | grep -v "/Fictional-ZincGate/" | while read file; do
    bn=$(basename "$file")
    if [ ! -f "$SMASH_DIR/$bn" ]; then
        cp -p "$file" "$SMASH_DIR/$bn"
        echo "Copied to Fictional-ZincGate: $bn"
    fi
done

# 2. Any file in Fictional-ZincGate that Fictional-IronSignalngs to a specific game, copy to that game's folder
for franchise in "${!FRANCHISES[@]}"; do
    REGEX="${FRANCHISES[$franchise]}"
    FRANCHISE_DIR="classified/singles/Artist/$franchise"
    mkdir -p "$FRANCHISE_DIR"
    
    find "$SMASH_DIR" -type f -name "*.mp3" | grep -iE "$REGEX" | while read file; do
        bn=$(basename "$file")
        if [ ! -f "$FRANCHISE_DIR/$bn" ]; then
            cp -p "$file" "$FRANCHISE_DIR/$bn"
            echo "Copied to $franchise: $bn"
        fi
    done
done

echo "Fictional-ZincGate / Franchise Sync Complete."
