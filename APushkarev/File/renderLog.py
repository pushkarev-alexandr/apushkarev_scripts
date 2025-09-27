# Saves a pair of keys (file path) and (path to the script that rendered it) to a database
# Limitation: if the file is moved, the link (file path) -> (script path) is lost

# v1.1.0
# created by: Pushkarev Aleksandr

# changelog:
# v1.0.0 - Initial release
# v1.1.0 - Refactor: streamline file path handling and improve code readability. Now works correctly for Read nodes with localization enabled

# TODO
# - use sqlite database instead of json

import nuke, os, json, re

json_path = os.path.dirname(__file__).replace("\\", "/") + "/render_log.json"

def unifyFrameVar(s):
    """Unify frame variable representation."""
    return re.sub(r"%\d*d", "%d", re.sub(r"#+", "%d", s))

def get_file_path_from_knob(kn):
    filename = unifyFrameVar(os.path.basename(kn.value()))
    dirname = os.path.dirname(kn.getEvaluatedValue())
    return f"{dirname}/{filename}"

def renderLog():
    node = nuke.thisNode()
    nkPath = nuke.root().name()
    if node.Class() == "Write" and nkPath != "Root":
        path = get_file_path_from_knob(node["file"])
        if path and nkPath:
            if not os.path.isfile(json_path):
                with open(json_path, "w") as f:
                    f.write("{}")
            with open(json_path, "r") as f:
                json_data = json.load(f)
            json_data[path] = nkPath
            with open(json_path, "w") as f:
                json.dump(json_data, f, indent=1)

def getRelatedScriptPath():
    if not os.path.isfile(json_path):
        nuke.message(f"Can't find {json_path}")
        return
    
    node = nuke.selectedNode()
    kn = node.knob("file")
    if not kn:
        nuke.message("Select Read or Write node")
        return
    
    local_kn = node.knob("localizationPolicy")
    if local_kn:
        # Temporarily disable localization to get the correct file path (getEvaluatedValue returns original path only when localization is off)
        local_value = local_kn.value()
        local_kn.setValue("off")
        path = get_file_path_from_knob(kn)
        local_kn.setValue(local_value)
    else:
        path = get_file_path_from_knob(kn)
    with open(json_path, "r") as f:
        json_data = json.load(f)
    nkPath = json_data.get(path)
    nuke.message(nkPath if nkPath else "No data for this file")
