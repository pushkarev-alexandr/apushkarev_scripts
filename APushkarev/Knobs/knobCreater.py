# In Nuke, you cannot create knobs like IArray_Knob and Eyedropper_Knob from the default menu, so a custom menu is created

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke

def knobCreater():
    nodes = nuke.selectedNodes()
    if not nodes:
        nuke.message("Select nodes")
        return
    type_panel = nuke.Panel("Select Knob Type")
    type_panel.addEnumerationPulldown("Knob Types", "IArray_Knob Multiline_Eval_String_Knob Eyedropper_Knob Format_Knob")
    if type_panel.show():
        kn_type = type_panel.value("Knob Types")
        parms_panel = nuke.Panel("Parameters")
        parms_panel.addSingleLineInput("name", "")
        parms_panel.addSingleLineInput("label", "")
        if kn_type=="IArray_Knob":
            parms_panel.addSingleLineInput("rows", "")
            parms_panel.addSingleLineInput("columns", "")
        if parms_panel.show():
            name = parms_panel.value("name")
            label = parms_panel.value("label")
            for node in nodes:
                if kn_type=="IArray_Knob":
                    kn = nuke.IArray_Knob(name,label,(int(parms_panel.value("rows")), int(parms_panel.value("columns"))))
                elif kn_type=="Multiline_Eval_String_Knob":
                    kn = nuke.Multiline_Eval_String_Knob(name,label)
                elif kn_type=="Eyedropper_Knob":
                    kn = nuke.Eyedropper_Knob(name,label)
                elif kn_type=="Format_Knob":
                    kn = nuke.Format_Knob(name,label)
                else:
                    kn = None
                if kn:
                    node.addKnob(kn)
