# Installation

## Local Development Install

From the repository root, enter the core package before creating a virtual environment
and installing the package in editable mode:

```bash
cd packages/core
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Verify the Install

Run the test suite from `packages/core` with that environment active.

```bash
python -m pytest
```

You can also run one of the example applications directly.

```bash
python examples/simple/quickhead/app.py docs/usage.md -n 5
python examples/simple/quickhead/app.py --help
```

## Running the Test Suite

The project uses `pytest` for the test suite. Run the existing checks from `packages/core`:

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
- The maintainer [release checklist](open-source-release.md#release-preparation-checklist)
  records package metadata checks and publication approval gates.

To distribute your own application, expose a function returning `app.main()` through
`[project.scripts]`, for example `mytool = "mytool.cli:main"`. Build a wheel first, then
choose an optional standalone binary or container if your deployment needs one.
See the official [packaging guide](https://spmse.github.io/quickli/docs/guides#packaging-guide)
for a complete `pyproject.toml`, PyInstaller commands, and a Dockerfile.
