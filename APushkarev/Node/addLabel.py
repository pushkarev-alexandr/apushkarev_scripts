# Adds a label to selected nodes
# If the input ends with a number, that number will be set as the font size for Dot or StickyNote
# You can simply enter a number to set the font size
# If the input is empty, the entire label on the node will be removed

#v1.0.0
#created by: Pushkarev Aleksandr

import nuke

def addLabel():
    selected = nuke.selectedNodes()
    if not selected:
        return
    inpt = nuke.getInput("Label")
    if inpt==None:
        return
    spl = inpt.split(" ")
    if spl[-1].isdigit():
        splLabel = " ".join(spl[0:-1])
        font_size = int(spl[-1])
    else:
        font_size = None
    for node in selected:
        kn = node.knob("label")
        if node.Class() in ["Dot", "StickyNote"] and font_size!=None:
            node["note_font_size"].setValue(font_size)
            label = splLabel
        else:
            label = inpt
        if label:
            value = kn.value()
            if not value.count(label):
                if value:
                    label = "\n" + label
                kn.setValue(value + label)
                if node.Class()!="Dot":
                    node.setYpos(node.ypos()-6)
        elif font_size==None:
            kn.setValue("")
