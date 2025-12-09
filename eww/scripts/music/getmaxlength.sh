#! /usr/bin/bash

PLAYER_PRESENT=$(playerctl -l)
if [ ! "$PLAYER_PRESENT" ]; then
    echo "0"
    exit
fi

MAX=$(playerctl metadata --format "{{mpris:length}}")
MAX=$(("$MAX"/1000000))

echo -n "$MAX"