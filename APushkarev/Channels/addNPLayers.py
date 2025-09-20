# Adds N and P layers which are not present in Nuke by default but are very necessary

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke

def addNPLayers():
    layers = ["N", "P"]
    for layer in layers:
        if layer not in nuke.layers():
            nuke.Layer(layer, [layer + ".red", layer + ".green", layer + ".blue", layer + ".alpha"])
