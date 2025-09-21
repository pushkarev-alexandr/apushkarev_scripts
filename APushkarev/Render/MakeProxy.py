# Renders proxy to the Temp folder for selected reads and sets the path in Read proxy

# v1.0.1
# created by: Pushkarev Aleksandr

# v1.0.0 initial release
# v1.0.1 set channels to rgba for write

import nuke, nukescripts
import os
from pathlib import Path

def main():
    nodes = nuke.selectedNodes("Read")
    nukescripts.clear_selection_recursive()

    nuke.root()["proxy"].setValue(True)

    for read in nodes:
        path = Path(read["file"].value())
        proxy_path = str(Path(os.getenv("NUKE_TEMP_DIR")) / "proxy" / f"{path.parent.name}_proxy" / path.name).replace("\\", "/")

        write = nuke.createNode("Write", inpanel=False)
        write.setInput(0, read)
        write["proxy"].setValue(proxy_path)
        write["file_type"].setValue(path.suffix[1:])
        write["colorspace"].setValue(read["colorspace"].value())
        write["channels"].setValue("rgba")
        nuke.execute(write, read["first"].value(), read["last"].value())
        nuke.delete(write)

        read["proxy"].fromUserText(proxy_path)
