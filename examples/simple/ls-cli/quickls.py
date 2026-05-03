from __future__ import annotations

import sys
from pathlib import Path

from quickli import Application, Argument, Option, directory_path


app = Application(
    name="quickls",
    description="A tiny ls-like CLI built with quickli.",
    global_options=[
        Option("verbose", short_name="v", is_flag=True, help_text="Show the scanned directory."),
    ],
)


@app.entrypoint(
    help_text="List files in a directory.",
    arguments=[
        Argument(
            "path",
            required=False,
            default=Path("."),
            validators=[directory_path()],
        )
    ],
    options=[
        Option("all", short_name="a", is_flag=True, help_text="Include hidden files."),
        Option(
            "suffix",
            short_name="s",
            multiple=True,
            help_text="Filter by one or more suffixes.",
        ),
    ],
)
def list_directory(
    path: Path = Path("."),
    all: bool = False,
    suffix: list[str] | None = None,
    verbose: bool = False,
) -> str:
    items = sorted(path.iterdir(), key=lambda item: item.name)
    if not all:
        items = [item for item in items if not item.name.startswith(".")]
    if suffix:
        items = [item for item in items if any(item.name.endswith(value) for value in suffix)]

    lines: list[str] = []
    if verbose:
        lines.append(f"Listing: {path}")
    lines.extend(item.name for item in items)
    return "\n".join(lines)


if __name__ == "__main__":
    print(app.run(sys.argv[1:]))
