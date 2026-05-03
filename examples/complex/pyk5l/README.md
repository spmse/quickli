# Build `pyk5l`, a minimal kubectl-like CLI with quickli

This example shows how a larger `quickli` application can stay compact while still using
multiple commands, global options, local options, conversion, and validation.

Files in this example:

- `app.py`: runnable example application
- `manifests/web-pod.yaml`: sample manifest for the `apply` command
- `README.md`: guide and command overview

## Goal

The example demonstrates:

- a multi-command application through `@app.command(...)`
- a kubectl-like verb-resource command shape such as `get pods`
- shared global options such as `--context`, `--namespace`, and `--output`
- local command options for filtering, formatting, and log tail length
- built-in file validation for a simulated `apply` workflow
- reusable helper functions for rendering and resource lookup

## Command shape

The example now follows the familiar kubectl style as closely as the current `quickli`
command model allows.

- `get pods`
- `get services`
- `describe pod NAME`
- `logs POD`
- `apply MANIFEST`

The `get` and `describe` verbs are regular `quickli` commands. The resource kind is modeled
as a positional argument, which preserves the kubectl-like invocation pattern without adding
nested command support to the framework itself.

## Run the example

From the repository root:

```bash
PYTHONPATH=src python examples/complex/pyk5l/app.py get pods
PYTHONPATH=src python examples/complex/pyk5l/app.py --namespace ops get pods --output json
PYTHONPATH=src python examples/complex/pyk5l/app.py get services --service-type NodePort --verbose
PYTHONPATH=src python examples/complex/pyk5l/app.py describe pod api-7d4f5f6b89-l2xq9
PYTHONPATH=src python examples/complex/pyk5l/app.py logs web-6b5dd6cb6f-ptm8k --tail 2 --timestamps
PYTHONPATH=src python examples/complex/pyk5l/app.py apply examples/complex/pyk5l/manifests/web-pod.yaml --dry-run
```

## Included commands

- `get pods`: lists pods with optional label and status filters
- `get services`: lists services with an optional selector or service type filter
- `describe pod NAME`: prints pod details for one resource
- `logs NAME`: shows recent log lines with optional timestamps and tail length
- `apply MANIFEST`: previews a manifest file and simulates an apply step

## Resource mapping

- `Application` owns the command registry and the global options.
- `Argument("resource", validators=[...])` lets one command handle multiple kubectl-like resource kinds.
- `Argument("manifest", validators=[file_path()])` validates the manifest path for `apply`.
- `Option("tail", converter=int, validators=[positive_number()])` validates the log length.
- Local options on `get` model resource filters for both pods and services.
- Shared helper functions keep rendering and lookup logic outside the command handlers.

## Notes

- The example uses static in-memory cluster data. It does not talk to a real Kubernetes API.
- `--output` supports `table`, `json`, and `wide` for list-oriented commands.
- `--verbose` prepends the active context and namespace to the output.
- The example is intentionally minimal and focuses on CLI structure rather than cluster logic.
