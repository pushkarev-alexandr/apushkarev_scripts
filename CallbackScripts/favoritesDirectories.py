# When opening a script in the favorites chooser, a folder named 'nk' is added, which points to the folder where the currently opened script is stored

# v1.0.2
# created by: Pushkarev Aleksandr

# changelog:
# v1.0.0 initial release
# v1.0.1 added 'render' folder
# v1.0.2 added 'precomp' folder, renamed script to favoritesDirectories

import nuke, os

def favoritesDirs():
    rootname = nuke.root().name()
    if rootname != 'Root':
        dirname = os.path.dirname(rootname)
        render = os.path.dirname(dirname) + '/3d/render'
        precomp = os.path.dirname(dirname) + '/precomp'
        if os.path.isdir(dirname):
            nuke.addFavoriteDir('nk', dirname+'/')
        if os.path.isdir(render):
            nuke.addFavoriteDir('render', render+'/')
        if os.path.isdir(precomp):
            nuke.addFavoriteDir('precomp', precomp+'/')

nuke.addOnScriptLoad(favoritesDirs)
