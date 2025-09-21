# Bakes the label color of the selected Dot or all Dots if nothing is selected into HTML code
# After this, the label color does not change when zooming in or out
# The script was created to address the issue where Dots had colored labels but appeared black and white

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke

def bakeDotsColor():
    nodes = nuke.selectedNodes()
    if not nodes:
        nodes = nuke.allNodes("Dot")
    for node in nodes:
        if node.Class()=="Dot" and node["note_font_color"].value()!=0:
            val = node["label"].value()
            if not val.startswith("<pre><font color=#"):
                node["label"].setValue("<pre><font color=#" + format(node["note_font_color"].value(), "06x")[0:-2] + ">" + val)
