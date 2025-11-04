# Sets Nuke's autosave to the 'autosaves' folder next to the script

# v1.2.0
# created by: Pushkarev Aleksandr

import nuke

MODE = True  # If False, sets the default value

kn = nuke.toNode('preferences')['AutoSaveName']
if MODE:
	kn.setValue(r'[set rn [value root.name]; if {$rn eq ""} {return [getenv NUKE_TEMP_DIR]/.autosave} else {set af [file dirname $rn]/autosaves/; if {[file isdirectory $af]==0} {file mkdir $af}; return $af[file tail $rn].autosave}]')
else:  # Default value
	kn.setValue(r'[firstof [value root.name] [getenv NUKE_TEMP_DIR]/].autosave')
