# For selected Read nodes (or all Read nodes if nothing is selected), replaces relative paths with absolute paths using getEvaluatedValue

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke, os

def bakeRelativePaths():
    nodes = nuke.selectedNodes()
    if not nodes:
        nodes = nuke.allNodes("Read")
    for node in nodes:
        kn = node["file"]
        spl = list(os.path.split(kn.value()))
        spl[0] = os.path.dirname(kn.getEvaluatedValue())
        kn.setValue("/".join(spl))
