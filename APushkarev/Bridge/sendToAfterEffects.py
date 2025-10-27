# Opens the selected sequence in After Effects, creates a composition, and saves the project

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke
import os, re

jsx = os.path.join(os.path.dirname(__file__), 'sendToAfterEffects.jsx')

def findAEexe():
    """Finds the latest version of After Effects. If nothing is found, returns None"""
    adobe = 'C:/Program Files/Adobe'
    if os.path.isdir(adobe):
        for f in reversed(os.listdir(adobe)):
            ae_exe = f'{adobe}/{f}/Support Files/AfterFX.exe'
            if f.lower().count('after effects') and os.path.isfile(ae_exe):
                return ae_exe
    nuke.message("Can't find After Effects")

def getPrjPath():
    """Returns the path to the .aep project where the AE project will be saved after opening"""
    root = nuke.root().name()
    aeDir = f'{os.path.dirname(root)}/ae' if root!='Root' else os.getenv('NUKE_TEMP_DIR') + '/ae'
    filename = os.path.basename(root)[:-3] + '.aep' if root!='Root' else 'TEMP.aep'
    if not os.path.isdir(aeDir):
        try:
            os.makedirs(aeDir)
        except:
            nuke.message(f"Can't create folder for AE project in\n<i>{aeDir}</i>")
            return None
    return f'{aeDir}/{filename}'

def getFilename():
    """Returns the path to the file that is planned to be opened"""
    nodes = nuke.selectedNodes('Read')
    if len(nodes)!=1:
        nuke.message('Select <b>one</b> Read node')
        return
    node  = nodes[0]
    file = node['file'].value()
    file = re.sub(r'%\d*d', str(node['first'].value()), file)
    if os.path.isfile(file):
        return file
    else:
        nuke.message(f"File doesn't exist\n{file}")

def sendToAfterEffects():
    ae_exe = findAEexe()
    if not ae_exe: return
    prj_path = getPrjPath()
    if not prj_path: return
    seq_path = getFilename()
    if not seq_path: return

    with open(jsx, 'r') as f:
        script = f.read().replace('\n','')
    cmd = f'set AE_SEQUENCE_PATH={seq_path}'
    cmd = f'{cmd}&set AE_PROJECT_PATH={prj_path}'
    cmd = f'{cmd}&"{ae_exe}" -s "{script}"'
    cmd = f'start cmd /c "{cmd}"'
    os.system(cmd)
