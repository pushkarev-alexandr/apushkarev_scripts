# When saving the script, all colorspaces in Reads and Writes are baked

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke

def bakeColorspace(csKn):
    shortName = csKn.value()
    fullName = csKn.enumName(int(csKn.getValue()))

    spl = fullName.split()
    if len(spl) > 2:
        if shortName == spl[0] and shortName == spl[1]:
            brackCS = ' '.join(spl[2:len(spl)])
            if brackCS[0] == '(' and brackCS[-1] == ')':
                return brackCS[1:-1]
        elif fullName.startswith('Colorspaces/'):
            return shortName
    elif shortName == fullName and shortName.startswith('default (') and shortName.count('(') == 1 and shortName.count(')') == 1:
        typeName = shortName[shortName.index('(')+1:shortName.index(')')]
        for i in range(15):
            spl = csKn.enumName(i).split()
            if len(spl) > 2 and typeName == spl[0] and typeName == spl[1]:
                brackCS = ' '.join(spl[2:len(spl)])
                if brackCS[0] == '(' and brackCS[-1] == ')':
                    return brackCS[1:-1]
        return typeName
    return shortName

def colorspaceAutobaking():
    for node in nuke.allNodes('Read') + nuke.allNodes('Write'):
        node['colorspace'].setValue(bakeColorspace(node['colorspace']))

# onUserCreate does not allow getting the values of file and colorspace, so we do this when saving the script
nuke.addOnScriptSave(colorspaceAutobaking)
