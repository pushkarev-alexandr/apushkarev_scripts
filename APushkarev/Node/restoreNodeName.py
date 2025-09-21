# Sets the node name based on its class name

#v1.1.0
#created by: Pushkarev Aleksandr

import nuke

def restoreNodeName():
    for node in nuke.selectedNodes():
        cl = node.Class()
        if cl=="Roto":
            node["output"].setValue("alpha")
        for i in range(1,500):
            if not nuke.toNode(cl+str(i)):
                node["name"].setValue(cl+str(i))
                break
