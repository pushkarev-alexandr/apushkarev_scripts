# Extend frames for Read node

#v1.0.0
#created by: Pushkarev Aleksandr

import nuke, os

def extendFrames():
    for node in nuke.selectedNodes("Read"):
        dir = os.path.dirname(node["file"].value())
        lst = nuke.getFileNameList(dir)
        if len(lst)==1 and lst[0].count(" ")==1:
            spl = lst[0].split(" ")
            if spl[-1].count("-")==1:
                first = spl[-1].split("-")[0]
                last = spl[-1].split("-")[-1]
                if first.isdigit() and last.isdigit():
                    node["first"].setValue(int(first))
                    node["origfirst"].setValue(int(first))
                    node["last"].setValue(int(last))
                    node["origlast"].setValue(int(last))
                    node["updateLocalization"].execute()
