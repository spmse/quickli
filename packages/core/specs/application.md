# Application Specification

## Purpose

The application resource represents the library-level CLI configuration.
It owns the command registry and dispatches explicit input tokens to a handler.

## Responsibilities

- Maintain a unique registry of commands.
- Optionally expose a single application-level entrypoint without commands.
- Expose a declarative registration API.
- Route user input to the selected command.
- Render plain-text help output.
- Return the selected handler result to the caller.
- Optionally expose an executable shell through `Application.main()`.
- Aggregate command help into application-level help output.
- Parse application-level global options before command dispatch.
- Optionally register a built-in `shell-completion` command that generates scripts for
  bash, zsh, and PowerShell.

## Technical Notes

- The current implementation is intentionally minimal.
- Command lookup is string-based.
- Applications may run as commandless CLIs through a root entrypoint.
- Commands can define explicit argument and option resources.
- Applications can define explicit global option resources.
- Execution supports positional string arguments and named options.
- Options currently support `--long value`, `--long=value`, and `-s value` forms.
- Flags are represented as boolean options.
- Arguments and options may convert raw string input through callables.
- Commands may include nested subcommands.
- Help output includes generated usage, argument descriptions, and option descriptions.
- Global and local options are rendered separately in help output.
- Global options may appear before or after the command name.
- When both commands and an application entrypoint exist, command names take precedence and
	the entrypoint acts as a fallback.
- `Application.run()` reads `sys.argv[1:]` by default when no explicit `argv` argument is
	passed and `auto_sys_argv=True` (the default). Pass an explicit list to override this for
	a single call, or set `auto_sys_argv=False` at construction time to use an empty list
	unconditionally.
- `Application.run(argv)` returns the selected handler result or generated help text.
- `Application.run()` does not print results, render process-level errors, or choose process
	exit codes; those responsibilities belong to the caller unless `main()` is used.
- `Application.main(argv=None, output_format="text")` provides an executable shell that:
	- reads `sys.argv[1:]` when `argv` is omitted,
	- prints successful results to stdout,
	- maps unexpected internal failures to `InternalCLIError`,
	- wraps user callback failures in `UserCodeError` while preserving the original error, and
	- returns process-friendly exit codes.
- `Application` may accept a global `error_handler` callback that can replace or adapt a
	quickli error before `main()` renders it.
- `Application.main(..., output_format="json")` emits machine-readable success and error
	payloads for automated scenarios.
- The core package provides JSON/YAML rendering and loading helpers through
	`quickli.parsers`.
- The resource must remain dependency-light and compatible with Python `3.12` to `3.14`.
- When `shell_completion=True`, the `Application` automatically registers a built-in
  `shell-completion` command.
- `Application.generate_completion(shell)` produces a completion script string for the
  requested shell (`bash`, `zsh`, `powershell`, or the `pwsh` alias).
- The standalone functions `generate_bash_completion`, `generate_zsh_completion`, and
  `generate_powershell_completion` are available from the public package interface.
- `SUPPORTED_SHELLS` is a public constant that lists all supported shell names.

## Future Extensions

- Typed argument conversion beyond booleans and raw strings.
- Nested command groups.
- Shell completion within commands (arguments and options).
- Config-driven application setup.
- Plugin discovery and registration.
