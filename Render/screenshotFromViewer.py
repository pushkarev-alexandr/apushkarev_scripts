# Renders the current frame of the active viewer and saves it to the current script's folder in the 'screenshots' subfolder or in the NUKE_TEMP_DIR folder

# v1.2.3
# created by: Pushkarev Aleksandr

# changelog:
# v1.1.1 channels are set to rgba
# v1.2.0 Small refactoring. Removed the limit on the number of screenshots, implemented with while loop. Colorspace is now present in the naming.
# v1.2.1 Now the screenshot name is derived from the script name
# v1.2.2 Added frame number to screenshot file name
# v1.2.3 Added support for aces1.3 display mode

import nuke, nukescripts
import subprocess, os, re

def setColorspace(node, default_space, aces_space, display_space):
    config = nuke.root()["OCIO_config"].value()
    display = config.startswith("fn-nuke_")

    node["raw"].setValue(False)
    if node.knob("transformType"):
        node["transformType"].setValue("display" if display else "colorspace")

    if config == "nuke-default":
        node["colorspace"].setValue(default_space)
    elif config.startswith("fn-nuke_"):
        node["ocioDisplay"].setValue(display_space)
    else:
        node["colorspace"].setValue(aces_space)

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
    path_template = f"{scrDir}/{prefix}_{{}}_{colorspace}.{nuke.frame()}.png"
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
    vp_value = viewer["viewerProcess"].value()
    isRec709 = vp_value.count("Rec.709") or vp_value == "rec709"
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
        setColorspace(write, "rec709", "Output - Rec.709", "Rec.1886 Rec.709 - Display")
    else:
        setColorspace(write, "sRGB", "Output - sRGB", "sRGB - Display")
    nuke.execute(write, nuke.frame(), nuke.frame())
    nuke.delete(write)
    subprocess.call(("explorer", "/select,", os.path.normpath(path)))
