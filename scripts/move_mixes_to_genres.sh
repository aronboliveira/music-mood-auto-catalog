#!/bin/bash
set -e

mkdir -p "classified/albums/Genre/CityPop"
mkdir -p "classified/albums/Genre/DnB"
mkdir -p "classified/albums/Genre/GameOST"

declare -A MIX_MOVES=(
    ["*City-Pop*"]="CityPop"
    ["*CITY-POP*"]="CityPop"
    ["*JAPANESE-CITY-POP*"]="CityPop"
    ["*japanese-city-pop*"]="CityPop"
    ["*jungle-mix*"]="DnB"
    ["*Jungle-Mix*"]="DnB"
    ["*nintendo-music*"]="GameOST"
)

shopt -s nullglob
for pattern in "${!MIX_MOVES[@]}"; do
    genre="${MIX_MOVES[$pattern]}"
    
    for file in classified/albums/Artist/Various/$pattern; do
        echo "Moving to Genre: $file -> classified/albums/Genre/$genre/"
        mv "$file" "classified/albums/Genre/$genre/"
    done
done
shopt -u nullglob

echo "Mixes moved to Genres successfully."
