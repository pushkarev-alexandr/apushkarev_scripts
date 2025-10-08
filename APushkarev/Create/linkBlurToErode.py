
# When creating a node, Blur links the size to the Erode, FilterErode, or Dilate node if such a node was selected before creation.
# If a Roto, RotoPaint, or Keyer node is selected, Blur will always set the channel to alpha.

# v1.3.0
# created by: Pushkarev Aleksandr

# changelog:
# v1.0.0 - Initial version
# v1.2.0 - Blur affects the same channels as Erode. Minor refactoring
# v1.3.0 - Added same behavior for Erode and Dilate nodes as for FilterErode. For Roto, RotoPaint, Keyer, Blur always sets channel to alpha

import nuke

def create_blur_node(channels=None, size_expr=None):
    blur = nuke.createNode("Blur")
    if size_expr is not None:
        blur["size"].setExpression(size_expr)
    if channels is not None:
        blur["channels"].setValue(channels)
    return blur

def linkBlurToErode():
    nodes = nuke.selectedNodes()
    if len(nodes) != 1:
        return
    node = nodes[0]
    if node.Class() in ["FilterErode", "Erode", "Dilate"]:
        create_blur_node(
            channels=node["channels"].value(),
            size_expr=f"abs({node.name()}.size)"
        )
    elif node.Class() in ["Roto", "RotoPaint"]:
        if node["output"].value() == "alpha":
            create_blur_node(channels="alpha")
    elif node.Class() == "Keyer":
        create_blur_node(channels="alpha")
