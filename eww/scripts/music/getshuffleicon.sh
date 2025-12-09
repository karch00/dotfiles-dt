#! /usr/bin/bash

PLAYER_PRESENT=$(playerctl -l)
if [ ! "$PLAYER_PRESENT" ]; then
    echo ""
    exit
fi

SHUFFLE=$(playerctl shuffle)
if [ "$SHUFFLE" == "On" ]; then
    echo "󰒟"
else
    echo "󰒞"
fi