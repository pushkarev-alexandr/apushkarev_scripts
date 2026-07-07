# Fixes the error when importing mov or mp4 into Nuke and Nuke reports it cannot find the colorspace Gamma2.2 or sRGB

# v1.1.1
# created by: Pushkarev Aleksandr

# changelog:
# v1.1.1 added support for aces1.3 display mode

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
        isRec709, isSRGB = cs in ['default (Gamma2.2)', 'default (rec709)'], cs == 'default (sRGB)'
        if not isRec709 and not isSRGB:
            return

        if conf.startswith('fn-nuke_'):
            node['raw'].setValue(True)
            ocio = nuke.createNode('OCIODisplay', inpanel=False)
            ocio.setSelected(False)
            ocio.setInput(0, node)
            ocio.autoplace()
            ocio['display'].setValue('Rec.1886 Rec.709 - Display' if isRec709 else 'sRGB - Display')
            ocio['invert'].setValue(True)
        else:   
            node['colorspace'].setValue('Output - Rec.709' if isRec709 else 'Output - sRGB')

nuke.addOnCreate(nukeColorspaceGammaError, nodeClass='Read')
