# Renders the current frame of the active viewer and saves it to the current script's folder in the 'screenshots' subfolder or in the NUKE_TEMP_DIR folder

# v1.2.1
# created by: Pushkarev Aleksandr

# changelog:
# v1.1.1 channels are set to rgba
# v1.2.0 Small refactoring. Removed the limit on the number of screenshots, implemented with while loop. Colorspace is now present in the naming.
# v1.2.1 Now the screenshot name is derived from the script name

import nuke, nukescripts
import subprocess, os, re

def setColorspace(node, space1, space2=None):
    availableCS = nuke.root().knob("int8Lut").values()
    l = len(availableCS)
    kn = node.knob("colorspace")
    for i in range(l):
        if availableCS[i]==space1 or availableCS[i].split("/").pop()==space1:
            kn.setValue(space1)
            node["raw"].setValue(False)
            break
        elif availableCS[i]==space2 or availableCS[i].split("/").pop()==space2:
            kn.setValue(space2)
            node["raw"].setValue(False)
            break

def validation(viewerWindow, basedir):
    """Validates the viewer window and base directory."""
    if not viewerWindow:
        return "No active viewer"
    if viewerWindow.activeInput() is None:
        return "Viewer is not connected"
    if not os.path.isdir(basedir):
        return "Cannot find folder to save screenshots"
    return ""

def get_unique_screenshot_path(scrDir, rootname, colorspace):
    if rootname == "Root":
        prefix = "screenshot"
    else:
        prefix = os.path.splitext(os.path.basename(rootname))[0]
        prefix = re.sub(r"v\d+", "", prefix, flags=re.IGNORECASE)      # remove version tokens like v001
        prefix = prefix.rstrip("._-")

    i = 1
    path_template = f"{scrDir}/{prefix}_{{}}_{colorspace}.png"
    path = path_template.format(i)
    while os.path.isfile(path):
        i += 1
        path = path_template.format(i)
    return path

def screenshotFromViewer():
    viewerWindow = nuke.activeViewer()
    rootname = nuke.root().name()
    basedir = os.getenv("NUKE_TEMP_DIR") if rootname=="Root" else nuke.script_directory()

    validation_message = validation(viewerWindow, basedir)
    if validation_message:
        nuke.message(validation_message)
        return
    
    viewer = viewerWindow.node()
    isRec709 = viewer["viewerProcess"].value() == "Rec.709 (ACES)"
    node = viewer.input(viewerWindow.activeInput())
    nukescripts.clear_selection_recursive()

    write = nuke.createNode("Write")
    write.setInput(0, node)

    scrDir = f"{basedir}/screenshots"
    os.makedirs(scrDir, exist_ok=True)

    path = get_unique_screenshot_path(scrDir, rootname, "rec709" if isRec709 else "srgb")
    
    write["file"].setValue(path)
    write["channels"].setValue("rgba")
    if isRec709:
        setColorspace(write, "rec709", "Output - Rec.709")
    else:
        setColorspace(write, "sRGB", "Output - sRGB")
    nuke.execute(write, nuke.frame(), nuke.frame())
    nuke.delete(write)
    subprocess.call(("explorer", "/select,", os.path.normpath(path)))
