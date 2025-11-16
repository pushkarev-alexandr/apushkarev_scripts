# Inverts the disable state of selected nodes

# v1.1.0
# created by: Pushkarev Aleksandr

import nuke

def invertDisable():
    for node in nuke.selectedNodes():
        kn = node.knob('disable')
        if kn:
            kn.setValue(not kn.value())
