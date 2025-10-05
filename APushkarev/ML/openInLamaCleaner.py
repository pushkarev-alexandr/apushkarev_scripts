# Opens the selected Read or Write node in the Lama-Cleaner application

# v1.1.1
# created by: Pushkarev Aleksandr

# TODO
# - Make universal and make installation incstruction
# - Prompt to overwrite the file or save with a new name
# - Does not output the mask

import nuke, os

lama_cleaner_folder = os.getenv("LAMA_CLEANER_FOLDER")
lama_cleaner_folder = os.path.normpath(lama_cleaner_folder)
use_model_dir = os.getenv("LAMA_CLEANER_USE_MODEL_DIR", "False").lower() in ("1", "true", "yes")

def openInLamaCleaner():
    if not lama_cleaner_folder or not os.path.isdir(lama_cleaner_folder):
        nuke.message("LAMA_CLEANER_FOLDER is not set or invalid")
        return

    for venv_name in ["venv", ".venv", "lama-cleaner"]:
        activate_file = os.path.join(lama_cleaner_folder, venv_name, "Scripts", "activate.bat")
        if os.path.isfile(activate_file):
            break
    else:
        nuke.message("""Could not find activate.bat to activate the virtual environment in the Lama-Cleaner folder.
Please make sure the virtual environment is created and contains Scripts/activate.bat.""")
        return

    sel = nuke.selectedNodes("Write") + nuke.selectedNodes("Read")
    if not sel:
        nuke.message("Select a Read or Write node")
        return
    
    node = sel[0]
    file = node["file"].getEvaluatedValue()
    if not os.path.isfile(file):
        nuke.message(file + "\nThis file does not exist")
        return

    allowed_exts = {'.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp', '.webp'}
    ext = os.path.splitext(file)[1].lower()
    if ext not in allowed_exts:
        nuke.message(f"File has unsupported extension: {ext}\nSupported extensions: {', '.join(allowed_exts)}")
        return

    outdir = os.path.dirname(file)

    lama_cmd = "lama-cleaner --gui"
    if use_model_dir:
        lama_cmd += f" --model-dir {lama_cleaner_folder}\\models"
    lama_cmd += f" --input {file} --output-dir {outdir}"

    cmd = f'''cd /d {lama_cleaner_folder}
call {activate_file}
{lama_cmd}'''.replace("\n", "&")
    cmd = f'start cmd.exe /c "{cmd}"'
    os.system(cmd)
