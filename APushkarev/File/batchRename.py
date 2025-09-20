# Selects a folder and renames strings in all files within it, replacing 'from' with 'to'.
# Primarily used to rename sequence versions, e.g., from v002 to v003.

#v1.0.0
#created by: Pushkarev Aleksandr

import nuke, os

def batchRename():
    p = nuke.Panel("From To")
    p.addFilenameSearch("folder", "")
    p.addSingleLineInput("from", "")
    p.addSingleLineInput("to", "")
    if not p.show():
        return
    path = p.value("folder").replace("\\", "/").rstrip("/") + "/"
    if not os.path.isdir(path):  # Проверяем существование папки
        nuke.message("Folder doesn't exist")
        return
    fromm = p.value("from")
    to = p.value("to")
    lst = os.listdir(path)
    for file in lst:
        os.rename(path + file, path + file.replace(fromm, to))
