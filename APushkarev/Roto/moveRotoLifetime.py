# Shifts the lifetime of elements in the Roto/RotoPaint node by the specified number of frames

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke
import nukescripts

offset = 0
paints = []

class ModalFramePanel(nukescripts.PythonPanel):
    def __init__( self ):
         nukescripts.PythonPanel.__init__( self, "Move Lifetime")
         self.move = nuke.Int_Knob( "move", "Move:" )
         self.addKnob( self.move )
         self.move.setValue(0)
    def showModalDialog( self ):
         result = nukescripts.PythonPanel.showModalDialog( self )
         if result:
            global offset
            offset = self.move.value()

def fillPaints(layer):
    global paints
    for element in layer:
        if isinstance(element, nuke.rotopaint.Layer):
            fillPaints(element)
        elif isinstance(element, nuke.rotopaint.Stroke) or isinstance(element, nuke.rotopaint.Shape):
            paints.append(element)

def moveRotoLifetime():
    global paints
    ModalFramePanel().showModalDialog()

    for node in nuke.selectedNodes():
        curvesKnob = node.knob("curves")
        if curvesKnob.getSelected() == []:
            fillPaints(curvesKnob.rootLayer)
        else:
            paints = curvesKnob.getSelected()

        for element in paints:
            if not isinstance(element, nuke.rotopaint.Layer):
                attrs = element.getAttributes()
                ltt = attrs.getValue(nuke.frame(), "ltt")
                if ltt==1 or ltt==4:
                    ltm = attrs.getValue(nuke.frame(), "ltm")
                    ltm += offset
                    attrs.set("ltm", ltm)
                if ltt==2 or ltt==3 or ltt==4:
                    ltn = attrs.getValue(nuke.frame(), "ltn")
                    ltn += offset
                    attrs.set("ltn", ltn)
        curvesKnob.changed()
        paints=[]
