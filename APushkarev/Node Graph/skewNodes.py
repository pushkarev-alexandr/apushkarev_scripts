# Shifts nodes so they are not aligned in a single vertical line

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke

def skewNodes():
    nodes = nuke.selectedNodes()
    nodes.sort(key=lambda x: x.ypos())
    scale = 30
    for i, node in enumerate(nodes):
        node.setXpos(node.xpos() + i * scale)
