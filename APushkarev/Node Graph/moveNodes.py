# Allows moving selected nodes

# v1.0.0
# created by: Pushkarev Aleksandr

# v1.0.0 initial release

import nuke

moveStep = 20

def moveSel_up():
    for n in nuke.selectedNodes():
        n.setYpos(int(n.ypos() - moveStep))
        
def moveSel_down():
    for n in nuke.selectedNodes():
        n.setYpos(int(n.ypos() + moveStep))
        
def moveSel_right():
    for n in nuke.selectedNodes():
        n.setXpos(int(n.xpos() + moveStep))
        
def moveSel_left():
    for n in nuke.selectedNodes():
        n.setXpos(int(n.xpos() - moveStep))
