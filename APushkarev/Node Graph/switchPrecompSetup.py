# Select a Write node, and this script will create a setup with a Switch node and a Read node to enable or disable precomp

#v1.0.2
#created by: Pushkarev Aleksandr

import nuke, os, re

#----Read from Write block-----

def isNukeSequence(s):
    """check if input string is sequence and can be used in read['file'].fromUserText() function"""
    if s.count("#") and s.count(" ")==1:
        nums = s.split(" ")[-1]
        if nums.count("-")==1 and nums.split("-")[0].isdigit() and nums.split("-")[1].isdigit():
            return True
    return False

def isSequence(s):
    if s.count("#") or re.search(r"%\d*d", s):
        return True
    else:
        return False

def removeFrameVar(s):
    return re.sub(r"%\d*d", "", re.sub(r"#", "", s))

def isSameSequence(s1, s2):
    if isSequence(s1)==isSequence(s2) and removeFrameVar(s1)==removeFrameVar(s2):
        return True
    return False

def unifyFrameVar(s):
    return re.sub(r"%\d*d", "%d", re.sub(r"#+", "%d", s))

def readFromWrite(node):
    file = node["file"].value()
    dirName = os.path.dirname(file)
    basename = os.path.basename(file)
    if os.path.isdir(dirName):
        lst = nuke.getFileNameList(dirName, False, False, False)
        if lst:
            for i in lst:
                cond1 = i==basename
                cond2 = isNukeSequence(i) and isSameSequence(i.split(" ")[0], basename)
                s1_pattern = unifyFrameVar(basename).replace("%d", "\d+")
                cond3 = isSequence(basename) and re.fullmatch(s1_pattern, i)
                if any([cond1, cond2, cond3]):
                    path = dirName + "/" + i
                    read = nuke.createNode("Read", inpanel=False)
                    read["file"].fromUserText(path)
                    if node["raw"].value():
                        read["raw"].setValue(True)
                    else:
                        read["colorspace"].setValue(node["colorspace"].value())
                    read["localizationPolicy"].setValue(0)
                    read["updateLocalization"].execute()
                    return read

#----Read from Write end-----


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

def inputsFromOneNodeToAnother(fromNode, toNode):
    """Takes all inputs connected to fromNode and connects them to toNode"""
    for depNode in fromNode.dependent(forceEvaluate = False):
        for i in range(depNode.inputs()):
            if depNode.input(i)==fromNode:
                depNode.setInput(i, toNode)

def switchPrecompSetup():
    try:
        write = nuke.selectedNode()
    except:
        return
    write.setSelected(False)
    input = write.input(0)
    write.setXYpos(write.xpos() + 110, write.ypos() + 10)
    input.setSelected(True)
    dot = nuke.createNode("Dot", inpanel=False)
    dot.setXpos(newXY(dot, input)[0])
    dot.setYpos(newXY(dot, write)[1])
    switch = nuke.createNode("Switch", inpanel=False)
    write.setInput(0, dot)
    switch.setYpos(switch.ypos() + 50)
    read = readFromWrite(write)
    if read:
        read.setSelected(False)
        switch.setSelected(True)
        read.setXpos(newXY(read, write)[0])
        read.setYpos(newXY(read, switch)[1])
        switch.setInput(1, read)
    inputsFromOneNodeToAnother(write, switch)
