# Toggles between ACEScg and ACES2065 in Nuke's working space settings

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke

def toggleWorkingSpace():
    if nuke.root().knob('colorManagement').value()=='OCIO':
        kn = nuke.root().knob('workingSpaceLUT')
        if kn.value() == 'scene_linear':
            kn.setValue('default')
        else:
            kn.setValue('scene_linear')
