# If the Roto or RotoPaint node was created with a selected CornerPin, matchmove the root layer of the created Roto or RotoPaint node

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke, itertools

def getCornerPinTimes(node):
    times = []
    for toFrom in ['to', 'from']:
        for i in range(4):
            kn = node[toFrom + str(i + 1)]
            for c in range(2):
                for n in range(kn.getNumKeys(c)):
                    t = kn.getKeyTime(n, c)
                    if t not in times:
                        times.append(t)
    if times:
        return times
    else:
        return [nuke.frame()]

def convertCornerPinToMatrix(valuesTO, valuesFROM):
    valuesTO = list(itertools.chain(*valuesTO))
    valuesFROM = list(itertools.chain(*valuesFROM))

    matrixTo = nuke.math.Matrix4()
    matrixFrom = nuke.math.Matrix4()
    
    matrixTo.mapUnitSquareToQuad(*valuesTO)
    matrixFrom.mapUnitSquareToQuad(*valuesFROM)

    matrixFromCornerPin = matrixTo * matrixFrom.inverse()
    matrixFromCornerPin.transpose()

    return matrixFromCornerPin

def storeCornerPinValues(node):
    lst = []
    for toFrom in ['to', 'from']:
        for i in range(4):
            kn = node[toFrom + str(i + 1)]
            lst.append(kn.toScript())
    return lst

def restoreCornerPin(node,lst):
    for j,toFrom in enumerate(['to', 'from']):
        for i in range(4):
            kn = node[toFrom + str(i + 1)]
            kn.fromScript(lst[4 * j + i])

def matchmoveCornerPin(node):
    if not node['from1'].isAnimated():
        for i in range(4):
            node['from' + str(i + 1)].fromScript(node['to' + str(i + 1)].toScript())
    if not node['to1'].isAnimated():
        for i in range(4):
            node['to' + str(i + 1)].fromScript(node['from' + str(i + 1)].toScript())
    for i in range(4):
        node['from' + str(i + 1)].clearAnimated()

def matchmoveFromCornerPin():
    roto = nuke.thisNode()
    sel = nuke.selectedNodes()
    if len(sel) == 1 and sel[0].Class() == 'CornerPin2D':
        cpNode = sel[0]
        storedValues = storeCornerPinValues(cpNode)  # Store the values in the node before matchmoving, so they can be restored later
        matchmoveCornerPin(cpNode)  # Matchmove the node at the current frame
        times = getCornerPinTimes(cpNode)
        root = roto.knob('curves').rootLayer
        for t in times:
            valuesTO = [cpNode[kn].valueAt(t) for kn in ['to1', 'to2', 'to3', 'to4']]
            valuesFROM = [cpNode[kn].valueAt(t) for kn in ['from1', 'from2', 'from3', 'from4']]
            transformMatrix = convertCornerPinToMatrix(valuesTO, valuesFROM)
            
            for i in range(16):
                matrixAnimCurve = root.getTransform().getExtraMatrixAnimCurve(0, i)
                matrixAnimCurve.addKey(t, transformMatrix[i])
        roto.knob('curves').changed()
        restoreCornerPin(cpNode,storedValues)

# Does not work because Roto has no name
def matchmoveFromTracker():
    roto = nuke.thisNode()
    print('RotoName: ' + roto['name'].value())
    sel = nuke.selectedNodes()
    if len(sel) == 1 and sel[0].Class() == 'Tracker4':
        tracker = sel[0]
        name = roto['name'].value()
        curvesKn = roto.knob('curves')
        rootTrans = curvesKn.rootLayer.getTransform()
        rootTrans.getTranslationAnimCurve(0).expressionString = f'{name}.translate.x'
        rootTrans.getTranslationAnimCurve(0).useExpression = True
        rootTrans.getTranslationAnimCurve(1).expressionString = f'{name}.translate.y'
        rootTrans.getTranslationAnimCurve(1).useExpression = True
        rootTrans.getRotationAnimCurve(2).expressionString = f'{name}.rotate'
        rootTrans.getRotationAnimCurve(2).useExpression = True
        rootTrans.getScaleAnimCurve(0).expressionString = f'{name}.scale'
        rootTrans.getScaleAnimCurve(0).useExpression = True
        rootTrans.getScaleAnimCurve(1).expressionString = f'{name}.scale'
        rootTrans.getScaleAnimCurve(1).useExpression = True
        rootTrans.getPivotPointAnimCurve(0).expressionString = f'{name}.center.x'
        rootTrans.getPivotPointAnimCurve(0).useExpression = True
        rootTrans.getPivotPointAnimCurve(1).expressionString = f'{name}.center.y'
        rootTrans.getPivotPointAnimCurve(1).useExpression = True
        curvesKn.changed()

nuke.addOnUserCreate(matchmoveFromCornerPin, nodeClass='Roto')
nuke.addOnUserCreate(matchmoveFromCornerPin, nodeClass='RotoPaint')
