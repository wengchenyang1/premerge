""" Formatter tool """

import argparse
import subprocess
import sys

import utils as utils


def format_cpp(file_path) -> int:
    """
    Formats a C++ file using clang-format.

    :param file_path: The path to the C++ file to format.
    """
    # Run clang-format on the file
    result = subprocess.run(["clang-format", "-i", file_path], check=False)
    return result.returncode


def format_python(file_path) -> int:
    """
    Formats a Python file using black.

    :param file_path: The path to the Python file to format.
    """
    # Run black on the file
    result_isort = subprocess.run(["isort", file_path], check=False)
    result_black = subprocess.run(["black", file_path], check=False)
    return result_black.returncode + result_isort.returncode


if __name__ == "__main__":
    accepted_formats = {
        format_cpp: [".cpp", ".cc", ".h", ".hpp"],
        format_python: [".py"],
    }
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Formats source code files.")
    parser.add_argument("--full", action="store_true", help="Format all relevant files")
    args = parser.parse_args()

    # Get the list of files to format
    if args.full:
        files = utils.get_all_files(accepted_formats)
    else:
        files = utils.get_changed_files()

    # Format each file
    sys.exit(utils.process_files(files, accepted_formats))
