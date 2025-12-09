#! /usr/bin/bash

PLAYER_PRESENT=$(playerctl -l)
if [ ! "$PLAYER_PRESENT" ]; then
    echo 0
    exit
fi

CURRENT_LENGTH=$(playerctl position)
echo "$CURRENT_LENGTH"