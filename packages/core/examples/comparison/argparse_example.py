import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    head_parser = subparsers.add_parser("head")
    head_parser.add_argument("path")
    head_parser.add_argument("--lines", type=int, default=10)

    tail_parser = subparsers.add_parser("tail")
    tail_parser.add_argument("path")
    tail_parser.add_argument("--lines", type=int, default=10)

    cat_parser = subparsers.add_parser("cat")
    cat_parser.add_argument("path")

    ls_parser = subparsers.add_parser("ls")
    ls_parser.add_argument("path", nargs="?", default=".")

    mkdir_parser = subparsers.add_parser("mkdir")
    mkdir_parser.add_argument("path")

    rm_parser = subparsers.add_parser("rm")
    rm_parser.add_argument("path")

    rmdir_parser = subparsers.add_parser("rmdir")
    rmdir_parser.add_argument("path")

    cut_parser = subparsers.add_parser("cut")
    cut_parser.add_argument("path")
    cut_parser.add_argument("--field", type=int, default=1)
    cut_parser.add_argument("--delimiter", default=",")
    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "head":
        with open(args.path, "r", encoding="utf-8") as handle:
            selected = [
                line.rstrip("\n") for _, line in zip(range(args.lines), handle)
            ]
        print("\n".join(selected))
    elif args.command == "tail":
        with open(args.path, "r", encoding="utf-8") as handle:
            entries = handle.readlines()
        selected = (
            entries[-args.lines:] if len(entries) >= args.lines else entries
        )
        print("".join(selected).rstrip("\n"))
    elif args.command == "cat":
        with open(args.path, "r", encoding="utf-8") as handle:
            print(handle.read().rstrip("\n"))
    elif args.command == "ls":
        entries = sorted(entry.name for entry in Path(args.path).iterdir())
        print("\n".join(entries))
    elif args.command == "mkdir":
        Path(args.path).mkdir(parents=True, exist_ok=True)
        print(f"created {args.path}")
    elif args.command == "rm":
        Path(args.path).unlink(missing_ok=True)
        print(f"removed {args.path}")
    elif args.command == "rmdir":
        Path(args.path).rmdir()
        print(f"removed {args.path}")
    elif args.command == "cut":
        with open(args.path, "r", encoding="utf-8") as handle:
            lines = [line.rstrip("\n") for line in handle]
        selected = []
        for line in lines:
            values = line.split(args.delimiter)
            if 1 <= args.field <= len(values):
                selected.append(values[args.field - 1])
        print("\n".join(selected))
