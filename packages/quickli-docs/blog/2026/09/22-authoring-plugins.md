---
title: "Authoring Your First quiCkLI Plugin"
description: "A step-by-step guide to building, testing, and distributing a quiCkLI plugin."
slug: authoring-a-quickli-plugin
authors:
  - spmse
date: 2026-09-22
draft: true
tags: [general, plugins, tutorial, quickli]
---

This post walks you through building a small but complete `quickli` plugin from scratch,
including the Python package structure, writing tests, and the steps needed to distribute
it so others can install it with `pip`.

:::caution

Core supports explicit in-process plugin loading. It does not automatically discover
installed plugins through Python package entry points.

:::

{/* truncate */}

## Before you start

Make sure you have `quickli` installed:

```bash
$ pip install quickli
```

You should also be familiar with the `quickli` [plugin API](/blog/quickli-plugin-system)
before following this guide.

## What we will build

We will create a plugin called `quickli-hello` that adds a `hello` command to any
`quickli` application. The command accepts an optional `--uppercase` flag and an optional
`name` argument.

```
demo hello Ada --uppercase
# HELLO ADA
```

## Project structure

```
quickli-hello/
├── pyproject.toml
├── src/
│   └── quickli_hello/
│       └── __init__.py
└── tests/
    └── test_hello_plugin.py
```

## Step 1: Create the plugin package

Create `src/quickli_hello/__init__.py`:

```python
"""quickli-hello: adds a hello command to any quickli application."""

from __future__ import annotations

import quickli


class HelloPlugin(quickli.Plugin):
    """Plugin that adds a configurable hello command."""

    @property
    def name(self) -> str:
        return "quickli-hello"

    @property
    def description(self) -> str:
        return "Adds a hello command that greets a user by name."

    def register(self, application: quickli.Application) -> None:
        @application.command(
            help_text="Greets a user by name.",
            arguments=[quickli.Argument("name", required=False, default="world")],
            options=[quickli.Option("uppercase", short_name="u", is_flag=True)],
        )
        def hello(name: str = "world", uppercase: bool = False) -> str:
            message = f"hello {name}"
            if uppercase:
                message = message.upper()
            return message
```

## Step 2: Write a pyproject.toml

```toml
[build-system]
requires = ["setuptools>=69"]
build-backend = "setuptools.build_meta"

[project]
name = "quickli-hello"
version = "0.1.0"
description = "A quickli plugin that adds a hello command."
requires-python = ">=3.12"
dependencies = ["quickli>=0.1.1"]

[tool.setuptools]
package-dir = {"" = "src"}
```

## Step 3: Write tests

Create `tests/test_hello_plugin.py`:

```python
"""Tests for the quickli-hello plugin."""

import unittest

import quickli
from quickli_hello import HelloPlugin


class HelloPluginContractTests(unittest.TestCase):
    def test_plugin_name(self) -> None:
        plugin = HelloPlugin()
        self.assertEqual(plugin.name, "quickli-hello")

    def test_plugin_description(self) -> None:
        plugin = HelloPlugin()
        self.assertIn("hello", plugin.description.lower())


class HelloPluginBehaviorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = quickli.Application(name="demo")
        self.app.load_plugin(HelloPlugin())

    def test_hello_with_default_name(self) -> None:
        result = self.app.run(["hello"])
        self.assertEqual(result, "hello world")

    def test_hello_with_explicit_name(self) -> None:
        result = self.app.run(["hello", "Ada"])
        self.assertEqual(result, "hello Ada")

    def test_hello_with_uppercase_flag(self) -> None:
        result = self.app.run(["hello", "Ada", "--uppercase"])
        self.assertEqual(result, "HELLO ADA")

    def test_hello_with_short_flag(self) -> None:
        result = self.app.run(["hello", "Ada", "-u"])
        self.assertEqual(result, "HELLO ADA")

    def test_hello_command_is_in_application_registry(self) -> None:
        self.assertIn("hello", self.app.commands)

    def test_plugin_is_tracked_in_application(self) -> None:
        self.assertEqual(len(self.app.plugins), 1)
        self.assertEqual(self.app.plugins[0].name, "quickli-hello")


if __name__ == "__main__":
    unittest.main()
```

Run the tests:

```bash
$ PYTHONPATH=src python -m unittest discover -s tests -v
```

## Step 4: Use the plugin in an application

```python
import quickli
from quickli_hello import HelloPlugin

app = quickli.Application(name="my-app", description="My CLI application.")
app.load_plugin(HelloPlugin())

print(app.run())
```

Running `python app.py hello Ada --uppercase` produces `HELLO ADA`.

## Step 5: Publish to PyPI (optional)

Once the plugin is ready, build and upload it:

```bash
$ pip install build twine
$ python -m build
$ twine upload dist/*
```

Users can then install and use it:

```bash
$ pip install quickli-hello
```

## Naming conventions

We recommend prefixing your plugin's package name with `quickli-` so it is easy to
discover on PyPI. The plugin `name` property should match the distribution name.

## Summary

A complete `quickli` plugin requires:

1. A class that subclasses `quickli.Plugin`.
2. Implementations of `name`, `description`, and `register`.
3. A `pyproject.toml` that declares `quickli` as a dependency.
4. Tests that verify the contract and the registered behavior.

## Reference

- [Plugin API overview](/blog/quickli-plugin-system)
- [Plugin concept documentation](/docs/concepts/plugin)
- [Plugin specification on GitHub](https://github.com/spmse/quickli/blob/main/packages/core/specs/plugin.md)
