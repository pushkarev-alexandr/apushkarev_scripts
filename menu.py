import nuke, nukescripts
import os

for root, dirs, _ in os.walk(os.path.dirname(__file__)):
    dirs[:] = [d for d in dirs if d not in ('__pycache__', '.git')]
    nuke.pluginAddPath(root.replace('\\', '/'))

nuke.menu('Animation').addCommand('Set Animation Speed','import AnimationSpeed; AnimationSpeed.SetAnimationSpeed()')
nuke.menu('Properties').addCommand('Bake all animation', 'import BakeAnimation; BakeAnimation.bake()')
nuke.menu('Animation').addCommand('copy knob name/copy knob name', 'import copyKnobName; copyKnobName.copyKnobName()')
nuke.menu('Animation').addCommand('copy knob name/copy full knob name', 'import copyKnobName; copyKnobName.copyFullKnobName()')
nuke.menu('Animation').addCommand('label this', 'import labelThisKnob; labelThisKnob.labelThis()')
nuke.menu('Nuke').addCommand('APushkarev/Bridge/Send to After Effects', 'import sendToAfterEffects; sendToAfterEffects.sendToAfterEffects()', icon='after-effects.png')
nuke.menu('Nuke').addCommand('APushkarev/Channels/Add N P Layers', 'import addNPLayers; addNPLayers.addNPLayers()')
nuke.menu('Nuke').addCommand('APushkarev/Channels/Check Channels', 'import checkChannels; checkChannels.checkChannels()')
nuke.menu('Nodes').addCommand('Channel/Shuffle', 'import createShuffleNode; createShuffleNode.createShuffleNode()', 'shift+j', icon='Shuffle.png', shortcutContext=2)
import setColorspace
setColorspace.addColorspaceMenu(nuke.menu('Nuke').menu('APushkarev'))
nuke.menu('Nuke').addCommand('APushkarev/Create/Link Blur to Erode', 'import createBlur; createBlur.main()', 'Ctrl+B', shortcutContext=2)
nuke.menu('Nuke').addCommand('APushkarev/File/Bake Relative Paths', 'import bakeRelativePaths; bakeRelativePaths.bakeRelativePaths()')
nuke.menu('Nuke').addCommand('APushkarev/File/Batch Rename', 'import batchRename; batchRename.batchRename()')
nuke.menu('Nuke').addCommand('APushkarev/File/Copy to New Version', 'import copyToNewVersion; copyToNewVersion.copyToNewVersion()')
nuke.menu('Nuke').addCommand('APushkarev/File/Read from Write', 'import createReadFromWrite; createReadFromWrite.createReadFromWrite()', '+r', shortcutContext=2)
nuke.menu('Nuke').addCommand('APushkarev/File/Extend Frames', 'import extendFrames; extendFrames.extendFrames()', 'Alt+Shift+D', shortcutContext=2)
nuke.menu('Nuke').addCommand('APushkarev/File/Open in Explorer', 'import openInExplorer; openInExplorer.openInExplorer()', 'Shift+B')
nuke.menu('Nuke').addCommand('APushkarev/File/Rename File', 'import renameFile; renameFile.main()')
import renderLog
nuke.addAfterRender(renderLog.renderLog)
nuke.menu('Nuke').addCommand('APushkarev/File/Nk Script Path from Read', 'import renderLog;renderLog.getRelatedScriptPath()')
nuke.menu('Nuke').addCommand('APushkarev/File/Set Z in Read', 'import setZinRead; setZinRead.setZinRead()')
nuke.menu('Nuke').addCommand('APushkarev/Formats/Add Square Formats', 'import addSquareFormats; addSquareFormats.addSquareFormats()')
import shortcuts
shortcuts.createShortcutsMenu(nuke.menu('Nuke').menu('APushkarev'))
nuke.menu('Nuke').addCommand('APushkarev/Knobs/Add Custom Knob', 'import knobCreater; knobCreater.knobCreater()')
nuke.menu('Nuke').addCommand('APushkarev/ML/Ollama Chat', 'import OllamaChat; OllamaChat.main()')
nuke.menu('Nuke').addCommand('APushkarev/ML/Open In Lama Cleaner', 'import openInLamaCleaner; openInLamaCleaner.openInLamaCleaner()')
nuke.menu('Nuke').addCommand('APushkarev/Node/Add Label', 'import addLabel; addLabel.addLabel()', 'i', shortcutContext=2)
nuke.menu('Nuke').addCommand('APushkarev/Node/Bake Dots Color', 'import bakeDotsColor; bakeDotsColor.bakeDotsColor()')
nuke.menu('Nuke').addCommand('APushkarev/Node/Batch Knob Edit', 'import batchKnobEdit; batchKnobEdit.batchKnobEdit()')
nuke.menu('Nodes').addCommand('Time/FrameHold', 'import customFrameHold; customFrameHold.customFrameHold()', 'h', icon='FrameHold.png', shortcutContext=2)
nuke.menu('Nodes').addCommand('Other/Backdrop', 'import customSimpleBackdrop; customSimpleBackdrop.createBackdrop()', 'Alt+B', icon='Backdrop.png', shortcutContext=2)
nuke.menu('Nuke').addCommand('APushkarev/Node/Restore Node Name', 'import restoreNodeName; restoreNodeName.restoreNodeName()')
nuke.menu('Nuke').addCommand('APushkarev/Node/Show Class Name', 'import showClassName; showClassName.showClassName()', 'Ctrl+Alt+Shift+I')
nuke.menu('Nuke').addCommand('APushkarev/Node Graph/Dotify', 'import dotify; dotify.main()')
nuke.menu('Nuke').addCommand('APushkarev/Node Graph/Jump Between Clones', 'import jumpBetweenClones; jumpBetweenClones.jumpBetweenClones()', 'Shift+W', shortcutContext=2)
nuke.menu('Nuke').addCommand('APushkarev/Node Graph/Lock Position', 'import lockPosition; lockPosition.lockPosition()')
nuke.menu('Nuke').addCommand('APushkarev/Node Graph/Move Nodes/Up', 'import moveNodes; moveNodes.moveSel_up()', 'Ctrl+Shift+Up')
nuke.menu('Nuke').addCommand('APushkarev/Node Graph/Move Nodes/Down', 'import moveNodes; moveNodes.moveSel_down()', 'Ctrl+Shift+Down')
nuke.menu('Nuke').addCommand('APushkarev/Node Graph/Move Nodes/Right', 'import moveNodes; moveNodes.moveSel_right()', 'Ctrl+Shift+Right')
nuke.menu('Nuke').addCommand('APushkarev/Node Graph/Move Nodes/Left', 'import moveNodes; moveNodes.moveSel_left()', 'Ctrl+Shift+Left')
nuke.menu('Nuke').addCommand('APushkarev/Node Graph/Skew Nodes', 'import skewNodes; skewNodes.skewNodes()')
nuke.menu('Nuke').addCommand('APushkarev/Node Graph/Smart Connect', 'import smartConnect; smartConnect.smartConnect()', '+a', shortcutContext=1)
nuke.menu('Nodes').addCommand('Merge/Merge','import smartMerge; smartMerge.smartMerge()', 'M', shortcutContext=2, icon='Merge.png')
nuke.menu('Nuke').addCommand('APushkarev/Node Graph/Sort Reads By Filename', 'import sortReadsByFilename; sortReadsByFilename.main()')
nuke.menu('Nuke').addCommand('APushkarev/Node Graph/Sticky Shot Name', 'import stickyShotName; stickyShotName.stickyShotName()')
nuke.menu('Nuke').addCommand('APushkarev/Node Graph/Switch Precomp Setup', 'import switchPrecompSetup; switchPrecompSetup.switchPrecompSetup()', 'Ctrl+Shift+W')
nuke.menu('Nuke').addCommand('APushkarev/Node Graph/Toggle Working Space', 'import toggleWorkingSpace; toggleWorkingSpace.toggleWorkingSpace()', 'Alt+Shift+W')
nuke.menu('Nuke').addCommand('APushkarev/Node Graph/Unhide All Inputs', 'import unhideAllInputs; unhideAllInputs.unhideAllInputs()')
nuke.menu('Nuke').addCommand('APushkarev/Node Graph/View Difference', 'import viewDifference; viewDifference.viewDifference()', 'Shift+D', shortcutContext=2)
nuke.menu('Nuke').addCommand('APushkarev/Node Graph/View Mask', 'import viewMask; viewMask.viewMask()', 'Alt+Shift+A')
nuke.menu('Nuke').addCommand('APushkarev/Proj/Clear nk folder', 'import clearNkFolder; clearNkFolder.clearNkFolder()')
nuke.menu('Nuke').addCommand('APushkarev/Render/Make Proxy', 'import MakeProxy; MakeProxy.main()')
nuke.menu('Nuke').addCommand('APushkarev/Render/Split Render', 'import SplitRender; SplitRender.SplitRender()', 'Ctrl+Alt+S', shortcutContext=2)
nuke.menu('Nuke').addCommand('APushkarev/Roto/Follow Path', 'import FollowPath; FollowPath.FollowPath()')
nuke.menu('Nuke').addCommand('APushkarev/Roto/Move Lifetime', 'import moveRotoLifetime; moveRotoLifetime.moveRotoLifetime()')
nuke.menu('Nuke').addCommand('APushkarev/Transform/Card Reconcile', 'import CardReconcile; CardReconcile.main()')
import corenerpinLabel
nuke.menu('Nuke').addCommand('APushkarev/Transform/CornerPin to Tracker', 'import cornerPinToTracker; cornerPinToTracker.cornerPinToTracker()')
menu = nuke.menu('Nodes').menu('Draw')
for rotoname in ['Roto', 'RotoPaint']:
    menu.findItem(rotoname).setScript(f'import createLinkedRoto; createLinkedRoto.createLinkedRoto("{rotoname}")')
