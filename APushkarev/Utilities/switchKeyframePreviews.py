# Disables Keyframe Previews to prevent the Tracker node from hanging

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke

def switchKeyframePreviews():
    isSelected = True
    nodes = nuke.selectedNodes("Tracker4")
    if not nodes:
        nodes = nuke.allNodes("Tracker4")
        isSelected = False
    if not nodes:
        nuke.message("There is no Tracker nodes")
        return
    off = False
    for node in nodes:
        if node.knob("zoom_window_behaviour").getValue() != 4 or node.knob("keyframe_display").getValue() != 3:
            off = True
    for node in nodes:
        zoom = node.knob("zoom_window_behaviour")
        keys = node.knob("keyframe_display")
        if off:
            zoom.setValue(4)
            keys.setValue(3)
        else:
            zoom.setValue(0)
            keys.setValue(2)
    message = "Keyframe previews is "
    if off:
        message += "OFF"
    else:
        message += "ON"
    if isSelected:
        message += " for selected trackers"
    else:
        message += " for all trackers"
    nuke.message(message)
