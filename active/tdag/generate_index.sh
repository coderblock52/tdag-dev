#!/usr/bin/env bash
#
# generate_index.sh
# Generates a file-tree index of this TDAG project.
#

# Ensure we run from the script’s directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

OUTPUT_FILE="tdag_index.txt"

# Remove any old index
[ -f "$OUTPUT_FILE" ] && rm "$OUTPUT_FILE"

# Generate the index:
#  - find . -mindepth 1 prints all entries under the root
#  - sed indents each level by 4 spaces
find . -mindepth 1 \
  | sed -E 's|[^/]*/|    |g' \
  > "$OUTPUT_FILE"

echo "Generated index at $SCRIPT_DIR/$OUTPUT_FILE"