# Renders selected Write nodes over the global range via command line

# v1.2.1
# created by: Pushkarev Aleksandr

# TODO
# Should be launched with --safe and NUKE_PATH manually set for required files

import nuke, os

def split_interval(start, end, num_segments):
    interval_length = end - start + 1
    if interval_length < num_segments:
        return [(start, end)]
    
    segment_length = interval_length // num_segments
    remainder = interval_length % num_segments
    
    subintervals = []
    current_start = start
    
    for i in range(num_segments):
        current_end = current_start + segment_length - 1
        if remainder > 0:
            current_end += 1
            remainder -= 1
        if current_start <= end:
            subintervals.append((current_start, min(current_end, end)))
        current_start = current_end + 1
    
    return subintervals

def renderCMD():
    rootname = nuke.root().name()
    if rootname=='Root':  # Script must be saved somewhere
        nuke.message('Save the script before rendering!')
        return
    if not nuke.selectedNodes('Write'):  # At least one Write node must be selected
        nuke.message('Select a Write node to render')
        return
    ff = nuke.root().firstFrame()
    lf = nuke.root().lastFrame()
    panel = nuke.Panel('Render CMD')
    panel.addSingleLineInput('range', f'{ff}-{lf}')
    panel.addSingleLineInput('number of processes', '1')
    panel.addBooleanCheckBox('close cmd window when done', True)
    if not panel.show():
        return
    nuke.scriptSave()
    spl = panel.value('range').split('-')
    ff = int(spl[0])
    lf = int(spl[1])
    nuke_exe = f'"{nuke.EXE_PATH}"'
    nukex_flag = '--nukex -i -X'  # When launching NukeX from CLI, Nuke requires the interactive license flag
    for node in nuke.selectedNodes('Write'):
        node_name = node.name()
        filename = node['file'].value()
        if not node_name or not filename:
            continue
        node['create_directories'].setValue(True)
        for i in split_interval(ff, lf, int(panel.value('number of processes'))):
            # With /c consoles close after render; with /k they stay open to read errors if any
            close_flag = ['/k', '/c'][panel.value('close cmd window when done')]
            cmd = ' '.join(['start cmd', close_flag, nuke_exe, nukex_flag, node_name, rootname, f'{i[0]}-{i[1]}'])
            os.popen(cmd)

# nuke.menu('Nuke').addCommand('Render/Render CMD', 'renderCMD.renderCMD()', 'F6')
