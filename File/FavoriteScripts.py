# Adds an interface for favorite scripts that can be opened via shortcut or from a list

# v1.4.0
# created by: Pushkarev Aleksandr

import nuke, json, getpass, os, re

json_path = os.path.dirname(__file__).replace('\\','/') + '/FavoriteScripts.json'
favorite_menu_name = 'Favorite Scripts'

def openScript(filename):
    """Opens the specified script, searching for versions with hash marks in the name. The number of hash marks doesn't matter"""
    basename = os.path.basename(filename)
    if os.path.isfile(filename):  # If the file exists, simply open the script
        nuke.scriptOpen(filename)
        return
    elif basename.count('#') == 1:  # If the file doesn't exist, check if it's the latest version file
        dirname = os.path.dirname(filename)
        if os.path.isdir(dirname):
            lst = os.listdir(dirname)
            lst.reverse()
            pattern = re.sub(r'#+', r'\d+', basename)  # Replace any consecutive hash marks with \d+ to search for versions
            for f in lst:
                if re.fullmatch(pattern, f):
                    scriptFile = os.path.join(dirname, f)
                    if scriptFile.endswith('.nk') and os.path.isfile(scriptFile):
                        nuke.scriptOpen(scriptFile)
                        return
        nuke.message(f"Can't find any version of {filename} file")
        return
    nuke.message(f"Can't find {filename}")

def createMenuFromList(userNkLst=[]):
    """Creates a favorite scripts menu from a list of files for the user"""
    file_menu = nuke.menu('Nuke').menu('File')
    favorite_menu = file_menu.menu(favorite_menu_name)
    # If the menu exists, clear all items in it, if it doesn't exist, create it
    if favorite_menu:
        favorite_menu.clearMenu()
    else:
        favorite_menu = file_menu.addMenu(favorite_menu_name, index=3)

    # Iterate through the list and create menu items for each element if the file ends with .nk
    for i, filename in enumerate(userNkLst):
        if filename.endswith('.nk'):
            if i <= 9:
                favorite_menu.addCommand(os.path.basename(filename), f"FavoriteScripts.openScript('{filename}')", f'Ctrl+Alt+{i+1}')
            else:
                favorite_menu.addCommand(os.path.basename(filename), f"FavoriteScripts.openScript('{filename}')")
    
    # Add mandatory menu items
    favorite_menu.addCommand('Add Script...', 'FavoriteScripts.addScriptToMenu()')
    favorite_menu.addCommand('Remove Script...', 'FavoriteScripts.removeScriptFromMenu()')
    favorite_menu.addCommand('Update menu', 'FavoriteScripts.updateMenu()')

def addScriptToMenu():
    """Adds a script to the json file and to the menu"""
    filename = nuke.getFilename('Choose script file', '*.nk')
    
    if filename and filename.endswith('.nk'):
        if not os.path.isfile(json_path):
            with open(json_path, 'w') as file:
                file.write('{}')
        
        with open(json_path, 'r') as file:
            json_data: dict = json.load(file)
        
        user = getpass.getuser()
        json_data.setdefault(user, [])
        if filename not in json_data[user]:
            json_data[user].append(filename)
        
        with open(json_path, 'w') as file:
            json.dump(json_data, file, indent=4)
        
        createMenuFromList(json_data.get(user))

def removeScriptFromMenu():
    """Removes a script from the menu and database"""
    if not os.path.isfile(json_path):
        nuke.message(f'Cannot find file: {json_path}')
        return
    with open(json_path, 'r') as file:
        json_data: dict = json.load(file)
    
    userNkLst = json_data.get(getpass.getuser())
    if not userNkLst:
        return
    p = nuke.Panel('Remove Scripts from Favorites')
    for filename in userNkLst:
        p.addBooleanCheckBox(os.path.basename(filename), False)
    if not p.show():
        return
    for i in reversed(range(len(userNkLst))):
        if p.value(os.path.basename(userNkLst[i])):
            del userNkLst[i]
    with open(json_path, 'w') as file:
        json.dump(json_data, file, indent=4)

    createMenuFromList(userNkLst)

def updateMenu():
    """Creates the menu on Nuke startup"""
    if os.path.isfile(json_path):
        with open(json_path, 'r') as file:
            json_data: dict = json.load(file)
        userNkLst = json_data.get(getpass.getuser())
        if userNkLst:
            createMenuFromList(userNkLst)
            return
    createMenuFromList()  # If there's no settings file or no settings for the user or the settings list is empty, create a menu without a script list

updateMenu()
