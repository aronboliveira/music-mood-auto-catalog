#!/bin/bash
set -e

# Singles
mv "classified/singles/Artist/Fictional-LunarSpire/Fictional-Track-4a46d43c.mp3" "classified/singles/Artist/Fictional-AzurePhoenix/" 2>/dev/null || true
mv classified/singles/Artist/Fictional-LunarSpire/Fictional-Kw-990c5767-*.mp3 "classified/singles/Artist/Fictional-AzurePhoenix/" 2>/dev/null || true
mv "classified/singles/Artist/Fictional-CrystalCipher/Fictional-Track-1b51c91Fictional-Track-eccbc87e.mp3" "classified/singles/Artist/Fictional-EmeraldRaven/" 2>/dev/null || true
mv "classified/singles/Artist/Fictional-CrystalCipher/Fictional-Track-adf1edbe.mp3" "classified/singles/Artist/Fictional-TimberNeedle/" 2>/dev/null || true

# Albums - move back from Various to proper Artist folders
declare -A ALBUM_MOVES=(
    ["*Fictional-Kw-efa19b51*"]="Fictional-Kw-47f3a013"
    ["*Fictional-Kw-74757e7a*"]="Fictional-Kw-29262247"
    ["Fragile-Fictional-IronHarbor*"]="Fictional-IronHarbor"
    ["Fictional-Kw-289ffeb2*"]="Fictional-Kw-289ffeb2"
    ["Fictional-Kw-98dc0157*"]="Fictional-Kw-98dc0157"
    ["Fictional-Kw-d66b4bd5*"]="Fictional-Kw-2e1bb15f"
    ["Fictional-PhantomHorizon*"]="Fictional-PhantomHorizon"
    ["Fictional-Kw-0f3147d9*"]="Fictional-Kw-e5ed2409"
    ["Fictional-Kw-96344f5c*"]="Fictional-EbonyBloom"
    ["Fictional-Kw-635fd34e*Fictional-Kw-96344f5c*"]="Fictional-EbonyBloom"
    ["Fictional-Kw-2077e4a6*"]="Fictional-ZincNeedle"
    ["Fictional-IvoryLighthouse*"]="Fictional-IvoryLighthouse"
    ["Fictional-MarbleRose*"]="Fictional-MarbleRose"
    ["R-E-M-*"]="Fictional-MarbleRose"
    ["Fictional-Kw-ac99b7e5*"]="Fictional-Kw-e407c5d8"
    ["Fictional-Kw-0f63b2c0*"]="Fictional-Kw-0f63b2c0"
    ["Fictional-Kw-061d5554*"]="Fictional-SterlingBeacon"
    ["*CYBERPUNK*"]="CyberpunkBeats"
    ["*EGYPTIAN*"]="EgyptianMetal"
    ["*PIRATE*"]="PirateMetal"
    ["*Dark-Angel-Metal*"]="DarkAngelMetal"
    ["*Medieval-Music*"]="MedievalAmbience"
    ["*Nintendo*"]="Nintendo"
    ["*N64*"]="Nintendo"
)

for pattern in "${!ALBUM_MOVES[@]}"; do
    dest="${ALBUM_MOVES[$pattern]}"
    # Create dir if not exists
    mkdir -p "classified/albums/Artist/$dest"
    
    # Enable nullglob to safely loop through matches
    shopt -s nullglob
    for file in classified/albums/Artist/Various/$pattern; do
        echo "Moving album: $file -> classified/albums/Artist/$dest/"
        mv "$file" "classified/albums/Artist/$dest/"
    done
    shopt -u nullglob
done

echo "Obvious misclassifications moved successfully."
