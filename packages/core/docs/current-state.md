# Current State and Agent Guide

This page is the concise working contract for agents and maintainers. It describes the
current Alpha implementation, not every planned feature mentioned in historical notes.

## Source-of-Truth Hierarchy

When sources appear to disagree, use this order:

1. `src/quickli` is the implementation source of truth for current behavior.
2. `tests/` records behavior currently verified by automated tests.
3. `specs/` defines resource contracts and labels planned behavior explicitly.
4. `docs/` explains supported usage, workflows, and current limitations.
5. `docs/adr/` records accepted architectural decisions and their consequences.
6. `README.md` is the concise public overview and links to the detailed sources.
7. `CHANGELOG.md` and release notes are historical context, not API contracts.

If implementation and tests disagree, report the discrepancy before changing either one.
Do not treat a future extension, approval gate, example-only behavior, or historical note as
an implemented feature.

## Machine-Readable Feature Summary

The following YAML is an index for agents. Detailed behavior is defined by the sources above.

```yaml
project: quickli
status: alpha
runtime: library-and-shell
implemented:
  - application_entrypoint
  - named_commands
  - global_and_local_options
  - positional_arguments
  - converters
  - validators
  - repeatable_options
  - boolean_flags
  - generated_help
  - automatic_help_flags
  - docstring_help_fallback
  - render_json
  - render_yaml
  - render_toml
  - nested_subcommands
  - shell_completion
  - configuration_files
  - opt_in_config_init_command
  - explicit_config_init_routine
  - plugin_loading
  - standard_executable_runtime
  - structured_cli_errors
not_implemented:
  - plugin_discovery_via_entry_points
release_process: tag-driven
release_please: implemented
release_version_source: core_release_tag
```

`Application.run(tokens)` accepts explicit tokens and returns a handler result or help text.
`Application.main(argv=None)` provides the executable shell. It reads `sys.argv[1:]` by
default, prints results, maps failures to quickli errors, and returns exit codes.

Core JSON/YAML rendering and loading helpers are available in `quickli.parsers`. The `pyk5l`
example still keeps its own table and wide renderers.

## Parsing Behavior Matrix

| Input or operation                         | Current behavior                         | Evidence                   |
| ------------------------------------------ | ---------------------------------------- | -------------------------- |
| `run([])` without entrypoint               | Returns generated application help       | application, tests         |
| `run([])` with entrypoint                  | Invokes entrypoint with defaults         | application, tests         |
| `run(["--help"])` or `run(["-h"])`          | Returns application help without execution | application, help tests |
| `run(["env", "show", "--help"])`           | Returns nested command help with full path | application, help tests |
| Named command token                        | Dispatches to matching command           | application, tests         |
| Nested subcommand token                    | Dispatches to matching nested subcommand | command, tests             |
| Unknown command without entrypoint         | Raises `CommandNotFoundError`            | application                |
| Unknown token with entrypoint              | Passes token to entrypoint               | implementation, tests      |
| Global option around command               | Parses as global option                  | application, command specs |
| Local option                               | Parses after command selection           | command spec               |
| `--long value`, `--long=value`, `-s value` | Supports these forms                     | option spec                |
| Combined short flags like `-abc`           | Supported for flag options only          | command, option specs      |
| `--`                                       | Remaining tokens are positional          | command                    |
| Repeated non-flag option                   | Accumulates converted values in a list   | option spec                |
| Repeated flag                              | Accumulates occurrences as an integer    | option spec                |
| Converter                                  | Runs before validators and handler       | validation guide           |
| Validator                                  | Runs after conversion and before handler | validation guide           |
| Handler exception                          | Raises `UserCodeError` with original cause | command, tests          |
| `auto_init_config=True` with `Config`       | Registers `init` without startup writes   | application, config tests |
| `app.init_config()`                        | Creates defaults or loads existing config | application, config spec |
| JSON/YAML non-mapping config root          | Raises `ConfigError`                     | config, config tests      |
| `load_plugin` with valid plugin            | Calls register, appends to plugin list   | plugin spec, tests         |
| `load_plugin` with empty name              | Raises `PluginLoadError`                 | plugin spec, tests         |
| `load_plugin` with duplicate name          | Raises `PluginLoadError`                 | plugin spec, tests         |
| `load_plugin` when register fails          | Wraps exception in `PluginLoadError`     | plugin spec, tests         |

The approved future behavior for an unknown command is to fail with the command and root help
when both named commands and an entrypoint exist. That behavior is implementation-deferred and
must not be described as current behavior until a separate runtime branch changes the code and
tests.

## Exception Matrix

| Exception                  | Raised for                                           | Owner                |
| -------------------------- | ---------------------------------------------------- | -------------------- |
| `CLIError`                 | Base class for framework errors                      | exceptions           |
| `CommandRegistrationError` | Invalid or duplicate registration                    | registration         |
| `CommandNotFoundError`     | Unknown command without entrypoint                   | application dispatch |
| `CommandExecutionError`    | Parsing, conversion, validation, or binding failures | command              |
| `UserCodeError`            | User-provided handler or error override failure      | runtime boundary     |
| `InternalCLIError`         | Unexpected quickli internal runtime failure          | runtime boundary     |
| `PluginLoadError`          | Invalid plugin name, duplicate plugin, or register failure | plugin loading |
| `ConfigError`              | Configuration access, parsing, encoding, or shape failure | configuration |
| `ConfigValidationError`    | Loaded configuration fails its schema                    | configuration |

Framework exceptions remain usable as library errors. `Application.main()` now provides the
default executable policy for printing them, serializing them as JSON, and returning exit
codes.

## Do Not Assume

- `Application.run()` reads `sys.argv[1:]` only when its argument is omitted and
  `auto_sys_argv=True`. Explicit `None` or `[]` means no tokens.
- Do not assume `Application.run()` prints a returned string; call `Application.main()` when
  you want quickli to own process I/O.
- Do not assume unknown commands already follow the approved future failure behavior.
- Do not assume advanced YAML syntax is supported by the minimal core YAML parser.
  Configuration files use PyYAML instead; for example, `Config("app.yaml").load()`
  supports nested mappings and flow collections.
- Automatic `--help`/`-h` handling is enabled by default through `Application`.
  For example, `app.run(["deploy", "--help"])` bypasses required input and handler execution.
  Explicit options keep their aliases; `auto_help=False` disables the feature.
- Do not assume plugin discovery via entry points is supported; only explicit loading through
  `Application.load_plugin()` is implemented.
- Do not change `src/quickli` or `tests/` for documentation-only work.
- Do not use release notes or the changelog to infer an API contract.

## Validation Matrix

| Change area                | Required validation                                  | Scope                       |
| -------------------------- | ---------------------------------------------------- | --------------------------- |
| Agent guidance or Markdown | Check links, tables, YAML, and line length           | Required                    |
| Public behavior docs       | Compare claims with implementation, tests, and specs | Required                    |
| Python runtime behavior    | Ruff and the unit suite                              | Baseline; no source changes |
| Runnable examples          | Run when behavior is described or changed            | Recommended                 |
| Packaging                  | Build distributions when packaging files change      | Not required                |
| GitHub workflows           | Validate workflow files when workflows change        | Out of scope                |

For each change, inspect the final diff against the approved scope. User acceptance remains
a separate release gate. The official
[stability outline](https://spmse.github.io/quickli/docs/roadmap#stability-and-fix-release-outline)
tracks the documentation audit, configuration fixes, and release validation.

## Agent Scope Checklist

Before editing, identify the relevant specification and confirm that the requested work belongs
to one work package. After editing, report files inspected, assumptions, validations, risks, and
follow-ups.
