# Synchronizes the viewer and monitorOut colorspace when changed via knobChanged and on creation (either by the user or when opening/copying the script)
# Ensures that monitorOut always has the same colorspace as the viewer

# v1.0.1
# created by: Pushkarev Aleksandr

# changelog:
# v1.0.0 Initial release
# v1.0.1 Add try-except for monitorOutOutputTransform, to prevent LiveGroup exception

import nuke, getpass

def monitorOutKnobChanged():
    node = nuke.thisNode()
    kn = nuke.thisKnob()
    if kn.name()=='viewerProcess' and node.knob('monitorOutOutputTransform'):
        node['monitorOutOutputTransform'].setValue(kn.value())

def monitorOutOnCreate():
    node = nuke.thisNode()
    if node.knob('monitorOutOutputTransform'):
        try:
            node['monitorOutOutputTransform'].setValue(node['viewerProcess'].value())
        except:
            print('Probably we are in LiveGroup')

nuke.addKnobChanged(monitorOutKnobChanged, nodeClass='Viewer')  
nuke.addOnCreate(monitorOutOnCreate, nodeClass='Viewer')
