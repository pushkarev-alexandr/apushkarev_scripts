# Allows you to change the value of a specified parameter or set an expression for multiple selected nodes.

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke

def batchKnobEdit():
    selected = nuke.selectedNodes()
    selected.reverse()
    if not selected:
        nuke.message("nothing selected")
        return
    
    p = nuke.Panel("Multi edit:")

    p.addSingleLineInput("knob to change: ", "")
    p.addEnumerationPulldown("new value is: ", "value expression")
    p.addSingleLineInput("new value: ", "")
    p.addButton("cancel")    
    p.addButton("edit")

    if not p.show():
        return

    knob = p.value("knob to change: ").lower()
    newVal = p.value("new value: ")
    isExpr = (p.value("new value is: ") == "expression")
    
    if not(knob and newVal):
        nuke.message("Please fill the gaps")
        return

    index = None
    if knob.endswith(".x"):
        index = 0
        knob = knob[0:-2]
    elif knob.endswith(".y"):
        index = 1
        knob = knob[0:-2]

    nsk = []
    ve = []

    if isExpr:
        for node in selected:
            kn = node.knob(knob)
            if kn:
                if index!=None:
                    kn.setExpression(newVal, index)
                else:
                    kn.setExpression(newVal)
            else:
                nsk.append(node.name())
    else:
        for node in selected:
            kn = node.knob(knob)
            if kn:
                try:
                    if isinstance(kn.value(), bool):
                        if newVal.lower()=="false" or newVal=="0":
                            kn.setValue(False)
                        if newVal.lower()=="true" or newVal=="1":
                            kn.setValue(True)
                    elif isinstance(kn.value(), int):
                        kn.setValue(int(newVal))
                    elif isinstance(kn.value(), float) or isinstance(kn.value(), tuple):
                        lst = newVal.split()
                        l = len(lst)
                        for i in range(l):
                            kn.setValue(float(lst[i]), i)
                    elif isinstance(kn.value(), list):
                        lst = newVal.split()
                        l = len(lst)
                        for i in range(l):
                            kn.setValue(float(lst[i]), i)
                        if l==1:
                            kn.setSingleValue(True)
                            node.hideControlPanel()
                    elif isinstance(kn.value(), str):
                        kn.setValue(newVal)
                    else:
                        nuke.message("Value error")
                        return
                except:
                    ve.append(node.name())
            else:
                nsk.append(node.name())

    if nsk:
        mes = "No such knob for:"
        for i in nsk:
            mes += " " + i
        nuke.message(mes)
    
    if ve:
        mes = "Value error for:"
        for i in ve:
            mes += " " + i
        nuke.message(mes)
