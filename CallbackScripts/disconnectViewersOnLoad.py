# When opening the script, all inputs of all viewers are disconnected so that the tree is not processed and the script does not slow down

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke

def disconnectViewers():
    for node in nuke.allNodes('Viewer'):
        for i in range(node.inputs()):
            node.setInput(i, None)

nuke.addOnScriptLoad(disconnectViewers)
