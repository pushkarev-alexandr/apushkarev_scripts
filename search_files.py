import os, configparser

def find_string_in_py_files(root_folder, search_string):
    """
    Recursively searches for a string in .py files in the specified directory and prints the file names.

    :param root_folder: The root folder to start the search from.
    :param search_string: The string to search for.
    """
    found_count = 0
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        if search_string in f.read():
                            print(file_path)
                            found_count += 1
                except Exception as e:
                    print(f"Failed to read file {file_path}: {e}")

    if found_count == 0:
        print("Files with the specified string were not found.")
    else:
        print(f"\nSearch complete. Files found: {found_count}.")

def get_scripts_folder():
    """Returns the scripts folder path from the config file."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config["Paths"]["scripts_folder"]

if __name__ == "__main__":
    scripts_folder = get_scripts_folder()

    string_to_find = "Pushkarev"

    if os.path.isdir(scripts_folder):
        find_string_in_py_files(scripts_folder, string_to_find)
    else:
        print(f"Error: Directory not found at path '{scripts_folder}'")
