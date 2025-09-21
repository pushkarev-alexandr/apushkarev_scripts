# Replaces the standard merge, connects the B input, and places the merge node below
# If multiple nodes are selected, creates a stack of multiple merges

# v1.2.0
# created by: Pushkarev Aleksandr

import nuke, nukescripts

def center(node):
    """Returns center of the node"""
    x = node.xpos() + node.screenWidth() / 2
    y = node.ypos() + node.screenHeight() / 2
    return [x, y]

def newXY(node1, node2):
    """Returns x,y coordinates for node1 to be placed in center of node2"""
    c = center(node2)
    x = c[0] - node1.screenWidth() / 2
    y = c[1] - node1.screenHeight() / 2
    return [int(x), int(y)]

def nodesInputsDict(node):
    res = {}
    for dep in node.dependent(nuke.INPUTS, False):
        for i in range(dep.inputs()):
            if dep.input(i).name()==node.name():
                res[dep] = i
    return res

def restoreInputs(node, nodesDict):
    for n, i in nodesDict.items():
        n.setInput(i, node)

def smartMerge():
    padding = 80
    selected = nuke.selectedNodes()
    if not selected:
        nuke.createNode("Merge2")
        return
    nukescripts.clear_selection_recursive()
    if len(selected)==1:
        merge = nuke.createNode("Merge2")
        merge.setInput(0, selected[0])
        xy = newXY(merge, selected[0])
        merge.setXYpos(xy[0], xy[1] + padding)
    selected.reverse()
    merges=[]
    nodesDict = nodesInputsDict(selected[0])
    for i in range(len(selected)-1):
        merge = nuke.createNode("Merge2")
        merge.setSelected(False)
        dot = nuke.createNode("Dot")
        dot.setSelected(False)
        if i==0:
            merge.setInput(0, selected[i])
            xy1 = newXY(merge, selected[i])
            xy2 = newXY(merge, selected[i + 1])
            merge.setXYpos(xy1[0], max(xy1[1], xy2[1]) + padding)
        else:
            merge.setInput(0, merges[-1])
            xy1 = newXY(merge, merges[-1])
            xy2 = newXY(merge, selected[i + 1])
            merge.setXYpos(xy1[0], max(xy1[1], xy2[1]) + padding)
        merge.setInput(1, dot)
        dot.setInput(0, selected[i + 1])
        dotx = newXY(dot, selected[i + 1])[0]
        doty = newXY(dot, merge)[1]
        dot.setXYpos(dotx, doty)
        merges.append(merge)
    restoreInputs(merge, nodesDict)
