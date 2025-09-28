import nuke, nukescripts
import os

for root, dirs, _ in os.walk(os.path.dirname(__file__)):
    dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git")]
    nuke.pluginAddPath(root.replace("\\", "/"))

nuke.menu('Nuke').addCommand('APushkarev/Channels/Add N P Layers', 'import addNPLayers; addNPLayers.addNPLayers()')
nuke.menu('Nuke').addCommand('APushkarev/Channels/Check Channels', 'import checkChannels; checkChannels.checkChannels()')
nuke.menu('Nuke').addCommand('APushkarev/Create/Link Blur to Erode', 'import linkBlurToErode; linkBlurToErode.linkBlurToErode()', 'Ctrl+B', shortcutContext=2)
nuke.menu('Nuke').addCommand('APushkarev/File/Bake Relative Paths', 'import bakeRelativePaths; bakeRelativePaths.bakeRelativePaths()')
nuke.menu('Nuke').addCommand('APushkarev/File/Batch Rename', 'import batchRename; batchRename.batchRename()')
nuke.menu('Nuke').addCommand('APushkarev/File/Rename File', 'import renameFile; renameFile.main()')
import renderLog
nuke.addAfterRender(renderLog.renderLog)
nuke.menu("Nuke").addCommand("APushkarev/File/Nk Script Path from Read", "import renderLog;renderLog.getRelatedScriptPath()")
nuke.menu('Nuke').addCommand('APushkarev/File/Set Z in Read', 'import setZinRead; setZinRead.setZinRead()')
nuke.menu('Nuke').addCommand('APushkarev/Formats/Add Square Formats', 'import addSquareFormats; addSquareFormats.addSquareFormats()')
nuke.menu('Nuke').addCommand('APushkarev/Knobs/Add Custom Knob', 'import knobCreater; knobCreater.knobCreater()')
nuke.menu('Nuke').addCommand('APushkarev/ML/Ollama Chat', 'import OllamaChat; OllamaChat.main()')
nuke.menu('Nuke').addCommand('APushkarev/ML/Open In Lama Cleaner', 'import openInLamaCleaner; openInLamaCleaner.openInLamaCleaner()')
nuke.menu('Nuke').addCommand('APushkarev/Node/Add Label', 'import addLabel; addLabel.addLabel()', 'i', shortcutContext=2)
nuke.menu('Nuke').addCommand('APushkarev/Node/Bake Dots Color', 'import bakeDotsColor; bakeDotsColor.bakeDotsColor()')
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
nuke.menu('Nuke').addCommand('APushkarev/Node Graph/Switch Precomp Setup', 'import switchPrecompSetup; switchPrecompSetup.switchPrecompSetup()', 'Ctrl+Shift+W')
nuke.menu('Nuke').addCommand('APushkarev/Node Graph/Unhide All Inputs', 'import unhideAllInputs; unhideAllInputs.unhideAllInputs()')
nuke.menu('Nuke').addCommand('APushkarev/Node Graph/View Mask', 'import viewMask; viewMask.viewMask()', 'Alt+Shift+A')
nuke.menu('Nuke').addCommand('APushkarev/Render/Make Proxy', 'import MakeProxy; MakeProxy.main()')
nuke.menu('Nuke').addCommand('APushkarev/Transform/Card Reconcile', 'import CardReconcile; CardReconcile.main()')
import corenerpinLabel
nuke.menu('Nuke').addCommand('APushkarev/Transform/CornerPin to Tracker', 'import cornerPinToTracker; cornerPinToTracker.cornerPinToTracker()')
nuke.menu('Nuke').addCommand('APushkarev/Transform/Distort Tracker', 'import distortTracker; distortTracker.distortTracker()')
nuke.menu('Nuke').addCommand('APushkarev/Transform/Merge Trackers Nodes', 'import mergeTrackers; mergeTrackers.mergeTrackers()')
nuke.menu('Nuke').addCommand('APushkarev/Transform/Transform CornerPin', 'import transformCornerPin; transformCornerPin.transformCornerPin()')
nuke.menu('Nuke').addCommand('APushkarev/Transform/Transform Tracker', 'import transformTracker; transformTracker.transformTracker()')
nuke.menu('Nuke').addCommand('APushkarev/Utilities/List Frame Server Workers', 'import listFrameServerWorkers; listFrameServerWorkers.listFrameServerWorkers()')
import PerformanceTimers
nuke.menu('Nuke').addCommand('APushkarev/Utilities/Reload Module', 'import ReloadModule; ReloadModule.ReloadModule()')
nuke.menu('Nuke').addCommand('APushkarev/Utilities/WrapItUp Fix', 'import WrapItUpFix; WrapItUpFix.WrapItUpFix()')
nuke.menu('Nuke').addCommand('Cache/Localization/Open Localization Folder', 'import open_remove_localization;open_remove_localization.open_localization_folder()')
nuke.menu('Nuke').addCommand('Cache/Localization/Remove Localization Folder', 'import open_remove_localization;open_remove_localization.remove_localization_folder()')
from openNkAsNewComp import openNkAsNewComp
nukescripts.addDropDataCallback(openNkAsNewComp)
from updateLocalization import updateLocalizationMain
nuke.addAfterRender(updateLocalizationMain)
import CustomGuides
nuke.menu('Nuke').addCommand('File/Open Copy...', 'import openCopy; openCopy.openCopy()', 'Ctrl+Alt+O', index=2)
import FooocusViewer
nukescripts.registerWidgetAsPanel("FooocusViewer.ImageGallery", "Fooocus Viewer", "uk.co.thefoundry.FooocusViewer")
