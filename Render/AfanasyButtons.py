# This module provides functions to interact with the Afanasy render farm from Nuke.
# It allows users to set their render node status to "Free" (available for rendering) or to "NIMBY",
# which marks the node as unavailable for rendering and ejects all currently assigned tasks.

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke
import json
import afnetwork, cgruconfig

def send_action(params: dict = None, operation: dict = None):
    action = {
        "user_name": cgruconfig.VARS["USERNAME"],
        "host_name": cgruconfig.VARS["HOSTNAME"],
        "type": "renders",
        "mask": cgruconfig.VARS["HOSTNAME"]
    }
    if params:
        action["params"] = params
    if operation:
        action["operation"] = operation
    afnetwork.sendServer(json.dumps({"action": action}))

def setFree():
    send_action({"nimby": False})

def ejectAndNIMBY():
    send_action({"NIMBY": True}, {"type": "eject_tasks"})
