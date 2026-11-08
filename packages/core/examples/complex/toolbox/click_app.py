"""A four-command toolbox application built with Click."""

import click

from operations import copy_file, echo_text, make_directory, touch_file


@click.group()
def toolbox():
    """File and text utilities."""


@toolbox.command()
@click.argument("source")
@click.argument("destination")
def cp(source: str, destination: str) -> None:
    click.echo(copy_file(source, destination))


@toolbox.command()
@click.argument("path")
def mkdir(path: str) -> None:
    click.echo(make_directory(path))


@toolbox.command()
@click.argument("path")
def touch(path: str) -> None:
    click.echo(touch_file(path))


@toolbox.command()
@click.argument("text")
def echo(text: str) -> None:
    click.echo(echo_text(text))


if __name__ == "__main__":
    toolbox()
