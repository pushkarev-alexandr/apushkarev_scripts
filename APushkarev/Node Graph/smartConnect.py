# v1.0.1
# create by: Pushkarev Aleksandr

import nuke

def center(node):
    """Returns center of the node"""
    x = node.xpos() + node.screenWidth() / 2
    y = node.ypos() + node.screenHeight() / 2
    return [x, y]

def newXY(node,center):
    x = center[0] - node.screenWidth() / 2
    y = center[1] - node.screenHeight() / 2
    return [x, y]

def smartConnect():
    selected = nuke.selectedNodes()
    if not selected:
        return
    if len(selected)==1:
        if selected[0].Class()=="Dot":
            node = selected[0]
            top = node.input(0)
            dep = node.dependent(nuke.INPUTS, forceEvaluate = False)
            bottom = dep[0]
            if abs(top.xpos()-node.xpos())<abs(bottom.xpos()-node.xpos()):
                node.setXpos(int(newXY(node,center(top))[0]))
                node.setYpos(int(newXY(node,center(bottom))[1]))
            else:
                node.setXpos(int(newXY(node,center(bottom))[0]))
                node.setYpos(int(newXY(node,center(top))[1]))
            return
        else:
            return
    selected.reverse()
    node1 = selected[0]
    node2 = selected[1]
    node1.setInput(0,node2)
    if len(selected)>2:
        node1.setInput(1,selected[2])
    x1 = node1.xpos()
    y1 = node1.ypos()
    x2 = node2.xpos()
    y2 = node2.ypos()
    if abs(x2-x1)<abs(y2-y1):
        node1.setXpos(int(newXY(node1,center(node2))[0]))
    else:
        node1.setYpos(int(newXY(node1,center(node2))[1]))
