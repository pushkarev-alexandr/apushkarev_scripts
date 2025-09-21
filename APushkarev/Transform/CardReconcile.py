# Selects a card and a camera and performs Reconcile

#v1.0.0
#created by: Pushkarev Aleksandr

import math, re, threading
import nuke, nukescripts

class FormatRangeDialog(nukescripts.PythonPanel):
    def __init__(self):
        super().__init__()
        self.first_frame = nuke.Int_Knob("first_frame", "frame range")
        self.first_frame.setValue(nuke.root().firstFrame())
        self.addKnob(self.first_frame)
        self.last_frame = nuke.Int_Knob("last_frame", "")
        self.last_frame.setValue(nuke.root().lastFrame())
        self.last_frame.clearFlag(nuke.STARTLINE)
        self.addKnob(self.last_frame)
        self.format = nuke.Format_Knob("format", "format")
        self.addKnob(self.format)

def cameraProjectionMatrix(cameraNode, frame, format):
    'Calculate the projection matrix for the camera based on its knob values.'
    # modified code from nukescripts.snap3D.cameraProjectionMatrix

    # Matrix to transform points into camera-relative coords.
    wm = nuke.math.Matrix4()
    for i in range(16):
        wm[i] = cameraNode['world_matrix'].getValueAt(frame, i)
    
    wm.transpose()
    camTransform = wm.inverse()

    # Matrix to take the camera projection knobs into account
    roll = float(cameraNode['winroll'].getValueAt(frame, 0))
    scale_x, scale_y = [float(v) for v in cameraNode['win_scale'].getValueAt(frame)]
    translate_x, translate_y = [float(v) for v in cameraNode['win_translate'].getValueAt(frame)]
    m = nuke.math.Matrix4()
    m.makeIdentity()
    m.rotateZ(math.radians(roll))
    m.scale(1.0 / scale_x, 1.0 / scale_y, 1.0)
    m.translate(-translate_x, -translate_y, 0.0)

    # Projection matrix based on the focal length, aperture and clipping planes of the camera
    focal_length = float(cameraNode['focal'].getValueAt(frame))
    h_aperture = float(cameraNode['haperture'].getValueAt(frame))
    near = float(cameraNode['near'].getValueAt(frame))
    far = float(cameraNode['far'].getValueAt(frame))
    projection_mode = int(cameraNode['projection_mode'].getValueAt(frame))
    p = nuke.math.Matrix4()
    p.projection(focal_length / h_aperture, near, far, projection_mode == 0)

    # Matrix to translate the projected points into normalised pixel coords
    imageAspect = float(format.height()) / float(format.width())

    t = nuke.math.Matrix4()
    t.makeIdentity()
    t.translate( 1.0, 1.0 - (1.0 - imageAspect / float(format.pixelAspect())), 0.0 )

    # Matrix to scale normalised pixel coords into actual pixel coords.
    x_scale = float(format.width()) / 2.0
    y_scale = x_scale * format.pixelAspect()
    s = nuke.math.Matrix4()
    s.makeIdentity()
    s.scale(x_scale, y_scale, 1.0)

    # The projection matrix transforms points into camera coords, modifies based
    # on the camera knob values, projects points into clip coords, translates the
    # clip coords so that they lie in the range 0,0 - 2,2 instead of -1,-1 - 1,1,
    # then scales the clip coords to proper pixel coords.
    return s * t * p * m * camTransform

def getCardCornersCoords(card):
    nukescripts.clear_selection_recursive()
    edit_geo = nuke.createNode("EditGeo", inpanel=False)
    edit_geo.setInput(0, card)
    python_geo = nuke.createNode("PythonGeo", inpanel=False)
    python_geo.setInput(0, edit_geo)

    points = python_geo["geo"].getGeometry()[0].points()
    nuke.delete(edit_geo)
    nuke.delete(python_geo)

    columns = int(card["columns"].value())
    res = [points[:3],
           points[columns*3:columns*3+3],
           points[len(points)-3:],
           points[len(points)-columns*3-3:len(points)-columns*3]]
    return res

def cardCameraSelect():
    nodes = nuke.selectedNodes()
    cards = [n for n in nodes if re.match(r"^Card\d?$", n.Class())]
    cameras = [n for n in nodes if re.match(r"^Camera\d?$", n.Class())]
    if not cards:
        nuke.message("No Card selected")
        return None, None
    if not cameras:
        nuke.message("No Camera selected")
        return None, None
    return cards, cameras[0]

def reconcile(card_name, first_frame, last_frame, camera, format, corners, cornerpin):
    task = nuke.ProgressTask(f"{card_name} reconcile")
    for frame in range(first_frame, last_frame + 1):
        if task.isCancelled():
            return
        task.setProgress(int(100 * (frame - first_frame) / (last_frame - first_frame)))
        task.setMessage(f"frame {frame}")
        cam_matrix = cameraProjectionMatrix(camera, frame, format)
        for i, (x, y, z) in enumerate(corners):
            t_pos = cam_matrix * nuke.math.Vector4(x, y, z, 1)
            x_ndc, y_ndc = t_pos.x / t_pos.w, t_pos.y / t_pos.w
            for kname in (f"to{i+1}", f"from{i+1}"):
                cornerpin[kname].setValueAt(x_ndc, frame, 0)
                cornerpin[kname].setValueAt(y_ndc, frame, 1)

def main():
    cards, camera = cardCameraSelect()
    if not cards or not camera:
        return
    dialog = FormatRangeDialog()
    if not dialog.showModalDialog():
        return
    format = dialog.format.value()
    first_frame = dialog.first_frame.value()
    last_frame = dialog.last_frame.value()

    for card in cards:
        corners = getCardCornersCoords(card)

        cornerpin = nuke.createNode("CornerPin2D")
        for i in range(1,5):
            cornerpin[f"to{i}"].setAnimated()
            cornerpin[f"from{i}"].setAnimated()

        threading.Thread(target=reconcile, args=(card.name(), first_frame, last_frame, camera, format, corners, cornerpin)).start()
