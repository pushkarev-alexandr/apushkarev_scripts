# Returns the Blocky filter which is available in Nuke but hidden by default

# created by: Pushkarev Aleksandr

import nuke

nuke.menu('Nodes').addCommand('Filter/Blocky', 'nuke.createNode("Blocky")', icon='Blocky.png')
