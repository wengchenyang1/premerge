#!/usr/bin/env python3

""" Check if the current branch is not master branch """
import subprocess
import sys


def is_master_branch() -> int:
    """
    Checks if the current branch is master or main.

    :return: Exits with status code 1 if the current branch is master or main, 0 otherwise.
    """
    # Get the current branch
    branch = (
        subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        .strip()
        .decode("utf-8")
    )

    # Check if the current branch is master or main
    if branch in ["master", "main"]:
        err_msg = "You cannot commit directly to master or main branch!"
        print(f"\033[91m{err_msg}\033[0m")
        sys.exit(1)


if __name__ == "__main__":
    is_master_branch()
