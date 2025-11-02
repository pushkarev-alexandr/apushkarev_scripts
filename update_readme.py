import os
import json
import configparser
from collections import defaultdict

# Path to the file with descriptions
config = configparser.ConfigParser()
config.read("config.ini")
INFO_FILE = config["Paths"]["scripts_info_file"]
README_FILE = os.path.join(os.path.dirname(__file__), "README.md")

# Scan all .py files in subfolders
def find_scripts(root_dir):
    scripts_by_folder = defaultdict(list)
    for folder, _, files in os.walk(root_dir):
        rel_folder = os.path.relpath(folder, root_dir).replace('\\', '/')
        if rel_folder == '.':
            continue  # skip the root folder
        for f in files:
            if f.endswith('.py'):
                scripts_by_folder[rel_folder].append(f)
    return scripts_by_folder

# Read descriptions from info_file
with open(INFO_FILE, encoding='utf-8') as f:
    scripts_info = json.load(f)

scripts_by_folder = find_scripts(os.path.dirname(__file__))

# Build markdown section
lines = []
lines.append('## Script Descriptions\n')

# Group by top-level folder
grouped = defaultdict(lambda: defaultdict(list))
for rel_folder, scripts in scripts_by_folder.items():
    parts = rel_folder.split('/')
    if len(parts) == 1:
        top = parts[0]
        sub = None
    else:
        top = parts[0]
        sub = '/'.join(parts[1:])
    grouped[top][sub].extend(scripts)

for top in sorted(grouped):
    lines.append(f'### {top}')
    for sub in sorted(grouped[top]):
        if sub:
            lines.append(f'#### {sub}')
        for script in sorted(grouped[top][sub]):
            script_name = os.path.splitext(script)[0]
            info = scripts_info.get(script_name)
            tooltip = info['tooltip'] if info and info.get('tooltip') else '(No description)'
            lines.append(f'- **{script}**: {tooltip}')
        lines.append('')

new_section = '\n'.join(lines)

# Read README.md and add section to the end
with open(README_FILE, encoding='utf-8') as f:
    readme = f.read().rstrip()

if '## Script Descriptions' in readme:
    # Remove old section
    readme = readme.split('## Script Descriptions')[0].rstrip()

with open(README_FILE, 'w', encoding='utf-8') as f:
    f.write(readme + '\n\n' + new_section + '\n')

print('README.md updated with script descriptions.')
