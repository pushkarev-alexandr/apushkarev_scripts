# Creates a Transform node from a Roto or RotoPaint curve with animation along the curve,
# and an expression for rotation following the curve's direction.

# Usage:
# Select one or more Roto or RotoPaint nodes.
# Click "Follow Path".
# A Transform node will be created with its pivot at (0, 0), and its translation animated along the selected curve.
# The "rotate" knob will have an expression that rotates the element along the direction of movement.
# The initial orientation should be set manually, and the object should be positioned in the lower-left corner.
# If multiple curves exist in the Roto, a Transform will be created for the selected curve, or for all curves if none are selected.
# You can also draw a curve using the Brush tool.

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke, nukescripts
import re

def getCurves(layer):
    curves = []
    for element in layer:
        if isinstance(element, nuke.rotopaint.Layer):
            curves += getCurves(element)
        elif isinstance(element, nuke.rotopaint.Stroke) or isinstance(element, nuke.rotopaint.Shape):
            curves.append(element)
    return curves

def FollowPath():
    nodes = nuke.selectedNodes("Roto") + nuke.selectedNodes("RotoPaint")
    if not nodes:
        nuke.message("Select <b>Roto</b> or <b>Rotopaint</b> node")
        return
    nodes.reverse()
    ff = nuke.root().firstFrame()
    lf = nuke.root().lastFrame()
    res = nuke.getInput("Animation Framerange:", f"{ff}-{lf}")
    if not res:
        return
    if not re.fullmatch(r"\d+-\d+", res):
        nuke.message("Invalid Framerange")
        return
    spl = res.split("-")
    ff = int(spl[0])
    lf = int(spl[1])
    for node in nodes:
        nukescripts.clear_selection_recursive()
        node.setSelected(True)
        kn = node.knob("curves")
        curves = kn.getSelected()
        if not curves:
            curves = getCurves(kn.rootLayer)
        
        n = lf-ff + 1
        for curve in curves:
            transform = nuke.createNode("Transform", inpanel=False)
            transform["center"].setValue((0, 0))
            transform["rotate"].setExpression("-degrees(atan2(translate.x(frame+1)-translate.x(frame), translate.y(frame+1)-translate.y(frame)))")
            trKn = transform["translate"]
            trKn.setAnimated()
            for i in range(n):
                ind = i/(n - 1) 
                eval = curve.evaluate(0, nuke.frame()) if isinstance(curve, nuke.rotopaint.Shape) else curve.evaluate(0)
                xy = list(eval.getPoint(ind))[:2]
                trKn.setValueAt(xy[0], i + ff, 0)
                trKn.setValueAt(xy[1], i + ff, 1)
