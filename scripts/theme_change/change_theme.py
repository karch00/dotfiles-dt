import os
import pathlib
import shutil
import sys
from typing import Any
import pathlib
import subprocess
import re


THEME_NAME = sys.argv[1]
CONFIG= f"{pathlib.Path.home()}/.config"
THEMES_FOLDER = "/usr/share/system_themes"
OBSIDIAN_PATH = f"{pathlib.Path.home()}/Study/.obsidian/themes/Typewriter"
VESKTOP_PATH = f"{CONFIG}/vesktop/themes"
COMPONENT_PATHS = {
    "dunst": f"{CONFIG}/dunst",
    "eww": f"{CONFIG}/eww",
    "gtk-3.0": f"{CONFIG}/gtk-3.0",
    "homepage": "/usr/share/homepage",
    "hypr": f"{CONFIG}/hypr",
    "kitty": f"{CONFIG}/kitty",
    "nvim": f"{CONFIG}/nvim/lua",
    "obsidian": OBSIDIAN_PATH,
    "rofi": f"{CONFIG}/rofi",
    "sddm": f"/usr/share/sddm/themes/karch/",
    "starship": CONFIG,
    "superfile": f"{CONFIG}/superfile/theme",
    "vesktop": VESKTOP_PATH,
    "waybar": f"{CONFIG}/waybar",
    "wlogout": f"{CONFIG}/wlogout",
    "zshrc": pathlib.Path.home()
}
COMPONENTS_RESTART = {
    "swww": "swww img %wallpaper% --transition-type center --transition-fps 60",
    "waybar": "killall waybar && nohup waybar &> /dev/null"
}



def move_configs(theme_name: str, themes_dir: str, components: dict[str, str]) -> None:
    """
    Move the color config of each file to its respective configuration directory

    # Params:
    - theme_name (str): The name of the theme 
    - themes_dir (str): Directory with all themes
    - components (dict[str, str]): List of components with their paths as values
    """
    
    theme_path = f"{themes_dir}/{theme_name}"
    for component, path in components.items():
        filename = os.listdir(f"{theme_path}/{component}")[0]
        shutil.copyfile(f"{theme_path}/{component}/{filename}", f"{path}/{filename}")

def restart_components(components: dict[str, str], args: dict[str, Any]) -> None:
    """
    Restarts all components in the components dictionary by executing the command passed as values.
    Formatted arguments will be replaced in order by the list of args.

    # Params:
    - components (dict[str, str): Dictionary with component:commands as items
    - args (dict[str, Any]): Dictionary with keys to replace each component command arg with its value
    """
    for _, command in components.items():
        command_args = re.findall(string=command, pattern=r"%[a-zA-Z0-9]{1,}%")
        
        for arg in command_args:
            command = command.replace(arg, args[arg])
        
        print(command)
        subprocess.run(command, shell=True)

def main() -> int:
    if not os.path.exists(f"{THEMES_FOLDER}/{THEME_NAME}"):
        print(">>> Theme not found <<<")
        return 0
    
    # Move configs 
    move_configs(theme_name=THEME_NAME, themes_dir=THEMES_FOLDER, components=COMPONENT_PATHS)

    # Restart components
    wallpaper = f"{THEMES_FOLDER}/{THEME_NAME}/wallpaper/wp"
    restart_components(COMPONENTS_RESTART, args={"%wallpaper%": wallpaper})

    return 1

if __name__ == "__main__":
    main()
