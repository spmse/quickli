# Plugin Specification

## Purpose

A plugin is a planned extension that **could** extend the base application without modifying the
core package directly.

> [!WARNING] Current Status

> - The plugin system is not implemented in the initial scaffold.
> - The concept is documented for future design only; it is not part of the current public API.
> - Current examples and public documentation focus on the core application, command,
>   argument, option, conversion, validation, and help layers.

## Planned Technical Direction (Not Implemented)

- Discover plugins through Python package metadata or explicit loading.
- Allow plugins to register commands and resources against an application instance.
- Define a stable plugin lifecycle before supporting third-party plugins publicly.

## Risks

- Plugin loading affects security, compatibility, and error isolation.
- A weak lifecycle contract will create long-term maintenance costs.
