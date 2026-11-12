# Build a four-command toolbox with quickli, Click, and argparse

This example implements the same `cp`, `mkdir`, `touch`, and `echo` commands in three
different CLI libraries. The file operations are shared so the examples focus on command
registration and dispatch.

Run an application from this directory with the repository's `src` directory on
`PYTHONPATH`:

```bash
PYTHONPATH=../../../src python quickli_app.py --help
PYTHONPATH=../../../src python quickli_app.py echo hello
python click_app.py echo hello
python argparse_app.py echo hello
```

Install the `dev` extra from `packages/core` to run the Click example and integration tests.
From `packages/core`, run the tests with:

```bash
python -m pip install -e ".[dev]"
python -m unittest discover -s tests -p 'test_toolbox_examples.py'
```

The tests use temporary directories and files; they do not modify the working directory.
