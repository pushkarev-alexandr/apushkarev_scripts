# Adds information about the selected knob's value to the label

# v1.0.0
# created by: Pushkarev Aleksandr

# TODO: If we add a label to a group's link knob, the label should be created for the group node, not the original node

import nuke

def addLabel(node,label):
    kn = node.knob('label')
    value = kn.value()
    if not value.count(label):
        if value:
            label = '\n' + label
        kn.setValue(value + label)
        node.setYpos(node.ypos() - 6)

def labelThis():
    node = nuke.thisNode()
    kn = nuke.thisKnob()
    if kn.label():
        label = kn.label() + ' [value ' + kn.name() + ']'
    else:
        label = kn.name() + ' [value ' + kn.name() + ']'
    addLabel(node,label)
