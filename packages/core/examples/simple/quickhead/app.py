from __future__ import annotations

from pathlib import Path
from sys import argv

from quickli import Application, Argument, Option, file_path, positive_number

app = Application(
    name="quickhead",
    description="A tiny head-like CLI built with quickli.",
)


@app.entrypoint(
    help_text=(
        "Display the first few lines of a file. If no value is given, the first 10 "
        "lines are displayed."
    ),
    arguments=[Argument("file", validators=[file_path()])],
    options=[
        Option(
            "lines",
            short_name="n",
            converter=int,
            validators=[positive_number()],
            help_text="Number of lines to display.",
        ),
        Option(
            "tailmode",
            short_name="t",
            is_flag=True,
            help_text="Display the last few lines instead of the first.",
        ),
    ],
)
def head(file: Path, lines: int = 10, tailmode: bool = False) -> str:
    content = file.read_text(encoding="utf-8").splitlines(keepends=True)
    if tailmode:
        return "".join(content[-lines:])
    return "".join(content[:lines])


if __name__ == "__main__":
    print(app.run(argv[1:]))
