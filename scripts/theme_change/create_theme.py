import re
import os
import pathlib
import shutil



TERMINAL_COLORS = {
    0: "0-Black",
    1: "1-Red",
    2: "2-Green",
    3: "3-Yellow",
    4: "4-Blue",
    5: "5-Purple",
    6: "6-Cyan",
    7: "7-White",

    8: "8-Contrast Black",
    9: "9-Contrast Red",
    10: "10-Contrast Green",
    11: "11-Contrast Yellow",
    12: "12-Contrast Blue",
    13: "13-Contrast Purple",
    14: "14-Contrast Cyan",
    15: "15-Contrast white"
}
CUSTOM_COLORS = {
    16: "16-Accent",
    17: "17-Active accent",
    18: "18-Inactive border",
    19: "19-Cursor"
}
NVIM_COLORS = {
    20: "20--5% Black",
    21: "21-+5% Black",
    22: "22-+10% Black",
    23: "23-+5% Color22",
    24: "24-+5% Color23",
    25: "25-+40% Black",
    26: "26-+10% Color25",
    27: "27-+5% Color25",
    28: "28-Light grey",
    29: "29-Baby pink",
    30: "30-Pink",
    31: "31-+15% Black",
    32: "32-Nord blue",
    33: "33-Sea blue",
    34: "34-+5% Yellow",
    35: "35-Dark purple",
    36: "36-Teal",
    37: "37-Orange",
    38: "38-Status line (bot)",
    39: "39-Ligth BG",
    40: "40-Side menu",
    41: "41-Folders",
    42: "42-Yellow-orange"
}
STARSHIP_COLORS = {
    43: "43-Prompt 1",
    44: "44-Prompt 2",
    45: "45-Prompt 3",
    46: "46-Prompt 4"
}

HEX_VALUES = {
    "0":0, "1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9,
    "a":10, "b":11, "c":12, "d":13, "e":14, "f":15
}

HOME = pathlib.Path.home()
TEMPLATE_DIR = "./templates"
CACHE_DIR = "./cache"
THEMES_DIR = "/usr/share/system_themes"
COMPONENTS = [
    "dunst", 
    "eww",
    "gtk-3.0", 
    "homepage", 
    "hypr", 
    "kitty",
    "nvim", 
    "obsidian", 
    "rofi",
    "sddm",
    "superfile",
    "vesktop",
    "waybar", 
    "wlogout",
    "zshrc", 
    "starship"
]



def hex_to_rgb(hex: str) -> list[int]:
    """Converts an hex code to rgb

    # Params:
    - hex (str): Hex code 

    # Returns:
    - rgb (list[int]): List of [R,G,B] colors
    """
    rgb_code = []
    rgb = 0

    for idx in range(0, 6):
        exp = int(not idx % 2)  
        rgb += (16**exp) * HEX_VALUES[hex[idx]]
 
        if exp == 0:
            rgb_code.append(rgb)
            rgb= 0 

    return rgb_code


def get_colors(color_list : dict[int, str]) -> dict[int, str]:
    """Gets terminal colors from user input as hex

    # Returns:
    - ansi_colors (dict[str, str]): Chosen colors
    """

    ansi_colors = {}
    keys = list(color_list.keys())

    for idx in range(keys[0], keys[-1]+1):
        while True:
            hex_color = input(f">>> {color_list[idx]}: ")

            if re.match(r"^#[a-fA-F0-9]{6}$", hex_color) or re.match(r"^[a-fA-F0-9]{6}$", hex_color):
                break
            print("[ Hex color not valid ]")
        
        ansi_colors[idx] = hex_color.replace("#", "")

    return ansi_colors

def replace_colors(code_str: str, color_dict: dict[int, str]) -> str:
    """Replaces all colors under the format %c(INT)% from the inputted string

    # Params:
    - code_str (str): Code to replace the colors from
    - color_dict (dict[int, str]): Color dictionary to get color values from

    # Returns:
    - replaced (str): Code string with replaced colors
    """
    replaced_str = code_str
    for color, code in color_dict.items():
        replaced_str = replaced_str.replace(f"%c{color}%", code)

    return replaced_str

def generate_color_files(template_dir: str, cache_dir: str, components: list[str], color_dict: dict[int, str]) -> None:
    """Generates color files for each component by reading the template, replacing the colors and moving it to the cache dir
    
    # Params:
    - template_dir (str): templates directory
    - cache_dir (str): cache directory 
    - components: (list[str]): list of components 
    - color_dict (dict[int, str]): color map indicating which color hexcode has each ID
    """
    for comp in components:
        print(f">>> Creating color file for [ {comp} ]")

        comp_template_dir = f"{template_dir}/colors/{comp}"
        comp_cache_dir = f"{cache_dir}/{comp}"
        file = os.listdir(comp_template_dir)[0]

        with open(f"{comp_template_dir}/{file}", mode="r", encoding="utf-8") as f:
            contents = f.read()
        replaced_contents = replace_colors(contents, color_dict)
       
        try:
            os.makedirs(comp_cache_dir) if not os.path.exists(comp_cache_dir) else ...
            open(f"{comp_cache_dir}/{file}", mode="x", encoding="utf-8").close()
        except Exception:
            ...

        with open(f"{comp_cache_dir}/{file}", mode="w", encoding="utf-8") as f:
            f.seek(0)
            f.truncate(0)

            f.write(replaced_contents)

