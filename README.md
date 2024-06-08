# Pre-merge Job Runner

This repository contains an all-in-one python script run pre-merge jobs for code quality checks. These checks include formatting, linting, and copyright management for both Python and C++ files.

## Installation

To set up the pre-merge job runner, follow these steps:

1. **Clone the Repository**

    Clone the repository to your project's root folder:

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

    The `setup.sh` script will set up necessary configurations.

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

