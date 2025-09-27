# Selects a folder and renames strings in all files within it, replacing 'from' with 'to'.
# Primarily used to rename sequence versions, e.g., from v002 to v003.

#v1.1.0
#created by: Pushkarev Aleksandr

# changelog:
# v1.0.0 - Initial release
# v1.1.0 - Set folder selection from Read/Write nodes

import nuke, os

def batchRename():
    nodes = nuke.selectedNodes("Read") + nuke.selectedNodes("Write")
    folder = ""
    if nodes:
        folder = nodes[0].knob("file").value().rsplit("/", 1)[0]

    p = nuke.Panel("From To")
    p.addFilenameSearch("folder", folder)
    p.addSingleLineInput("from", "")
    p.addSingleLineInput("to", "")
    if not p.show():
        return
    path = p.value("folder").replace("\\", "/").rstrip("/") + "/"
    if not os.path.isdir(path):
        nuke.message("Folder doesn't exist")
        return
    fromm = p.value("from")
    to = p.value("to")
    lst = os.listdir(path)
    errors = []
    for file in lst:
        try:
            os.rename(path + file, path + file.replace(fromm, to))
        except Exception as e:
            errors.append(f"{file}: {e}")
    if errors:
        nuke.message("Some files failed to rename:\n" + "\n".join(errors))
