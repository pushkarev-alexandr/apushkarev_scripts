"""
If a Switch node is selected, compares two images from the switch inputs using difference.
If two nodes are selected, compares them. If a Merge node is selected, deletes it.
If nothing is selected, creates a Merge node in difference mode.
"""

# v1.1.0
# created by: Pushkarev Aleksandr

import nuke, nukescripts

def viewDifference():
    sel = nuke.selectedNodes()
    if not sel:  # If no nodes are selected, just create a merge in difference mode
        nuke.createNode('Merge2', inpanel=False)['operation'].setValue('difference')
        return
    window = nuke.activeViewer()
    viewer = window.node()
    differNodes = None  # 2 nodes to connect the merge to
    node = sel[0]  # First selected node, check if it's a Switch
    dep = node.dependencies(nuke.INPUTS)  # What the first selected node is connected to
    if len(sel) == 1 and node.Class() == 'Switch' and len(dep) == 2:  # If one Switch node with two connected inputs is selected
        differNodes = dep  # Connect merge to them
    elif len(sel) == 2:  # If any two nodes are selected
        differNodes = sel  # Connect merge to them
    if differNodes:  # If there are nodes to connect merge to
        nukescripts.clear_selection_recursive()  # Clear selection to connect the node manually
        merge = nuke.createNode('Merge2', inpanel=False)
        merge['operation'].setValue('difference')
        for i, node in enumerate(differNodes):  # Connect merge, order doesn't matter
            merge.setInput(i, node)
        # Reset gain for the current input, so after deleting the merge the viewer and first input values are both 1
        viewer['gain'].setValue(1)
        for i in range(viewer.inputs()):  # Disconnect all connected viewer inputs
            viewer.setInput(i, None)
        viewer.setInput(0, merge)  # Set the first input to merge
        window.activateInput(0)  # Activate the first input, if the second input was active, without this command nothing will be visible in the viewer
        viewer['gain'].setValue(64)  # Set viewer gain to maximum
    elif len(sel) == 1 and node.Class() == 'Merge2':  # If one node is selected and it's a Merge, delete this node
        viewer['gain'].setValue(1)  # Reset viewer gain
        for i in range(viewer.inputs()):  # Disconnect viewer inputs
            viewer.setInput(i, None)
        nuke.delete(node)  # Delete merge
