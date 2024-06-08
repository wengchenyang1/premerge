# Copyright (c) 2024, CWeng

""" Pre-push and pre-merge checks. """

import io
import os
import subprocess
from typing import List

from pylint import lint
from pylint.reporters.text import TextReporter

CPP_FILE_EXT = [".h", ".cpp", "hpp", "cc"]
PY_FILES_EXT = [".py"]

EXCLUDED_DIRS = ["build", ".vscode"]

PYLINT_FAIL = 8.0

_SUCCESS = 0
_FAIL = 1


def get_changed_files(target_extensions: List[str]) -> List[str]:
    """
    Returns a list of changed files in the current git repository including the latest commit.
    """
    result = subprocess.run(
        ["git", "status", "--porcelain", "-u"], stdout=subprocess.PIPE, check=True
    )

    lines = result.stdout.decode("utf-8").split("\n")
    files = set()
    for line in lines:
        parts = line.split()
        if len(parts) > 1:
            status = parts[0][0]
            file_name = parts[2] if status in ("R", "C") else parts[1]
            if any(
                file_name.endswith(ext) for ext in target_extensions
            ) and os.path.exists(file_name):
                files.add(file_name)

    if not files:
        result = subprocess.run(
            ["git", "log", "-1", "--name-only", "--pretty=format:"],
            stdout=subprocess.PIPE,
            check=True,
        )

        lines = result.stdout.decode("utf-8").split("\n")
        for line in lines:
            if (
                line
                and any(line.endswith(ext) for ext in target_extensions)
                and os.path.exists(line)
            ):
                files.add(line)

    return list(files)


def lint_python_files() -> int:
    python_files = get_changed_files(PY_FILES_EXT)
    if python_files:
        for file in python_files:
            pylint_output = io.StringIO()
            reporter = TextReporter(pylint_output)
            lint.Run([file], reporter=reporter, exit=False)
            output = pylint_output.getvalue()
            print(output)
            score_line = next(
                line
                for line in output.split("\n")
                if "Your code has been rated at" in line
            )
            score = float(score_line.split("/")[0].split(" ")[-1])
            if score < PYLINT_FAIL:
                print(f"Failed linting with score {score}")
                return _FAIL
    return _SUCCESS


def format_python_files() -> int:
    try:
        python_files = get_changed_files(PY_FILES_EXT)
        if python_files:
            for file in python_files:
                _ = subprocess.run(
                    ["isort", file], capture_output=True, text=True, check=True
                )
                black_process = subprocess.run(
                    ["black", file],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    check=True,
                )

                if "reformatted" in black_process.stdout:
                    raise ValueError(f"{file} was reformatted.")
        return _SUCCESS
    except ValueError as error:
        print(f"Error: {error}")
        return _FAIL


def format_cpp_files() -> int:
    try:
        cpp_files = get_changed_files(CPP_FILE_EXT)
        if cpp_files:
            for cpp_file in cpp_files:
                result = subprocess.run(
                    ["clang-format", "-output-replacements-xml", cpp_file],
                    capture_output=True,
                    text=True,
                    check=True
                )
                _ = subprocess.run(
                    ["clang-format", "-i", cpp_file],
                    capture_output=False,
                    text=False,
                    check=False
                )
                if "<replacement " in result.stdout:
                    raise ValueError(f"The file {cpp_file} would be reformatted.")

            # If no errors were raised, format the files in-place
            subprocess.run(
                ["clang-format", "-i"] + cpp_files,
                capture_output=True,
                text=True,
                check=True,
            )
        return _SUCCESS
    except ValueError as error:
        print(f"Error: {error}")
        return _FAIL
    except subprocess.CalledProcessError as cpe:
        print(f"Subprocess error: {cpe}")
        return _FAIL


def lint_cpp_files() -> int:
    try:
        cpp_files = get_changed_files(CPP_FILE_EXT)
        if cpp_files:
            process = subprocess.run(
                ["cpplint"] + cpp_files,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
            if process.returncode != 0:
                error_message = process.stderr
                formatted_error_message = "\n".join(
                    f" - {line}" for line in error_message.split("\n") if line
                )
                raise ValueError(
                    f"Linting failed with the following messages:\n{formatted_error_message}"
                )
        return _SUCCESS
    except ValueError as error:
        print(f"Error: {error}")
        return _FAIL


def write_copyright() -> int:
    try:

        def _get_owner_name() -> str:
            owner_file = ".owner"
            if not os.path.exists(owner_file):
                print(
                    f"File '{owner_file}' does not exist. "
                    "Please create it and write the owner name inside.",
                )
                with open(owner_file, "w", encoding="utf-8") as file:
                    owner_name = input("Enter the owner name: ")
                    file.write(owner_name + "\n")
                print(
                    f"File '{owner_file}' has been created with the owner name '{owner_name}'."
                )
            else:
                with open(owner_file, "r", encoding="utf-8") as file:
                    owner_name = file.readline().strip()
                    if not owner_name:
                        owner_name = input(
                            "The .owner file is empty. Enter the owner name: "
                        )
                        with open(owner_file, "w", encoding="utf-8") as file:
                            file.write(owner_name + "\n")
                        print(
                            f"The .owner file has been updated with the owner name '{owner_name}'."
                        )
                    else:
                        print(f"Company name '{owner_name}' read from '{owner_file}'.")

            return owner_name

        def _write_copyright_to_files(license_text: str, files: List[str]):
            for file_name in files:
                with open(file_name, "r+", encoding="utf-8") as file_obj:
                    content = file_obj.read()
                    file_obj.seek(0, 0)
                    file_obj.write(license_text.rstrip("\r\n") + "\n" + content)

        def _get_files_without_copyright(extension: List[str]) -> List[str]:
            max_lines_to_search = 4
            all_files = get_changed_files(extension)
            target_files = []
            for file_name in all_files:
                with open(file_name, "r", encoding="utf-8") as file_obj:
                    lines = [next(file_obj) for _ in range(max_lines_to_search)]
                    if not any("copyright (c)" in line.lower() for line in lines):
                        target_files.append(file_name)
            return target_files

        year = subprocess.getoutput("date +%Y")
        owner = _get_owner_name()
        cpp_license = f"/** Copyright (c) {year}, {owner} **/"
        py_license = f"# Copyright (c) {year}, {owner}"

        cpp_files = _get_files_without_copyright(CPP_FILE_EXT)
        _write_copyright_to_files(cpp_license, cpp_files)

        py_files = _get_files_without_copyright(PY_FILES_EXT)
        _write_copyright_to_files(py_license, py_files)

        if cpp_files or py_files:
            raise ValueError("There are files without copyright!")

        return _SUCCESS
    except ValueError as error:
        print(f"Error: {error}")
        return _FAIL


if __name__ == "__main__":
    write_copyright()

    format_cpp_files()
    format_python_files()

    lint_cpp_files()
    lint_python_files()
