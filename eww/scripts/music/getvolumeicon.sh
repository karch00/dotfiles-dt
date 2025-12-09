#! /usr/bin/bash

PLAYER_PRESENT=$(playerctl -l)
if [ ! "$PLAYER_PRESENT" ]; then
    echo "0"
    exit
fi

OFF=""
LOW=""
MID=""
HIGH=""

VOLUME=$( bc <<< "$(playerctl volume) * 100" )
VOLUME=$(printf "%.0f" "$VOLUME")
if (( VOLUME == 0 )); then
    echo "$OFF"
elif (( VOLUME <= 33 )); then
    echo "$LOW"
elif (( VOLUME <= 55 )); then
    echo "$MID"
else
    echo "$HIGH"
fi