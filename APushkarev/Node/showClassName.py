# Displays a message with the class names of the selected nodes

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke

def showClassName():
    res = ""
    nodes = nuke.selectedNodes()
    nodes.reverse()
    for node in nodes:
        res += node.Class() + "\n"
    if res:
        nuke.message(res)
