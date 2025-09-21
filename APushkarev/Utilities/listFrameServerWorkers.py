# Displays a list of available server workers for rendering

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke
from hiero.ui.nuke_bridge.FnNsFrameServer import frameServer

def listFrameServerWorkers():
    lst = []
    for worker in frameServer.getStatus(1).workerStatus:
        name = worker.address.split(" - ")[1].lower()
        if name not in lst:
            lst.append(name)
    lst.sort()
    nuke.message("\n".join(lst + [f"\ncount: {len(lst)}"]))
