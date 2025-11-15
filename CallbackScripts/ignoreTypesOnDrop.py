# Prevents loading files of certain formats via drag-and-drop when dropping a folder
# Sets the correct colorspace for the source if `setColorspaceFromSettings` exists

# v1.4.0
# created by: Pushkarev Aleksandr

# v1.2.0 replaced greenfx_structure_helper with gfx
# v1.3.0 removed json_helper
# v1.4.0 moved colorspace setting to a separate script `setColorspaceFromSettings`

import nuke, nukescripts, os

try:
    import setColorspaceFromSettings
    _has_setColorspaceFromSettings = True
except ImportError:
    setColorspaceFromSettings = None
    _has_setColorspaceFromSettings = False

def ignoreTypesOnDrop(mimeType, text):
    # Check that the text length is not more than 260 characters, otherwise we get ValueError: _isdir: path too long for Windows
    if len(text) < 260 and os.path.isdir(text):  # Check if we are loading a folder or a file
        lst = nuke.getFileNameList(text, False, False, False, False)
        ignoreFileTypes = ['.3de_bcompress', '.tmp', 'Thumbs.db']
        isForbiddenTypes = False
        for file in lst:
            for type in ignoreFileTypes:
                if file.endswith(type):
                    isForbiddenTypes = True
                    break
        if isForbiddenTypes:
            for file in lst:
                if not any([file.endswith(type) for type in ignoreFileTypes]):
                    read = nuke.createNode('Read')
                    read.knob('file').fromUserText(f'{text}/{file}')
                    if _has_setColorspaceFromSettings and hasattr(setColorspaceFromSettings, 'setColorspaceFromSettings'):
                        setColorspaceFromSettings.setColorspaceFromSettings(read, text)
        else:
            return False
        return True
    else:
        return False

nukescripts.addDropDataCallback(ignoreTypesOnDrop)
