# Adds a menu with popular colorspaces and shortcuts for them. Sets the colorspace depending on color management

# v1.7.0
# created by: Pushkarev Aleksandr

# v1.4.0 Moved menu creation outside
# v1.5.0 Minor reorganization/refactoring of the script. Now the script can set colorspace in NukeStudio
# v1.6.0 Added menu creation with popular colorspaces and shortcuts for them
# v1.7.0 ACES 1.3: display mode for sRGB/Rec.709 on Write, OCIODisplay after Read

import nuke

COLORSPACES = {
    "ACES2065-1": {"spaces": ["ACES - ACES2065-1", "ACES2065-1"]},
    "ACEScg": {"spaces": ["ACES - ACEScg", "ACEScg"]},
    "sRGB": {
        "spaces": ["Output - sRGB", "sRGB"],
        "display": "sRGB - Display",
    },
    "Rec.709": {
        "spaces": ["Output - Rec.709", "rec709"],
        "display": "Rec.1886 Rec.709 - Display",
    },
    "sRGB - Texture": {"spaces": ["Utility - sRGB - Texture", "sRGB - Texture"]},
    "Linear - sRGB": {"spaces": ["Utility - Linear - sRGB", "Linear Rec.709 (sRGB)", "linear"]},
    "RED - REDlogFilm - REDcolor3": {"spaces": ["Input - RED - REDlogFilm - REDcolor3", "REDLog"]},
    "RED - REDLog3G10 - REDWideGamutRGB": {
        "spaces": ["Input - RED - REDLog3G10 - REDWideGamutRGB", "Log3G10 REDWideGamutRGB", "REDLog"]
    },
    "ARRI - V3 LogC (EI160) - Wide Gamut": {
        "spaces": ["Input - ARRI - V3 LogC (EI160) - Wide Gamut", "ARRI LogC3 (EI800)", "AlexaV3LogC"]
    },
}


def _is_fn_nuke_ocio():
    knob = nuke.root().knob("OCIO_config")
    return knob is not None and knob.value().startswith("fn-nuke_")


def _resolve_knob_value(knob, candidates):
    """Pick first matching value from knob enumeration."""
    if knob is None:
        return None
    for candidate in candidates:
        for value in knob.values():
            short = value.split("\t\t")[0].split("/")[-1]
            if value == candidate or short == candidate:
                return candidate
    return None


def _restore_selection(nodes):
    for node in nuke.allNodes():
        node.setSelected(False)
    for node in nodes:
        node.setSelected(True)


def _find_read_ocio_display(read_node):
    for node in read_node.dependent(nuke.INPUTS | nuke.HIDDEN_INPUTS):
        if node.Class() == "OCIODisplay" and node.input(0) is read_node:
            return node
    return None


def _remove_read_ocio_display(read_node):
    ocio = _find_read_ocio_display(read_node)
    if ocio is None:
        return
    for node in ocio.dependent(nuke.INPUTS | nuke.HIDDEN_INPUTS):
        for i in range(node.inputs()):
            if node.input(i) is ocio:
                node.setInput(i, read_node)
    nuke.delete(ocio)


def _add_read_ocio_display(read_node, display):
    ocio = _find_read_ocio_display(read_node)
    if ocio is not None:
        ocio["display"].setValue(display)
        ocio["invert"].setValue(True)
        return

    for node in nuke.allNodes():
        node.setSelected(False)
    read_node.setSelected(True)

    ocio = nuke.createNode("OCIODisplay", inpanel=False)
    ocio["display"].setValue(display)
    ocio["invert"].setValue(True)


def _configure_write(write_node, target_cs, display_mode, display):
    if display_mode:
        write_node["transformType"].setValue("display")
        write_node["ocioDisplay"].setValue(display)
    else:
        write_node["transformType"].setValue("colorspace")
        write_node["colorspace"].setValue(target_cs)


def _configure_read(read_node, target_cs, display_mode, display):
    if display_mode:
        read_node["raw"].setValue(True)
        _add_read_ocio_display(read_node, display)
    else:
        _remove_read_ocio_display(read_node)
        read_node["raw"].setValue(False)
        read_node["colorspace"].setValue(target_cs)


def setColorspace(config):
    """
    config: colorspace entry dict with 'spaces' list and optional 'display' name,
            or legacy list of colorspace names.
    """
    if isinstance(config, list):
        config = {"spaces": config}

    spaces = config["spaces"]
    display = config.get("display")

    if nuke.env["studio"]:
        import hiero.ui

        active_view = hiero.ui.activeView()
        if not isinstance(active_view, hiero.ui.BinView):
            return
        items = active_view.selection()
    else:
        items = nuke.selectedNodes("Read") + nuke.selectedNodes("Write")

    if not items:
        return

    selected_nodes = nuke.selectedNodes() if not nuke.env["studio"] else None

    try:
        display_mode = (
            not nuke.env["studio"]
            and _is_fn_nuke_ocio()
            and display is not None
        )

        target_cs = _resolve_knob_value(nuke.root().knob("int8Lut"), spaces)
        if target_cs is None and not display_mode:
            nuke.message("Can't find colorspace, try to change nuke's colormanagement")
            return

        for item in items:
            if nuke.env["studio"]:
                if target_cs is None:
                    nuke.message("Can't find colorspace, try to change nuke's colormanagement")
                    return
                item.activeItem().setSourceMediaColourTransform(target_cs)
                continue

            if item.Class() == "Write":
                _configure_write(item, target_cs, display_mode, display)
            elif item.Class() == "Read":
                _configure_read(item, target_cs, display_mode, display)
    finally:
        if selected_nodes is not None:
            _restore_selection(selected_nodes)


def addColorspaceMenu(menu: nuke.Menu):
    for i, name in enumerate(COLORSPACES):
        config = COLORSPACES[name]
        menu.addCommand(
            f"Colorspaces/{name}",
            f"import setColorspace; setColorspace.setColorspace({config!r})",
            f"Alt+{i + 1}",
            shortcutContext=0 if nuke.env["studio"] else 2,
        )
