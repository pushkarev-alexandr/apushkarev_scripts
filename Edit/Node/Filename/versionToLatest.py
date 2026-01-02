# Replaces the standard Nuke "Version To Latest" behavior.
# The default script stops at the first missing version (e.g., with v6 and v8 present but no v7, a v2 read would only jump to v6).
# This script continues to the highest available version (v8 in that example).

# v1.2.1
# created by: Pushkarev Aleksandr

import nuke, nukescripts, os, re

def unifyFrameVar(s):
    return re.sub(r'%\d*d', '%d', re.sub(r'#+', '%d', s))

def versionToLatest():
    for node in nuke.selectedNodes('Read'):
        f = node['file'].value()
        file = unifyFrameVar(f)
        v = nukescripts.version_get(file, 'v')[1]
        for i in range(20, 0, -1):
            newV = str(int(v) + i).zfill(len(v))
            newFile = file.replace('v' + v, 'v' + newV).replace('%d', str(node['first'].value()))
            if os.path.isfile(newFile):
                node['file'].setValue(f.replace('v' + v, 'v' + newV))
                node.knob('updateLocalization').execute()
                break
