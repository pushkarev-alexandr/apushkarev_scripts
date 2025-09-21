# Converts all animated knobs to trackers in a Tracker node

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke

def hasAnyAnimation(kn):
    """
    Checks if a knob has animation. If both channels are expressions or one is an expression and the other is not animated, returns False, because we cannot get a frame range from an expression.
    If one channel has animation and the other is an expression, we bake the expression within the animation range.
    """
    return any([kn.isAnimated(0) and not kn.hasExpression(0), kn.isAnimated(1) and not kn.hasExpression(1)])

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

def alreadyHad(node, name, index):
    """Checks if the exact same animation already exists in previously processed knobs"""
    toScr = node[name+str(index)].toScript()
    for n in ["to", "from"]:
        for i in range(1, 5):
            if n!=name or i!= index:
                if node[n+str(i)].toScript()==toScr:
                    return True
            else:
                return False

def cornerPinToTracker():
    """
    Converts all animated knobs to trackers in a Tracker node. If the same animation already exists, a new tracker with identical animation will not be created.
    Knobs with expressions are converted only if one of the channels has baked animation.
    """
    sel = [n for n in nuke.selectedNodes() if n.Class()=="CornerPin2D"]
    if not sel:
        return
    elif len(sel)!=1:
        nuke.message("Select only one CornerPin node")
        return
    node = sel[0]
    tracker = None
    newTracks = 0
    for n in ["to", "from"]:
        for i in range(1, 5):
            knName = n+str(i)
            kn = node.knob(knName)
            if hasAnyAnimation(kn) and not alreadyHad(node, n, i):
                if not tracker:
                    tracker = nuke.createNode("Tracker4")
                tracks = tracker.knob("tracks")
                tracker.knob("add_track").execute()
                for t in getTimesForXY(kn):
                    chan = 2+31*newTracks
                    x = kn.getValueAt(t, 0)
                    y = kn.getValueAt(t, 1)
                    tracks.setValueAt(x, t, chan)
                    tracks.setValueAt(y, t, chan+1)
                newTracks+=1
                newTrackName = tracks.toScript().replace("track 1", knName)
                tracks.fromScript(newTrackName)
