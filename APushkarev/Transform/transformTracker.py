# Transforms all tracks in tracker node
# Usefull if your image was transformed and you need tracker node to be transformed as well

#v1.0.0
#created by: Pushkarev Aleksandr

import nuke

def getTracksNum(tracks):
    tracksnum = 0
    while not tracks.fullyQualifiedName(tracksnum * 31).endswith(".tracks"):
        tracksnum += 1
    return tracksnum

def getTimesForXY(tracks, i):
    times = []
    for j in range(2):
        chan = 2 + j + 31 * i
        for n in range(tracks.getNumKeys(chan)):
            t = tracks.getKeyTime(n, chan)
            if t not in times:
                times.append(t)
    return times

def transformTracker():
    selected = nuke.selectedNodes()
    trackersList = [node for node in selected if node.Class()=="Tracker4"]
    transformsList = [node for node in selected if node.Class()=="Transform"]
    if not (trackersList and transformsList):
        nuke.message("Select Tracker and Transform nodes")
        return
    if len(transformsList) > 1:
        nuke.message("Select one Transform node")
        return
    
    transformMatrix = transformsList[0]["matrix"].value()
    for tracker in trackersList:
        tracks = tracker["tracks"]
        for i in range(getTracksNum(tracks)):
            times = getTimesForXY(tracks, i)
            for t in times:
                chan = 2 + 31 * i
                x = tracks.getValueAt(t, chan)
                y = tracks.getValueAt(t, chan + 1)
                res = transformMatrix * nuke.math.Vector4(x, y, 0, 1)
                tracks.setValueAt(res.x, t, chan)
                tracks.setValueAt(res.y, t, chan + 1)
