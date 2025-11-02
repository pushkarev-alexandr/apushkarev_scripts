# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.

# Added comments to the standard Nuke autolabel, added my own custom labels and label removal logic.
# All additions are wrapped in CUSTOM BLOCK tags with numbers. Inline additions are marked with EDITED comments.
# Installation: place this file in any pluginPath folder and it will work instead of the standard autolabel.

# v2.0.0
# modified by: Pushkarev Aleksandr

import os
import nuke_internal as nuke
import re
import math

def __concat_result_string(name, label):
  """Combines the name and label, moves the label to a new line, and removes leading and trailing spaces"""
  if label is None or label == "":
    return name
  return str(name + "\n" + label).strip()

class ColorspaceStringExtractor:
  def __init__(self):
    self.__colorspace_str = str()

  def __stripDefaultStrings(self, csName):
    if csName.startswith("default"):
      if csName == "default":
        csName = "" # this should not happen, this is the final fallback if all else has gone wrong
      else:
        csName = csName[9:-1] # strip off "default (" and ")"
        if csName == "custom":
          csName = ""
    return csName

  # Only take the name before any tab characters as those are delimiters from the Colorspace knob
  def __stripTabSuffixFromName(self, csName):
    if csName:
      return csName.split('\t')[0]
    return ""

  def __extractRoleName(self, csName):
    r"""
    Based on the formatting in ColorspaceKnob.cpp, the role string
    will appear as such: "role\trole (colorspace)". Since we don't
    want to display the role name twice, we need to extract the
    second occurrence along with it's colorspace.

    Returns "role (colorspace)", else will return None.
    """
    result = re.search(r".+\t(.+\s\(.+\))$", csName)
    if result is not None:
      return result.group(1)
    return None

  def extractColorspaceFromKnobValue(self, csKnobValue):
    csName = self.__extractRoleName(csKnobValue)
    if csName:
      self.__colorspace_str = csName
    else:
      csName = self.__stripDefaultStrings(csKnobValue)
      if csName:
        csName = os.path.basename(csName)
        self.__colorspace_str = "(" + self.__stripTabSuffixFromName(csName) + ")"

  def result(self):
    return self.__colorspace_str

def _getAutoLabelColorspace(cs_extractor):
  """
  returns the colorspace-name string to use on auto-labels
  handles defaults, NUKE vs OCIO modes and NUKE UI.
  """
  labelType = "colorspace"
  labelKnob = None
  transformKnob = nuke.thisNode().knob("transformType")
  
  if transformKnob and transformKnob.enabled() and transformKnob.visible():
      labelType = transformKnob.value()

  # Transform type knob may not directly match the knob name.
  if labelType == "colorspace":
    labelKnob = nuke.thisNode().knob("colorspace")
  elif labelType == "display":
    labelKnob = nuke.thisNode().knob("display")

  if labelKnob and labelKnob.enabled():
    csId = int(labelKnob.getValue())
    if not nuke.usingOcio():
      isDefault = (0 == csId)
      if isDefault :
        # maintaining old behaviour, don't show the colorspace in the autolabel
        # in NUKE colorspace mode
        return ""
    cs_extractor.extractColorspaceFromKnobValue(list(labelKnob.values())[csId])
  else:
    return ""

  if not cs_extractor.result():
    # fall back to tcl if we don't have a colorspace
    cs_extractor.extractColorspaceFromKnobValue(nuke.value(labelType))
  assert cs_extractor.result() != "."

def getSelectionFromSceneGraph(scene_graph_knob):
  selected_items = scene_graph_knob.getSelectedItems()
  if len(selected_items) > 0:
    return selected_items[-1]

