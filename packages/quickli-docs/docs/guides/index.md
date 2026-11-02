---
id: guides-index
title: Implementation Guides
sidebar_position: 1
description: >
  Step-by-step tutorials that walk through the reference examples in the quickli source
  package. Learn how the framework primitives fit together by reading and running real code.
keywords: [quickli, tutorial, guide, cli, python, example]
---

# Implementation Guides

These guides walk through the reference examples that ship with the `quickli` source
package. Each guide explains the code line-by-line so you can follow along, run the
examples yourself, and understand how the framework primitives work together.

## How to use these guides

Every guide is self-contained. You can read them in any order, but the sequence below
builds knowledge progressively from the smallest possible example to a larger multi-command
application.

1. **[Hello World](./01-hello-world.md)** — your first entrypoint, one argument, one flag.
2. **[File viewer (quickcat)](./02-building-cat-cli.md)** — global options, multiple file
   arguments, and the `file_path` validator.
3. **[Directory listing (quickls)](./03-building-ls-cli.md)** — optional arguments,
   multiple options, and the `directory_path` validator.
4. **[Directory creator (quickmkdir)](./04-building-mkdir-cli.md)** — repeatable options
   and combining multiple paths in one call.
5. **[File head (quickhead)](./05-building-head-cli.md)** — numeric conversion with `int`
   and the `positive_number` validator.
6. **[Multi-command CLI (pyk5l)](./06-multi-command-kubectl.md)** — multiple commands,
   global options, and custom validators on a kubectl-like application.
