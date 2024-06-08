#!/bin/bash

# Get the directory of the script
cwd="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Get the parent directory
parent_dir=$(dirname "$cwd")

# Get the config directory
config_dir="$cwd/config"

# Check if config directory exists
if [ ! -d "$config_dir" ]; then
  echo "Config directory does not exist."
  exit 1
fi

# Iterate over each file in the config directory
for file in "$config_dir"/*; do
  # Get the filename
  filename=$(basename -- "$file")

  # Get the path of the file in the parent directory
  parent_file_path="$parent_dir/$filename"

  # Check if the file exists in the parent directory
  if [ ! -f "$parent_file_path" ]; then
    # If the file does not exist, copy it to the parent directory
    cp "$file" "$parent_dir"
  fi
done
