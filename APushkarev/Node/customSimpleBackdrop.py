"""Custom backdrop creation, simplified version. Sets z_order correctly on creation, assigns a random backdrop color,
makes the backdrop slightly wider relative to selected nodes than standard, sets font size relative to backdrop size"""

# v1.0.1
# created by: Pushkarev Aleksandr

import nuke, nukescripts
import colorsys, random, os, getpass

def linerp(a, b, c, d, x):
    x = float(x)
    if x < a:
        return c
    elif x > b:
        return d
    else:
        ret = (x-a)*(d-c)/(b-a)+c
        return ret

def isInsideBackdrop(node, backdrop):
    """Returns True if the selected node is inside the selected backdrop"""
    nXl = node.xpos()
    nYt = node.ypos()
    nXr = nXl+node.screenWidth()
    nYb = nYt+node.screenHeight()
    bXl = backdrop.xpos()
    bYt = backdrop.ypos()
    bXr = bXl+backdrop.screenWidth()
    bYb = bYt+backdrop.screenHeight()
    if ((nXl < bXr and nXl > bXl) or (nXr < bXr and nXr > bXl)) and ((nYt < bYb and nYt > bYt) or (nYb < bYb and nYb > bYt)):
        return True
    else:
        return False

def insideBackdropsList(node):
    """Returns a list of backdrops inside which the selected node is located"""
    lst = []
    for backdrop in nuke.allNodes('BackdropNode'):
        if backdrop.name()!=node.name() and isInsideBackdrop(node,backdrop):
            lst.append(backdrop)
    return lst

def maxBackdropsZOrder(node):
    bLst = insideBackdropsList(node)
    l = len(bLst)
    if l>0:
        max = bLst[0].knob('z_order').value()
        for i in range(1,l):
            z = bLst[i].knob('z_order').value()
            if z>max:
                max=z
        return max
    else:
        return -1

def getOffset(z_order, backsMin):
    """Calculates how much to increase z_order so that the backdrop does not end up under the newly created backdrop"""
    if backsMin <= z_order:
        return z_order - backsMin + 1
    else:
        return 0

def createBackdrop():
    nodePath = os.path.dirname(__file__).replace('\\','/') + '/customSimpleBackdrop.nk'  # Pre-prepared backdrop with callbacks
    if not os.path.isfile(nodePath):  # If there's no such node, call the standard backdrop
        nukescripts.autobackdrop.autoBackdrop()
        return
    selected = nuke.selectedNodes()
    backdrop = nuke.nodePaste(nodePath)  # In any case, create the node, and then apply changes to it or not
    if selected:
        bdX = min([node.xpos() for node in selected])
        bdY = min([node.ypos() for node in selected])
        bdW = max([node.xpos() + node.screenWidth() for node in selected]) - bdX
        bdH = max([node.ypos() + node.screenHeight() for node in selected]) - bdY
        left, top, right, bottom = (-30, -35, 30, 30)
        bdX += left
        bdY += top
        bdW += (right - left)
        bdH += (bottom - top)
        fontSize = int(linerp(15000, 30000000, 25, 200, bdW * bdH))  # Set font size depending on backdrop size
        backdrop['note_font_size'].setValue(fontSize)
        extra = fontSize
        if bdW < 150:
            extra += 30
        backdrop['xpos'].setValue(bdX)
        backdrop['ypos'].setValue(bdY - extra)
        backdrop['bdwidth'].setValue(bdW)
        backdrop['bdheight'].setValue(bdH + extra)
    else:
        backdrop['center'].setValue(False)  # If nothing was selected, I usually use the backdrop for notes, so the center is not needed there
    # Set z_order for the new backdrop, 1 more than the maximum z_order of backdrops inside which our backdrop is located
    # Sets 0 if the new backdrop is not inside other backdrops
    # This prevents the new backdrop from being hidden behind those inside which it is created
    z_order = int(maxBackdropsZOrder(backdrop)+1)  # Set z_order to our backdrop after size manipulations!
    backdrop['z_order'].setValue(z_order)
    if selected:  # If there are selected nodes, find backdrops among them and shift them relative to our new backdrop
        selectedBackdrops = [n for n in selected if n.Class()=='BackdropNode']  # Select backdrops from selected nodes
        if selectedBackdrops:
            backsMin = min([n['z_order'].value() for n in selectedBackdrops])  # Find the minimum z_order among them
            offset = getOffset(z_order,backsMin)  # Get offset for selected nodes, if they need to be shifted (by how much we need to shift the minimum, we shift all the others by the same amount)
            if offset:  # Shift if the offset is not zero
                for node in selectedBackdrops:
                    node['z_order'].setValue(node['z_order'].value() + offset)

    if getpass.getuser() in ['abelousov']:
        backdrop.knob('tile_color').setValue(1061109759)  # Lekha asked for a gray backdrop
    else:
        R, G, B = colorsys.hsv_to_rgb(random.random(),random.uniform(0.2,0.5),random.uniform(0.2,0.8))  # Random color with reduced saturation and brightness
        backdrop.knob('tile_color').setValue(int('%02x%02x%02x%02x' % (int(R*255), int(G*255), int(B*255), 255), 16))  # Set random color
    backdrop.showControlPanel()

    for node in selected:  # Select nodes so the backdrop can be dragged with nodes immediately
        node.setSelected(True)
    return backdrop
