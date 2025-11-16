# When creating a Read node, checks all formats and assigns a name to untitled formats

# v1.1.0
# created by: Pushkarev Aleksandr

import nuke

def nameFromFormat(format: nuke.Format) -> str:
    """
    Naming: width and height separated by an underscore.
    If the pixel aspect is not equal to 1, it is also appended at the end, separated by an underscore.
    Input: format, Output: name for this format.
    """
    res = f'{format.width()}_{format.height()}'
    aspect = format.pixelAspect()
    if aspect!=1:
        if aspect%1==0:
            res += f'_{int(aspect)}'
        else:
            res += f'_{round(aspect, 5)}'
    return res

def nameAllUntitledFormats():
    """Iterates through all formats in Nuke and assigns a name to untitled formats"""
    for f in nuke.formats():
        if f.name()==None:
            f.setName(nameFromFormat(f))

# The function is triggered every time a Read node is added
nuke.addOnCreate(nameAllUntitledFormats, nodeClass='Read')