def extractGeoObjectName(_class):
  geo_objects = ["Camera3", "Axis3", "Light3"]
  label = str()

  if _class in geo_objects:
    node = nuke.thisNode()
    read_from_file_knob = node.knob("read_from_file")
    if not read_from_file_knob or not read_from_file_knob.value():
      return label

    scene_graph_knob = node.knob("scene_graph")
    if scene_graph_knob:
      return getSelectionFromSceneGraph(scene_graph_knob)

    node_name_knob = node.knob("fbx_node_name")
    if node_name_knob:
      default_name = "-------          "; # declared/defined in SceneReader.cpp
      selected_value = int(node_name_knob.getValue())
      selected_string = node_name_knob.values()[selected_value]
      if selected_string != default_name:

        file_ext = ""
        if node.knob("file"):
          file_path = node.knob("file").value()
          file_ext = os.path.splitext(file_path)[1].lower()

        # abc files display the entire path for their node name knob
        # we're only interested in the object name so this should be extracted.
        # This may be a temporary solution before the "node name" knob is made
        # more consistent across file formats.
        if file_ext == ".abc":
          label = os.path.basename(selected_string)
        elif file_ext:
          label = selected_string
    if node.knob("file"):  # EDITED: added so that instead of fbx_node_name, the file name is displayed
      label = os.path.basename(node.knob("file").value())
  return label

# CUSTOM BLOCK 1: Custom Functions
def removeLabel(labelKn, labelsToDelete):
  """Takes a label knob and removes from it the labels specified in labelsToDelete"""
  label = labelKn.value()
  if label == '':  # If the label is empty, nothing to remove
    return
  if isinstance(labelsToDelete, str):  # If input is a string, not a list, put it into a list
    labelsToDelete = [labelsToDelete]
  for toDelete in labelsToDelete:  # Iterate over all labels to delete
    if label.count(toDelete):
        if label == toDelete:
            label = ''
            break
        elif label.startswith(toDelete + '\n'):
            label = label.replace(toDelete + '\n', '')
        else:
            label = label.replace('\n' + toDelete, '')
  if labelKn.value() != label:  # If the label has changed
    try:  # Try/except is used because, for example, in LiveGroup node the label is read-only and Nuke throws an error
      labelKn.setValue(label)
    except:
      pass

def customPlusLabel(custom, label):
  """Properly combines the label and custom text (if the label is empty, just return the custom text; if not empty, prepend the custom text with a newline before the label)"""
  if label:
    if custom:
      return custom + "\n" + label
    else:
      return label
  else:
    return custom

# SHUFFLE2 Custom Functions
def isInConnectedToAny(node, inNum=0):
  """Checks if in1 or in2 is connected to anything. inNum=0 is in1, inNum=1 is in2"""
  mappings = node.knob('mappings').value()
  for m in mappings:
    if m[0] == inNum:
      return True
  return False

def getInputLayersList(node):
  """Returns a list of input channels that are connected to the output; if it's rgba, returns an empty list"""
  inLst = []
  for i in range(2):
    if isInConnectedToAny(node, i):
      value = node.knob(f'in{i + 1}').value()
      if value not in inLst:
        inLst.append(value)
  rgbLst = ['rgba', 'rgb', 'alpha']
  if len(inLst)==2:
    if inLst[0] in rgbLst and inLst[1] in rgbLst:
      inLst = []
  elif len(inLst)==1:
    if inLst[0] in rgbLst:
      inLst = []
  return inLst

def getOutputLayersList(node):
    """Returns a list of filtered output layers"""
    outLst = []
    mappings = node.knob('mappings').value()
    for m in mappings:
        if m[0] != -1:
            layerName = m[2].split('.')[0]
            if layerName not in outLst:
                outLst.append(layerName)
    outVals = [node.knob('out1').value(), node.knob('out2').value()]
    if 'forward' in outLst and 'backward' in outLst:
        if outVals[0] == 'motion':
            outLst.remove('forward')
            outLst.remove('backward')
            outLst.insert(0,'motion')
        elif outVals[1]=='motion':
            outLst.remove('forward')
            outLst.remove('backward')
            outLst.append('motion')
    if 'disparityL' in outLst and 'disparityR' in outLst:
        outLst.remove('disparityL')
        outLst.remove('disparityR')
        if outLst and node.knob('out1').value() == 'disparity':
            outLst.insert(0, 'disparity')
        else:
            outLst.append('disparity')
    if len(outLst) == 2:
        rgbLst = ['rgba', 'rgb', 'alpha']
        if outLst[0] == 'rgba' and outVals[0] in rgbLst:
            outLst[0] = outVals[0]
        elif outLst[1] == 'rgba' and outVals[1] in rgbLst:
            outLst[1] = outVals[1]
    elif len(outLst) == 1:
        if outLst[0] == 'rgba':
            outLst = []
    return outLst

