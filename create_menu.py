import os
import json
import configparser

# Path to the scripts folder (current folder)
cur_dir = os.path.dirname(__file__)
info_file = r"Z:\Nuke_Workgroup\python\ScriptsManager\scripts_info.json"
menu_file = os.path.join(cur_dir, "menu.py")
config_file = os.path.join(cur_dir, "config.ini")

# Load script information
with open(info_file, "r", encoding="utf-8") as f:
    scripts_info = json.load(f)

# Load renaming rules from config.ini
config = configparser.ConfigParser()
config.optionxform = str  # disables converting keys to lowercase
config.read(config_file)
renaming_map = dict(config.items("Renaming")) if config.has_section("Renaming") else {}

def apply_renaming(menu_path, renaming_map):
    """Replaces parts of menu_path according to renaming_map"""
    parts = menu_path.split("/")
    new_parts = [renaming_map.get(part, part) for part in parts]
    return "/".join(new_parts)

def write_menu_line(file, info):
    """Writes a command line to menu.py similar to writeAndAddMenu"""
    if info.get("custom_cmd_checkbox"):
        custom_command = info.get("custom_command", "")
        # Apply renaming for custom_command using replace()
        for old, new in renaming_map.items():
            custom_command = custom_command.replace(old, new)
        file.write(custom_command + "\n")
    else:
        menu_path = info.get("menu_path", "")
        menu_path = apply_renaming(menu_path, renaming_map)
        command = info.get("command", "")
        icon = info.get("icon", "")
        shortcut = info.get("shortcut", "")
        context = info.get("shortcut_context", "")
        index = info.get("index", -1)

        args = [f"'{menu_path}'", f"'{command}'"]
        if shortcut:
            args.append(f"'{shortcut}'")
        if icon:
            args.append(f"icon='{icon}'")
        if index != -1:
            args.append(f"index={index}")
        if context in ["0", "1", "2"]:
            args.append(f"shortcutContext={context}")

        args_str = ", ".join(args)
        file.write(f"nuke.menu('Nuke').addCommand({args_str})\n")

with open(menu_file, "w", encoding="utf-8") as menu:
    menu.write("import nuke, nukescripts\n\n")
    for root, dirnames, files in os.walk(cur_dir):
        if root == cur_dir:
            dirnames.remove(".git")
            continue
        for file_name in files:
            if file_name.endswith(".py"):
                script_name = os.path.splitext(file_name)[0]
                info = scripts_info.get(script_name)
                if info:
                    write_menu_line(menu, info)
