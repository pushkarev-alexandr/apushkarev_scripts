# Sets the required resize to width or height. Sets shortcut. Adds a button to create a Reformat node with the format of the selected Read node.

# v1.1.0
# created by: Pushkarev Aleksandr

import nuke, nukescripts

def createReformat():
    nodes = nuke.selectedNodes()
    nukescripts.clear_selection_recursive()
    if not nodes:
        reformat = nuke.createNode('Reformat')
        reformat['format'].setValue(reformat['format'].value().name())
        return
    nodes.reverse()
    for node in nodes:
        node.setSelected(True)
        reformat = nuke.createNode('Reformat')
        nodeAspect = node.width()/node.height()
        reformat['resize'].setValue(['width', 'height'][nodeAspect>nuke.root().width()/nuke.root().height()])
        reformat['format'].setValue(reformat['format'].value().name())
        reformat.setSelected(False)

def formatFromSelected():
    nodes = nuke.selectedNodes()
    nukescripts.clear_selection_recursive()
    for node in nodes:
        reformat = nuke.createNode('Reformat', inpanel=False)
        reformat.setSelected(False)
        reformat['format'].setValue(node['format'].value().name())
        reformat.setXYpos(node.xpos()-100,node.ypos())
