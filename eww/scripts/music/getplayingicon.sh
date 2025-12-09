#! /usr/bin/bash

PLAYER_PRESENT=$(playerctl -l)
if [ ! "$PLAYER_PRESENT" ]; then
    echo ""
    exit
fi

STATUS=$(playerctl status)
if [ "$STATUS" == "Playing" ]; then
    echo ""
else
    echo ""
fi