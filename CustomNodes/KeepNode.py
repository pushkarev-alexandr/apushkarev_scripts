# In addition to the Remove node, adds a Keep node that creates a Remove node with the "keep" operation and "rgba" channels

# created by: Pushkarev Aleksandr

import nuke

nuke.menu('Nodes').addCommand('Channel/Keep', "n=nuke.createNode('Remove'); n['operation'].setValue('keep'); n['channels'].setValue('rgba')", icon='Add.png')
