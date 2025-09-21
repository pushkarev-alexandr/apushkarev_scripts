# Merges multiple selected Tracker nodes into a single node

#v1.0.0
#created by: Pushkarev Aleksandr

import nuke, nukescripts

def xmlSplitter(xml):
    res = []
    openedCount = 0
    openedI = -1
    closedCount = 0
    closedI = -1
    for i, letter in enumerate(xml):
        if letter=="{":
            openedCount+=1
            if openedCount==1:
                openedI = i
        if letter=="}":
            closedCount+=1
            if openedCount==closedCount and openedCount!=0:
                closedI=i
                res.append(xml[openedI:closedI+1])
                openedCount = 0
                openedI = -1
                closedCount = 0
                closedI = -1
    return res

def mergeTrackers():
    selected = nuke.selectedNodes()
    selected = [i for i in selected if i.Class()=="Tracker4"]  # Only trackers sort
    if not selected or len(selected)==1:
        return
    nukescripts.clear_selection_recursive()
    tracks = nuke.createNode("Tracker4").knob("tracks")
    baseParts = xmlSplitter(tracks.toScript())
    
    curvesFinal = ""
    count = 0
    for node in selected:
        nodesBaseParts = xmlSplitter(node.knob("tracks").toScript())
        nodesCurvesXML = nodesBaseParts[2][1:-2]
        count+=len(xmlSplitter(nodesCurvesXML))
        curvesFinal+=nodesCurvesXML
    spl = baseParts[0].split(" ")
    spl[3] = str(count)
    baseParts[0] = " ".join(spl)
    baseParts[2] = "{" + curvesFinal + "\n}"
    tracks.fromScript("\n".join(baseParts))
