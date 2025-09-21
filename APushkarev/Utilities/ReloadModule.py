# Reloads a module with the specified name. Useful when changes have been made to the module and you don't want to restart Nuke

#v1.0.0
#created by: Pushkarev Aleksandr

import nuke
import importlib

def ReloadModule():
    module_name = nuke.getInput("Module name")
    if not module_name:
        return

    try:
        module = importlib.import_module(module_name)
        importlib.reload(module)
        nuke.message(f"Module {module_name} successfully reloaded")
        return module
    except ImportError:
        nuke.message(f"Error: module {module_name} not found")
        return None
    except Exception as e:
        nuke.message(f"Error reloading module {module_name}: {e}")
        return None
