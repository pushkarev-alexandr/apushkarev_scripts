#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# Copies all files of the selected Read node to a new version (tested only on sequences)

# v1.1.0
# created by: Pushkarev Aleksandr

# v1.0.0 initial release
# v1.1.0 Read node's file is updated to the newly copied version

import nuke
import os, shutil, re

def versionUp(path):
    pattern = r"(v)(\d+)(\D?)"
    
    def replacer(match):
        prefix, num, suffix = match.groups()
        new_num = str(int(num) + 1).zfill(len(num))
        return f"{prefix}{new_num}{suffix}"
    
    return re.sub(pattern, replacer, path)

def copyToNewVersion():
    for node in nuke.selectedNodes("Read"):
        file_kn = node["file"]
        path = file_kn.value()
        new_path = versionUp(path)
        if nuke.ask(f"Copy {path} to\n{new_path}?"):
            ext = os.path.splitext(path)[1]
            dirname = os.path.dirname(path)
            new_dir = os.path.dirname(new_path)
            os.makedirs(new_dir, exist_ok=True)
            lst = os.listdir(dirname)
            l = len(lst)
            task = nuke.ProgressTask("Copying...")
            for i,f in enumerate(lst):
                if task.isCancelled():
                    return
                if f.endswith(ext):
                    old_file = dirname+"/"+f
                    new_filename = versionUp(f)
                    new_file = new_dir+"/"+new_filename
                    task.setMessage(new_filename)
                    task.setProgress(int((i+1)/l*100))
                    shutil.copy2(old_file,new_file)
            del task
            file_kn.setValue(new_path)
            node["updateLocalization"].execute()
