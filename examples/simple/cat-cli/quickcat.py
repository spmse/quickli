from __future__ import annotations

import sys
from pathlib import Path

from quickli import Application, Argument, Option, file_path


app = Application(
    name="quickcat",
    description="A tiny cat-like CLI built with quickli.",
    global_options=[
        Option("verbose", short_name="v", is_flag=True, help_text="Enable verbose output."),
    ],
)


@app.entrypoint(
    help_text="Print one or more text files to stdout.",
    arguments=[
        Argument("path", help_text="Primary file path.", validators=[file_path()]),
    ],
    options=[
        Option("encoding", short_name="e", default="utf-8", help_text="Text encoding."),
        Option("number", short_name="n", help_text="Print line numbers.", is_flag=True),
        Option(
            "include",
            short_name="i",
            multiple=True,
            validators=[file_path()],
            help_text="Additional file paths to print after the primary file.",
        ),
    ],
)
def show(
    path: Path,
    encoding: str = "utf-8",
    number: bool = False,
    include: list[Path] | None = None,
    verbose: bool = False,
) -> str:
    input_paths = [path, *(include or [])]
    rendered_chunks: list[str] = []

    for input_path in input_paths:
        text = input_path.read_text(encoding=encoding)
        lines = text.splitlines()

        if number:
            lines = [f"{index:>4}  {line}" for index, line in enumerate(lines, start=1)]

        if verbose:
            rendered_chunks.append(f"==> {input_path} <==")
        rendered_chunks.append("\n".join(lines))

    return "\n".join(chunk for chunk in rendered_chunks if chunk)


if __name__ == "__main__":
    print(app.run(sys.argv[1:]))
