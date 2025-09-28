# Saves a pair of keys (file path) and (path to the script that rendered it) to a database
# Limitation: if the file is moved, the link (file path) -> (script path) is lost

# v1.2.1
# created by: Pushkarev Aleksandr

# changelog:
# v1.0.0 - Initial release
# v1.1.0 - Refactor: streamline file path handling and improve code readability. Now works correctly for Read nodes with localization enabled
# v1.2.0 - Migration: switched from JSON file storage to SQLite database for improved performance and reliability
# v1.2.1 - You can pass a node as an argument to the renderLog function, so you can use this script anywhere. It is used before sending a render to the render farm.

import nuke, os, sqlite3, re

db_path = os.path.join(os.path.dirname(__file__), "render_log.sqlite")

def unifyFrameVar(s):
    """Unify frame variable representation."""
    return re.sub(r"%\d*d", "%d", re.sub(r"#+", "%d", s))

def get_file_path_from_knob(kn):
    filename = unifyFrameVar(os.path.basename(kn.value()))
    dirname = os.path.dirname(kn.getEvaluatedValue())
    return f"{dirname}/{filename}"

def _init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS render_log (
            file_path TEXT PRIMARY KEY,
            script_path TEXT
        )
    """)
    conn.commit()
    conn.close()

def renderLog(node = None):
    if node is None:
        node = nuke.thisNode()
    nkPath = nuke.root().name()
    if node.Class() == "Write" and nkPath != "Root":
        path = get_file_path_from_knob(node["file"])
        if path and nkPath:
            _init_db()
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("REPLACE INTO render_log (file_path, script_path) VALUES (?, ?)", (path, nkPath))
            conn.commit()
            conn.close()

def getRelatedScriptPath():
    if not os.path.isfile(db_path):
        nuke.message(f"Can't find {db_path}")
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

    _init_db()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT script_path FROM render_log WHERE file_path = ?", (path,))
    row = c.fetchone()
    conn.close()
    nkPath = row[0] if row else None
    nuke.message(nkPath if nkPath else "No data for this file")
