---
id: guides-index
title: Implementation Guides
sidebar_position: 1
description: >
  Step-by-step tutorials that walk through the reference examples in the quickli source
  package. Learn how the framework primitives fit together by reading and running real code.
keywords: [quickli, tutorial, guide, cli, python, example]
---

# Implementation Guides

These guides walk through the reference examples that ship with the `quickli` source
package. Each guide explains the code line-by-line so you can follow along, run the
examples yourself, and understand how the framework primitives work together.

## How to use these guides

Every guide is self-contained. You can read them in any order, but the sequence below
builds knowledge progressively from the smallest possible example to a larger multi-command
application.

1. **[Hello World](./01-hello-world.md)** — your first entrypoint, one argument, one flag.
2. **[File viewer (quickcat)](./02-building-cat-cli.md)** — global options, multiple file
   arguments, and the `file_path` validator.
3. **[Directory listing (quickls)](./03-building-ls-cli.md)** — optional arguments,
   multiple options, and the `directory_path` validator.
4. **[Directory creator (quickmkdir)](./04-building-mkdir-cli.md)** — repeatable options
   and combining multiple paths in one call.
5. **[File head (quickhead)](./05-building-head-cli.md)** — numeric conversion with `int`
   and the `positive_number` validator.
6. **[Multi-command CLI (pyk5l)](./06-multi-command-kubectl.md)** — multiple commands,
   global options, and custom validators on a kubectl-like application.

## Prerequisites

Install quickli before running any example:

```bash
pip install quickli
```

All examples run on Python 3.12, 3.13, and 3.14.
