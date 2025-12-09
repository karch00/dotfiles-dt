import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import requests
import json
import os

SESSION = requests.Session()
MISSING_METADATA = {
    "title": "No song playing",
    "artist": "---",
    "image": "./assets/music_placeholder.png",
    "length": 1,
    "progress_time": "00:00",
    "progress_bar": 0,
    "volume": 0,
    "volume_icon": "",  
    "status_icon": "",
    "shuffle_icon": "󰒟",
    "repeat_icon": "󰑖"
}
VOLUME_ICONS = {"off": "", "low": "", "mid": "", "high": ""}
STATUS_ICONS = {"Playing": "", "Paused": "", "Stopped": ""}  
SHUFFLE_ICONS = {False: "󰒞", True: "󰒟"} 
REPEAT_ICONS = {"None": "󰑗", "Playlist": "󰑖", "Track": "󰑘"} 

def getProgressTime(position: int):
    """Process raw position in seconds and returns time elapsed in mm:ss"""
    minutes = position // 60
    seconds = position % 60
    if minutes < 10:
        minutes = f"0{minutes}"
    if seconds < 10:
        seconds = f"0{seconds}"
    
    return f"{minutes}:{seconds}"

def getVolumeIcon(volume: int):
    """Gets current volume and returns its correspondent icon"""
    if volume == 0:
        return VOLUME_ICONS["off"]
    elif volume <= 20:
        return VOLUME_ICONS["low"]
    elif volume <= 35:
        return VOLUME_ICONS["mid"]
    elif volume <= 100:
        return VOLUME_ICONS["high"]

def playerAvailable(bus) -> str:
    """Checks if any player is available"""
    for service in bus.list_names():
        if service.startswith("org.mpris.MediaPlayer2.") and "playerctld" not in service:
            return service
    return None

def isLastSong(current_title: str, current_artist: str) -> bool:
    """Checks if last song is same as current. Writes new song if False."""
    current_song = f"{current_title}{current_artist}".strip()
    
    try:
        with open("./temp/last_song", mode="r", encoding="UTF-8") as f:
            last_song = f.readline().strip()
    except FileNotFoundError:
        with open("./temp/last_song", mode="w", encoding="UTF-8") as f:
            f.write(current_song)
        return False
    
    if last_song == current_song:
        return True
    else:
        with open("./temp/last_song", mode="w", encoding="UTF-8") as f:
            f.write(current_song)
        return False

def createImage(data: bytes):
    """Creates image from binary data"""
    with open("./temp/music", "wb") as f: 
        f.write(data)

def getImage(image: str, title: str, artist: str) -> str:
    """Gets the image link and downloads it, returns the relative path to the downloaded image or the placeholder if unsuccessful"""
    try:
        is_last_song = isLastSong(current_title=title, current_artist=artist)
        if is_last_song:
            return "./temp/music"
        
        if not image or image == "None":
            return "./assets/music_placeholder.png"
            
        request = SESSION.get(image, timeout=5) 
        if not request or not request.ok:
            return "./assets/music_placeholder.png" 
        createImage(request.content)
        
        return "./temp/music"
    except Exception:
        return "./assets/music_placeholder.png"

def getPlayerData(properties) -> dict:
    """Get all relevant music and player data"""
    try:
        all_data = properties.GetAll("org.mpris.MediaPlayer2.Player")
    except dbus.DBusException:
        return None

    metadata = all_data.get("Metadata", {})
    title = metadata.get("xesam:title", "No song playing")
    image = metadata.get("mpris:artUrl", "None")
    artist_list = metadata.get("xesam:artist", ["---"])
    artist = artist_list[0] if artist_list else "---"
    length = metadata.get("mpris:length", 0) // 1000000

    position = all_data.get("Position", 0) // 1000000
    volume = int(all_data.get("Volume", 0) * 100)
    status = all_data.get("PlaybackStatus", "Paused")
    shuffle = all_data.get("Shuffle", False)
    loop = all_data.get("LoopStatus", "None")

    return {
        "title": title,
        "artist": artist,
        "image": getImage(image, title=title, artist=artist),
        "length": length,
        "progress_time": getProgressTime(position),
        "progress_bar": position,
        "volume": volume,
        "volume_icon": getVolumeIcon(volume),
        "status": status,
        "status_icon": STATUS_ICONS.get(status, ""), 
        "shuffle_icon": SHUFFLE_ICONS[shuffle],
        "repeat_icon": REPEAT_ICONS[loop]
    }

def createCallback(properties):
    """Callback function to onPropertiesChanged, allows passing of main function player properties"""
    def onPropertiesChanged():
        """Returns new player updated data"""
        data = getPlayerData(properties=properties)
        if data:
            print(json.dumps(data))
    return onPropertiesChanged

def main():
    """Main function, call point"""
    try:
        DBusGMainLoop(set_as_default=True)
        bus = dbus.SessionBus()

        player_name = playerAvailable(bus=bus) 
        if not player_name:
            print(json.dumps(MISSING_METADATA))
            return

        player = bus.get_object(player_name, "/org/mpris/MediaPlayer2")
        properties: dbus.Interface = dbus.Interface(player, "org.freedesktop.DBus.Properties")

        initial_data = getPlayerData(properties=properties)
        if initial_data:
            print(json.dumps(initial_data))

        callback = createCallback(properties=properties)
        player.connect_to_signal(
            "PropertiesChanged",
            callback,
            dbus_interface="org.freedesktop.DBus.Properties"
        )

        def updatePosition() -> bool: 
            """Updates position as it progresses since DBus does not automatically update it by default"""
            try:
                data = getPlayerData(properties=properties)
                if data: 
                    print(json.dumps(data))
            except Exception:
                pass
            
            return True
        
        GLib.timeout_add(100, updatePosition)
        loop = GLib.MainLoop()
        loop.run()
    
    except Exception as e:
        print(json.dumps(MISSING_METADATA))

if __name__ == "__main__":
    main()
