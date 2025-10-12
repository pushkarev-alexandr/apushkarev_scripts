# Moves all Afanasy scripts, autosaves, and temporary files ending with a tilde to the autosave folder

# v1.2.0
# created by: Pushkarev Aleksandr

import nuke, os, shutil, re

def clearNkFolder():
    rootname = nuke.root().name()
    if rootname=="Root":
        # You can select either a folder or a file; the only difference is that if you select a file, the check f!=basename+"~" will work
        rootname = nuke.getFilename("Folder to clear")
    if not rootname:
        return
    basename = os.path.basename(rootname)
    dirname = os.path.dirname(rootname)
    autosave = f"{dirname}/autosaves"
    os.makedirs(autosave, exist_ok=True)
    if os.path.isdir(dirname):
        lst = os.listdir(dirname)
        for f in lst:
            # Check for Afanasy file, file ending with tilde (do not touch the current script just in case), and autosave files
            if f.count(".nk")==3 or (f.endswith("~") and f!=basename + "~") or re.search(r"autosave\d?$", f):
                src = f"{dirname}/{f}"
                dst = f"{autosave}/{f}"
                shutil.move(src, dst)
