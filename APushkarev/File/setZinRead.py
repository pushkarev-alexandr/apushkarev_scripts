# Replaces the IP address string in Read nodes with just Z in all Read nodes in the script

# v1.0.1
# created by: Pushkarev Aleksandr

# v1.0.1 Changed the 'frm' variable

import nuke

def setZinRead():
    frm = "//192.168.100.56/data"
    to = "Z:"
    
    for node in nuke.allNodes("Read"):
        kn = node.knob("file")
        kn.setValue(kn.value().replace(frm, to))
