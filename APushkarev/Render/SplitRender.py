# Splits render by passes using shuffle

# v1.2.0
# created by: Pushkarev Aleksandr

import nuke, nukescripts
import re

keepRGBA = True  # Adds Remove node and deletes all passes except rgba
postage_stamp = True  # Enable or disable postage_stamp on Shuffle nodes to see what's being shuffled
hide_input = False  # Hide or show inputs of Shuffle nodes
create_dots = True  # Create or not a dot at the end after Shuffle/Remove
width_gap = 150  # Distance between shuffles horizontally
height_gap = 100  # Distance down from the dot

def layerPriority(layer):
    priority = ['rgba', 'rgb', 'diffuse', 'reflection', 'refraction', 'sss']
    for i, item in enumerate(priority):
        if item in layer.lower():
            return i
    return len(priority)

def SplitRender():
    nodes = nuke.selectedNodes()
    nodes.reverse()
    for node in nodes:
        nukescripts.clear_selection_recursive()
        node.setSelected(True)
        layers = {}
        crypto_layers = []
        for ch in node.channels():
            layer = ch.split('.')[0]
            channel = ch.split('.')[1]
            if re.fullmatch(r"CryptoObject\d*", layer) or re.fullmatch(r"CryptoMaterial\d*", layer):
                crypto_name = layer.rstrip('0123456789')
                if crypto_name not in crypto_layers:  # Save cryptomatte passes that need to be added later
                    crypto_layers.append(crypto_name)
                continue  # Skip cryptomatte passes
            if layer not in layers:
                layers[layer] = [f'{layer}.{channel}']
            else:
                layers[layer].append(f'{layer}.{channel}')
        layers = dict(sorted(layers.items(), key=lambda item: layerPriority(item[0])))  # Sort by priority
        def_chans = ['rgba.red', 'rgba.green', 'rgba.blue', 'rgba.alpha']
        readDot = nuke.createNode('Dot', inpanel=False)  # Dot after the read node
        readDot.setYpos(readDot.ypos() + 50)
        for i, layer in enumerate(layers):
            channels = layers[layer]
            if channels[-1].endswith('.red'):  # Sometimes channel lists are reversed
                channels.reverse()
            shuffle = nuke.createNode('Shuffle2', inpanel=False)
            shuffle.setInput(0, readDot)
            shuffle.setXYpos(node.xpos() + i*width_gap, readDot.ypos() + height_gap)
            shuffle['postage_stamp'].setValue(postage_stamp)
            shuffle['hide_input'].setValue(hide_input)
            if layer=='rgba':
                shuffle['label'].setValue('rgba')
            shuffle['in1'].setValue(layer)
            mapping = list(zip([0]*len(channels), channels, def_chans[:len(channels)]))
            shuffle['mappings'].setValue(mapping)
            if keepRGBA:
                remove = nuke.createNode('Remove', inpanel=False)
                remove['operation'].setValue('keep')
                remove['channels'].setValue('rgba')
                remove.setYpos(remove.ypos() + 12)
            if create_dots:
                dot = nuke.createNode('Dot', inpanel=False)
                dot.setYpos(dot.ypos() + 30)
        for j, layer in enumerate(crypto_layers):
            remove = None
            if keepRGBA:
                remove = nuke.createNode('Remove', inpanel=False)
                remove.setInput(0, readDot)
                remove['operation'].setValue('keep')
                remove['channels'].setValue(layer)
                for x in range(3):
                    remove['channels' + str(x + 2)].setValue(layer + str(x).zfill(2))
                remove.setXYpos(node.xpos() + (i + j + 1)*width_gap, readDot.ypos() + height_gap)
                remove['hide_input'].setValue(hide_input)
            cryptomatte = nuke.createNode('Cryptomatte', inpanel=False)
            cryptomatte['cryptoLayerChoice'].setValue(j)
            cryptomatte.setInput(0, [readDot, remove][keepRGBA])
            if keepRGBA:
                cryptomatte.setYpos(cryptomatte.ypos() + 12)
            else:
                cryptomatte.setXYpos(node.xpos() + (i + j + 1)*width_gap, readDot.ypos() + height_gap)
            cryptomatte['postage_stamp'].setValue(postage_stamp)
            cryptomatte['hide_input'].setValue(hide_input)
            if create_dots:
                dot = nuke.createNode('Dot', inpanel=False)
                dot.setYpos(dot.ypos() + 30)
