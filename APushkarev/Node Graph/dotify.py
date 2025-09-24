# Instead of a fan of inputs diverging from a single point, creates a grid

# v1.0.0
# created by: Pushkarev Aleksandr

from typing import Tuple, Union
import nuke, nukescripts

def getNodeCenter(node: nuke.Node) -> Tuple[float, float]:
    """Returns a tuple with the coordinates of the center for the specified node"""
    x = node.xpos() + node.screenWidth() / 2
    y = node.ypos() + node.screenHeight() / 2
    return x, y

def newXY(node1: nuke.Node, node2: nuke.Node) -> Tuple[int, int]:
    """Calculates the position of node1 so that its center matches the center of node2"""
    c = getNodeCenter(node2)
    x = int(c[0]-node1.screenWidth()/2)
    y = int(c[1]-node1.screenHeight()/2)
    return x, y

def _extract_pair(data) -> Tuple[object, object]:
    """
    Returns the first two elements from a list or tuple. If there is only one element or the type is not a list or tuple, returns it twice as a tuple.
    In summary, converts any type of data into a pair of values.
    """
    if isinstance(data, (list, tuple)) and len(data) >= 2:
        return data[:2]
    return data if not isinstance(data, (list, tuple)) else data[0], data if not isinstance(data, (list, tuple)) else data[0]

def setXYpos(node: nuke.Node, to_nodes: Union[nuke.Node, Tuple[nuke.Node, nuke.Node]], offset: Union[int, Tuple[int, int]]=(0,0)) -> None:
    """
    For the node `node`, sets `x` and `y` positions relative to `to_nodes` or a list of nodes, the first for `x`, the second for `y`. Also applies the `offset`.
    Both `to_nodes` and `offset` can be a single variable or a pair (list or tuple).
    A single variable will be applied to both `x` and `y`; if a list is provided, the first element will be applied to `x`, the second to `y`.
    Args:
        node (nuke.Node): The node for which to set new `xpos` and `ypos` values.
        to_nodes (nuke.Node | Tuple[nuke.Node, nuke.Node]): Node or list of nodes relative to which to set new `xpos` and `ypos` values.
        offset (int | Tuple[int, int]): Offset for `xpos` and `ypos`.
    Example:
        >>> setXYpos(dot1, (blur, dot2), (10, 15))
    """
    xnode, ynode = _extract_pair(to_nodes)
    xoffset, yoffset = _extract_pair(offset)
    node.setXYpos(newXY(node, xnode)[0] + int(xoffset), newXY(node, ynode)[1] + int(yoffset))

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
    setXYpos(new_dot, (nodes[0], main_dot))

    x_last = getNodeCenter(nodes[-1])[0]
    x_main_dot = getNodeCenter(main_dot)[0]
    nodes = nodes[1:] if abs(x_last-x_main_dot) > nodes[-1].screenWidth() / 2 else nodes[1:-1]

    for node in nodes:
        dot = nuke.createNode("Dot", inpanel=False)
        dot.setSelected(False)
        dot.setInput(0, main_dot)
        node.setInput(0, dot)
        new_dot.setInput(0, dot)
        new_dot = dot
        setXYpos(dot, (node, main_dot))
