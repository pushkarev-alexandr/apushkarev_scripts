# Fixes the error when importing mov or mp4 into Nuke and Nuke reports it cannot find the colorspace Gamma2.2 or sRGB

# v1.1.0
# created by: Pushkarev Aleksandr

import nuke

def nukeColorspaceGammaError():
    try:
        nuke.root()['colorManagement']
    except:
        return
    node = nuke.thisNode()
    file = node['file'].value().lower()
    cs = node['colorspace'].value()
    cm = nuke.root()['colorManagement'].value()
    conf = nuke.root()['OCIO_config'].value()
    if (file.endswith('.mp4') or file.endswith('.mov') or file.endswith('.mxf')) and cm=='OCIO' and conf!='nuke-default':
        if cs in ['default (Gamma2.2)', 'default (rec709)']:
            node['colorspace'].setValue('Output - Rec.709')
        elif cs=='default (sRGB)':
            node['colorspace'].setValue('Output - sRGB')

nuke.addOnCreate(nukeColorspaceGammaError, nodeClass='Read')
