# Nuke Python Scripts

## Installation Instructions

1. Download and place the `apushkarev_scripts` folder into your user `.nuke` directory.
2. In the `.nuke` directory, create a `menu.py` file if it does not exist.
3. Add the following line at the end of `menu.py`:
	```python
	nuke.pluginAddPath('./apushkarev_scripts')
	```
4. Start Nuke. The scripts and menus will be available.

## Script Descriptions

### APushkarev
#### Channels
- **addNPLayers.py**: Adds N and P layers which are not present in Nuke by default but are very useful
- **checkChannels.py**: Select two nodes; the script checks if the channels in these two nodes match. Useful for comparing if channels are missing or new ones have appeared in a new render

#### Create
- **createBlur.py**: When creating a Blur node, links its size to the Erode node if Erode was selected before creation

#### File
- **bakeRelativePaths.py**: For selected Read nodes (or all Reads if none are selected), replaces relative paths with full paths using getEvaluatedValue
- **batchRename.py**: Select a folder; in all files in this folder, the string 'from' will be renamed to 'to'. For example, you can rename version v002 to v003
- **copyToNewVersion.py**: Copies all files of the selected Read node to a new version (tested only on sequences)
- **createReadFromWrite.py**: Creates a Read node from a Write node
- **extendFrames.py**: Extend frames for Read node
- **openInExplorer.py**: This script opens the folder containing the file referenced by the selected node in Nuke. If no node is selected, it opens the folder of the current script.
- **renameFile.py**: Renames a file and updates the name in the selected Read node
- **renderLog.py**: After rendering, saves to the database the path to the rendered file and the path to the script that rendered this file.
- **setZinRead.py**: Changes the path in all Reads from //192.168.100.56/data to disk Z

#### Formats
- **addSquareFormats.py**: Allows you to add square formats, since by default only square_512 is available

#### Knobs
- **knobCreater.py**: Nuke does not allow creating certain knobs like IArray_Knob and Eyedropper_Knob from the menu; this script provides a custom menu for such knobs

#### ML
- **OllamaChat.py**: Chat with artificial intelligence
- **openInLamaCleaner.py**: Opens the selected Read in the Lama-Cleaner application

#### Node
- **addLabel.py**: Adds a label to selected nodes; if an empty string is specified, removes the existing label
- **bakeDotsColor.py**: Bakes the label color of the selected dot (or all if none are selected) into HTML code. After this, the label color does not change when zooming in or out. Created for the Mira project where colored labels on dots were needed but remained black and white
- **batchKnobEdit.py**: Allows you to change the value of a specified parameter or set an expression for multiple selected nodes
- **restoreNodeName.py**: Sets the node name based on its class name; for Roto nodes, sets output to alpha
- **showClassName.py**: Displays a message with the class names of selected nodes

#### Node Graph
- **dotify.py**: Instead of a fan of inputs diverging from one dot, creates a grid
- **jumpBetweenClones.py**: Allows switching between clones
- **lockPosition.py**: Locks the position of selected nodes in their current place. Calling the command again unlocks position changes. Adds code to the node's knobChanged to block position changes.
- **moveNodes.py**: Allows moving nodes with arrow keys in the node graph
- **skewNodes.py**: Shifts nodes so they are not in a single vertical line
- **smartConnect.py**: Aligns nodes when connecting them
- **smartMerge.py**: Replaces the standard Merge, connects the B input and places the Merge node below. If several nodes are selected, creates a stack of multiple Merges
- **sortReadsByFilename.py**: Sorts and aligns selected Reads by filename
- **switchPrecompSetup.py**: Select a Write node, and a setup is created from it using a Switch node and a Read node
- **unhideAllInputs.py**: Makes all inputs visible
- **viewMask.py**: Puts the alpha channel from the second selected node into the red channel of the first selected node to evaluate where alpha is used. If pressed again, removes the ChannelMerge node

#### Proj
- **clearNkFolder.py**: Moves all Afanasy scripts, autosaves, and temporary files ending with a tilde to the autosave folder

#### Render
- **MakeProxy.py**: Renders proxy to the Temp folder for selected Reads and sets the path in Read proxy

#### Roto
- **FollowPath.py**: This script animates an object to move along a Roto or RotoPaint node's curve, automatically creating a Transform node with translation and rotation following the path
- **moveRotoLifetime.py**: Shifts the lifetime of elements in the Roto/RotoPaint node by the specified number of frames

#### Transform
- **CardReconcile.py**: Creates a CornerPin from a Card node
- **corenerpinLabel.py**: When pressing the copy_from or copy_to button, removes the matchmove or stabilize label (this label is set by the matchmove/stabilize button in the hotbox)
- **cornerPinToTracker.py**: Converts all animated knobs to Tracker node trackers
- **distortTracker.py**: Distorts the position of Tracker node points using a distortion equalizer node
- **mergeTrackers.py**: Merges several selected Tracker nodes into one node
- **transformCornerPin.py**: Transforms CornerPin points as specified in the selected Transform node
- **transformTracker.py**: Transforms Tracker points as specified in the selected Transform node

#### Utilities
- **PerformanceTimers.py**: Adds buttons to enable and disable Performance Timers in Nuke
- **ReloadModule.py**: Reloads the module with the specified name. Useful when you have made changes to a module
- **listFrameServerWorkers.py**: Displays a list of available host machines running FrameServer and accessible from the current machine, i.e. where you can send renders using Nuke's standard tools

### Cache
#### Localization
- **open_remove_localization.py**: Adds extra buttons to the Cache/Localization menu for opening the localization folder and removing this folder

### CallbackScripts
- **openNkAsNewComp.py**: If you drop a .nk file into Nuke, it will open as a new project instead of copying its contents
- **updateLocalization.py**: When rendering finishes, the script finds the Read node that corresponds to the Write node used for rendering and updates localization

### Custom
- **CustomGuides.py**: Adds rule of thirds and symmetry guides to the viewer. Also adds a new matte format 2.387 for 2048x858.

### File
- **openCopy.py**: Copies the selected script to the temp folder and opens it so as not to modify the user's script

### NukePanels
- **FooocusViewer.py**: Panel for Fooocus, displays images generated via Fooocus

### Render
- **AfanasyButtons.py**: Adds Set Free and Eject and NIMBY buttons to Nuke

