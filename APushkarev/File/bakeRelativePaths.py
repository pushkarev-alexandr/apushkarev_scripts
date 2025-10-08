# For selected Read nodes (or all Read nodes if nothing is selected), replaces relative paths with absolute paths using getEvaluatedValue

# v1.1.0
# created by: Pushkarev Aleksandr

import nuke, os

def bakeRelativePaths():
    nodes = nuke.selectedNodes()
    if not nodes:
        nodes = nuke.allNodes("Read")
    for node in nodes:
        kn = node["file"]
        spl = list(os.path.split(kn.value()))

        loc_knob = node["localizationPolicy"]
        loc_value = loc_knob.value()
        loc_knob.setValue("off")
        spl[0] = os.path.dirname(kn.getEvaluatedValue())
        loc_knob.setValue(loc_value)

        kn.setValue("/".join(spl))
