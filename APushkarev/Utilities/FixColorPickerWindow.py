# When the Color Picker window goes off-screen, resets its position by removing the line in uistate.ini

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke
import os

def main():
    file_path = os.path.join(os.path.expanduser("~"), ".nuke\\uistate.ini")
    if not os.path.isfile(file_path):
        nuke.message("Could not find uistate.ini file")
        return

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    filtered_lines = [line for line in lines if not line.startswith("ColorPicker=@Rect(")]

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(filtered_lines)

    nuke.message("Please restart Nuke")
