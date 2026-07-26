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
runtime: library-level
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
  - docstring_help_fallback
not_implemented:
  - standard_executable_runtime
  - nested_subcommands
  - shell_completion
  - configuration_files
  - plugin_loading
  - core_json_or_yaml_rendering
  - combined_short_flags
release_process: tag-driven
release_please: approved_but_not_implemented
```

`Application.run(tokens)` accepts explicit tokens and returns a handler result or help text.
It does not read `sys.argv`, print results, render process-level errors, or choose exit codes.
The caller owns those executable-program responsibilities.

The `pyk5l` example has example-specific table, JSON, and wide renderers. Those renderers do
not add JSON or YAML output support to the core framework.

## Parsing Behavior Matrix

| Input or operation | Current behavior | Evidence |
| --- | --- | --- |
| Input or operation | Current behavior | Evidence |
| --- | --- | --- |
| `run([])` without entrypoint | Returns generated application help | application, tests |
| `run([])` with entrypoint | Invokes entrypoint with defaults | application, tests |
| Named command token | Dispatches to matching command | application, tests |
| Unknown command without entrypoint | Raises `CommandNotFoundError` | application |
| Unknown token with entrypoint | Passes token to entrypoint | implementation, tests |
| Global option around command | Parses as global option | application, command specs |
| Local option | Parses after command selection | command spec |
| `--long value`, `--long=value`, `-s value` | Supports these forms | option spec |
| `--` | Remaining tokens are positional | command |
| Repeated non-flag option | Accumulates converted values in a list | option spec |
| Repeated flag | Accumulates occurrences as an integer | option spec |
| Converter | Runs before validators and handler | validation guide |
| Validator | Runs after conversion and before handler | validation guide |
| Handler exception | Propagates; no process policy | command, runtime boundary |

The approved future behavior for an unknown command is to fail with the command and root help
when both named commands and an entrypoint exist. That behavior is implementation-deferred and
must not be described as current behavior until a separate runtime branch changes the code and
tests.

## Exception Matrix

| Exception | Raised for | Owner |
| --- | --- | --- |
| Exception | Raised for | Owner |
| --- | --- | --- |
| `CLIError` | Base class for framework errors | exceptions |
| `CommandRegistrationError` | Invalid or duplicate registration | registration |
| `CommandNotFoundError` | Unknown command without entrypoint | application dispatch |
| `CommandExecutionError` | Parsing, conversion, validation, or binding failures | command |
| Any handler exception | Failure in application handler code | caller; not wrapped |

Framework exceptions are library errors. The current library does not decide whether to print
them, convert them to a process status, or show a traceback. A future executable runtime must
define that contract separately.

## Do Not Assume

- Do not assume `Application.run()` reads `sys.argv` or behaves like a complete executable.
- Do not assume a returned string is printed; the caller must print or otherwise use it.
- Do not assume unknown commands already follow the approved future failure behavior.
- Do not assume `pyk5l` renderers are core JSON or YAML support.
- Do not assume plugin classes, discovery, or registration APIs exist because `specs/plugin.md`
  describes a planned direction.
- Do not assume nested subcommands, shell completion, configuration files, or combined short
  flags are supported.
- Do not change `src/quickli` or `tests/` for documentation-only work.
- Do not use release notes or the changelog to infer an API contract.

## Validation Matrix

| Change area | Required validation | Scope |
| --- | --- | --- |
| Change area | Required validation | Scope |
| --- | --- | --- |
| Agent guidance or Markdown | Check links, tables, YAML, and line length | Required |
| Public behavior docs | Compare claims with implementation, tests, and specs | Required |
| Python runtime behavior | Ruff and the unit suite | Baseline; no source changes |
| Runnable examples | Run when behavior is described or changed | Recommended |
| Packaging | Build distributions when packaging files change | Not required |
| GitHub workflows | Validate workflow files when workflows change | Out of scope |

For this work, inspect the final diff and verify that only documentation or repository guidance
changed. Do not commit the changes; user acceptance remains a separate step.

## Agent Scope Checklist

Before editing, identify the relevant specification and confirm that the requested work belongs
to one work package. After editing, report files inspected, assumptions, validations, risks, and
follow-ups.
