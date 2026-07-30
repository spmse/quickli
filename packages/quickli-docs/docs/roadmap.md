---
id: roadmap
title: Development Roadmap
sidebar_position: 3
description: Planned steps for the next stages of quickli development.
---

# Development Roadmap

quickli is an Alpha project. This roadmap describes the next planned steps rather than
promising fixed delivery dates. Each step will be implemented, tested, documented, and
reviewed before it is treated as complete.

## Near-term priorities

1. **Release readiness**
   - Make versioning and release artifacts derive from the release tag.
   - Verify the package on Python 3.12, 3.13, and 3.14.
   - Publish the same tested distributions to PyPI and attach release evidence to GitHub.
2. **Executable runtime boundary**
   - Provide a small, explicit wrapper for `sys.argv`, output, errors, and exit codes.
   - Keep `Application.run(tokens)` as the library-level API.
3. **More complete command composition**
   - Evaluate nested subcommands and clearer unknown-command errors.
   - Preserve the current small command, argument, and option abstractions.

## Following priorities

- configuration files with an explicit precedence model
- shell completion generated from registered commands and options
- a deliberate plugin loading and registration API
- combined short flags, if they can be added without making parsing ambiguous

## How priorities are chosen

The project favors changes that improve the learning experience and keep the core small.
New behavior should have a written specification, focused unit tests, runnable examples, and
updated documentation. Planned items may be reordered as feedback and implementation risks
become clearer.