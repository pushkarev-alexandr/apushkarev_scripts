# Renames the file and updates the filename in the selected Read node
# Note: Sequences are not supported, only single files are supported.

# v1.0.1
# created by: Pushkarev Aleksandr

# changelog:
# v1.0.0 - Initial release
# v1.0.1 - Bug fix

# TODO
# - Should rename not only Read nodes, but any nodes with a 'file' knob
# - Should support renaming sequences

import nuke
import os

def main():
    nodes = nuke.selectedNodes("Read")
    if not nodes:
        return
    if len(nodes)>1:
        nuke.message("Only one node should be selected")
        return
    node = nodes[0]
    kn = node["file"]
    path = kn.value()
    if not os.path.exists(path):
        nuke.message(f"The file {path} does not exist!")
        return
    old_name = os.path.basename(path)
    new_name = nuke.getInput("New filename", old_name)
    if not new_name:
        return
    new_path = f"{os.path.dirname(path)}/{new_name}"
    os.rename(path, new_path)
    kn.setValue(new_path)
