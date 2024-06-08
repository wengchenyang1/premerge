#!/bin/bash

# Find the absolute path of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define the filenames
PYLINT_RC_FILE=".pylintrc"
CLANG_FORMAT_FILE=".clang-format"

# Check if .pylintrc and .clang-format exist in the current folder
if [[ ! -f "$SCRIPT_DIR/$PYLINT_RC_FILE" ]]; then
    echo "$PYLINT_RC_FILE does not exist in the current directory."
    exit 1
fi

if [[ ! -f "$SCRIPT_DIR/$CLANG_FORMAT_FILE" ]]; then
    echo "$CLANG_FORMAT_FILE does not exist in the current directory."
    exit 1
fi

# Check if .pylintrc and .clang-format exist in the parent folder
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

if [[ ! -f "$PARENT_DIR/$PYLINT_RC_FILE" ]]; then
    cp "$SCRIPT_DIR/$PYLINT_RC_FILE" "$PARENT_DIR"
    echo "Copied $PYLINT_RC_FILE to the parent directory."
else
    echo "$PYLINT_RC_FILE already exists in the parent directory."
fi

if [[ ! -f "$PARENT_DIR/$CLANG_FORMAT_FILE" ]]; then
    cp "$SCRIPT_DIR/$CLANG_FORMAT_FILE" "$PARENT_DIR"
    echo "Copied $CLANG_FORMAT_FILE to the parent directory."
else
    echo "$CLANG_FORMAT_FILE already exists in the parent directory."
fi

echo "Setup complete."
