# Makes all inputs visible

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke

def unhideAllInputs():
    for node in nuke.allNodes():
        kn = node.knob("hide_input")
        if kn and kn.value():
            kn.setValue(False)
