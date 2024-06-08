# Pre-merge Job Runner

This repository contains scripts and tools to run pre-merge jobs for code quality checks. These checks include formatting, linting, and copyright management for both Python and C++ files.

## Installation

To set up the pre-merge job runner, follow these steps:

1. **Clone the Repository**

    If you haven't already, clone the repository to your local machine:

    ```sh
    git clone <repository-url>
    ```

2. **Add as a Submodule**

    If you are integrating this as a submodule in your existing repository, add it using the following command:

    ```sh
    git submodule add <submodule-repository-url> premerge
    ```

3. **Run the Setup Script**

    ```sh
    bash ./premerge/setup.sh
    ```

    The `setup.sh` script will set up necessary configurations and install any required dependencies.

## Usage

### Running the Pre-merge Checks

To run the pre-merge checks, execute the following command in your project root directory:

```sh
python premerge/pre_merge.py
```