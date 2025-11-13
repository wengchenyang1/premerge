# Pre-merge Job Runner

This repository contains a single Python script that runs pre-merge jobs on _most recently changed files_. These jobs encompass formatting, linting, and copyright management for (currently)

* Python
* C++

files.

## Installation

To set up the pre-merge job runner, follow these steps:

1. **Add as a Submodule**

    You may integrate this as a submodule in your existing repository. Navigate to your project root folder and add `premerge` using the following command:

    ```sh
    git submodule add https://github.com/wengchenyang1/premerge.git premerge
    ```

    If the submodule already exists, you can initialize and update it after cloning the repository using:

    ```sh
    git submodule update --init --recursive
    ```

2. **Run the Setup Script**

    On Linux/macOS:

    ```sh
    bash ./premerge/setup.sh
    ```

    On Windows:

    ```bat
    premerge\setup.bat
    ```

    The setup script will set up necessary configurations, such as copying template config files for linting and formatting to the root folder (if there are not any).

3. **Install Dependencies**

    The pre-merge tool requires the following tools to be installed:

    **Python Tools** (install via pip):

    ```sh
    pip install pylint black isort cpplint
    ```

    **C++ Tools**:
    * **clang-format** (for C++ formatting):
      * Windows: `scoop install llvm` or download from [LLVM releases](https://llvm.org/releases/)
      * Linux: `sudo apt install clang-format`
      * macOS: `brew install clang-format`

## Usage

### Running the Pre-merge Checks

To run the pre-merge checks, execute the following command in your project root directory:

```sh
python premerge/pre_merge.py
```

## Note

This setup script and accompanying pre-merge checks are designed for quick implementation and execution of a series of verification tasks in small projects. While it serves well for basic use cases, it may not be the optimal solution for larger projects with more complex requirements.

The single-file structure of this setup may limit its extensibility and scalability. For more extensive projects, consider using more sophisticated tools and frameworks that are specifically designed for larger codebases and more intricate workflows.

## TODOs

See issues.
