---
sidebar_position: 6
---

# Plugin

`Plugin` is a documented future concept in `quickli`.

## Current status

- Plugin loading and registration are **not implemented**.
- The concept is kept in the documentation and specs to guide future design decisions.

## Intended direction

Future plugin support is expected to focus on:

- discovery and loading
- registration against an application instance
- lifecycle guarantees for compatibility and error isolation

Because plugins affect security and compatibility boundaries, the concept is tracked
carefully before entering the public runtime API.
