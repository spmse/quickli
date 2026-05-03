from __future__ import annotations

import sys
from pathlib import Path

from quickli import Application, Argument, Option, directory_path


app = Application(
    name="quickmkdir",
    description="A tiny mkdir-like CLI built with quickli.",
    global_options=[
        Option("verbose", short_name="v", is_flag=True, help_text="Print created directories."),
    ],
)


@app.entrypoint(
    help_text="Create one or more directories.",
    arguments=[Argument("path", validators=[directory_path(exists=None)])],
    options=[
        Option(
            "extra",
            short_name="e",
            multiple=True,
            validators=[directory_path(exists=None)],
            help_text="Create additional directories in the same call.",
        ),
        Option("parents", short_name="p", is_flag=True, help_text="Create parent directories."),
        Option("exist-ok", is_flag=True, help_text="Ignore existing directories."),
    ],
)
def create(
    path: Path,
    extra: list[Path] | None = None,
    parents: bool = False,
    exist_ok: bool = False,
    verbose: bool = False,
) -> str:
    paths = [path, *(extra or [])]
    for item in paths:
        item.mkdir(parents=parents, exist_ok=exist_ok)

    if not verbose:
        return "created"

    return "\n".join(f"created: {item}" for item in paths)


if __name__ == "__main__":
    print(app.run(sys.argv[1:]))
