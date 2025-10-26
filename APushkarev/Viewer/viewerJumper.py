# Can jump between adjacent Read nodes

# v1.0.0
# created by: Pushkarev Aleksandr

# TODO
# - Should jump not only among Read nodes, but among any nodes regardless of their position — just go to the neighboring one
# - Should jump not only left and right, but in any direction

import nuke

def viewerJumper(right=True):
    activeViewer = nuke.activeViewer()
    if not activeViewer:
        return
    activeInput = activeViewer.activeInput()
    if activeInput == None:
        return
    viewerNode = activeViewer.node()
    node = viewerNode.input(activeInput)
    for n in nuke.allNodes('Read'):
        d = n.xpos() - node.xpos() if right else node.xpos() - n.xpos()
        if d > 0 and d < 120 and node.ypos() == n.ypos():
            viewerNode.setInput(activeInput, n)
