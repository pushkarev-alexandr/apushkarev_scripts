# When creating a node, Blur links the size to the Erode node if an Erode node was selected before creation

# v1.2.0
# created by: Pushkarev Aleksandr

# v1.2.0 Blur affects the same channels as Erode. Minor refactoring

import nuke

def linkBlurToErode():
    nodes = nuke.selectedNodes()
    if len(nodes)==1 and nodes[0].Class()=="FilterErode":
        erode = nodes[0]
        blur = nuke.createNode("Blur")
        blur["size"].setExpression(f"abs({erode.name()}.size)")
        blur["channels"].setValue(erode["channels"].value())
