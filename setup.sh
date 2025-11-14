#!/bin/bash

# Find the absolute path of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define the filenames
FILES_TO_COPY=(".pylintrc" ".clang-format" "CPPLINT.cfg")

# Function to check and copy files
copy_if_not_exists() {
    local file=$1
    local source_dir=$2
    local dest_dir=$3

    if [[ ! -f "$source_dir/$file" ]]; then
        echo "$file does not exist in the current directory."
        exit 1
    fi

    if [[ ! -f "$dest_dir/$file" ]]; then
        cp "$source_dir/$file" "$dest_dir"
        echo "Copied $file to the project root directory."
    else
        echo "$file already exists in the project root directory."
    fi
}

# Check if files exist in the current folder and copy them to the current working directory (project root)
PROJECT_ROOT="$(pwd)"

for file in "${FILES_TO_COPY[@]}"; do
    copy_if_not_exists "$file" "$SCRIPT_DIR" "$PROJECT_ROOT"
done

echo "Setup complete."
