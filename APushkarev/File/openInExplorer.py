# This script opens the folder containing the file referenced by the selected node in Nuke.
# If no node is selected, it opens the folder of the current script.

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke
import os

def openIfExists(file):
    """Opens the folder containing the file if it exists"""
    first_dir = os.path.dirname(file)
    second_dir = os.path.dirname(first_dir)
    if os.path.isdir(first_dir):
        os.startfile(first_dir)
    elif os.path.isdir(second_dir):
        os.startfile(second_dir)

def openInExplorer():
    nodes = nuke.selectedNodes()
    # If nothing is selected, open the folder where the current script is located
    if not nodes:
        openIfExists(nuke.root().name())
        return
    node = nodes[0]  # Only process the first selected node
    for n in ["file", "outfile"]:
        file_kn = node.knob(n)
        if isinstance(file_kn, nuke.File_Knob):
            # Handle Z drive mapped via IP address
            file_path = file_kn.evaluate()
            z_drive_unc = os.getenv("Z_DRIVE_UNC_PATH")
            if z_drive_unc:
                file_path = file_path.replace(z_drive_unc.replace("\\", "/"), "Z:")
            openIfExists(file_path)
            return
