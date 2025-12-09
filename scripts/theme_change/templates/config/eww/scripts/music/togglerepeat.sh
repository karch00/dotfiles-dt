#! /usr/bin/bash

PLAYER_PRESENT=$(playerctl -l)
if [ ! "$PLAYER_PRESENT" ]; then
    exit
fi

CURRENT_REPEAT=$(playerctl loop)
if [ "$CURRENT_REPEAT" == "None" ]; then
    playerctl loop "Playlist"
    echo 1
elif [ "$CURRENT_REPEAT" == "Playlist" ]; then
    playerctl loop "Track"
    echo 2
elif [ "$CURRENT_REPEAT" == "Track" ]; then
    playerctl loop "None"
    echo 3
fi
