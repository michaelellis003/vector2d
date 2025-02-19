# Python Package Template

The `python-package-template` repository offers a robust template for creating Python packages. It incorporates best practices for project structure, dependency management, testing, and continuous integration, enabling developers to quickly set up and maintain high-quality Python projects.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pyright](https://img.shields.io/badge/Pyright-enabled-brightgreen)](https://github.com/microsoft/pyright)
[![codecov](https://codecov.io/github/timvancann/yt-python-ci/graph/badge.svg?token=V7PPBOI0F0)](https://codecov.io/github/timvancann/yt-python-ci)
[![License](https://img.shields.io/github/license/michaelellis003/python-package-template)](https://github.com/michaelellis003/python-package-template/blob/main/LICENSE)

## Table of Contents
1. [Features](#features)  
2. [Getting Started](#getting-started)  
3. [Using uv](#using-uv)  
   - [Managing Dependencies](#managing-dependencies)  
   - [Synchronizing](#synchronizing)  
4. [Pre-commit Configuration](#pre-commit-configuration)  
5. [GitHub Actions](#github-actions)  
   - [Continuous Integration](#continuous-integration-ci)  
   - [Release Workflow](#release-workflow)

## Features
- [uv](https://docs.astral.sh/uv/) for Python package management and environment handling.
- Pre-commit hooks to enforce consistent code style, including:
    - [Ruff](https://docs.astral.sh/ruff/) for linting and formatting,
    - [Pyright](https://github.com/microsoft/pyright) for static type checking.
- [Pytest](https://docs.pytest.org/en/stable/) for running code tests.
- **GitHub Actions** for CI/CD, including automated tests, lint checks, and release tagging.

## Getting Started
1. Install uv 
- [See the uv documentation](https://docs.astral.sh/uv/) for more details and alternate methods. Examples include:
    ```
    # On macOS and Linux.
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
    ```
    # On Windows.
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
    Or, from PyPI:
    ```
    # With pip.
    pip install uv
    ```
    ```
    # Or pipx.
    pipx install uv
    ```
    If installed via the standalone installer, uv can update itself to the latest version:
    ```
    uv self update
    ```

2. Install pre-commit
    ```
    pip install pre-commit
    ```

3. Update project metadata in:
    - `pyproject.toml`:
        - Change the project name, version, and author information to match your package.
    - `README.md`, `LICENSE`, `CHANGELOG.md` (optional):
        - Replace placeholder names, badges, and repository links with those for your project.

4. Synchronize dependencies:
    From within the project directory, run:
    ```
    uv lock
    ```
    This updates the project's lockfile.

5. Initialize pre-commit hooks:
    Enable pre-commit hooks in your local environment so they run automatically before every commit:
    ```
    pre-commit install
    ```

## Using uv
For the full uv documentation, visit the [full docs](https://docs.astral.sh/uv/)

### Managing Dependencies
- Adding Dependencies  
    - To add a new runtime dependency to your project, use:
        ```
        uv add <package_name>
        ```
    - Example:
        ```
        uv add requests
        ```
        This updates your `pyproject.toml` under [project.dependencies] and synchronizes your virtual environment automatically.

    - For dev-only dependencies, you can specify --dev:
        ```
        uv add pytest --dev
        ```
        This updates [project.optional-dependencies.dev] in your pyproject.toml.

- Removing Dependencies
    - Similarly, to remove a dependency:
        ```
        uv remove requests
        ```
        uv removes the package from your pyproject.toml and uninstalls it from your virtual environment.

- Updating version
    - Before releasing a new version of your package you will need to manually update the version number in the pyproject.toml. If you do not update the verrsion number before merging into the main branch the release workflow will fail.

### Synchronizing
Whenever you modify your pyproject.toml manually (e.g., adjusting versions, adding optional dependencies, etc.), run:

```
uv sync
```
`uv sync` ensures that all project dependencies are installed and up-to-date with the lockfile. If the project virtual environment (.venv) does not exist, it will be created. The project is re-locked before syncing unless the --locked or --frozen flag is provided.


## Pre-commit Configuration
Your `.pre-commit-config.yaml` defines hooks that run automatically on git commit. These hooks help maintain consistent code quality and style:

- uv-pre-commit → uv-lock
    - Ensures your dependencies stay pinned and consistent.
- ruff-pre-commit → ruff, ruff-format
    - ruff checks style, complexity, and potential errors.
    - ruff-format enforces standardized code formatting.
- pyright-python → pyright
    - Performs static type checking to spot errors before they are committed.

When these hooks run, they reference configurations in `pyproject.toml`. Below are some key sections:

### Ruff Configuration
```
[tool.ruff]
# Set the maximum line length to 79.
line-length = 79
indent-width = 4

# Assume Python 3.10
target-version = "py310"
```

#### Lint Rules
The Ruff Linter is an extremely fast Python linter designed as a drop-in replacement for Flake8 (plus dozens of plugins), isort, pydocstyle, pyupgrade, autoflake, and more.
```
[tool.ruff]
line-length = 79 #  Line length is set to 79.
indent-width = 4
target-version = "py310" # Target version is Python 3.10.

[tool.ruff.lint]
select = ["F", "E4", "E7", "E9", "E501", "N", "D", "UP", "B", "SIM", "I"]
ignore = ["D206", "D300"]
fixable = ["ALL"] # Fixable rules let Ruff automatically fix recognized issues when --fix is used.
unfixable = []
dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"
```

#### pydocstyle:
Whether to use Google-style, NumPy-style conventions, or the PEP 257 defaults when analyzing docstring sections.
```
[tool.ruff.lint.pydocstyle]
convention = "google" # Accepts: "google", "numpy", or "pep257".
```

#### isort (Imports)
Configures how imports are sorted and grouped (e.g., split-on-trailing-comma = true to keep trailing commas)
```
[tool.ruff.lint.isort]
force-single-line = false
force-wrap-aliases = false
lines-after-imports = -1
lines-between-types = 0
split-on-trailing-comma = true
```

### Ruff Formatter
The Ruff formatter is an extremely fast Python code formatter designed as a drop-in replacement for Black
```
[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"
docstring-code-format = true
docstring-code-line-length = "dynamic"
```

### GitHub Actions
Stored under the .github/workflows/ directory
#### Continuous Integration (CI)

Workflow file: `.github/workflows/ci.yml`

1. Ruff Job
    - Checks out code.
    - Sets up uv via a custom GitHub Action (.github/actions/setup-uv).
    - Runs pre-commit, which includes Ruff and Pyright checks.
2. Pytest Job
    - Depends on Ruff Job, so it only runs if all code checks pass.
    - Installs dependencies via uv pip install ..
    - Runs pytest with coverage: --cov and --cov-report=xml.
    - Uploads coverage to Codecov using the CODECOV_TOKEN secret.
This ensures each branch is linted, type-checked, and tested with consistent environments.

#### Release Workflow

Workflow file: `.github/workflows/release.yml`

- Triggers on closed pull requests merging into main.
- Steps:
    1. Checkout + Setup uv
    2. Extract Version
        - Uses toml-cli via uvx to read project.version from pyproject.toml.
    3. Create and Push Tag
        - Tags the commit with the version (e.g., v0.1.0).
        - Updates the floating major version tag (e.g., v0 → v0.1.0).
This process automatically tags your releases based on the version in pyproject.toml, making it easy to track and reference changes.
