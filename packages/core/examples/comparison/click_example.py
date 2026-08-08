from pathlib import Path

import click


@click.group()
def toolbox() -> None:
    """A small collection of file utilities."""


@toolbox.command("head")
@click.argument("path")
@click.option("--lines", default=10, type=int)
def head(path: str, lines: int) -> None:
    with open(path, "r", encoding="utf-8") as handle:
        selected = [line.rstrip("\n") for _, line in zip(range(lines), handle)]
    click.echo("\n".join(selected))


@toolbox.command("tail")
@click.argument("path")
@click.option("--lines", default=10, type=int)
def tail(path: str, lines: int) -> None:
    with open(path, "r", encoding="utf-8") as handle:
        entries = handle.readlines()
    selected = entries[-lines:] if len(entries) >= lines else entries
    click.echo("".join(selected).rstrip("\n"))


@toolbox.command("cat")
@click.argument("path")
def cat(path: str) -> None:
    with open(path, "r", encoding="utf-8") as handle:
        click.echo(handle.read().rstrip("\n"))


@toolbox.command("ls")
@click.argument("path", required=False, default=".")
def ls(path: str) -> None:
    entries = sorted(entry.name for entry in Path(path).iterdir())
    click.echo("\n".join(entries))


@toolbox.command("mkdir")
@click.argument("path")
def mkdir(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)
    click.echo(f"created {path}")


@toolbox.command("rm")
@click.argument("path")
def rm(path: str) -> None:
    Path(path).unlink(missing_ok=True)
    click.echo(f"removed {path}")


@toolbox.command("rmdir")
@click.argument("path")
def rmdir(path: str) -> None:
    Path(path).rmdir()
    click.echo(f"removed {path}")


@toolbox.command("cut")
@click.argument("path")
@click.option("--field", default=1, type=int)
@click.option("--delimiter", default=",", show_default=True)
def cut(path: str, field: int, delimiter: str) -> None:
    with open(path, "r", encoding="utf-8") as handle:
        lines = [line.rstrip("\n") for line in handle]
    selected = []
    for line in lines:
        values = line.split(delimiter)
        if 1 <= field <= len(values):
            selected.append(values[field - 1])
    click.echo("\n".join(selected))


if __name__ == "__main__":
    toolbox()
