# Scripts can be opened via drag-and-drop

# v1.1.0
# created by: Pushkarev Aleksandr

import nuke, threading

class openScriptThread(threading.Thread):
    def __init__(self,path):
        threading.Thread.__init__(self)
        self.path = path
    
    def run(self):
        nuke.executeInMainThread(nuke.scriptOpen,self.path)

def openNkAsNewComp(mimeType, text):
    if mimeType=='text/plain' and text.endswith('.nk') and not text.count('_track_'):
        isProjectFile = False
        file = open(text,'r')
        for i in file:
            if i=='Root {\n':
                isProjectFile = True
                break
        file.close()
        if isProjectFile:
            openScriptThread(text).start()
            return True
        else:
            return False
    else:
        return False
