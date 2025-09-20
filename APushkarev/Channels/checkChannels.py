# Selects two nodes, the script checks if the channels in these two nodes match,
# useful for comparing if channels are missing in a new render or if new ones have appeared

# v1.0.0
# created by: Pushkarev Aleksandr

#TODO: output differing channels

import nuke

def checkChannels():
    nodes = nuke.selectedNodes()
    if len(nodes) != 2:
        nuke.message("You need to select 2 nodes")
        return
    if nodes[0].channels() != nodes[1].channels():
        nuke.message("Channels are different")
    else:
        nuke.message("Channels match!")
