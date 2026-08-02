---
id: introduction
title: Introduction
sidebar_position: 1
description: Learn why quickli exists and what the framework provides.
---

import { MinimalExample } from '@site/src/components/QuickliExamples';

# Introduction

quiCkLI is an **educational minimal framework** for building Python command-line
interfaces. It provides a small set of explicit building blocks without hiding the command
line behind a large abstraction layer.

## Why quickli?

Many CLI frameworks are designed to solve every possible problem. That is useful for large
applications, but it can make the fundamentals difficult to see. quickli takes a smaller
approach so that developers can learn how a CLI is assembled:

- `Application` owns registration and dispatch.
- `Command` represents a named operation.
- `Argument` describes positional input.
- `Option` describes named input and flags.
- Converters and validators turn text into checked values.

The framework is intentionally dependency-light and keeps the library boundary visible.
`Application.run()` still returns handler results to the caller, while `Application.main()`
offers a standard executable shell for `sys.argv`, output, structured runtime errors, and
exit codes.

## A small example

The following commandless application accepts JSON or YAML text and normalizes it to JSON:

<MinimalExample />

The next page shows how to install quickli and run a complete example.

## Where to go next

Read [quiCkLI Concepts](./concepts/quickli-concepts.md) to understand how
`Application`, `Command`, `Argument`, `Option`, and `Plugin` relate to each other.

See the [development roadmap](./roadmap.md) for the project's planned next steps.