nuke.menu('Nodes').addCommand('Transform/Reformat', 'import createReformat; createReformat.createReformat()', 'Ctrl+R', icon='Reformat.png')
nuke.menu('Nodes').addCommand('Transform/Reformat from selected', 'import createReformat; createReformat.formatFromSelected()', 'Ctrl+Alt+R', icon='Reformat.png', index=17)
nuke.menu('Nuke').addCommand('APushkarev/Transform/Distort Tracker', 'import distortTracker; distortTracker.distortTracker()')
import matchmoveRotoFromCornerPin
nuke.menu('Nuke').addCommand('APushkarev/Transform/Merge Trackers Nodes', 'import mergeTrackers; mergeTrackers.mergeTrackers()')
nuke.menu('Nuke').addCommand('APushkarev/Transform/Transform CornerPin', 'import transformCornerPin; transformCornerPin.transformCornerPin()')
nuke.menu('Nuke').addCommand('APushkarev/Transform/Transform Tracker', 'import transformTracker; transformTracker.transformTracker()')
nuke.menu('Nuke').addCommand('APushkarev/Utilities/Fix Color Picker Window', 'import FixColorPickerWindow; FixColorPickerWindow.main()')
nuke.menu('Nuke').addCommand('APushkarev/Utilities/Fix FrameRange is not callable', 'import FixFrameRangeIsNotCallable; FixFrameRangeIsNotCallable.main()')
nuke.menu('Nuke').addCommand('APushkarev/Utilities/List Frame Server Workers', 'import listFrameServerWorkers; listFrameServerWorkers.listFrameServerWorkers()')
nuke.menu('Nuke').addCommand('APushkarev/Utilities/Menu Scripts Viewer', 'import MenuScriptsViewer; MenuScriptsViewer.main()')
import PerformanceTimers
nuke.menu('Nuke').addCommand('APushkarev/Utilities/Reload Module', 'import ReloadModule; ReloadModule.ReloadModule()')
nuke.menu('Nuke').addCommand('APushkarev/Utilities/Scripts Tab', 'import ScriptsTab; ScriptsTab.runScriptsTab()', 'Ctrl+Tab')
nuke.menu('Nuke').addCommand('APushkarev/Utilities/Switch Keyframe Previews', 'import switchKeyframePreviews; switchKeyframePreviews.switchKeyframePreviews()')
nuke.menu('Nuke').addCommand('APushkarev/Viewer/Toggle Masking Mode', 'import toggleMaskingMode; toggleMaskingMode.toggleMaskingMode()', 'Ctrl+Alt+D')
nuke.menu('Nuke').addCommand('APushkarev/Viewer/Jump Right', 'import viewerJumper; viewerJumper.viewerJumper(right=True)', 'Ctrl+Right', shortcutContext=2)
nuke.menu('Nuke').addCommand('APushkarev/Viewer/Jump Left', 'import viewerJumper; viewerJumper.viewerJumper(right=False)', 'Ctrl+Left', shortcutContext=2)
nuke.menu('Nuke').addCommand('Cache/Localization/Localize Folder', 'import localizeFolder; localizeFolder.main()')
nuke.menu('Nuke').addCommand('Cache/Localization/Open Localization Folder', 'import open_remove_localization;open_remove_localization.open_localization_folder()')
nuke.menu('Nuke').addCommand('Cache/Localization/Remove Localization Folder', 'import open_remove_localization;open_remove_localization.remove_localization_folder()')
import colorspaceAutobaking
import colorspaceTclKnob
import disconnectViewersOnLoad
import dropCameraAxisFBX
import favoritesDirectories
import gizmoDropper
import ignoreTypesOnDrop
import monitorOutKnobChanged
import nameUntitledFormats
import nukeColorspaceGammaError
from openNkAsNewComp import openNkAsNewComp
nukescripts.addDropDataCallback(openNkAsNewComp)
from updateLocalization import updateLocalizationMain
nuke.addAfterRender(updateLocalizationMain)
import autosaveToFolder
import CustomGuides
import BlockyNode
import KeepNode
nuke.menu('Nuke').addCommand('Edit/Copy With Links', 'import copyWithLinks; copyWithLinks.copyWithLinks()', index=16)
nuke.menu('Nuke').addCommand('Edit/Node/Invert Disable', 'import invertDisable; invertDisable.invertDisable()', 'Alt+D', index=14)
import FavoriteScripts
nuke.menu('Nuke').addCommand('File/Open Copy...', 'import openCopy; openCopy.openCopy()', 'Ctrl+Alt+O', index=2)
import FooocusViewer
nukescripts.registerWidgetAsPanel('FooocusViewer.ImageGallery', 'Fooocus Viewer', 'uk.co.thefoundry.FooocusViewer')
nuke.menu('Nuke').addCommand('Render/Afanasy/Set Free', 'import AfanasyButtons; AfanasyButtons.setFree()', icon='free.png')
nuke.menu('Nuke').addCommand('Render/Afanasy/Eject and NIMBY', 'import AfanasyButtons; AfanasyButtons.ejectAndNIMBY()', icon='stop.png')
nuke.menu('Nuke').addCommand('Render/Gif Render', 'import gif_render; gif_render.gif_render()')
nuke.menu('Nuke').addCommand('Render/Screenshot', 'import screenshotFromViewer; screenshotFromViewer.screenshotFromViewer()', 'F3')
