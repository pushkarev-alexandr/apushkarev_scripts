"""
This script is designed to find and copy .py files from a working folder
to the current directory. It searches for files containing a specific string
(e.g., the author's last name) and copies them, preserving the relative
folder structure.
"""
import os, configparser, shutil
from pathlib import Path

def get_ignores(scripts_folder):
    """Reads a .gitignore file from the scripts_folder and returns a dictionary
    categorizing ignored files and directories.
    """
    res = {"dirs": [], "files": []}
    ignore_file = os.path.join(scripts_folder, ".gitignore")
    if os.path.exists(ignore_file):
        with open(ignore_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if line.endswith("/"):
                        res["dirs"].append(line[:-1])
                    else:
                        res["files"].append(line)
    return res

def get_config_ignore_files():
    """Reads the [IgnoreFiles] section from config.ini and returns a set of filenames to ignore."""
    ignore_files = set()
    if config.has_section("IgnoreFiles") and "files" in config["IgnoreFiles"]:
        files_str = config["IgnoreFiles"]["files"]
        # Split by comma and strip whitespace
        ignore_files = set(f.strip() for f in files_str.split(",") if f.strip())
    return ignore_files

def find_and_copy_files(root_folder, search_string, renaming_map=None):
    """
    Recursively finds and copies files based on specified criteria.
    - Copies .py files containing a specific search string.
    - Copies all README.md files.
    The folder structure relative to the root_folder is preserved in the destination.

    :param root_folder: The root folder to start the search from.
    :param search_string: The string to search for in .py files.
    :param renaming_map: A dictionary for renaming folders in the destination path.
                         Example: {'old_name': 'new_name'}
    """
    found_count = 0
    ignores = get_ignores(root_folder)
    ignore_files_config = get_config_ignore_files()
    for dirpath, dirnames, filenames in os.walk(root_folder):
        if dirpath == root_folder:
            continue  # Skip the root folder itself
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(file_path, root_folder)  # Calculate relative path to preserve directory structure
            should_copy = False

            # Ignore files from config.ini [IgnoreFiles]
            if filename in ignore_files_config:
                continue

            # Condition 1: .py file with the search string
            if filename.endswith(".py"):
                if any(p in ignores["dirs"] for p in Path(relative_path).parts) or filename in ignores["files"]:
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            file_content = f.read()
                            if search_string in file_content:
                                print(f"Found match in: {file_path}")
                                should_copy = True
                    except Exception as e:
                        print(f"Failed to read file {file_path}: {e}")

            # Condition 2: README.md file
            elif filename.lower() == "readme.md":
                print(f"Found README file: {file_path}")
                should_copy = True

            if should_copy:
                try:
                    # Apply folder renaming from the map if provided
                    path_parts = relative_path.split(os.sep)
                    renaming_map = renaming_map or {}
                    modified_path_parts = [renaming_map.get(part, part) for part in path_parts]
                    modified_relative_path = os.path.join(*modified_path_parts)

                    destination_path = os.path.join(os.getcwd(), modified_relative_path)

                    # Create destination directory if it doesn't exist
                    destination_dir = os.path.dirname(destination_path)
                    if destination_dir:
                        os.makedirs(destination_dir, exist_ok=True)

                    # If .py file, apply renaming_map to file content
                    if filename.endswith(".py"):
                        try:
                            with open(file_path, "r", encoding="utf-8", errors="ignore") as src_f:
                                content = src_f.read()
                            for old, new in renaming_map.items():
                                content = content.replace(old, new)
                            with open(destination_path, "w", encoding="utf-8") as dst_f:
                                dst_f.write(content)
                            shutil.copystat(file_path, destination_path)
                        except Exception as e:
                            print(f"Failed to copy and rename file content {file_path}: {e}")
                            continue
                    else:
                        # For non-.py files, just copy as is
                        shutil.copy2(file_path, destination_path)
                    print(f"Copied to: {destination_path}")
                    found_count += 1
                except Exception as e:
                    print(f"Failed to copy file {file_path}: {e}")

    if found_count == 0:
        print("\nNo matching files were found to copy.")
    else:
        print(f"\nSearch and copy complete. Files found and copied: {found_count}.")

def get_scripts_folder():
    """Returns the scripts folder path from the config file."""
    if config.has_section("Paths") and "scripts_folder" in config["Paths"]:
        return config["Paths"]["scripts_folder"]
    return ""

def get_renaming_map():
    """Returns a dictionary of renaming rules from the [Renaming] section of the config file."""
    if config.has_section("Renaming"):
        return dict(config.items("Renaming"))
    return {}

if __name__ == "__main__":
    if not os.path.exists("config.ini"):
        print("Error: config.ini file not found.")
        exit(1)

    config = configparser.ConfigParser()
    config.optionxform = str  # Disables converting keys to lowercase
    config.read("config.ini")

    scripts_folder = get_scripts_folder()
    renaming_map = get_renaming_map()

    string_to_find = "Pushkarev"

    if os.path.isdir(scripts_folder):
        find_and_copy_files(scripts_folder, string_to_find, renaming_map)
    else:
        print(f"Error: Directory not found at path '{scripts_folder}'")
