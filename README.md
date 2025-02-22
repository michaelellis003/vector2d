# Vector 2d

[![Python 3.10 | 3.11 | 3.12](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pyright](https://img.shields.io/badge/Pyright-enabled-brightgreen)](https://github.com/microsoft/pyright)
[![codecov](https://codecov.io/gh/michaelellis003/vector2d/graph/badge.svg?token=C2HWA2FGQB)](https://codecov.io/gh/michaelellis003/vector2d)
[![License](https://img.shields.io/github/license/michaelellis003/python-package-template)](https://github.com/michaelellis003/python-package-template/blob/main/LICENSE)

A example Python library providing a 2-dimensional vector class with efficient memory usage. Inspired by chapter 11 of *Fluent Python (2nd edition)* by Luciano Ramalho.

## Features

- Immutable and hashable 2D vector implementation
- Supports positional pattern matching
- Efficient memory usage with `__slots__`
- Methods for vector operations, including magnitude and angle calculations
- Byte serialization and deserialization
- `ShortVector2d` variant using single-precision floats for reduced memory footprint

## Installation

Install via GitHub:

```sh
pip install git+https://github.com/michaelellis003/vector2d.git
```

## Usage

### Creating Vectors

```python
from vector2d import Vector2d, ShortVector2d

v1 = Vector2d(3, 4)
print(abs(v1))
print(format(v1, 'p'))
```

### Hashability

```python
v1 = Vector2d(3, 4)
v2 = Vector2d(3, 4)
print(hash(v1) == hash(v2))
print({v1: 'vector1'}[v2])
```

### Pattern Matching

```python
def match_vector(v):
    match v:
        case Vector2d(0, 0):
            print(f'{v!r} is null')
        case Vector2d(0):
            print(f'{v!r} is vertical')
        case Vector2d(_, 0):
            print(f'{v!r} is horizontal')
        case Vector2d(x, y) if x == y:
            print(f'{v!r} is diagonal')
        case _:
            print(f'{v!r} is generic')
```

### Memory Efficiency

The `__slots__` attribute prevents the creation of `__dict__`, reducing memory overhead:

```python
v = Vector2d(1, 2)
print(v.__dict__)  # AttributeError: 'Vector2d' object has no attribute '__dict__'
```

### ShortVector2d (Single-Precision Floats)

For optimized memory usage:

```python
v1 = ShortVector2d(1.0, 2.0)
v2 = ShortVector2d(3.0, 4.0)
```

## API Reference

### `Vector2d`

- `__init__(x: float, y: float)`: Initialize a vector.
- `x`: Get the x-coordinate.
- `y`: Get the y-coordinate.
- `__iter__()`: Iterate over (x, y).
- `__repr__()`, `__str__()`: String representations.
- `__bytes__()`, `frombytes(octets)`: Serialization support.
- `__eq__()`, `__hash__()`: Equality and hash support.
- `__abs__()`: Returns the magnitude.
- `__format__(format_spec)`: Custom formatting.
- `angle()`: Returns the angle in radians.

### `ShortVector2d`

Same as `Vector2d` but using single-precision floats.

## Contributing

### Setting Up the Development Environment

This project uses [Poetry](https://python-poetry.org/) for dependency management and packaging.

1. Install Poetry if you haven’t already:

   ```sh
   pipx install poetry
   ```

2. Clone the repository and navigate into the project directory:

   ```sh
   git clone git@github.com:michaelellis003/vector2d.git
   cd vector2d
   ```

3. Install dependencies:

   ```sh
   poetry install
   ```

### Running Tests

To run tests locally:

```sh
poetry run pytest -v --durations=0 --cov --cov-report=xml
```

### Submitting Contributions

1. Create a new branch:

   ```sh
   git checkout -b feature-branch
   ```

2. Make changes and commit:

   ```sh
   git commit -m "Describe changes here"
   ```

3. Push the branch and create a pull request:

   ```sh
   git push origin feature-branch
   ```

4. If you a satisfied with your changes and want to open a PR then bump the
package version using Poetry. If you forget to do this before closing a PR
to main then the tag-and-release.yml workflow will fail.

   ```sh
   poetry version <bump-rule>
   ```

Provide a valid bump rule: patch, minor, major, prepatch, preminor, premajor, prerelease.

## CI/CD Workflows

This project uses GitHub Actions for continuous integration and deployment.

### On Push to Non-Main Branches

- **Linting & Formatting:** Runs `pre-commit` checks using `ruff`.
- **Testing:** Runs `pytest` across Python 3.10, 3.11, and 3.12.
- **Coverage Upload:** Sends test coverage reports to Codecov.

### On Merging into Main

- **Tagging & Releasing:** Automatically tags a new version based on `pyproject.toml`.
- **Builds the Package:** Uses Poetry to create distribution files.
- **Creates a GitHub Release:** Uploads the built package to GitHub releases.

## Acknowledgments

This implementation is based on *Fluent Python (2nd edition)* by Luciano Ramalho.




