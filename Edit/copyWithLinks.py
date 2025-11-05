# Copies the node and links all knobs to the copied node

# v2.1.0
# created by: Pushkarev Aleksandr

import nuke, nukescripts


forbiddenKnTypes = [nuke.Tab_Knob, nuke.Text_Knob, nuke.Obsolete_Knob, nuke.Script_Knob, nuke.PyScript_Knob, nuke.PythonCustomKnob]
gizmoGroupStart = ['name', 'help', 'onCreate', 'onDestroy', 'knobChanged', 'updateUI']
startOfCustomKn = ['lifetimeStart', 'lifetimeEnd', 'useLifetime', 'lock_connections', 'mapsize', 'window']
nodeForbiddenKnStart = ['enable', 'name', 'help', 'onCreate', 'onDestroy', 'knobChanged']

def preventSelfLinking(node, newNode):
    """
    Renames the knob if it has the same name as the node we want to link to.
    I already forgot why I did this, so I'm not using it for now, but I kept it because there was probably a precedent.
    """
    nn = node.name()
    kn = newNode.knob(nn)
    if kn:
        for i in range(1, 100):
            newName = nn + '_clone' + str(i)
            if not newNode.knob(newName):
                kn.setName(newName)
                break

def copyPasteNode(node):
        """Performs the necessary actions to copy the node"""
        xpos = node.xpos()
        ypos = node.ypos()
        node.setSelected(True)
        nuke.nodeCopy('%clipboard%')
        nukescripts.clear_selection_recursive()
        newNode = nuke.nodePaste('%clipboard%')
        newNode.setSelected(False)
        newNode.setXYpos(xpos + 100, ypos + 50)
        return newNode

def setExpressions(node, keys, fr, to):
    """Sets expressions on knobs in the specified range"""
    newNode = copyPasteNode(node)
    # preventSelfLinking(node, newNode)
    for i in range(fr, to):
        knName = keys[i]
        if type(node[knName]) not in forbiddenKnTypes:
            newNode[knName].setExpression(f'{node.name()}.{knName}')

def copyWithLinks():
    selected = nuke.selectedNodes()
    if not selected:
        return
    nukescripts.clear_selection_recursive()
    for node in selected:
        # Preparation
        keys = list(node.knobs().keys())  # Get the list of all knobs
        startOfCustomKnCopy = startOfCustomKn.copy()  # Since we modify the list, we get its copy each time and do not change the original list
        if keys.count('gizmo_file'):  # For gizmo, one more knob
            startOfCustomKnCopy.append('gizmo_file')
        eni = keys.index('enable') if 'enable' in keys else None  # Get the index of the enable knob for regular nodes
        namei = keys.index('name') if 'name' in keys else None  # Not all nodes have the enable knob, get the index of the name knob
        # -------------------
        if keys[0:6] == gizmoGroupStart:  # This is either a gizmo or a group
            lsi = keys.index('lifetimeStart')  # Need to find from which point linking is possible
            customKnIndex = lsi + len(startOfCustomKnCopy)
            if keys[lsi:customKnIndex] == startOfCustomKnCopy:  # If startOfCustomKn knobs exist, then after them are custom knobs
                setExpressions(node, keys, customKnIndex, len(keys))
        elif eni and keys[eni:eni + 6] == nodeForbiddenKnStart:  # Otherwise, if a regular node
            setExpressions(node, keys, 0, eni)
        elif eni == None and namei and keys[namei:namei + 5] == nodeForbiddenKnStart[1:]:  # Not all nodes have the enable knob (e.g., transform doesn't), but must have the name knob
            setExpressions(node, keys, 0, namei)
