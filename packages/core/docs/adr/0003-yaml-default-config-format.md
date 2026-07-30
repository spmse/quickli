# ADR 0003: YAML as Default Configuration Format with Multi-Format Support

## Status

Accepted

## Context

ADR 0002 established TOML as the sole configuration format, using the standard
library `tomllib` module for reading and a minimal built-in writer for output.
That decision kept the module dependency-free but limited flexibility.

Two new requirements drove a reassessment:

1. **YAML as default**: YAML is the dominant configuration format across modern
   developer tooling (Kubernetes, GitHub Actions, Docker Compose, Ansible, and
   many others).  Adopting YAML as the default makes quickli-based CLIs feel
   natural in those ecosystems.

2. **JSON Schema generation**: Application authors need a way to produce a
   `schema.json` from their `ConfigSchema` for editor auto-completion (e.g.
   JSON Schema support in VS Code, IntelliJ), CI validation, and documentation.

Key questions that shaped the decision:

1. Which format should be the default and recommended option?
2. Should the old TOML support be removed or preserved?
3. How should format selection work?
4. Is adding `pyyaml` as a runtime dependency acceptable?
5. How should `generate_schema_json` be structured?

## Decision

### Default format: YAML

YAML becomes the recommended and default configuration format.  The file
extension drives automatic format detection (`.yaml` / `.yml` → YAML,
`.json` → JSON, `.toml` → TOML).  YAML is also the fallback when the file
has no recognised extension.

All documentation, examples, and developer guidance recommend `.yaml` for new
projects.

### Format support: YAML, JSON, TOML (all preserved)

TOML support is kept for backward compatibility and because it remains valid
for users who prefer it.  JSON support is added at no extra cost (stdlib `json`).
No format is removed.

### Format selection: extension inference with explicit override

`Config` infers the format from `path.suffix`.  An optional `format` parameter
allows callers to override inference when the file name does not reflect the
format.

```python
# Automatic (YAML inferred from .yaml)
Config(path="~/.myapp/config.yaml", schema=schema)

# Explicit override
Config(path="~/.myapp/config", schema=schema, format="yaml")
```

### Dependency: `pyyaml>=6.0.1` as a required runtime dependency

YAML cannot be supported from the standard library alone.  `pyyaml` is the
de-facto standard library for YAML in Python and is used by most of the
ecosystem that adopts YAML.

Because YAML is the default format, `pyyaml` is added as a required runtime
dependency rather than an optional extra.  This keeps the installation story
simple: `pip install quickli` provides full YAML support immediately.

### JSON Schema generation: `generate_schema_json`

A new `generate_schema_json(schema, title="", description="")` function converts
a `ConfigSchema` into a JSON Schema (draft 2020-12) dict.  The caller serialises
the result with `json.dumps`.  This keeps the function composable and avoids
coupling it to a specific output path.

## Options Considered

### Default format: YAML

Benefits:

- Universal adoption in modern developer tooling and cloud-native ecosystems.
- Human-readable, supports comments (unlike JSON), and handles complex nested
  structures without the one-level limitation of the built-in TOML writer.
- Natural fit for CLI tools deployed alongside Kubernetes, CI pipelines, and
  container orchestration.

Risks:

- Requires `pyyaml` as a runtime dependency; the module is no longer
  dependency-free.
- YAML's implicit type coercion (e.g. `yes` → `True`, bare integers as strings)
  can surprise beginners.  `yaml.safe_load` mitigates most cases.

### Default format: keep TOML

Benefits:

- No new dependency; the module remains stdlib-only.

Risks:

- TOML is primarily a project-file format (`pyproject.toml`), not a
  universal application configuration format.
- The built-in writer is limited to one level of nesting.

Decision: **YAML as default**.  The ecosystem fit and feature richness outweigh
the dependency cost.  `pyyaml` is a stable, widely-used library with no known
high-severity vulnerabilities at version 6.0.1.

### Dependency: optional extra vs. required

**Option A**: `pyyaml` as an optional extra (e.g. `pip install quickli[yaml]`).

Benefits:

- Keeps the default install footprint minimal.

Risks:

- Users who follow the documentation (which recommends YAML) will encounter an
  `ImportError` unless they add the extra.  This is a confusing experience.
- Conditional import logic increases code complexity.

**Option B**: `pyyaml` as a required dependency.

Benefits:

- Simple installation: `pip install quickli` works out of the box.
- No conditional import branches or confusing errors.

Decision: **Option B**.  YAML is the default; requiring `pyyaml` is the
correct expression of that choice.

### JSON Schema format: draft 2020-12 vs. draft-07

Draft 2020-12 is the current stable specification and is supported by all
major validators and editors.  Draft-07 is the previous long-lived version
with broad legacy support.

Decision: **draft 2020-12**.  The output is simple enough (object with
properties and required) that both drafts produce identical documents for
the supported field types.  Using the newer draft future-proofs the output.

## Consequences

Positive consequences:

- Applications can now use YAML as the default configuration format, matching
  modern developer expectations.
- JSON and TOML remain available; existing code using `.toml` paths continues
  to work unchanged.
- `generate_schema_json` enables editor auto-completion and CI schema validation
  with a single function call.
- Format inference is transparent: callers choose a format by choosing a file
  extension.

Tradeoffs:

- `pyyaml` is now a runtime dependency.  This is a deliberate trade-off for
  first-class YAML support.
- YAML's implicit type coercion edge cases require `yaml.safe_load`; this is
  used throughout.
- The TOML writer's one-level nesting limitation remains.  Users who need deeply
  nested TOML should switch to YAML or JSON.

Follow-up:

- A future release could add support for layered configuration
  (file + environment variables + CLI options).
- XDG base directory and platform-specific config paths could be offered as
  optional helpers.
- A TOML writer with unlimited nesting could replace the current built-in one.