def move_config_files(template_dir: str, cache_dir: str, components: list[str]) -> None:
    """Moves config files for each component from template to cache

    # Params:
    - template_dir (str): templates directory
    - cache_dir (str): cache directory
    - components (list[str]): list of components 
    """
    for comp in components:
        print(f">>> Moving config files for [ {comp} ]")
        comp_template_dir = f"{template_dir}/config/{comp}"
        comp_cache_dir = f"{cache_dir}/{comp}"

        for file in os.listdir(comp_template_dir):
            try:
                shutil.copytree(f"{comp_template_dir}/{file}", f"{comp_cache_dir}/", dirs_exist_ok=True)
            except Exception:
                shutil.copy(f"{comp_template_dir}/{file}", f"{comp_cache_dir}/")

def main():
    if os.geteuid() != 0:
        print("[ Must run script with sudo privileges ]")
        return

    print("---===---===--{ Theme generator }--===---===---")
    theme_name = input(">>> Theme name? ")

    # Wallpaper picking
    while True:
        wallpaper_path = input(">>> Wallpaper path? ")
        if os.path.exists(wallpaper_path):
            os.makedirs(f"{CACHE_DIR}/wallpaper")
            shutil.copyfile(wallpaper_path, f"{CACHE_DIR}/wallpaper/wp")
            break
        print("[ Wallpaper not found ]")


    # Terminal color picking
    while True:
        print("\n --- { Terminal colors } --- ")
        selected_term_colors = get_colors(TERMINAL_COLORS)
        
        print(" --- { Selected colors preview} ---")
        for color in selected_term_colors:
            color_name = TERMINAL_COLORS[int(color)]
            color_code = selected_term_colors[color]
            rgb_color = hex_to_rgb(color_code)

            space_number = 24 - len(color_name)
            print(f">>> {color_name}:{' '*space_number}{color_code} \033[38;2;{rgb_color[0]};{rgb_color[1]};{rgb_color[2]}m██████\033[0m")
        
        if input(">>> Confirm[y/n]? ").lower() in ["y", "", " "]: 
            break

    # Custom color picking
    while True:
        print("\n --- { Custom colors } --- ")
        selected_custom_colors = get_colors(CUSTOM_COLORS)

        print(" --- {Selected colors preview} ---")
        for color in selected_custom_colors:
            color_name = CUSTOM_COLORS[int(color)]
            color_code = selected_custom_colors[color]
            rgb_color = hex_to_rgb(color_code)

            space_number = 24 - len(color_name)
            print(f">>> {color_name}:{' '*space_number}{color_code} \033[38;2;{rgb_color[0]};{rgb_color[1]};{rgb_color[2]}m██████\033[0m")
        
        if input(">>> Confirm[y/n]? ").lower() in ["y", "", " "]: 
            break

    # NVIM color picking
    while True:
        print("\n --- { NVIM colors } --- ")
        selected_nvim_colors = get_colors(NVIM_COLORS)
        
        print(" --- { Selected colors preview} ---")
        for color in selected_nvim_colors:
            color_name = NVIM_COLORS[int(color)]
            color_code = selected_nvim_colors[color]
            rgb_color = hex_to_rgb(color_code)

            space_number = 24 - len(color_name)
            print(f">>> {color_name}:{' '*space_number}{color_code} \033[38;2;{rgb_color[0]};{rgb_color[1]};{rgb_color[2]}m██████\033[0m")
        
        if input(">>> Confirm[y/n]? (Modifiable @ ~/.config/nvim/lua/chadrc.lua) ").lower() in ["y", "", " "]: 
            break

    # Starship color picking
    while True:
        print("\n --- { Starship prompt colors } --- ")
        selected_starship_colors = get_colors(STARSHIP_COLORS)
        
        print(" --- { Selected colors preview} ---")
        for color in selected_starship_colors:
            color_name = STARSHIP_COLORS[int(color)]
            color_code = selected_starship_colors[color]
            rgb_color = hex_to_rgb(color_code)

            space_number = 24 - len(color_name)
            print(f">>> {color_name}:{' '*space_number}{color_code} \033[38;2;{rgb_color[0]};{rgb_color[1]};{rgb_color[2]}m██████\033[0m")
        
        if input(">>> Confirm[y/n]? (Modifiable @ ~/.config/starship.toml) ").lower() in ["y", "", " "]: 
            break
   
    print("\n>>> Creating color files <<<\n")
    all_colors = selected_term_colors | selected_custom_colors | selected_nvim_colors | selected_starship_colors

    # Generate color files from templates
    generate_color_files(TEMPLATE_DIR, CACHE_DIR, COMPONENTS, all_colors)
    move_config_files(TEMPLATE_DIR, CACHE_DIR, COMPONENTS)

    # Move to themes folder
    print("\n>>> Moving theme to folder <<<")
    os.makedirs(f"{THEMES_DIR}/{theme_name}") if not os.path.exists(f"{THEMES_DIR}/{theme_name}") else ...
    for dir in os.listdir(CACHE_DIR):
        shutil.move(f"{CACHE_DIR}/{dir}", f"{THEMES_DIR}/{theme_name}/{dir}")

    print("\n\n>>> Theme created <<<")



if __name__ == "__main__":
    main()
