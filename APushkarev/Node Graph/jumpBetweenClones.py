# Allows switching between clones

#v1.1.0
#created by: Pushkarev Aleksandr

import nuke

def jumpBetweenClones():
    nodes = nuke.selectedNodes()
    if not nodes:
        return
    sel = nodes[0]
    sel.setSelected(False)
    for node in nuke.allNodes(sel.Class()):
        if node.name()==sel.name() and node!=sel:
            node.setSelected(True)
            nuke.zoomToFitSelected()        
            break
