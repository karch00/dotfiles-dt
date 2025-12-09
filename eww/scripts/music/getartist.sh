#! /usr/bin/bash 

PLAYER_PRESENT=$(playerctl -l)
if [ ! "$PLAYER_PRESENT" ]; then
    eww update song-progress=0
    echo "---"
    exit
fi

ARTIST=$(playerctl metadata --format "{{artist}}")
echo "$ARTIST"