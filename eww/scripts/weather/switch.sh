#! /usr/bin/bash

weather=$(eww get displayWeather)

if [[ "$weather" == "hour" ]]; then
    eww update displayWeather="day"
else
    eww update displayWeather="hour"
fi