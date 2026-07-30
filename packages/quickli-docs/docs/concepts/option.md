---
sidebar_position: 5
---

# Option

`Option` describes a named input that modifies command behavior.

## Supported forms

- long form: `--output value`
- long assignment form: `--output=value`
- short form: `-o value`

## Core capabilities

- default values
- required options
- boolean flags (`is_flag=True`)
- conversion callables for non-flag values
- validators for converted values
- repeatable values (`multiple=True`)

Repeatable non-flag options accumulate values in a list. Repeatable flags accumulate
occurrence counts.

## Local and global options

Options can be defined on commands (local) or at the application level (global).
Global options may appear before or after the command name.
