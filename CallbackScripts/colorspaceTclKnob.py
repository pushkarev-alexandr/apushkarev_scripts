# Adds a knob to the Write node that remaps colorspace values, and this knob can be used as a variable for colorspace via [value csp]

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke

def manageCspTclKnob():
    old_kn_name = 'old_csp'  # If you need to change the knob name, write the old one here, and the new one in kn_name
    kn_name = 'csp'  # The current name for the colorspace knob

    # tcl for the knob, can be updated, extended, and edited
    csp_tcl = kn_name + ' "\\[set csp \\[value colorspace]\\nset in \\[list \\"ACES - ACES2065-1\\" \\"ACES - ACEScg\\" \\"Output - sRGB\\" \\"Output - Rec.709\\" \\"Utility - Linear - sRGB\\" \\"Utility - sRGB - Texture\\"]\\nset out \\[list aces acescg srgb rec709 linear texture]\\nset i \\[lsearch \\$in \\$csp]\\nif \\{\\[value raw]\\} \\{return raw\\} elseif \\{\\$i != -1\\} \\{lindex \\$out \\$i\\}]"'

    node = nuke.thisNode()
    if node.knob(old_kn_name):  # If there is a knob with the old name, remove it
        node.removeKnob(node.knob(old_kn_name))
        file = node['file'].value()
        new_file = file.replace('[value {}]'.format(old_kn_name), '[value {}]'.format(kn_name))
    node['file'].setValue(new_file)  # Change the expression in the file so the user doesn't notice anything
    knobs = node.writeKnobs(nuke.TO_SCRIPT | nuke.WRITE_NON_DEFAULT_ONLY).split('\n')
    if not node.knob(kn_name):  # If it doesn't exist, create it
        node.readKnobs('addUserKnob {43 ' + kn_name + ' l colorspace +INVISIBLE}\n' + csp_tcl)
    elif csp_tcl not in knobs:  # If it exists, but the tcl code needs to be updated
        node.readKnobs(csp_tcl)

nuke.addOnCreate(manageCspTclKnob, nodeClass='Write')
