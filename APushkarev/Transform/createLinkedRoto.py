# Select the Tracker node, press O or P and a linked Roto or RotoPaint will be created

# v1.0.1
# created by: Pushkarev Aleksandr

# changelog:
# v1.0.0 - initial release
# v1.0.1 - deselect before creating the Roto node so it doesn't get connected anywhere

import nuke

def createLinkedRoto(rotoname = 'Roto'):
    """rotoname can be Roto or RotoPaint"""
    sel = nuke.selectedNodes()
    if len(sel) == 1 and sel[0].Class() == 'Tracker4':
        tracker = sel[0]
        tracker.setSelected(False)
        roto = nuke.createNode(rotoname)
        name = tracker.name()
        curvesKn = roto.knob('curves')
        rootTrans = curvesKn.rootLayer.getTransform()
        for i in range(2):
            rootTrans.getTranslationAnimCurve(i).expressionString = f"{name}.translate.{['x', 'y'][i]}"
            rootTrans.getTranslationAnimCurve(i).useExpression = True
            rootTrans.getScaleAnimCurve(i).expressionString = f"{name}.scale"
            rootTrans.getScaleAnimCurve(i).useExpression = True
            rootTrans.getPivotPointAnimCurve(i).expressionString = f"{name}.center.{['x', 'y'][i]}"
            rootTrans.getPivotPointAnimCurve(i).useExpression = True
        rootTrans.getRotationAnimCurve(2).expressionString = f"{name}.rotate"
        rootTrans.getRotationAnimCurve(2).useExpression = True
        curvesKn.changed()
        roto.setXYpos(tracker.xpos() + 70, tracker.ypos() + 60)
        roto.setInput(0, None)
    else:
        nuke.createNode(rotoname)
