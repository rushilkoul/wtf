#!/usr/bin/env python3

import random
import string
import sys
from pathlib import Path

"""
fun lil script for testing out wtf.
give it a directory, it scrambles all the extensions to whatever 
run wtf in a directory where all extensions are random :o
"""

def random_extension():
    return "." + "".join(
        random.choices(string.ascii_lowercase, k=3)
    )


def scramble_directory(directory: Path):
    for file in directory.rglob("*"):
        if not file.is_file():
            continue
        if not file.suffix:
            continue

        new_name = file.with_suffix(random_extension())

        while new_name.exists():
            new_name = file.with_suffix(random_extension())

        file.rename(new_name)

        print(f"{file.name} -> {new_name.name}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python scrambler.py <directory>")
        sys.exit(1)

    # i should probably use pathlib in the main script too huh
    directory = Path(sys.argv[1])

    if not directory.is_dir():
        print("Not a valid directory.")
        sys.exit(1)

    scramble_directory(directory)