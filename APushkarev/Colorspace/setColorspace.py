# Adds a menu with popular colorspaces and shortcuts for them. Sets the colorspace depending on color management

# v1.6.0
# created by: Pushkarev Aleksandr

# v1.4.0 Moved menu creation outside
# v1.5.0 Minor reorganization/refactoring of the script. Now the script can set colorspace in NukeStudio
# v1.6.0 Added menu creation with popular colorspaces and shortcuts for them

# TODO
# - Add support for aces v1.3

import nuke

def setColorspace(spaces):
    """spaces: list of colorspaces by priority, e.g. ['Output - Rec.709', 'rec709']"""
    if nuke.env["studio"]:
        import hiero.ui
        activeView = hiero.ui.activeView()
        if not isinstance(activeView, hiero.ui.BinView):
            return
        items = activeView.selection()
    else:
        items = nuke.selectedNodes('Read') + nuke.selectedNodes('Write')
    
    if not items:
        return
    
    spaces = spaces if isinstance(spaces, list) else [spaces]
    availableCS = nuke.root().knob('int8Lut').values()

    targetCS = None
    for cs in availableCS:
        for sp in spaces:
            if cs==sp or cs.split('\t\t')[0].split('/')[-1]==sp:
                targetCS = sp
                break
        if targetCS:
            break

    if targetCS is None:
        nuke.message("Can't find colorspace, try to change nuke's colormanagement")
        return
    
    for item in items:
        if nuke.env["studio"]:
            item.activeItem().setSourceMediaColourTransform(targetCS)
        else:
            item['colorspace'].setValue(targetCS)
            item['raw'].setValue(False)

def addColorspaceMenu(menu: nuke.Menu):
    colorspaces = {
        "ACES2065-1": "ACES - ACES2065-1",
        "ACEScg": "ACES - ACEScg",
        "sRGB(Output - sRGB)": ["Output - sRGB", "sRGB"],
        "Rec.709": ["Output - Rec.709", "rec709"],
        "sRGB - Texture": "Utility - sRGB - Texture",
        "Linear - sRGB": "Utility - Linear - sRGB",
        "RED - REDlogFilm - REDcolor3": "Input - RED - REDlogFilm - REDcolor3",
        "RED - REDLog3G10 - REDWideGamutRGB": "Input - RED - REDLog3G10 - REDWideGamutRGB",
        "ARRI - V3 LogC (EI160) - Wide Gamut": "Input - ARRI - V3 LogC (EI160) - Wide Gamut"
    }
    for i, name in enumerate(colorspaces):
        cs = "'{}'".format(colorspaces[name]) if isinstance(colorspaces[name], str) else colorspaces[name]
        menu.addCommand(f"Colorspaces/{name}", f"import setColorspace; setColorspace.setColorspace({cs})", f"Alt+{i+1}", shortcutContext = 0 if nuke.env["studio"] else 2)