def getShuffleLayersLabel(node):
  """Returns a label for the Shuffle2 node"""
  ret = ''
  inLst = getInputLayersList(node)
  outLst = getOutputLayersList(node)
  if inLst:
    ret += '/'.join(inLst)
    if outLst:
      ret += '>>' + '/'.join(outLst)
  elif outLst:
    ret += '/'.join(outLst)
  if len(inLst) == 1 and len(outLst) == 1 and inLst[0] == outLst[0]:
    ret = inLst[0]
  return ret
# END OF CUSTOM BLOCK 1

def autolabel():
  """This function is run automatically by Nuke during idle, and the return
  text is drawn on the box of the node. It can also have side effects by
  setting knobs. Currently two knobs are provided that are useful:

  indicators = integer bit flags to turn icons on/off. The icons
  named indicator1, indicator2, indicator4, indicator8, etc are
  drawn if the corresponding bit is on. By default these are loaded
  from the path as indicator1.xpm, etc, but you can use the load_icon
  command to load other files.

  icon = name of a whole extra image you can draw, but it replaces
  any previous one."""

  # do the icons:
  # Checks if the node has animation, expression, clones, viewsplit, or link(Nuke16 or later), to set the corresponding indicators
  ind = nuke.expression("(keys?1:0)+(has_expression?2:0)+(clones?8:0)+(viewsplit?32:0)" + ("+(linked_node>0?(linked_node>1?192:64):0)" if nuke.NUKE_VERSION_MAJOR > 15 else ""))

  if int(nuke.numvalue("maskChannelInput", 0)) :  # Checks if maskChannelInput exists, which is when the node is masked by its internal mask rather than an external one
    ind += 4
  if int(nuke.numvalue("this.mix", 1)) < 1:  # mix indicator
    ind += 16

  try:
    this = nuke.toNode("this")  # Safely gets the current node
  except:
    pass
  if not this:
    return ""

  nuke.knob("this.indicators", str(ind))  # Sets the calculated value to the 'indicators' knob, which controls the display of icons for clone, animation, expressions, etc.

  # do stuff that works even if autolabel is turned off:
  # Refers to the checkbox in Nuke settings Edit/Preferences.../NodeGraph/autolabel
  name = nuke.value("name")  # Name of the current node
  _class = this.Class()


  # CUSTOM BLOCK 2: preparing the label for the current node, removing TCL that previously displayed node information
  labelKn = this.knob('label')
  if labelKn:
    if _class=='Blur' or _class=='FilterErode':
      removeLabel(labelKn, '[value size]')
    elif _class=='Switch' or _class=='Dissolve':
      removeLabel(labelKn, '[value which]')
    elif _class=='Defocus':
      removeLabel(labelKn, '[value defocus]')
    elif _class=='TimeOffset':
      removeLabel(labelKn, '[value time_offset]')
    elif _class=='Tracker4' or _class=='Tracker3':
      removeLabel(labelKn, '[value transform] / ref:[value reference_frame]')
    elif _class=='Colorspace':
      removeLabel(labelKn, '[value colorspace_in] >> [value colorspace_out]')
    elif _class=='MotionBlur':
      removeLabel(labelKn, 'samples [value shutterSamples]')
    elif _class=='VectorDistort':
      removeLabel(labelKn, 'ref [value referenceFrame]')
    elif _class=='FrameRange':
      removeLabel(labelKn, '[value first_frame]-[value last_frame]')
    elif _class=='afanasy':
      removeLabel(labelKn, '[value framefirst]-[value framelast]')
    elif _class=='Mirror' or _class=='Mirror2':
      kn1 = this.knob(['Vertical', 'flip'][_class=='Mirror2'])
      kn2 = this.knob(['Horizontal', 'flop'][_class=='Mirror2'])
      if kn1 and kn2:
        res = ''
        if kn1.value():
          res = 'vertical'
          if kn2.value():
            res+='/horizontal'
        elif kn2.value():
          res = 'horizontal'
        removeLabel(labelKn, res)
    elif _class=='Shuffle2':
      removeLabel(labelKn, ['[value in1]', '[value in2]', '[value out1]', '[value out2]', '[value in]', '[value out]'])
    elif _class=='Saturation':
      removeLabel(labelKn, ['[value saturation]', 'saturation [value saturation]'])
    elif _class=='AppendClip':
      removeLabel(labelKn, '[value firstFrame]')
    elif _class=='Retime':
      removeLabel(labelKn, ['retime [value output.first]', 'Retime_[value output.first]', 'speed [value speed]'])
    elif _class.startswith('LD_3DE'):
      removeLabel(labelKn, '[value direction]')
    if this.knob('filter') and this.knob('filter').values()[2:7]==['Keys', 'Simon', 'Rifman', 'Mitchell', 'Parzen']:  # If there is a filter knob and it is a transform filter
      removeLabel(labelKn, ['[value filter]', 'filter [value filter]', 'filter: [value filter]', 'filter::[value filter]'])
    if this.knob('mix'):
      removeLabel(labelKn, ['mix [value mix]', 'Mix [value mix]', 'mix=[value mix]', 'Mix=[value mix]', 'mix = [value mix]', 'Mix = [value mix]'])
  # END OF CUSTOM BLOCK 2

  label = nuke.value("label")  # Get the label of the current node
  if not label:
    label = ""
  else:
    try:
      label = nuke.tcl("subst", label)  # Executes tcl code from the label
    except:
      pass

  # Class-specific handling
  if _class == "Dot" or _class == "BackdropNode" or _class == "StickyNote":
    return label
  # Reads and Writes
  elif _class.startswith("Read") or _class.startswith("DeepWrite") or _class.startswith("Write") or _class.startswith( "Precomp" ) or _class.startswith( "LiveGroup" ):
    # Precomp and LiveGroup nodes have a "read file for output" knob, which is when the node reads the rendered precomp instead of the script itself
    # The Write node has a "reading" knob, which is when the Write node acts as a Read and reads what it has rendered
    reading = int(nuke.numvalue("this.reading", 0 ))

    if reading and (_class.startswith( "Precomp" ) or _class.startswith( "LiveGroup" )):
      # For Precomp and LiveGroup nodes, it takes the Write node to which the Output node is connected and gets the filename with the current frame number from that Write node
      filename = nuke.filename( node = this.output().input(0), replace = nuke.REPLACE )
    else:
      filename = nuke.filename(replace = nuke.REPLACE)  # Returns the full path from the file knob and substitutes the current frame number
    if filename is not None:
      name = __concat_result_string(name, os.path.basename(filename))  # Combine the node name and the filename of the Write or Read node, using only the filename

    # The label (Read) is displayed if the reading knob is enabled
    # There is also a check for checkHashOnRead and proxy, which may result in displaying (Read - unchecked)
    if reading:
      checkHashOnRead = False
      if _class.startswith( "Precomp" ) or _class.startswith( "LiveGroup" ):
        if this.output() != None and this.output().input(0) != None:
          checkHashOnReadKnob = this.output().input(0).knob( "checkHashOnRead" )
          if checkHashOnReadKnob:
            checkHashOnRead = checkHashOnReadKnob.value()
      else:
        checkHashOnRead = this.knob("checkHashOnRead").value()

      if checkHashOnRead == True and ( this.proxy() != True ):
        name = name + "\n(Read)"
      else:
        name = name + "\n(Read - unchecked)"
  elif _class == 'DeepRead':  # For DeepRead, only the filename is displayed
    filename = nuke.filename(replace = nuke.REPLACE)
    if filename is not None:
      name =  __concat_result_string(name, os.path.basename(filename))
  elif _class == 'GeoImport' or _class == 'GeoExport':
    filename = nuke.filename(replace = nuke.REPLACE)
    if filename is not None:
      name =  __concat_result_string(name, os.path.basename(filename))
  # During rendering, ParticleCache displays the message (Rendering)
  # If the "read from file" checkbox is enabled, the message (Read) is displayed
  elif _class.startswith("ParticleCache" ):
    rendering = int(nuke.numvalue("this.particle_cache_render_in_progress", 0 ))
    if rendering:
      name = name + "\n(Rendering)"
    else:
      reading = int(nuke.numvalue("this.particle_cache_read_from_file", 0 ))
      if reading:
        name = name + "\n(Read)"
  elif _class == "UnrealReader":
    reading = int(nuke.numvalue("this.reading", 0 ))
    if reading:
      filename = nuke.filename(replace = nuke.REPLACE)
      if filename is not None:
        name = __concat_result_string(name, os.path.basename(filename))
      name = name + "\n(Read)"
    else:
      # add name of sequence used
      sequences = this["sequence"].values()
      selected_sequence = int(this["sequence"].getValue())
      if len(sequences) > 0 and selected_sequence < len(sequences):
        sequence_path = sequences[selected_sequence].split("/")
        name = name + "\n" + sequence_path[len(sequence_path) - 1]
  elif _class == 'GeoMerge':
    k = this.knob('mode')
    if k:
      name = __concat_result_string(name, ['(merge-layers)', '(duplicate-prims)', '(flatten)', '(flatten-all)', '(unisolate)'][int(k.getValue())])
  elif _class == 'GeoPrune' or _class == 'GeoIsolate':
    k = this.knob('method')
    if k:
      name = __concat_result_string(name, ['(Hide)', '(Show)', '(Deactivate)', '(Activate)'][int(k.getValue())])
  elif _class == "GeoConstrain":
    k = this.knob('constraint')
    if k:
      name = __concat_result_string(name, ['(look-at)', '(parent)', '(transformation)', '(translation)', '(rotation)', '(scale)'][int(k.getValue())])
  elif _class == "GeoScopePrim":
    name = __concat_result_string(name, '(create)')
  elif _class == "GeoXformPrim":
    k = this.knob('mode')
    if k:
      name = __concat_result_string(name, ['(create)', '(edit)'][int(k.getValue())])

  # Everything above plus the label is displayed now if autolabel is disabled in the settings or this is an OFX node
  if nuke.numvalue("preferences.autolabel") == 0 or _class.find("OFX", 0) != -1:
    return __concat_result_string(name, label)

  # build the autolabel:
  # Extra information

  # If there is an 'operation' knob, its value is displayed next to the node without a line break (ChannelMerge has a separate handler)
  operation = nuke.value('this.operation', '')
  if operation != '' and _class != 'ChannelMerge' and _class != 'Precomp' and _class != 'LiveGroup':
    name = name + ' (' + operation + ')'

  # Здесь подготавливаются значения layer, mask и unpremult некоторые из них не будут использоваться, некоторые перезапишутся позже
  layer = nuke.value("this.output", nuke.value("this.channels", "-"))  # Сюда записывается либо output, либо channels, либо прочерк(означает что layer выводить не нужно)
  mask = nuke.value("this.maskChannelInput", "none")  # Если у ноды есть кноб maskChannelInput он будет выводиться
  unpremult = nuke.value("this.unpremult", "none")  # Если у ноды есть кноб unpremult он будет выводиться

  # For Camera3, Axis3, Light3, layer is replaced with geo_object_label
  geo_object_label = extractGeoObjectName(_class)
  if geo_object_label:
    layer = geo_object_label

  cs_extractor = ColorspaceStringExtractor()

  if _class.startswith("Read") or _class.startswith("Write") or _class.startswith("DeepWrite"):
    # do colorspace labeling for reads and writes
    if int(nuke.numvalue("this.raw", 0)):
      layer = "RAW"
    else:
      _getAutoLabelColorspace(cs_extractor)

      # additional to NUKE-mode default colorspaces not being shown, if the
      # colorspace is set to "custom" (aka unintialised) in the UI the name
      # comes through as empty, so ignore it.
      if cs_extractor.result():
        layer = cs_extractor.result()

    # For the Write node, instead of maskChannelInput, render order will be displayed
    if _class.startswith("Write") or _class.startswith("DeepWrite"):
      order = nuke.numvalue("this.render_order", 1)
      mask = str(order)
      if int(order) == 1:
        mask = "none"

  # CUSTOM BLOCK 3: Custom Reformat, ChannelMerge and LD_3DE nodes
  elif _class == "Reformat":
    if nuke.expression("!type"):
      format = nuke.value("format")
      if format is not None:  # Removed root format check so it always shows the reformat destination
        format_list = format.split()
        layer = " ".join(format_list[7:])
    elif nuke.expression("type") == 2:  # Added scale output if scale mode is enabled
      layer = "scale " + str(nuke.numvalue("this.scale", 1))
  elif _class == "ChannelMerge":
    if nuke.value("A") == nuke.value("B") == nuke.value("output"):
      layer = operation
    else:
      if operation in ['union', 'intersect', 'stencil']:
        operation = operation[0].upper()
      elif operation == "absminus":
        operation = "abs-"
      elif operation == "plus":
        operation = "+"
      elif operation == "minus":
        operation = "-"
      elif operation == "multiply":
        operation = "*"
      layer = nuke.value("A") + " " + operation + " " + nuke.value("B") + " =\n" + nuke.value("output")
  elif _class.startswith('LD_3DE'):  # direction instead of channels will be displayed
    layer = nuke.value("direction")
  # END OF CUSTOM BLOCK 3

  elif _class == "Premult" or _class == "Unpremult":
    # For Premult and Unpremult nodes, unpremult will not be displayed if its value is "alpha"
    unpremult = nuke.value("alpha")
    if unpremult == "alpha":
      unpremult = "none"
  elif _class == "Copy":
    layer = ""
    if nuke.value("to0") != "none":
      layer += nuke.value("from0") + " -> " + nuke.value("to0")
    if nuke.value("to1") != "none":
      layer += "\n" + nuke.value("from1") + " -> " + nuke.value("to1")
    if nuke.value("to2") != "none":
      layer += "\n" + nuke.value("from2") + " -> " + nuke.value("to2")
    if nuke.value("to3") != "none":
      layer += "\n" + nuke.value("from3") + " -> " + nuke.value("to3")
    if nuke.value("channels") != "none":
      layer += ("\n" + nuke.value("channels") + "->" + nuke.value("channels"))
    layer = layer.lstrip("\n")  # EDITED: remove leading newline for aesthetics
  elif _class == "FrameHold":
    value_inc = nuke.value("increment")
    rounding_mode = nuke.value("rounding_mode") if this.knob('rounding_mode') else None
    first_frame = nuke.value("knob.first_frame")
    if rounding_mode == "Whole frames":
      first_frame = math.floor(float(first_frame))
      value_inc = math.floor(float(value_inc))
    if float(value_inc):
      layer = "frame "+str(first_frame)+"+n*"+str(value_inc)
    else:
      layer = "frame "+str(first_frame)
  elif _class == "Precomp" or  _class == 'LiveGroup' or _class == "EdgeBlur":  # EDITED: added EdgeBlur so that it does not display the output field
    layer = '-'

  # maskChannelInput is displayed or render order for the write node
  if mask != "none":
    if int(nuke.numvalue("invert_mask", 0)):
      layer += (" / ~" + mask)
    else:
      layer += (" / " + mask)

  # If unpremult is not "none" and not the same as mask, it is displayed after the mask separated by a slash
  if unpremult != "none" and unpremult != mask and _class.find("Deep", 0) == -1:
    layer += ( " / " + unpremult)

  # CUSTOM BLOCK 4: Custom Labels
  # Additional custom labels, added before the label or instead of the label if it is empty using the customPlusLabel function
  if _class in ['Blur', 'FilterErode', 'Erode', 'EdgeBlur']:
    label = customPlusLabel(nuke.value('size'), label)
  elif _class=='Switch' or _class=='Dissolve':
    label = customPlusLabel(nuke.value('which'), label)
  elif _class=='Defocus':
    label = customPlusLabel(nuke.value('defocus'), label)
  elif _class=='TimeOffset':
    label = customPlusLabel(nuke.value('time_offset'), label)
  elif _class=='Tracker4' or _class=='Tracker3':
    kn1 = this.knob('transform')
    kn2 = this.knob('reference_frame')
    if kn1 and kn2:
      label = customPlusLabel(kn1.value() + ' / ref:' + str(int(kn2.value())), label)
  elif _class=='Colorspace':
    kn1 = this.knob('colorspace_in')
    kn2 = this.knob('colorspace_out')
    if kn1 and kn2:
      label = customPlusLabel(kn1.value() + ' >> ' + kn2.value(), label)
  elif _class=='MotionBlur':
    label = customPlusLabel('samples '+nuke.value('shutterSamples'), label)
  elif _class=='VectorDistort':
    label = customPlusLabel('ref '+nuke.value('referenceFrame'), label)
  elif _class=='ScanlineRender':
    v = this.knob('projection_mode').value()
    if v!='render camera':
      label = customPlusLabel(f'({v})', label)
  elif _class=='FrameRange':
    kn1 = this.knob('first_frame')
    kn2 = this.knob('last_frame')
    if kn1 and kn2:
      label = customPlusLabel(f'{int(kn1.value())}-{int(kn2.value())}', label)
  elif _class=='afanasy':
    kn1 = this.knob('framefirst')
    kn2 = this.knob('framelast')
    if kn1 and kn2:
      label = customPlusLabel(f'{int(kn1.value())}-{int(kn2.value())}', label)
  elif _class=='Mirror' or _class=='Mirror2':
    kn1 = this.knob(['Vertical', 'flip'][_class=='Mirror2'])
    kn2 = this.knob(['Horizontal', 'flop'][_class=='Mirror2'])
    if kn1 and kn2:
      res = ''
      if kn1.value():
        res = 'vertical'
        if kn2.value():
          res+='/horizontal'
      elif kn2.value():
        res = 'horizontal'
      label = customPlusLabel(res, label)
  elif _class=='Shuffle2':
    label = customPlusLabel(getShuffleLayersLabel(this), label)
  elif _class=='Saturation':
    label = customPlusLabel(nuke.value('saturation'), label)
  elif _class=='AppendClip':
    label = customPlusLabel(nuke.value('firstFrame'), label)
  elif _class=='Retime':
    res = ''
    if this['speed'].value()!=1:
      res = 'speed ' + nuke.value('speed')
    elif this['reverse'].value():
      res = 'reverse'
    elif this['output.first_lock'].value() and not any([this['input.first_lock'].value(),this['input.last_lock'].value(),this['output.last_lock'].value()]):
      res = 'retime ' + nuke.value('output.first')
    elif this['output.first_lock'].value() and this['output.last_lock'].value():
      res = nuke.value('output.first') + '-' + nuke.value('output.last')
    if res:
      label = customPlusLabel(res, label)
  if this.knob('filter') and this.knob('filter').values()[2:7]==['Keys', 'Simon', 'Rifman', 'Mitchell', 'Parzen']:  # Check that the filter is a transform filter and not like Blur or other similar nodes
    val = this['filter'].value()
    if isinstance(val,str) and this['filter'].value()!='cubic':
      label = customPlusLabel(f'({val})', label)
  if this.knob('mix'):
    if this.knob('mix').value()<1 and _class not in ['GridWarp3', 'GridWarpTracker', 'SplineWarp3']:
      label = customPlusLabel(label.rstrip(), f'mix {nuke.value("mix")}')
  # END OF CUSTOM BLOCK 4

  if cs_extractor.result():
    result = __concat_result_string(name, layer + "\n" + str(label))
  elif layer and layer != "rgba" and layer != "rgb" and layer != "-":  # EDITED: added check for layer is not None
    result = __concat_result_string(name, "(" + layer + ")" + "\n" + str(label))
  else:
    result = __concat_result_string(name, label)

  return result

