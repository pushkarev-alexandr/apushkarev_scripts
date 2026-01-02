# Extends the standard Edit/Remove Input command: if no node is selected, disconnects inputs from all viewers

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke

def removeInput():
    selected = nuke.selectedNodes()
    if not selected:
        selected = nuke.allNodes('Viewer')
    for node in selected:
        for i in range(node.inputs()):
            node.setInput(i, None)
