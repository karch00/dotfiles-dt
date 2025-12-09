#! /usr/bin/bash

PLAYER_PRESENT=$(playerctl -l)
if [ ! "$PLAYER_PRESENT" ]; then
    echo "󰑖"
    exit
fi

REPEAT=$(playerctl loop)
if [ "$REPEAT" == "None" ]; then
    echo "󰑗"
elif [ "$REPEAT" == "Track" ]; then
    echo "󰑘"
else
    echo "󰑖"
fi
