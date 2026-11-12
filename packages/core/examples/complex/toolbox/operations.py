"""File and text operations shared by the toolbox example applications."""

import shutil
from pathlib import Path


def copy_file(source: str, destination: str) -> str:
    copied_to = shutil.copy2(source, destination)
    return f"Copied {source} to {copied_to}"


def make_directory(path: str) -> str:
    Path(path).mkdir(parents=True, exist_ok=True)
    return f"Created directory {path}"


def touch_file(path: str) -> str:
    Path(path).touch(exist_ok=True)
    return f"Touched {path}"


def echo_text(text: str) -> str:
    return text
