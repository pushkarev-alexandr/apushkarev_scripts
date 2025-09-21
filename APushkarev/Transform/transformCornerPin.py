# Transforms CornerPin points
# Usefull if your image was transformed and you need CornerPin node to be transformed as well

#v1.0.0
#created by: Pushkarev Aleksandr

import nuke

def getTimesForXY(kn):
    times = []
    for j in range(2):
        for n in range(kn.getNumKeys(j)):
            t = kn.getKeyTime(n, j)
            if t not in times:
                times.append(t)
    if times:
        return times
    else:
        return [nuke.frame()]

def transformCornerPin():
    selected = nuke.selectedNodes()
    cornerPinsList = [node for node in selected if node.Class()=="CornerPin2D"]
    transformsList = [node for node in selected if node.Class()=="Transform"]
    if not (cornerPinsList and transformsList):
        nuke.message("Select CornerPin and Transform nodes")
        return
    if len(transformsList)>1:
        nuke.message("Select one Transform node")
        return
    
    transformMatrix = transformsList[0]["matrix"].value()
    for cNode in cornerPinsList:
        for tf in ["to", "from"]:
            for i in range(1, 5):
                kn = cNode.knob(tf+str(i))
                for t in getTimesForXY(kn):
                    x = kn.getValueAt(t, 0)
                    y = kn.getValueAt(t, 1)
                    res = transformMatrix*nuke.math.Vector4(x, y, 0, 1)
                    kn.setValueAt(res.x, t, 0)
                    kn.setValueAt(res.y, t, 1)
