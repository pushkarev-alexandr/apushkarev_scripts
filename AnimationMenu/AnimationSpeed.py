# Adds knobs and sets an expression on the selected knob to control the speed of its value change

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke

def SetAnimationSpeed():
    node = nuke.thisNode()
    kn = nuke.thisKnob()
    anims = nuke.animations()
    knName = kn.name()
    fullKnobName = knName
    # Get a list of all suffixes for the current knob [x,y] [r,g,b,a]
    # Empty list if the knob has no suffixes
    indexLst = []
    for i in range(kn.width()):
        n = kn.fullyQualifiedName(i)
        if n.count('.') == 2:
            indexLst.append(n.split('.')[2])
    index = 0
    if len(anims) == 1 and anims[0].count('.'):
        i = anims[0].split('.')[1]
        fullKnobName = anims[0]
        if i in indexLst:
            index = indexLst.index(i) + 1
    # Get the knob value; if the entire knob is selected, take the first value
    # Ideally, the knob created should be of the same type as the original
    if index:
        value = kn.value(index - 1)
    else:
        try:
            value = kn.value()[0]
        except:
            value = kn.value()

    # Creating necessary knobs
    # Tab
    if not node.knob('animation_speed_tab'):
        node.addKnob(nuke.Tab_Knob('animation_speed_tab', 'Animation Speed'))
    # Divider
    txtKnName = '{}_speed_text'.format(fullKnobName.replace('.', ''))
    if not node.knob(txtKnName):
        node.addKnob(nuke.Text_Knob(txtKnName, fullKnobName + ' speed'))
    # Start Frame
    startFrKnName = '{}_start_frame'.format(fullKnobName.replace('.', ''))
    if not node.knob(startFrKnName):
        node.addKnob(nuke.Int_Knob(startFrKnName, 'start frame'))
    startFrame = node.knob(startFrKnName)
    startFrame.setValue(nuke.frame())
    # Current Frame button
    buttonKnName = '{}_current_frame'.format(fullKnobName.replace('.', ''))
    if not node.knob(buttonKnName):
        node.addKnob(nuke.PyScript_Knob(buttonKnName, 'current frame', 'nuke.thisNode()["{}"].setValue(nuke.frame())'.format(startFrKnName)))
    # Start Value
    startValKnName = '{}_start_value'.format(fullKnobName.replace('.', ''))
    if not node.knob(startValKnName):
        node.addKnob(nuke.Double_Knob(startValKnName, 'start value'))
    startValue = node.knob(startValKnName)
    startValue.setValue(value)
    # Speed
    speedKnName = '{}_animation_speed'.format(fullKnobName.replace('.', ''))
    if not node.knob(speedKnName):
        node.addKnob(nuke.Double_Knob(speedKnName, 'animation speed'))
    speed = node.knob(speedKnName)
    speed.setValue(1)
    
    # Set expression
    expr = '{0}+(frame-{1})*{2}'.format(startValKnName, startFrKnName, speedKnName)
    if index:
        kn.setExpression(expr, index-1)
    else:
        kn.setExpression(expr)
