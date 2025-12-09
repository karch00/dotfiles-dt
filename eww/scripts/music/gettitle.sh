#! /usr/bin/bash

PLAYER_PRESENT=$(playerctl -l)
if [ ! "$PLAYER_PRESENT" ]; then
    eww update song-progress=0
    echo "No song playing"
    exit
fi

TITLE=$(playerctl metadata --format "{{title}}")
echo "$TITLE"