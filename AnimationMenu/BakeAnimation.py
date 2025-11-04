# Bakes animation on all knobs with expressions

# v1.0.1
# created by: Pushkarev Aleksandr

import nuke, nukescripts

class bakingRangePanel(nukescripts.PythonPanel):
    def __init__(self,ff,lf):
        nukescripts.PythonPanel.__init__(self, 'Frame range')
        self.rangeKn = nuke.String_Knob('range_kn', 'Range:', str(ff) + '-' + str(lf))
        self.addKnob(self.rangeKn)

def bake():
    ff = nuke.root().firstFrame()
    lf = nuke.root().lastFrame()
    panel = bakingRangePanel(ff,lf)
    if not panel.showModalDialog():
        return
    res = panel.rangeKn.value()
    if res.count('-') == 1:
        spl = res.split('-')
        if not (spl[0] and spl[1] and spl[0].isdigit() and spl[1].isdigit()):
            return
        ff = spl[0]
        lf = spl[1]
    elif res[0].isdigit():
        ff = res[0]
        lf = res[0]
    else:
        return
    #--------

    for node in nuke.selectedNodes():
        animKnobs = [k for k in node.knobs().values() if k.isAnimated()]
        for kn in animKnobs:
            if kn.hasExpression():
                for i in range(0, kn.width()):
                    animCurve = kn.animation(i)
                    if animCurve:  # For double knobs (like Blur size), the first may be animated but the second may not be
                        fullName = kn.fullyQualifiedName(i)
                        fullNameLst = fullName.split('.')
                        fullNameLst.pop(0)
                        partName = '.'.join(fullNameLst)
                        nuke.animation(fullName, 'generate', (ff, lf, '1', 'y', partName))
                        deleteKeys = []
                        for key in animCurve.keys():
                            if key.x > int(lf):
                                deleteKeys.append(key)
                        animCurve.removeKey(deleteKeys)
