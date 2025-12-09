#! /usr/bin/python
import pathlib
import json
import time

WEATHER_FILE = f"{pathlib.Path.home()}/.scripts/weatherfetch/weather.json"
ICON_MAP = {
    0: [" 󰖙", " 󰖔"],
    
    1: [" 󰖙", " 󰖔"],
    2: ["󰖕", "󰼱"],
    3: ["󰖐"],

    45: ["󰖑"],
    48: ["󰼰"],

    51: ["󰼳"],
    53: ["󰼳"],
    55: ["󰼳"],

    56: ["󰙿"],
    57: ["󰙿"],

    61: ["󰖗"],
    63: ["󰖗"],
    65: ["󰖖"],

    66: ["󰙿"],
    67: ["󰙿"],

    71: ["󰖘"],
    73: ["󰖘"],
    75: ["󰼶"],

    77: ["󰼶"],

    80: ["󰖗"],
    81: ["󰖗"],
    82: ["󰖖"],

    85: ["󰖘"],
    86: ["󰼶"],

    95: ["󰙾"],

    96: ["󰖒"],
    99: ["󰖒"]
}

def getWeatherJson(filepath: str) -> dict:
    """Returns data read from json

    Params:
    - filepath(str): Json file path 

    Returns:
    - dict: data retrieved
    """
    with open(file=filepath, mode="r", encoding="utf-8") as f:
        return json.load(fp=f)

def getIconIndex(daily_sunrise: list, daily_sunset: list) -> int:
    """Gets the icon index depending on if day or night

    Params:
    - daily_sunrise(list): list of daily sunrise unix timestamps
    - daily_sunset(list): list of daily sunset unix timestamps

    Returns:
    - int: index
    """
    current_time = time.time()
    sunrise = daily_sunrise[0]
    sunset = daily_sunset[0]

    if current_time > sunrise and current_time < sunset:
        return 0
    else:
        return 1

def getHourlyFirstIndex(hourly: dict) -> int:
    """Gets the first index to use on hourly data.

    Params:
    - hourly(dict): Complete daily data

    Returns:
    - int: first index to use
    """
    timelist = hourly["time"]
    current_time = time.time()
    for idx in range(0, len(timelist)):
        if current_time < timelist[idx]:
            return idx
    return 0

def getHourlyInfo(hourly: dict, daily: dict) -> list:
    """Gets the first 7 entries of the hourly dataset to be presented

    Params:
    - hourly(dict): Complete hourly data
    - daily(dict): Complete daily data, needed for icon

    Returns:
    - list: list of hourly data, from n (1h after) to n+6 (6h after)
    """
    global ICON_MAP

    starting_idx = getHourlyFirstIndex(hourly=hourly)
    toreturn = []
    for idx in range(starting_idx, starting_idx+6):
        timestamp = hourly["time"][idx]
        temp = hourly["temperature_2m"][idx]
        code = hourly["weather_code"][idx]
        wind = hourly["wind_speed_10m"][idx]
        precipitation_chance = hourly["precipitation_probability"][idx]
        rain = hourly["rain"][idx]
        snow = hourly["snowfall"][idx]

        sunset = daily["sunset"]
        sunrise = daily["sunrise"]
        icon = ICON_MAP[code][getIconIndex(sunrise, sunset)] if code in [0, 1, 2] else ICON_MAP[code][0]

        toreturn.append({
            "time": time.strftime("%H:%M", time.localtime(timestamp)),
            "icon": icon,
            "temperature_2m": int(temp), 
            "wind_speed_10m": int(wind), 
            "precipitation_probability": int(precipitation_chance), 
            "rain": int(rain), 
            "snowfall": int(snow)
        })

    return toreturn

def getDailyInfo(daily: dict) -> list:
    """Maps each day's weather to its respective data

    Params:
    - daily(dict): Complete daily data

    Returns:
    - list: list of daily data
    """
    global ICON_MAP

    toreturn = []
    for idx in range(0, 7):
        timestamp = daily["time"][idx]
        code = daily["weather_code"][idx]
        temp_min = daily["temperature_2m_min"][idx]
        temp_max = daily["temperature_2m_max"][idx]
        wind = daily["wind_speed_10m_max"][idx]
        precipitation_chance = daily["precipitation_probability_max"][idx]
        rain = daily["rain_sum"][idx]
        snow = daily["snowfall_sum"][idx]
        
        icon = ICON_MAP[code][0]

        toreturn.append({
            "time": time.strftime("%A", time.localtime(timestamp))[:3] if idx != 0 else time.strftime("%A", time.localtime(timestamp)),
            "icon": icon,
            "temperature_2m_min": int(temp_min),
            "temperature_2m_max": int(temp_max),
            "wind_speed_10m_max": int(wind),
            "precipitation_probability_max": int(precipitation_chance),
            "rain_sum": int(rain),
            "snowfall_sum": int(snow),
        })
    
    return toreturn



def main() -> None:
    jsondata = getWeatherJson(WEATHER_FILE)
 
    current = jsondata["current"]
    current["time"] = time.strftime("%H:%M", time.localtime(current["time"]))
    current["temperature_2m"] = int(current["temperature_2m"])
    current["wind_speed_10m"] = int(current["wind_speed_10m"])
    current["precipitation"] = int(current["precipitation"])
    current["rain"] = int(current["rain"])
    current["snowfall"] = int(current["snowfall"])
    
    sunset = jsondata["daily"]["sunset"]
    sunrise = jsondata["daily"]["sunrise"]
    current["icon"] = ICON_MAP[current["weather_code"]][getIconIndex(sunrise, sunset)] if current["weather_code"] in [0, 1, 2] else ICON_MAP[current["weather_code"]][0]

    hourly = getHourlyInfo(jsondata["hourly"], jsondata["daily"])
    daily = getDailyInfo(jsondata["daily"])

    print(json.dumps({
        "current": current,
        "hourly": hourly,
        "daily": daily
    }))

if __name__ == "__main__":
    main()
