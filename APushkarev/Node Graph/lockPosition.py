# Locks the position of selected nodes at their current position.
# Calling the command again unlocks position changes.
# Code is added to the node's knobChanged to prevent position changes.

# v1.0.0
# created by: Pushkarev Aleksandr

# v1.0.0 initial release

# TODO
# Currently, it does not account for existing code in knobChanged; new code should be appended to existing code

import nuke

def lockPosition():
    start = "nuke.thisNode().setXYpos("
    end = ") if nuke.thisKnob().name() in ['xpos', 'ypos'] else None"
    for node in nuke.selectedNodes():
        kn = node.knob("knobChanged")
        if kn:
            val = kn.value()
            if val.startswith(start) and val.endswith(end):
                kn.setValue("")
            elif val=="":  # Check to avoid overwriting existing knobChanged, as currently knobChanged is set from scratch instead of appending to existing code
                kn.setValue(f"{start}{node.xpos()}, {node.ypos()}{end}")
