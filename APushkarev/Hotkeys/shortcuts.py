# Creates a menu of shortcuts for commonly used nodes

# v1.1.1
# created by: Pushkarev Aleksandr

# v1.1.0 Moved menu creation to an external file
# v1.1.1 Restored menu creation to the main file

import nuke, re

def inputsFromOneNodeToAnother(fromNode,toNode):
    for depNode in fromNode.dependent(forceEvaluate = False):
        for i in range(depNode.inputs()):
            if depNode.input(i)==fromNode:
                depNode.setInput(i,toNode)

def createNode(cl):
    sel = nuke.selectedNodes()
    try:
        node = nuke.createNode(cl)
    except:
        return
    for n in sel:
        inputsFromOneNodeToAnother(n,node)
    if sel:
        node.autoplace()

def createShortcutsMenu(menu: nuke.Menu):
    shortcuts = [
        "Tracker4|shift+t",
        "Crop|z",
        "Premult|v",
        "Unpremult|alt+v",
        "ChannelMerge|alt+l",
        "Keymix|alt+j",
        "Dissolve|alt+shift+j",
        "Shuffle2|shift+j",
        "ShuffleCopy|shift+k",
        "Invert|shift+i",
        "Defocus|alt+a",
        "FilterErode|e",
        "Erode|shift+e|ErodeBlur",
        "Constant|shift+v",
        "Toe2|shift+c",
        "Grain2|shift+g",
        "Switch|shift+h",
        "Multiply|shift+m|ColorMult"
        ]
    for shortcut in shortcuts:
        spl = shortcut.split("|")
        digitless = re.sub(r"\d+$", "", spl[0])  # Node name without trailing digits, used for menu label and icon
        shift_mode = ["nuke", "shortcuts"][spl[1].lower().startswith("shift+")]  # If the shortcut starts with Shift, create the node via custom function
        command = f"import shortcuts; {shift_mode}.createNode('{spl[0]}')"
        icon = spl[2] if len(spl) > 2 else digitless
        menu.addCommand(f"Hotkeys/{digitless}", command, spl[1], icon=f"{icon}.png", shortcutContext=2)
