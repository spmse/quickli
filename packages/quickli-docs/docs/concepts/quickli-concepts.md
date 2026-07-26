---
sidebar_position: 1
---

# quiCkLI Concepts

This page lists the core concepts in `quickli` and explains how they work together.

## Application

An **application** is the CLI container. It owns command registration, parses input
tokens, dispatches execution, and renders application-level help.

Use one `Application` instance as the root of your CLI.

## Command

A **command** wraps one handler function and gives it a CLI-facing contract:

- command name
- help text
- arguments
- options

Commands are selected by name and executed through the application.

## Argument

An **argument** is a positional input value for a command.

Arguments are typically required, can define conversion logic, and can run validators
after conversion. An argument becomes optional when it defines a default value.

## Option

An **option** is a named input that changes behavior.

Options support long and short forms, defaults, required settings, conversion, and
validation. Boolean options act as flags, and repeatable options can collect multiple
values.

## Plugin

A **plugin** is a planned extension concept.

The plugin system is not implemented yet. The concept exists to guide future extension
design without changing the core package directly.

## How the concepts fit together

In a typical flow:

1. create an `Application`
2. register one or more `Command` handlers
3. define each command's `Argument` and `Option` resources
4. run the application with explicit command-line tokens (`argv`)
