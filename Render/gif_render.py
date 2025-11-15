# Renders a GIF from the selected node to a 'gif' folder next to the script using ffmpeg

# v1.0.0
# created by: Pushkarev Aleksandr

import nuke
import subprocess, os, re

FFMPEG = "Z:\\Programs\\Utilities\\ffmpeg\\ffmpeg.exe"

def gif_render():
    if not os.path.exists(FFMPEG):
        nuke.message(f"ffmpeg not found at {FFMPEG}")
        return

    nodes = nuke.selectedNodes()
    if not nodes:
        nuke.message("Select a node")
        return
    selected_node = nodes[-1]

    # Get save path
    root = nuke.root()
    script_path = root.name()
    if script_path == "Root":
        base_dir = f"{os.getenv('NUKE_TEMP_DIR', '/tmp')}/gif"
    else:
        base_dir = f"{os.path.dirname(script_path)}/gif".replace("\\", "/")

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # Unique path for sequence to avoid conflicts
    sequence_ext = "png"
    sequence_path = f"{base_dir}/temp.%04d.{sequence_ext}"

    # Request frame range
    fr_range = nuke.getInput("Frame range", f"{root.firstFrame()}-{root.lastFrame()}")
    if not fr_range:
        return
    elif not re.match(r"^\d+-\d+$", fr_range):
        nuke.message("Invalid frame range format.")
        return

    first_frame, last_frame = map(int, fr_range.split("-"))

    # Create Write node
    write = nuke.createNode("Write", inpanel=False)
    write.setInput(0, selected_node)
    write["file"].setValue(sequence_path)
    write["file_type"].setValue(sequence_ext)

    # Set colorspace
    if nuke.activeViewer():
        viewer_process = nuke.activeViewer().node()["viewerProcess"].value()
        if viewer_process == "Rec.709 (ACES)":
            write["colorspace"].setValue("Output - Rec.709")
        else:
            write["colorspace"].setValue("Output - sRGB")
    else:
        write["colorspace"].setValue("Output - sRGB")

    # Render
    try:
        nuke.execute(write, first_frame, last_frame)
    except:
        print("Render Cancelled")
        nuke.delete(write)
        return
    nuke.delete(write)

    # Create unique name for gif
    i = 1
    while True:
        gif_name = f"gif{i}.gif"
        gif_path = f"{base_dir}/{gif_name}"
        if not os.path.exists(gif_path):
            break
        i += 1

    # Assemble gif using ffmpeg
    ffmpeg_cmd = [
        FFMPEG.replace("/", "\\"),
        "-y",
        "-framerate", str(int(root.fps())),
        "-start_number", str(first_frame),
        "-i", sequence_path,
        "-loop", "0",
        gif_path
    ]

    try:
        subprocess.run(ffmpeg_cmd, check=True)

        # Delete PNG files after creating GIF
        for fname in os.listdir(base_dir):
            if re.match(r"temp\.\d{4}\.png$", fname):
                os.remove(os.path.join(base_dir, fname))

        base_dir = base_dir.replace("/", "\\")
        subprocess.Popen(f'explorer "{base_dir}"')
    except subprocess.CalledProcessError as e:
        nuke.message(f"ffmpeg error:\n{e}")
