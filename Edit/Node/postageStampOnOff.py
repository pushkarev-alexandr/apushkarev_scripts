# Same as the standard Postage Stamp On/Off, but if no nodes are selected, it toggles the postage stamp for all Read nodes

# v1.1.0
# created by: Pushkarev Aleksandr

import nuke

def postageStampOnOff():
    nodes = nuke.selectedNodes()
    if not nodes:
        nodes = nuke.allNodes('Read')
    if nodes:
        on = True
        for node in nodes:
            kn = node.knob('postage_stamp')
            if kn and kn.value():
                on = False
                break
        for node in nodes:
            kn = node.knob('postage_stamp')
            if kn:
                kn.setValue(on)
