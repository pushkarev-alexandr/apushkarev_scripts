# Adds a shortcut 'h' for creating FrameHold
# When created in Nuke 12 and below, the current frame is set; in Nuke 13 and above, this is done by default
# If only FrameHold nodes are selected, the current frame will be set in those nodes
# Different knob names in different versions of Nuke are taken into account

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke

def customFrameHold():
    nodes = nuke.selectedNodes('FrameHold')
    knName = 'first_frame' if nuke.NUKE_VERSION_MAJOR < 13 else 'firstFrame'
    if nodes:
        for n in nodes:
            n[knName].setValue(nuke.frame())
    else:
        framehold = nuke.createNode('FrameHold')
        if nuke.NUKE_VERSION_MAJOR < 13:
            framehold[knName].setValue(nuke.frame())
