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

`Application.run()` dispatches the selected command and returns the handler result (or
generated help text).

- It reads `sys.argv[1:]` **by default** when called without arguments.
- Pass an explicit list to override: `app.run(["greet", "Ada"])`.
- Set `auto_sys_argv=False` at construction to always use an empty list instead.
- It does **not** print output by default.
- It does **not** choose process exit codes.

`Application.main(argv=None)` adds the standard executable shell on top of `run()`.

- It reads `sys.argv[1:]` when `argv` is omitted.
- It prints normal command results.
- It converts runtime failures into structured quickli errors.
- It returns process-friendly exit codes.

That split keeps library use explicit while still giving executable applications a simple
default runtime.

## Registration API

`Application` offers decorator APIs for command registration:

- `@app.command(...)` for named commands in a multi-command CLI
- `@app.entrypoint(...)` for a commandless root flow

When both exist, command names take precedence, and the entrypoint acts as fallback.
