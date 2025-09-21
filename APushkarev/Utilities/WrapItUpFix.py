# Fixes the naming of Read nodes to work correctly with WrapItUp

#v1.0.0
#created by: Pushkarev Aleksandr

import nuke

def WrapItUpFix():
    for node in nuke.allNodes("Read"):
        kn = node["file"]
        val = kn.value()
        for pattern in [".%d.exr", "_%d.exr"]:
            if val.count(pattern):
                kn.setValue(val.replace(pattern, pattern.replace("%d", "%04d")))
