# Creates a Read node from a Write node

# v1.2.5
# created by: Pushkarev Aleksandr

# v1.2.4 - made it work not only for padding 4 (%04d)
# v1.2.5 - added .mp4 in addition to .mov. Renamed to createReadFromWrite

# TODO:
# make it work with WriteGeo

import nuke
import os, re

def isSingleFile(iFileName, basename):
    # Checks if the file is a single file (not a sequence)
    if len(iFileName.split(' ')) != 1:
        return False
    sep = ''
    if basename.count('%04d'):
        sep = '%04d'
    elif basename.count('#'):
        sep = '#'
    elif basename.count('####'):
        sep = '####'
    if sep:
        basePrt = basename.partition(sep)
        if basePrt[1]:
            len1 = len(basePrt[0])
            len2 = len(basePrt[1])
            len3 = len(basePrt[2])
            cond1 = basePrt[0] == iFileName[0:len1]
            cond2 = iFileName[len1:len1+len2].isdigit()
            cond3 = basePrt[2] == iFileName[len1+len2:len1+len2+len3]
            if cond1 and cond2 and cond3:
                return True
    return False

def createReadFromWrite():
    # Creates a Read node from the selected Write node(s)
    nodes = nuke.selectedNodes()
    if not nodes:
        return
    for node in nodes:
        if node.Class() != 'Write':
            continue
        path = node.knob('file').value()
        # If path is relative or has tcl expression
        if path.startswith('.') or (path.count('[') and path.count(']')):
            path = node['file'].getEvaluatedValue().replace(str(nuke.frame()), '%04d')
        if path.lower()[-4:] in [".mov", ".mp4"]:
            if os.path.exists(path):
                read = nuke.createNode('Read', inpanel=False)
                read.knob('file').fromUserText(path)
                if node.knob('raw').value():
                    read.knob('raw').setValue(True)
                else:
                    read.knob('colorspace').setValue(node.knob('colorspace').value())
                read.knob('localizationPolicy').setValue(0)
                read.knob('updateLocalization').execute()
                read.setXYpos(node.xpos() + 150, node.ypos())
                read.setSelected(False)
                if nuke.root().firstFrame() != 1:
                    retime = nuke.createNode('AppendClip', inpanel=False)
                    retime.setInput(0, read)
                    retime.setXYpos(read.xpos(), read.ypos() + 96)
        else:
            dirName = os.path.dirname(path)
            basename = os.path.basename(path)
            lst = nuke.getFileNameList(dirName, False, False, False)
            if lst:
                for i in lst:
                    name = i.split(' ')[0]
                    def replacer(match):
                        count = int(match.group(1))
                        return '#' * count
                    # Check for sequence or single file
                    if name == re.sub(r'%\d+d', '#', basename) or name == re.sub(r'%(\d{2})d', replacer, basename) or isSingleFile(i, basename):
                        path = dirName + '/' + i
                        read = nuke.createNode('Read', inpanel=False)
                        read.knob('file').fromUserText(path)
                        if node.knob('raw').value():
                            read.knob('raw').setValue(True)
                        else:
                            read.knob('colorspace').setValue(node.knob('colorspace').value())
                        read.knob('localizationPolicy').setValue(0)
                        read.knob('updateLocalization').execute()
                        read.setXYpos(node.xpos() + 150, node.ypos())
