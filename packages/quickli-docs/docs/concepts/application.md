---
sidebar_position: 2
---

# Application

`Application` is the root CLI container in `quickli`.

## What it owns

- command registration
- optional root entrypoint registration
- application-level global options
- command dispatch from input tokens
- application and command help rendering

## Execution model

`Application.run(argv)` accepts explicit command-line tokens and returns the selected
handler result (or generated help text).

- It does **not** read `sys.argv` itself.
- It does **not** print output by default.
- It does **not** choose process exit codes.

That boundary keeps runtime behavior explicit in your executable wrapper.

## Registration API

`Application` offers decorator APIs for command registration:

- `@app.command(...)` for named commands in a multi-command CLI
- `@app.entrypoint(...)` for a commandless root flow

When both exist, command names take precedence, and the entrypoint acts as fallback.
