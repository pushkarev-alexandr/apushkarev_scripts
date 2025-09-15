"""
This script is designed to find and copy .py files from a working folder
to the current directory. It searches for files containing a specific string
(e.g., the author's last name) and copies them, preserving the relative
folder structure.
"""
import os, configparser, shutil

def find_string_in_py_files(root_folder, search_string, renaming_map=None):
    """
    Recursively searches for a string in .py files, prints the file names,
    and copies them to the current directory, preserving the folder structure relative to root_folder.

    :param root_folder: The root folder to start the search from.
    :param search_string: The string to search for.
    :param renaming_map: A dictionary for renaming folders in the destination path.
                         Example: {'old_name': 'new_name'}
    """
    found_count = 0
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        if search_string in f.read():
                            print(f"Found match in: {file_path}")

                            # Calculate relative path to preserve directory structure
                            relative_path = os.path.relpath(file_path, root_folder)

                            # Apply folder renaming from the map if provided
                            path_parts = relative_path.split(os.sep)
                            renaming_map = renaming_map or {}
                            modified_path_parts = [renaming_map.get(part.lower(), part) for part in path_parts]
                            modified_relative_path = os.path.join(*modified_path_parts)

                            destination_path = os.path.join(os.getcwd(), modified_relative_path)

                            # Create destination directory if it doesn't exist
                            destination_dir = os.path.dirname(destination_path)
                            if destination_dir:
                                os.makedirs(destination_dir, exist_ok=True)

                            # Copy the file, preserving metadata
                            shutil.copy2(file_path, destination_path)
                            print(f"Copied to: {destination_path}")
                            found_count += 1
                except Exception as e:
                    print(f"Failed to process file {file_path}: {e}")

    if found_count == 0:
        print("Files with the specified string were not found.")
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
    config = configparser.ConfigParser()
    config.read("config.ini")

    scripts_folder = get_scripts_folder()
    renaming_map = get_renaming_map()

    string_to_find = "Pushkarev"

    if os.path.isdir(scripts_folder):
        find_string_in_py_files(scripts_folder, string_to_find, renaming_map)
    else:
        print(f"Error: Directory not found at path '{scripts_folder}'")
