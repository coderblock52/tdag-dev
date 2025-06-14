#!/usr/bin/env bash
#
# generate_index_json.sh
# Walks the TDAG project tree and outputs a JSON file `tdag_index.json`
# capturing directories as objects and files as "<extension> File".
#

# Ensure we run from the script’s directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

# Output file
OUTPUT_FILE="tdag_index.json"

# Use embedded Python for the heavy lifting, with variable expansion enabled
python3 - <<PYCODE
import os, json

output_file = "${OUTPUT_FILE}"

def build_tree(root_path):
    tree = {}
    for dirpath, dirnames, filenames in os.walk(root_path):
        parts = [] if dirpath in (root_path, "./") else os.path.relpath(dirpath, root_path).split(os.sep)
        node = tree
        for p in parts:
            node = node.setdefault(p, {})
        for f in filenames:
            # Determine extension (without the dot), fallback to "File" if none
            ext = os.path.splitext(f)[1]
            label = (ext[1:].capitalize() + " File") if ext else "File"
            node[f] = label
    return tree

tree = build_tree('.')
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(tree, f, indent=2)

print(f"Generated {output_file}")
PYCODE