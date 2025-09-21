# Copies the alpha channel from the second selected node into the red channel of the first selected node to evaluate where the alpha is used
# If run again, removes the ChannelMerge node

#v1.0.0
#created by: Pushkarev Aleksandr

import nuke, nukescripts

def viewMask():
    sel = nuke.selectedNodes()
    if len(sel)==1 and sel[0].Class()=="ChannelMerge" and sel[0]["B"].value()=="red" and sel[0]["output"].value()=="red" and sel[0]["A"].value()=="alpha":
        nuke.delete(sel[0])
        return
    sel.reverse()
    if len(sel)!=2:
        return
    nukescripts.clear_selection_recursive()
    merge = nuke.createNode("ChannelMerge", inpanel=False)
    for i, n in enumerate(sel):
        merge.setInput(i, n)
    x1 = sel[0].xpos()
    x2 = sel[1].xpos()
    x = int(x1-(x1-x2)/2)
    merge.setXpos(x)
    y = max(sel[0].ypos(), sel[1].ypos())+50
    merge.setYpos(y)
    merge["B"].setValue("red")
    merge["output"].setValue("red")
    viewer = nuke.activeViewer().node()
    for i in range(viewer.inputs()):
            viewer.setInput(i, None)
    viewer.setInput(0, merge)
