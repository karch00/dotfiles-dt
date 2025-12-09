import os
import json
import requests
import socket
import time
import pathlib

SESSION = requests.Session()
GEOLOCATION_URL = "https://api.ipbase.com/v2/info"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast?latitude=%%LAT%%&longitude=%%LON%%&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max,rain_sum,snowfall_sum,weather_code,sunrise,sunset&hourly=temperature_2m,precipitation_probability,rain,wind_speed_10m,snowfall,weather_code&current=temperature_2m,precipitation,rain,snowfall,wind_speed_10m,weather_code&timezone=Europe%2FBerlin&timeformat=unixtime"
WEATHER_FILE = f"{pathlib.Path.home()}/.scripts/weatherfetch/weather.json"
DEFAULT_TEMPLATE = {
    "updated": 0,
    "data": None,
}

def internetAvailable() -> bool:
    """Checks for internet connexion by pinging cloudflare DNS"""
    try:
        socket.create_connection(("1.1.1.1", 53)).close()
        return True
    except Exception:
        return False

def getGeolocation(url : str) -> tuple:
    """Gets geolocation from current ip 
    
    Params:
    - url(str): API url

    Returns:
    - tuple: langitude, longitude
    """
    req = SESSION.get(url)
    if not req.ok:
        return (50.6937, 3.1744) # Default Lille

    contents = req.json()["data"]
    latitude = contents["location"]["latitude"]
    longitude = contents["location"]["longitude"]

    return (latitude, longitude)

def getWeather(base_url: str, lat: int, lon: int) -> dict | None:
    """Gets weather data from given latitude and longitude

    Params:
    - base_url(str): Base API url with longitude and latitude to be replaced
    - lat(int): latitude
    - lon(int): longitude 
    """
    url = base_url.replace("%%LAT%%", str(lat))
    url = url.replace("%%LON%%", str(lon))

    req = SESSION.get(url)
    if not req.ok:
        return None

    return req.json()

def ensureFileExists(filepath: str) -> None:
    """Ensures file exists, resets it if it does, creates if not
    
    Params:
    - filepath(str): File path
    """
    if not os.path.exists(filepath):
        with open(filepath, mode="x", encoding="utf-8") as f:
            json.dump(fp=f, obj=DEFAULT_TEMPLATE)
    else:
        with open(filepath, mode="w", encoding="utf-8") as f:
            f.seek(0)
            f.truncate(0)
            json.dump(fp=f, obj=DEFAULT_TEMPLATE)

def getJsonContents(filepath: str) -> dict:
    """Gets json contents from given file

    Params:
    - filepath(str): File path

    Returns:
    - dict: Data read
    """
    with open(file=filepath, mode="r", encoding="utf-8") as f:
        return json.load(fp=f)

def writeToJson(filepath: str, content: dict) -> None:
    with open(file=filepath, mode="w", encoding="utf-8") as f:
        f.seek(0)
        f.truncate(0)
        json.dump(fp=f, obj=content)



def main() -> None: 
    ensureFileExists(WEATHER_FILE)

    while True:
        last_weather_data = getJsonContents(filepath=WEATHER_FILE)
        time_difference = time.time() - last_weather_data["updated"]
        if time_difference < 300:
            time.sleep(time_difference + 1)
            continue

        if not internetAvailable():
            time.sleep(5)
            continue

        lat, lon = getGeolocation(GEOLOCATION_URL)
        weather = getWeather(base_url=WEATHER_URL, lat=lat, lon=lon)
        if not weather:
            time.sleep(5)
            continue

        current_weather = weather["current"]
        hourly_weather = weather["hourly"]
        daily_weather = weather["daily"]
        weather_obj = {"updated": time.time()} | {"current": current_weather} | {"hourly": hourly_weather} | {"daily": daily_weather}

        writeToJson(filepath=WEATHER_FILE, content=weather_obj)



if __name__ == "__main__":
   main() 
