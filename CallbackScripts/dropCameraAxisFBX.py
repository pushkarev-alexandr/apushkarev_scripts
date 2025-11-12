# You can drag and drop an FBX file and a camera or axis will be created automatically depending on the file name

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke, nukescripts, os

def dropCameraAxisFBX(mimeType, text):
    basename = os.path.basename(text).lower()
    if mimeType=='text/plain' and text.endswith('.fbx') and (basename.count('camera') or basename.count('axis') or basename.count('null')):
        for i in range(2):
            try:
                # Since this condition is only met if the name contains either 'camera' or 'axis/null', 
                # the absence of the word 'camera' immediately implies that there is 'axis' or 'null' in the name,
                # so we do not check specifically for 'axis/null'
                node = nuke.createNode(['Axis', 'Camera'][basename.count('camera')] + str(3 - i))
                break
            except:
                node = None
        if node==None:
            return False
        node.knob('read_from_file').setValue(True)
        node.knob('file').setValue(text)
        return True
    else:
        return False

nukescripts.addDropDataCallback(dropCameraAxisFBX)
