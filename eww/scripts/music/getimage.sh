#! /usr/bin/bash

PLAYER_PRESENT=$(playerctl -l)
if [ ! "$PLAYER_PRESENT" ]; then
    echo "music_placeholder.png"
    exit
fi

TITLE=$(playerctl metadata --format "{{title}}{{artist}}")
PREVIOUS_TITLE=$"cat ./last_song"
if [[ "$TITLE" != "$PREVIOUS_TITLE" ]]; then
    echo "$TITLE" > "./last_song"

    IMAGE=$(playerctl metadata --format "{{mpris:artUrl}}") 
    curl "$IMAGE" > "./music"
    
    echo "music"
fi