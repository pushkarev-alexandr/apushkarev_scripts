# Adds the 'copy knob name' menu to the animation menu for copying knob names for use in expressions, Python scripting, and other tasks.
# 'copy knob name' copies the knob name, 'copy full knob name' copies in the format NodeName.KnobName

# v1.4.0
# created by: Pushkarev Aleksandr

import nuke

def versionRelatedCopy(txt):
    if nuke.NUKE_VERSION_MAJOR > 15:
        from PySide6.QtGui import QGuiApplication as qApp
        qApp.clipboard().setText(txt)
    elif nuke.NUKE_VERSION_MAJOR > 10:
        from PySide2.QtGui import QGuiApplication as qApp
        qApp.clipboard().setText(txt)
    else:
        import subprocess
        subprocess.check_call('echo ' + txt.strip() + '|clip', shell=True)

def copyKnobName():
    anims = nuke.animations()
    if len(anims) > 1 and anims[0].count('.') == 1:
        versionRelatedCopy(anims[0].split('.')[0])
    elif len(anims) == 1:
        versionRelatedCopy(anims[0].replace('this.', ''))  # the knob 'mix' is displayed as `this.mix`, remove `this.`

def copyFullKnobName():
    nodeName = nuke.thisNode().name()
    if nodeName:
        anims = nuke.animations()
        if len(anims) > 1 and anims[0].count('.') == 1:
            versionRelatedCopy(nodeName + '.' + anims[0].split('.')[0])
        elif len(anims) == 1:
            versionRelatedCopy(nodeName + '.' + anims[0].replace('this.', ''))  # the knob 'mix' is displayed as `this.mix`, remove `this.`
