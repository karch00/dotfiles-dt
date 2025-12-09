#! /usr/bin/bash

PLAYER_PRESENT=$(playerctl -l)
if [ ! "$PLAYER_PRESENT" ]; then
    echo "00:00"
    exit
fi

CURRENT_LENGTH=$(playerctl position)
CURRENT_LENGTH=$( printf "%0.f" "$CURRENT_LENGTH" )

CURRENT_MINS=$(("$CURRENT_LENGTH"/60))
if [ "$CURRENT_MINS" -lt 10 ]; then
    CURRENT_MINS="0$CURRENT_MINS"
fi
CURRENT_SECONDS=$(("$CURRENT_LENGTH"%60))
if [ "$CURRENT_SECONDS" -lt 10 ]; then
    CURRENT_SECONDS="0$CURRENT_SECONDS"
fi

echo "$CURRENT_MINS":"$CURRENT_SECONDS"