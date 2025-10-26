# Toggles masking mode

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke

def toggleMaskingMode():
    viewer = nuke.activeViewer().node()
    if viewer['masking_mode'].value()!='no mask':
        viewer['masking_mode'].setValue('no mask')
    else:
        viewer['masking_mode'].setValue('full')
        viewer['masking_ratio'].setValue(6)
