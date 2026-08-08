from pathlib import Path

try:
    from quickli import Application
except ImportError:  # pragma: no cover - example docs fallback
    Application = object

app = Application(name="toolbox")


@app.command(help_text="Print the first lines of a file.")
def head(path: str, lines: int = 10) -> str:
    with open(path, "r", encoding="utf-8") as handle:
        selected = [line.rstrip("\n") for _, line in zip(range(lines), handle)]
    return "\n".join(selected)


@app.command(help_text="Print the last lines of a file.")
def tail(path: str, lines: int = 10) -> str:
    with open(path, "r", encoding="utf-8") as handle:
        entries = handle.readlines()
    selected = entries[-lines:] if len(entries) >= lines else entries
    return "".join(selected).rstrip("\n")


@app.command(help_text="Print the contents of a file.")
def cat(path: str) -> str:
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read().rstrip("\n")


@app.command(help_text="List the contents of a directory.")
def ls(path: str = ".") -> str:
    entries = sorted(entry.name for entry in Path(path).iterdir())
    return "\n".join(entries)


@app.command(help_text="Create a directory.")
def mkdir(path: str) -> str:
    Path(path).mkdir(parents=True, exist_ok=True)
    return f"created {path}"


@app.command(help_text="Remove a file.")
def rm(path: str) -> str:
    Path(path).unlink(missing_ok=True)
    return f"removed {path}"


@app.command(help_text="Remove an empty directory.")
def rmdir(path: str) -> str:
    Path(path).rmdir()
    return f"removed {path}"


@app.command(help_text="Select columns from a delimited file.")
def cut(path: str, field: int = 1, delimiter: str = ",") -> str:
    with open(path, "r", encoding="utf-8") as handle:
        lines = [line.rstrip("\n") for line in handle]
    selected = []
    for line in lines:
        values = line.split(delimiter)
        if 1 <= field <= len(values):
            selected.append(values[field - 1])
    return "\n".join(selected)


if __name__ == "__main__":
    print(app.run())
