# Instead of a fan of inputs diverging from a single point, creates a grid

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke, nukescripts
import gfx_nuke

def check_nodes_connected_to_the_dot(nodes):
    """Returns dot all nodes connected to or None if no such node"""
    dot = None
    message = "All nodes have to be connected to {}<b>Dot</b> node!"
    for node in nodes:
        inpt = node.input(0)
        if inpt is None or inpt.Class() != "Dot":
            nuke.message(message.format(""))
            return
        if dot is None:
            dot = inpt
        elif inpt!=dot:
            nuke.message(message.format("the same "))
            return
    return dot

def main():
    nodes = nuke.selectedNodes()
    if len(nodes)<2:
        nuke.message("Select at least 2 nodes!")
        return
    nukescripts.clear_selection_recursive()

    main_dot = check_nodes_connected_to_the_dot(nodes)
    if main_dot is None: return

    nodes.sort(key=lambda n: n.xpos(), reverse=True)  # Sort by position

    new_dot = nuke.createNode("Dot", inpanel=False)
    new_dot.setSelected(False)
    new_dot.setInput(0, main_dot)
    nodes[0].setInput(0, new_dot)
    gfx_nuke.setXYpos(new_dot, (nodes[0], main_dot))

    x_last = gfx_nuke.getNodeCenter(nodes[-1])[0]
    x_main_dot = gfx_nuke.getNodeCenter(main_dot)[0]
    nodes = nodes[1:] if abs(x_last-x_main_dot) > nodes[-1].screenWidth() / 2 else nodes[1:-1]

    for node in nodes:
        dot = nuke.createNode("Dot", inpanel=False)
        dot.setSelected(False)
        dot.setInput(0, main_dot)
        node.setInput(0, dot)
        new_dot.setInput(0, dot)
        new_dot = dot
        gfx_nuke.setXYpos(dot, (node, main_dot))
