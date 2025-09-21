# Distorts position of 2d tracking points by 3DE4 lens distortion node

# v1.2.0
# created by: Pushkarev Aleksandr

import nuke, nukescripts, re

class distortTrackPanel(nukescripts.PythonPanel):
    """Panel to get Resolution scale, ranged between 1-10"""
    def __init__(self):
        nukescripts.PythonPanel.__init__(self, "Distort Track")
        self.resKn = nuke.Int_Knob("resolution scale", "Resolution Scale")
        self.resKn.setValue(8)
        self.textKn = nuke.Text_Knob("txt", "", "<i>Decrease this value if your tracking point is outside the format</i><br><i>and result is clipped by borders of format</i>")
        self.addKnob(self.resKn)
        self.addKnob(self.textKn)
    
    def knobChanged(self, kn):
        if self.resKn is kn:
            if self.resKn.value() > 10:
                self.resKn.setValue(10)
            elif self.resKn.value() < 1:
                self.resKn.setValue(1)

def tde4Lst():
    """Gets all LD_3DE4 nodes available in menu"""
    res = []
    m = nuke.menu("Nodes").menu("3DE4")
    if m:
        for i in m.items():
            s = i.script()
            if s.startswith("nuke.createNode(") and s.endswith(")"):
                r = re.search("LD_3DE.*", s[0:-2])
                if r:
                    res.append(r.group())
    return res

def getTracksNum(tracks):
    """Gets number of 2d tracker points"""
    tracksnum = 0
    while not tracks.fullyQualifiedName(tracksnum * 31).endswith(".tracks"):
        tracksnum+=1
    return tracksnum

def getTimesForXY(tracks, i):
    """Gets all key times for specific tracker point (function getKeyList doesn't support per channel selection)"""
    times = []
    for j in range(2):
        chan = 2 + j + 31 * i
        for n in range(tracks.getNumKeys(chan)):
            t = tracks.getKeyTime(n, chan)
            if t not in times:
                times.append(t)
    return times

def getMaxMinXY(tracks, i):
    """List of [maxX, maxY, minX, minY]"""
    times = getTimesForXY(tracks, i)
    if not times:
        return []
    xCh = 2 + 31 * i
    yCh = 3 + 31 * i
    maxX = tracks.getValueAt(times[0], xCh)
    maxY = tracks.getValueAt(times[0], yCh)
    minX = maxX
    minY = maxY
    for t in times:
        x = tracks.getValueAt(t, xCh)
        y = tracks.getValueAt(t, yCh)
        if x > maxX:
            maxX = x
        if y > maxY:
            maxY = y
        if x < minX:
            minX = x
        if y < minY:
            minY = y
    return [maxX, maxY, minX, minY]

def setupCropNode(crop, tracks, i):
    """Sets bbox to maximum values for particular tracker point"""
    topNode = crop.input(0)
    if topNode:
        curBBox = topNode.bbox()
        maxMinXY = getMaxMinXY(tracks, i)
        padding = 10
        if (curBBox.w() + curBBox.x()) < maxMinXY[0]:
            crop["box"].setValue(maxMinXY[0] + padding, 2)
        else:
            crop["box"].setValue(curBBox.w() + curBBox.x() + padding, 2)
        if curBBox.x() > maxMinXY[2]:
            crop["box"].setValue(maxMinXY[2]-padding, 0)
        else:
            crop["box"].setValue(curBBox.x()-padding, 0)
        
        if (curBBox.h() + curBBox.y()) < maxMinXY[1]:
            crop["box"].setValue(maxMinXY[1] + padding, 3)
        else:
            crop["box"].setValue(curBBox.h() + curBBox.y() + padding, 3)
        if curBBox.y() > maxMinXY[3]:
            crop["box"].setValue(maxMinXY[3]-padding, 1)
        else:
            crop["box"].setValue(curBBox.y()-padding, 1)

def distortTracker():
    # Check selected nodes
    sel = nuke.selectedNodes()
    trackers = [n for n in sel if n.Class()=="Tracker4"]
    distorts = [n for n in sel if n.Class() in tde4Lst()]
    if not trackers or len(distorts)!=1:
        nuke.message("Select Tracker nodes and one 3DE4 distortion node")
        return

    # Resolution scale dialog
    p = distortTrackPanel()
    if not p.showModalDialog():
        return
    resolutionScale = p.resKn.value()
    
    # Distort node setup
    distort = distorts[0]
    distort["disable"].setValue(False)
    dirKn = distort["direction"]
    dirKn.setValue(int(1-dirKn.getValue()))#invert direction
    modeKn = distort["mode"]
    orMode = modeKn.value()#store initial mode value
    modeKn.setValue("STMap")

    # If distort is not connected to any node, connect it to constant
    # To get format from it and make stmap appear in distort node
    if not distort.inputs():
        cons = nuke.createNode("Constant", inpanel=False)
        #cons["color"].setValue(1)
        distort.setInput(0, cons)
    
    # Set node distort connected to selected, to automatically connect new nodes
    if distort.inputs():
        nukescripts.clear_selection_recursive()
        distort.input(0).setSelected(True)
    # Crop is needed to get stmap works outside format
    crop = nuke.createNode("Crop", inpanel=False)
    formatWidth = crop.width()
    formatHeight = crop.height()
    # Reformat is needed to increase stmap resolution for precise result
    reformat = nuke.createNode("Reformat", inpanel=False)
    reformat["type"].setValue("scale")
    reformat["scale"].setValue(resolutionScale)
    reformat["pbb"].setValue(True)
    
    # Transform needs for STMap translation if tracking point is outside of format 
    nukescripts.clear_selection_recursive()
    distort.setSelected(True)
    transform = nuke.createNode("Transform", inpanel=False)
    transform["filter"].setValue("impulse")

    # Main cycle
    for tracker in trackers:
        tracks = tracker.knob("tracks")
        for i in range(getTracksNum(tracks)):
            setupCropNode(crop, tracks, i)  # Check
            for t in getTimesForXY(tracks, i):
                chan = 2 + 31 * i
                x = tracks.getValueAt(t, chan)
                y = tracks.getValueAt(t, chan + 1)
                xScaled = x * resolutionScale
                yScaled = y * resolutionScale
                # If tracking point is outside of format, translate STMap to sample correct value
                if x > formatWidth or x < 0 or y > formatHeight or y < 0:
                    transform["translate"].setValue(-xScaled, 0)
                    transform["translate"].setValue(-yScaled, 1)
                    newX = transform.sample("red", 0, 0)
                    newY = transform.sample("green", 0, 0)
                else:
                    transform["translate"].setValue(0, 0)
                    transform["translate"].setValue(0, 1)
                    newX = transform.sample("red", xScaled, yScaled)
                    newY = transform.sample("green", xScaled, yScaled)
                newX *= formatWidth
                newY *= formatHeight
                tracks.setValueAt(newX, t, chan)
                tracks.setValueAt(newY, t, chan + 1)
    
    # Delete nodes and restore distort initial values
    try:
        nuke.delete(cons)
    except:
        pass
    nuke.delete(crop)
    nuke.delete(reformat)
    nuke.delete(transform)
    dirKn.setValue(int(1-dirKn.getValue()))  # Invert direction back
    modeKn.setValue(orMode)
