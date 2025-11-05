# Creates a Shuffle2 node and immediately merges rgb into the P or N channel if the Read node's filename contains _P_ or _N_

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke, os

def inputsFromOneNodeToAnother(fromNode,toNode):
    for depNode in fromNode.dependent(forceEvaluate = False):
        for i in range(depNode.inputs()):
            if depNode.input(i) == fromNode:
                depNode.setInput(i, toNode)

def createNode(cl):
    sel = nuke.selectedNodes()
    try:
        node = nuke.createNode(cl)
    except:
        return
    for n in sel:
        inputsFromOneNodeToAnother(n,node)
    if sel:
        node.autoplace()

def createShuffleNode():
    sel = nuke.selectedNodes()
    if len(sel) == 2 and sel[0].Class() == 'Read' and sel[1].Class() == 'Read':
        pNode = None
        beautyNode = None
        for i, n in enumerate(sel):
            file = n['file'].value()
            base = os.path.basename(file)
            if base.count('_P_') or base.count('_N_'):
                layerNode = n
                beautyNode = sel[1 - i]
                if base.count('_P_'):
                    layerName = 'P'
                else:
                    layerName = 'N'
                break
        if layerNode and beautyNode:
            shuffle = nuke.createNode('Shuffle2')
            shuffle.setInput(0, beautyNode)
            shuffle.setInput(1, layerNode)
            shuffle['fromInput1'].setValue('A')
            shuffle['in1'].setValue('rgb')
            if layerName not in nuke.layers():
                nuke.Layer(layerName, [layerName + '.red', layerName + '.green', layerName + '.blue'])
                shuffle['out1'].setValue(layerName)
                shuffle['mappings'].setValue([(0, 'rgba.red', layerName + '.red'), (0, 'rgba.green', layerName + '.green'), (0, 'rgba.blue', layerName + '.blue')])
            else:
                shuffle['out1'].setValue(layerName)
                colors = ['red', 'green', 'blue']
                layerChannels = [ch for ch in nuke.channels() if ch.startswith(layerName + '.')]
                for i, ch in enumerate(layerChannels):
                    if i < 3:
                        shuffle['mappings'].setValue([(0, 'rgba.' + colors[i], ch)])
                    else:
                        shuffle['mappings'].setValue([(-1, 'black', ch)])
            return
    createNode('Shuffle2')
