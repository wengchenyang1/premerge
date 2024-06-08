""" Utilities for common functionalities """

import os
import subprocess
from typing import List

EXCLUDED_DIRS = ["Thirdparty", "Vocabulary", "build", ".vscode"]


def get_changed_files() -> List:
    """Returns a list of changed files in the current git repository including the latest commit."""
    result = subprocess.run(
        ["git", "status", "--porcelain", "-u"], stdout=subprocess.PIPE, check=False
    )

    lines = result.stdout.decode("utf-8").split("\n")

    files = set()
    for line in lines:
        parts = line.split()
        if len(parts) > 1:
            if parts[0][0] in ("R", "C"):
                # For renamed or copied files, extract the destination path
                files.add(parts[2])
            else:
                # For other files, extract the file path
                files.add(parts[1])

    # If there are no untracked or un-staged changes, get the latest commit changes
    if not files:
        # Get the output of the git log command for the latest commit
        result = subprocess.run(
            ["git", "log", "-1", "--name-only", "--pretty=format:"],
            stdout=subprocess.PIPE,
            check=False,
        )

        # Split the output into lines and add to the list of files
        lines = result.stdout.decode("utf-8").split("\n")
        for line in lines:
            if line:  # Ignore empty lines
                files.add(line)

    return list(files)


def get_all_files(accepted_formats: dict) -> List:
    """Returns a list of all relevant files in the current directory."""
    # Get all files in the current directory and its subdirectories
    files = []
    for dirpath, dirnames, filenames in os.walk("."):
        # Skip excluded directories
        for excluded_dir in EXCLUDED_DIRS:
            if excluded_dir in dirnames:
                dirnames.remove(excluded_dir)

        for filename in filenames:
            ext = os.path.splitext(filename)[1]
            if any(ext in extensions for extensions in accepted_formats.values()):
                files.append(os.path.join(dirpath, filename))

    return files


def process_files(files: list, accepted_formats: dict) -> int:
    """
    Processes a list of files using the specified functions.

    :param files: The list of files to process.
    :param accepted_formats: A dictionary mapping processing functions to file extensions.
    """
    exit_code = 0
    for file in files:
        ext = os.path.splitext(file)[1]

        for processor, extensions in accepted_formats.items():
            if ext in extensions:
                # Call the processing function
                exit_code += processor(file)
                break
    return exit_code
