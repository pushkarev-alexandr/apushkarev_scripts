# Opens the selected Read or Write node in the Lama-Cleaner application

# v1.0.0
# created by: Pushkarev Aleksandr

# TODO
# - Make universal and make installation incstruction
# - Check file extension
# - Prompt to overwrite the file or save with a new name
# - Does not output the mask

import nuke, os

def openInLamaCleaner():
    sel = nuke.selectedNodes("Write") + nuke.selectedNodes("Read")
    if not sel:
        nuke.message("Select a Read or Write node")
        return
    node = sel[0]
    file = node["file"].getEvaluatedValue()
    if not os.path.isfile(file):
        nuke.message(file + "\nThis file does not exist")
        return
    outdir = os.path.dirname(file)
    cmd = fr'''cd /d C:\Users\apushkarev\AppData\Local\miniconda3\Scripts
call activate D:\ML\lama-cleaner\python
lama-cleaner --model-dir D:\ML\lama-cleaner\models --gui --input {file} --output-dir {outdir}'''.replace("\n", "&")
    cmd = f'start cmd.exe /c "{cmd}"'
    os.system(cmd)
