# Scripts can be opened via drag-and-drop

# v1.2.0
# created by: Pushkarev Aleksandr

# changelog:
# v1.0.0 initial release
# v1.1.0 if the file name contains _track_ do not open it
# v1.2.0 add interface for choosing how to open .nk file; add user choice toggle and simplify logic

import nuke, threading

allow_user_choice = False  # If False (default), always open as new comp without asking user. Set to True to show user a choice.

class openScriptThread(threading.Thread):
    def __init__(self,path):
        threading.Thread.__init__(self)
        self.path = path
    
    def run(self):
        nuke.executeInMainThread(nuke.scriptOpen,self.path)

def is_nuke_project_file(path):
    """Check if file is a Nuke project by looking for 'Root {\n' line."""
    try:
        with open(path, 'r') as file:
            for line in file:
                if line == 'Root {\n':
                    return True
    except Exception:
        pass
    return False

def openNkAsNewComp(mimeType, text):
    if not (mimeType == 'text/plain' and text.endswith('.nk') and '_track_' not in text):
        return False

    if not is_nuke_project_file(text):
        return False

    if not allow_user_choice:
        openScriptThread(text).start()
        return True

    panel = nuke.Panel('Open .nk file')
    panel.addButton('Import into Current Script')
    panel.addButton('Open as New Comp')
    ret = panel.show()
    if ret == 1:
        openScriptThread(text).start()
        return True
    
    return False
