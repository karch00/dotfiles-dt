#!/bin/bash

# Get initial state
hyprctl monitors -j | jq -c '[.[] | .activeWorkspace.id]'

# Listen to Hyprland events and update on workspace changes
hyprctl --batch "$(hyprctl monitors -j | jq -r '.[].id' | xargs -I{} echo "dispatch focusmonitor {}")" 2>/dev/null

# Use stdbuf to disable buffering
socat -u UNIX-CONNECT:$XDG_RUNTIME_DIR/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock - | 
  stdbuf -oL grep --line-buffered -E "workspace>>|focusedmon>>" | 
  while read -r line; do
    hyprctl monitors -j | jq -c '[.[] | .activeWorkspace.id]'
  done
