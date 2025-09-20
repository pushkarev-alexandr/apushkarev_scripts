# Saves a pair of keys (file path) and (path to the script that rendered it) to a database
# Limitation: if the file is moved, the link (file path) -> (script path) is lost

# v1.0.0
# created by: Pushkarev Aleksandr

# TODO
# Needs review

import nuke, os, json, re

json_path = os.path.dirname(__file__).replace("\\", "/") + "/render_log.json"

def unifyFrameVar(s):
    return re.sub(r"%\d*d", "%d", re.sub(r"#+", "%d", s))

def renderLog():
    node = nuke.thisNode()
    nkPath = nuke.root().name()
    if node.Class()=="Write" and nkPath!="Root":
        file = node.knob("file").value()
        file = unifyFrameVar(file)
        if file and nkPath:
            if not os.path.isfile(json_path):
                f = open(json_path, "w")
                f.write("{}")
                f.close()
            f = open(json_path, "r")
            json_data = json.load(f)
            f.close()
            json_data[file] = nkPath
            f = open(json_path, "w")
            json.dump(json_data, f, indent=1)
            f.close()

def getRelatedScriptPath():
    if not os.path.isfile(json_path):
        nuke.message("Can't find " + json_path)
        return
    node = nuke.selectedNode()
    kn = node.knob("file")
    if kn:
        file = unifyFrameVar(kn.value())
        f = open(json_path, "r")
        json_data = json.load(f)
        f.close()
        nkPath = json_data.get(file)
        if nkPath:
            nuke.message(nkPath)
        else:
            nuke.message("No data for this file")

nuke.addAfterRender(renderLog)  # Executes in menu.py only for GUI mode to prevent render farm from writing unnecessary data
nuke.menu("Nuke").addCommand("APushkarev/File/Script Path from Read", "renderLog.getRelatedScriptPath()")

# Script for afanasy render node:

"""
import os, json, re

json_path = "C:/Users/Fincher/.nuke/python/render_log.json"

def unifyFrameVar(s):
    return re.sub(r"%\d*d", "%d", re.sub(r"#+", "%d", s))

for node in nuke.thisNode().dependencies():
    if node.Class()=="Write":
        nkPath = nuke.root().name()
        if nkPath!="Root":
            file = unifyFrameVar(node.knob("file").value())
            if file and nkPath:
                if not os.path.isfile(json_path):
                    f = open(json_path, "w")
                    f.write("{}")
                    f.close()
                f = open(json_path, "r")
                json_data = json.load(f)
                f.close()
                json_data[file] = nkPath
                f = open(json_path, "w")
                json.dump(json_data, f, indent=1)
                f.close()

cgru.render(nuke.thisNode())
"""
