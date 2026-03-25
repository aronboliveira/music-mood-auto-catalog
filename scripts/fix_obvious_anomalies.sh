#!/bin/bash
set -e

# Singles
mv "classified/singles/Artist/MichaelJackson/FictionalBand - rock-song-aad349.mp3" "classified/singles/Artist/PearlJam/" 2>/dev/null || true
mv classified/singles/Artist/MichaelJackson/FictionalBand - rock-song-875c60.mp3 "classified/singles/Artist/PearlJam/" 2>/dev/null || true
mv "classified/singles/Artist/YUI/FictionalBand - rock-song-2d3490.mp3" "classified/singles/Artist/JethroTull/" 2>/dev/null || true
mv "classified/singles/Artist/YUI/FictionalBand - rock-song-d36e5c.mp3" "classified/singles/Artist/DireStraits/" 2>/dev/null || true

# Albums - move back from Various to proper Artist folders
declare -A ALBUM_MOVES=(
    ["*Summer-Eletrohits*"]="SummerEletrohits"
    ["*Ne-Yo*"]="NeYo"
    ["Fragile-Yes*"]="Yes"
    ["Genesis*"]="Genesis"
    ["Journey*"]="Journey"
    ["Ls-Jack*"]="LsJack"
    ["Nujabes*"]="Nujabes"
    ["Phil-Collins*"]="PhilCollins"
    ["Pink-Floyd*"]="PinkFloyd"
    ["Shine-On-You-Crazy-Diamond*Pink-Floyd*"]="PinkFloyd"
    ["PRINCE*"]="Prince"
    ["Queen*"]="Queen"
    ["R.E.M.*"]="REM"
    ["R-E-M-*"]="REM"
    ["Sam-Smith*"]="SamSmith"
    ["Scorpions*"]="Scorpions"
    ["System-of-a-Down*"]="SystemOfADown"
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
