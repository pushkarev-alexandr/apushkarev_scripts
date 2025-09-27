# Automatically updates the Read node localization after rendering is complete (works only in GUI).
# Does not enable localization itself—if localization is not enabled in the Read node, it will not be turned on by this script.
# Safe for users who do not use localization.
# Installation: add to menu.py
# from updateLocalization import updateLocalizationMain
# nuke.addAfterRender(updateLocalizationMain)

# v1.1.0
# created by: Pushkarev Aleksandr

import nuke, threading, re

class updateLocalThread(threading.Thread):
    def __init__(self, node):
        threading.Thread.__init__(self)
        self.node = node
    
    def run(self):
        nuke.executeInMainThread(self.node.knob("updateLocalization").execute)

def isSequence(s):
    if s.count("#") or re.search(r"%\d*d", s):
        return True
    else:
        return False

def removeFrameVar(s):
    return re.sub(r"%\d*d", "", re.sub(r"#", "", s))

def isSameSequence(s1, s2):
    if isSequence(s1)==isSequence(s2) and removeFrameVar(s1)==removeFrameVar(s2):
        return True
    return False

def updateLocalizationMain():
    write = nuke.thisNode()
    path = write["file"].value()
    for node in nuke.allNodes("Read"):
        v = node.knob("file").value()
        if v==path or isSameSequence(v, path):
            updateLocalThread(node).start()
