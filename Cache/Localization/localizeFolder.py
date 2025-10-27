# Allows you to localize a folder and all its contents

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke
import threading, os, shutil

allowed_ext = ['.exr', '.png', '.jpeg', '.mov', '.mp4', '.mxf']

def localizeFolder(total_files, localPath):
    task = nuke.ProgressTask("Localization")
    l = len(total_files)
    for i, file in enumerate(total_files):
        if task.isCancelled():
            return
        print(file)
        task.setMessage(file)
        task.setProgress(int((i+1)/l*100))
        finalPath = f"{localPath}/{file.replace(':', '_')}"
        pathDir = os.path.dirname(finalPath)
        if not os.path.isdir(pathDir):
            os.makedirs(pathDir)
        if not os.path.exists(finalPath):
            shutil.copy2(file, finalPath)
    nuke.executeInMainThread(nuke.message, ('Copying completed successfully'))

def getTotalFiles(folder):
    total_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in allowed_ext:
                filePath = os.path.join(root, file).replace('\\','/')
                total_files.append(filePath)
    return total_files

def getFiles():
    folder = nuke.getFilename('Choose folder to copy')
    if folder==None:
        return
    if not os.path.isdir(folder):
        nuke.message('You need to select a folder')
        return
    localPath = nuke.toNode('preferences')['localCachePath'].getEvaluatedValue()
    if not localPath:
        nuke.message('Cannot determine localization folder')
        return
    localPath = localPath.rstrip('/')

def main():
    localPath = nuke.toNode('preferences')['localCachePath'].getEvaluatedValue().rstrip('/')
    if not localPath:
        nuke.message('Cannot determine localization folder')
        return
    folder = nuke.getFilename('Choose folder to copy')
    if folder==None:
        return
    if not os.path.isdir(folder):
        nuke.message('You need to select a folder')
        return
    total_files = getTotalFiles(folder)
    if not total_files:
        nuke.message(f'No files found with extensions {", ".join(allowed_ext)}')
        return
    try:
        threading.Thread(target=localizeFolder, args=(total_files,localPath)).start()
    except Exception as e:
        nuke.message(f"An error occurred: {e}")
