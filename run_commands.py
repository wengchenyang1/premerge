#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
from typing import List


def get_supported_commands() -> List[str]:
    """
    Returns a list of supported commands.
    """
    files = os.listdir("commands")

    commands = []
    for file in files:
        if file.endswith(".py") and (not file.startswith("utils")):
            command: str = file[:-3]
            commands.append(command)

    return commands


def run_commands():
    supported_commands = get_supported_commands()

    parser = argparse.ArgumentParser(description="Runs a command.")
    parser.add_argument(
        "command", nargs="?", choices=supported_commands, help="The command to run"
    )
    args, unknown_args = parser.parse_known_args()

    if args.command is None:
        parser.print_help()
        print("\nSupported commands:")
        for cmd in supported_commands:
            print(f"  {cmd}")
    else:
        script_path = os.path.join("commands", args.command + ".py")
        result = subprocess.run([sys.executable, script_path] + unknown_args)
        # Check the exit status of the subprocess and exit with the same status if it's non-zero
        if result.returncode != 0:
            print(f"{args.command} ........................... FAILED")
            sys.exit(result.returncode)


if __name__ == "__main__":
    run_commands()
