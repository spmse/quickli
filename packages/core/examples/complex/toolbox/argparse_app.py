"""A four-command toolbox application built with argparse."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from operations import copy_file, echo_text, make_directory, touch_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="toolbox", description="File and text utilities.")
    commands = parser.add_subparsers(dest="command", required=True)

    cp_parser = commands.add_parser("cp", help="Copy a file.")
    cp_parser.add_argument("source")
    cp_parser.add_argument("destination")
    cp_parser.set_defaults(run=lambda args: print(copy_file(args.source, args.destination)))

    mkdir_parser = commands.add_parser("mkdir", help="Create a directory.")
    mkdir_parser.add_argument("path")
    mkdir_parser.set_defaults(run=lambda args: print(make_directory(args.path)))

    touch_parser = commands.add_parser("touch", help="Create a file or update its timestamp.")
    touch_parser.add_argument("path")
    touch_parser.set_defaults(run=lambda args: print(touch_file(args.path)))

    echo_parser = commands.add_parser("echo", help="Write text.")
    echo_parser.add_argument("text")
    echo_parser.set_defaults(run=lambda args: print(echo_text(args.text)))

    return parser


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.run(args)


if __name__ == "__main__":
    main()
