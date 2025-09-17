# Copies the selected script to the temp folder and opens it to avoid modifying the user's script

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke
import os, shutil

def openCopy():
    src_file = nuke.getFilename("Open copy", pattern="*.nk")
    if not src_file:
        return
    if src_file.endswith(".nk"):
        dst_folder = os.getenv("NUKE_TEMP_DIR") + "/nk_copies"
        dst_file = os.path.join(dst_folder, os.path.basename(src_file))
        os.makedirs(dst_folder, exist_ok=True)
        shutil.copy2(src_file, dst_file)
        nuke.scriptOpen(dst_file)
    else:
        nuke.message("Select an .nk file")
