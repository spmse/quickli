# Installation

## Local Development Install

Create a virtual environment, activate it, and install the package in editable mode.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

## Verify the Install

Run the test suite from the repository root.

```bash
python -m pytest
```

You can also run one of the example applications directly.

```bash
PYTHONPATH=src python examples/simple/quickhead/app.py AGENTS.md -n 5
```

## Running the Test Suite

The project uses `pytest` for the test suite.

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest
python -m build --sdist --wheel
```

## Version Support

The target support range is Python 3.12, 3.13, and 3.14.

## Packaging Notes

- The package name is `quickli`.
- The repository uses the `src` layout.
- The project is licensed under MIT.
- Release Please manages versioned releases through `.github/workflows/release.yml`.
