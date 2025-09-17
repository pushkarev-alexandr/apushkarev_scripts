# Adds extra buttons to the Cache/Localization menu for opening the localization folder and deleting it

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke
import os, shutil

def get_localization_folder(path):
    """Returns the path to the localization folder if it exists"""
    local_folder = nuke.toNode("preferences")["localCachePath"].getEvaluatedValue()
    dirname = os.path.dirname(path).replace(":", "_")
    res_folder = os.path.join(local_folder, dirname)
    if os.path.exists(res_folder):
        return res_folder.replace("\\", "/")
    return ""

def process_localization_folders(action):
    """TODO: To delete localization, you also need to disable localization for the Read node"""
    nodes = nuke.selectedNodes("Read")
    if not nodes:
        nuke.message("No Read nodes selected.")
        return
    
    folders_dict = {}
    for node in nodes:
        local_folder = get_localization_folder(node["file"].getValue())
        if local_folder:
            folders_dict[local_folder] = node
    
    if not folders_dict:
        nuke.message("No localization folders found for the selected Read nodes.")
        return
    
    for local_folder, node in folders_dict.items():
        action(local_folder, node)

def open_action(local_folder, node):
    os.startfile(local_folder)

def remove_action(local_folder, node):
    try:
        shutil.rmtree(local_folder)
        node["localizationPolicy"].setValue("off")
        nuke.message(f"Localization folder successfully deleted:\n{local_folder}")
    except Exception as e:
        nuke.message(f"Error deleting {local_folder}:\n{e}")

def open_localization_folder():
    process_localization_folders(open_action)

def remove_localization_folder():
    process_localization_folders(remove_action)
