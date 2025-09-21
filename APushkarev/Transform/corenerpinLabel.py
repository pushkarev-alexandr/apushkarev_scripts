# When pressing the copy_from or copy_to button, removes the matchmove or stabilize label
# (this label is set by the matchmove/stabilize button in W_hotbox)

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke

def cornerpinLabel():
    node = nuke.thisNode()
    kn = nuke.thisKnob()
    label = node["label"]
    if (kn.name()=="copy_from" and label.value().startswith("stabilize ")) or (kn.name()=="copy_to" and label.value().startswith("matchmove ")):
        label.setValue("")

nuke.addKnobChanged(cornerpinLabel, nodeClass="CornerPin2D")
