---
sidebar_position: 3
---

# Command

`Command` represents one executable operation in a CLI.

## What a command contains

- a public command name
- help text (explicit or derived from a docstring)
- positional argument definitions
- named option definitions
- one handler callable

## Responsibilities

A command parses tokens that belong to it, validates the parsed values against resource
definitions, binds values to the handler signature, and executes the handler.

## Naming behavior

Commands are registered under unique names. Function names are normalized by replacing
underscores with hyphens when a name is not explicitly provided.
