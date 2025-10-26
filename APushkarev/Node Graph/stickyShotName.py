# Adds sticky notes to Read nodes with a recognizable shot name

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke, nukescripts, os, re

def stickyShotName():
    sel = nuke.selectedNodes()
    nukescripts.clear_selection_recursive()
    for node in sel:
        if node.Class() == 'Read':
            file = node['file'].value()
            filename = os.path.basename(file)
            match = re.match(r"\d{2}_[A-Z]{2,4}_\d{4}", filename) or re.match(r"[A-Z]{2,4}_\d{4}", filename)
            if match:
                shotname = match.group()
                stick = nuke.createNode('StickyNote')
                stick.setXYpos(node.xpos()-100,node.ypos()-100)
                stick.setSelected(False)
                stick['label'].setValue(shotname)
                stick['note_font_size'].setValue(50)
