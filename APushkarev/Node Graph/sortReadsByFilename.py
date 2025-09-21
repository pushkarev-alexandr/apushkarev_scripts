# Sorts/aligns selected Read nodes by their file name

# v1.0.1
# created by: Pushkarev Aleksandr

# v1.0.0 initial release
# v1.0.1 now sorting is done relative to the leftmost Read node

# TODO if there are numbers like _1, _2..., then _10 will come before _1, need to check this sorting

import nuke

def main():
    nodes = nuke.selectedNodes("Read")
    if not nodes:
        return

    nodes_dict: dict[str, nuke.Node] = {}
    for node in nodes:
        nodes_dict[node["file"].value()] = node

    # Align relative to the leftmost Read node
    x, y = nodes[-1].xpos(), nodes[-1].ypos()
    for node in nuke.selectedNodes():
        if node.xpos()<x:
            x, y = node.xpos(), node.ypos()

    for i, file in enumerate(sorted(nodes_dict)):
        node = nodes_dict[file]
        node.setXYpos(x + i * 110, y)
