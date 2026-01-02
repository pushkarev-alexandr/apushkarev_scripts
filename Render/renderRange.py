# Renders selected nodes over the global range, launches afanasy node over afanasy node's range, presses updateLocalization button on selected Read node

# v1.6.2
# created by: Pushkarev Aleksandr

# changelog:
# v1.6.1 Added IP address //192.168.100.56/data check in addition to Z: drive
# v1.6.2 Use Z_DRIVE_UNC_PATH environment variable instead of hardcoded UNC path

import nuke
import os

def renderGlobalRange():
    if not nuke.selectedNodes():
        nuke.menu('Nuke').menu('Cache').findItem('Clear All').invoke()
    for node in nuke.selectedNodes():
        if node.Class()=='Write':
            try:
                nuke.execute(node)
            except Exception as e:
                nuke.message(str(e))
        elif node.Class()=='afanasy':
            node.knob('render_button').execute()
        elif node.Class()=='Read':
            file = node.knob('file').value()
            unc_path = os.environ.get('Z_DRIVE_UNC_PATH', '').replace('\\', '/')
            if file.startswith('Z:/') or (unc_path and file.startswith(unc_path)):
                node.knob('localizationPolicy').setValue(0)
            node.knob('updateLocalization').execute()

def renderInputRange():
    for node in nuke.selectedNodes():
        if node.Class()=='Write':
            try:
                nuke.execute(node,node.firstFrame(), node.lastFrame())
            except Exception as e:
                nuke.message(str(e))
        elif node.Class()=='afanasy':
            node.knob('framefirst').setValue(node.firstFrame())
            node.knob('framelast').setValue(node.lastFrame())
            node.knob('auto_frame_button').execute()
            node.knob('render_button').execute()

def renderInOutRange():
    for node in nuke.selectedNodes():
        io_range = nuke.activeViewer().node().playbackRange()
        if node.Class()=='Write':
            try:
                nuke.execute(node, io_range.first(), io_range.last())
            except Exception as e:
                nuke.message(str(e))
        elif node.Class()=='afanasy':
            node.knob('framefirst').setValue(io_range.first())
            node.knob('framelast').setValue(io_range.last())
            node.knob('auto_frame_button').execute()
            node.knob('render_button').execute()

def renderCurrentFrame():
    for node in nuke.selectedNodes():
        if node.Class()=='Write':
            try:
                nuke.execute(node, nuke.frame(), nuke.frame())
            except Exception as e:
                nuke.message(str(e))