7. **[Configuration](../concepts/config.md#application-initialization-automatic-command-or-explicit-routine)**
   — JSON/YAML structures, custom schemas, initialization, and CLI overrides.
8. **[Logging guide](#logging-guide)** — a production-style application using Python logging.
9. **[Packaging guide](#packaging-guide)** — console scripts, executable binaries, and containers.

## Prerequisites

Install quickli before running any example:

```bash
pip install quickli
```

All examples run on Python 3.12, 3.13, and 3.14.

:::important[Use the matching framework version]
The guides describe the current source APIs. Until a release containing the new
initialization/help features is published, install the checkout with
`python -m pip install -e packages/core` from the repository root.
The dependency range in the packaging example is illustrative: choose a published version
that includes the APIs you use, then verify it in a clean environment.
:::

## Logging guide

quiCkLI does not install logging handlers or choose a logging policy. Use Python's
standard-library `logging` module, leaving the framework's stdout/error contract intact.
This example combines persistent settings, a repeatable verbosity flag, and named commands.

### 1. Define the application

Save this module as `mytool.py` initially. The packaging guide moves it into a package.

```python title="mytool.py" showLineNumbers
import logging
import sys
from pathlib import Path

from quickli import Application, Config, ConfigField, ConfigSchema, Option

logger = logging.getLogger(__name__)


def valid_log_level(value: str) -> str:
    if value not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
        raise ValueError("Use DEBUG, INFO, WARNING, ERROR, or CRITICAL.")
    return value


schema = ConfigSchema(fields=[
    ConfigField(
        "log_level", default="WARNING",
        validators=[valid_log_level], help_text="Default logging threshold.",
    ),
    ConfigField("workspace", default="local"),
])
config = Config(Path.home() / ".mytool" / "settings.yaml", schema=schema)
app = Application(
    "mytool",
    description="Inspect a configured workspace.",
    config=config,
    auto_init_config=True,
    global_options=[
        Option("verbose", short_name="v", is_flag=True, multiple=True),
    ],
)


@app.command(help_text="Inspect the configured workspace.")
def status(verbose: int = 0) -> dict[str, str]:
    data = config.load()
    level = "DEBUG" if verbose >= 2 else "INFO" if verbose else data.get("log_level", "WARNING")
    logging.getLogger().setLevel(level)
    logger.debug("Loaded configuration from %s", config.path)
    logger.info("Inspecting workspace %s", data.get("workspace", "local"))
    return {"workspace": data.get("workspace", "local"), "status": "ready"}


def main(argv: list[str] | None = None, *, output_format: str = "text") -> int:
    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )
    return app.main(argv, output_format=output_format)


if __name__ == "__main__":
    raise SystemExit(main())
```

### 2. Initialize and exercise the logger

1. Run `python mytool.py init` to create `~/.mytool/settings.yaml`.
2. Run `python mytool.py status`. The default threshold suppresses informational logs.
3. Run `python mytool.py status -v` to see informational messages on stderr.
4. Run `python mytool.py status -vv` to include debug messages.
5. Edit `log_level: WARNING` to `log_level: INFO` to change the persistent default.

Global options reach every selected handler. The built-in `init` command accepts them
without using them. Custom handlers must accept `verbose` or `**kwargs`.

:::tip[Keep output usable in pipelines]
Return results from handlers and let `app.main()` write stdout. Keep logs on stderr.
For example, `python mytool.py status -v > result.txt` saves only the result.
For structured output, call `main(["status", "-v"], output_format="json")` from Python:
stdout contains `{"ok": true, "result": {...}}`, while logs remain on stderr.
:::

### 3. Integrate with larger applications

- Create a named logger with `logging.getLogger(__name__)` in each module.
- Configure handlers once at the executable boundary, not during imports or plugin
  registration. An embedding application may already own the logging configuration.
- `basicConfig()` does nothing when root handlers already exist. Do not use `force=True`
  in reusable libraries: it removes the host application's handlers.
- Use lazy formatting, such as `logger.info("Processing %s", path)`, rather than building
  messages eagerly.
- Log diagnostic context, not credentials or entire configuration dictionaries.
- For persistent logs, attach `logging.handlers.RotatingFileHandler` with a size limit,
  backup count, and UTF-8 encoding instead of an unbounded file handler.
- An `error_handler` callback can inspect a `CLIError` and log it. Returning `None` keeps
  normal error rendering and exit codes. Avoid logging and rendering the same message
  twice unless the diagnostic log has a separate audience.

See [Application error handlers](../concepts/application.md#custom-error-handlers) and
the [Python logging cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
for handler composition.

## Packaging guide

Start with a Python package and console script. Build a standalone binary only if users
should not install Python; use a container when the deployment environment already runs
containers. These are application distribution choices, not features of quiCkLI itself.

### 1. Create a package with a console script

Move the logging example into this structure:

```text
mytool/
├── pyproject.toml
└── src/
    └── mytool/
        ├── __init__.py
        ├── __main__.py
        └── cli.py
```

- `cli.py` contains the complete logging example above.
- `__init__.py` can be empty.
- `__main__.py` enables `python -m mytool`:

```python title="src/mytool/__main__.py"
from mytool.cli import main

raise SystemExit(main())
```

Configure packaging and the shell command:

```toml title="pyproject.toml"
[build-system]
requires = ["setuptools>=69"]
build-backend = "setuptools.build_meta"

[project]
name = "mytool"
version = "0.1.0"
description = "Inspect a configured workspace."
requires-python = ">=3.12"
dependencies = ["quickli>=0.6,<0.7"]

[project.scripts]
mytool = "mytool.cli:main"

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
```

The name `mytool` is your application's distribution and import name; `quickli` remains
the framework dependency. Select a dependency range for the release you have tested.
The framework remains alpha; this example range stays within its current minor series.

1. Create and activate a virtual environment using `python -m venv .venv`.
2. Install locally with `python -m pip install -e .`.
3. Run `mytool init`, then `mytool status -v`.
4. Confirm `python -m mytool status` works too.
5. Install the build frontend with `python -m pip install build`.
6. Build a source distribution and wheel with `python -m build`.
7. Install `dist/mytool-0.1.0-py3-none-any.whl` into a clean environment and repeat the checks.

:::important[Entry points return an exit code]
Point `[project.scripts]` at `main`, not `app.run`. Installers create an executable wrapper
that calls the function and propagates its return code. `run()` returns a handler result;
`main()` prints results, handles errors, and returns an integer exit status.
:::

### 2. Build an executable binary

PyInstaller is an optional application build tool, not a required framework dependency.
Build from the activated environment where `mytool` and its dependencies are installed:

```bash
python -m pip install pyinstaller
python -m PyInstaller --clean --onefile --name mytool src/mytool/__main__.py
./dist/mytool init
./dist/mytool status -v
```

On Windows, run `dist\mytool.exe`. A directory bundle (`--onedir` instead of `--onefile`)
is easier to inspect and starts without extracting a one-file bundle.

:::warning[Build for each target]
PyInstaller is not a cross-compiler. Build and test on each target OS and architecture,
and verify the oldest supported Linux runtime when distributing Linux binaries.
Test JSON/YAML configuration, error exits, and any dynamically imported plugins in a
clean environment without your development installation. Review bundled licenses.
:::

Configuration stays under the user's home directory, not inside the executable bundle.
Do not embed writable configuration, credentials, or development files in the binary.

### 3. Containerize the application

Use the same package and console script. A multi-stage build keeps build tools out of the
runtime image, and a non-root user owns the writable configuration directory:

```dockerfile title="Dockerfile"
FROM python:3.12-slim AS builder
WORKDIR /build
COPY pyproject.toml ./
COPY src ./src
RUN python -m pip wheel --wheel-dir /wheels .

FROM python:3.12-slim
RUN useradd --create-home --uid 10001 app
COPY --from=builder /wheels /wheels
RUN python -m pip install --no-cache-dir --no-index --find-links=/wheels mytool \
    && rm -rf /wheels \
    && mkdir -p /home/app/.mytool \
    && chown app:app /home/app/.mytool
ENV HOME=/home/app
USER app
WORKDIR /home/app
ENTRYPOINT ["mytool"]
CMD ["status"]
```

Build and initialize a persistent configuration volume before running `status`:

```bash
docker build -t mytool:local .
docker volume create mytool-config
docker run --rm -v mytool-config:/home/app/.mytool mytool:local init
docker run --rm -v mytool-config:/home/app/.mytool mytool:local status -v
```

- `ENTRYPOINT` uses exec form, so signals and exit codes reach the CLI directly.
- The named volume preserves initialization across otherwise disposable containers.
- A bind mount must be writable by UID 10001; host permissions are not changed automatically.
- Add `.venv`, `dist`, `build`, `.git`, caches, and local secret/config files to
  `.dockerignore`. Never pass secrets through Dockerfile `ARG`, `ENV`, or copied files.
- For releases, pin base image digests and application dependency versions in your
  deployment build process, scan the image, and test the actual target architecture.

### 4. Verify the distributed result

1. Confirm initialization creates the intended schema and never resets an existing file.
2. Check commands, arguments, value options, repeated flags, and invalid input.
3. Verify logs go to stderr and successful results to stdout.
4. Check a successful exit code and a failing exit code outside the development environment.
5. Run on the Python versions and operating systems you promise to support.
