"""
AI wrote this. it works for what it needs to do.

generates dummy plaintext files with randomized extensions. 
helped pad the existing dataset
"""

import random
import string
from pathlib import Path

OUTPUT_DIR = Path("dataset/plaintxt")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

NUM_FILES = 1000

MIN_SIZE = 5000
MAX_SIZE = 50000

WORDS = """
the quick brown fox jumps over the lazy dog
computer science machine learning artificial intelligence python
random forest byte histogram entropy feature vector
linux kernel terminal command shell dataset classifier
network socket memory pointer compiler interpreter parser
apple banana orange database filesystem compiler virtual machine
security encryption password authentication binary hexadecimal decimal
""".split()

CODE_LINES = [
    "for i in range(10):",
    "print(value)",
    "return result",
    "if x > y:",
    "while True:",
    "break",
    "continue",
    "const app = express();",
    "let value = Math.random();",
    "function hello() {",
    "console.log(data);",
    "#include <stdio.h>",
    "int main() {",
    "return 0;",
    "}",
    "class FileDetector:",
    "import os",
    "from pathlib import Path",
]

LOG_LEVELS = [
    "INFO",
    "WARN",
    "ERROR",
    "DEBUG",
    "TRACE",
]

EXTENSIONS = [
    ".txt",
    ".log",
    ".cfg",
    ".ini",
    ".csv",
    ".json",
    ".xml",
    ".yaml",
    ".yml",
    ".md",
    ".c",
    ".py",
    ".js",
    ".css",
    ".html",
    ".sh",
]


def word():
    return random.choice(WORDS)


def paragraph():
    out = []

    for _ in range(random.randint(5, 20)):
        sentence = []

        for _ in range(random.randint(8, 20)):
            sentence.append(word())

        out.append(" ".join(sentence).capitalize() + ".")

    return "\n".join(out)


def code():
    lines = []

    for _ in range(random.randint(40, 200)):
        lines.append(random.choice(CODE_LINES))

    return "\n".join(lines)


def logs():
    lines = []

    for i in range(random.randint(100, 400)):
        lines.append(
            f"[{random.choice(LOG_LEVELS)}] "
            f"id={i} "
            f"pid={random.randint(1000,9999)} "
            f"value={random.randint(0,100000)}"
        )

    return "\n".join(lines)


def csv_table():
    rows = ["id,name,score"]

    for i in range(random.randint(100, 500)):
        rows.append(f"{i},user{i},{random.randint(0,100)}")

    return "\n".join(rows)


def json_blob():
    lines = ["{"]

    for i in range(random.randint(30, 100)):
        comma = "," if i else ""
        lines.append(
            f'  "key{i}": "{word()}"{comma}'
        )

    lines.append("}")

    return "\n".join(lines)


def markdown():
    out = ["# Example Document"]

    for i in range(random.randint(10, 40)):
        out.append(f"## Section {i}")
        out.append(paragraph())

    return "\n".join(out)


def xml():
    out = ["<root>"]

    for i in range(random.randint(50, 150)):
        out.append(f"  <item id=\"{i}\">{word()}</item>")

    out.append("</root>")

    return "\n".join(out)


def ini():
    out = []

    for i in range(random.randint(20, 60)):
        out.append(f"[section{i}]")

        for j in range(random.randint(3, 8)):
            out.append(f"key{j}={word()}")

        out.append("")

    return "\n".join(out)


def yaml():
    out = []

    for i in range(random.randint(50, 200)):
        out.append(f"{word()}: {word()}")

    return "\n".join(out)


def shell():
    out = [
        "#!/bin/bash",
        ""
    ]

    for _ in range(random.randint(40, 150)):
        out.append(random.choice([
            "echo hello",
            "cd /tmp",
            "ls -la",
            "mkdir build",
            "rm -rf output",
            "grep foo file.txt",
            "cat data.log",
            "sleep 1"
        ]))

    return "\n".join(out)


def random_identifiers():
    out = []

    for _ in range(random.randint(500, 2000)):
        out.append(
            "".join(
                random.choices(
                    string.ascii_letters + string.digits + "_",
                    k=random.randint(5, 40)
                )
            )
        )

    return "\n".join(out)


GENERATORS = [
    paragraph,
    code,
    logs,
    csv_table,
    json_blob,
    markdown,
    xml,
    ini,
    yaml,
    shell,
    random_identifiers,
]


ENCODINGS = [
    "utf-8",
    "utf-16-le",
    "utf-16-be",
    "latin-1",
    "ascii",
]


for i in range(NUM_FILES):

    pieces = []

    target_size = random.randint(MIN_SIZE, MAX_SIZE)

    while True:
        pieces.append(random.choice(GENERATORS)())

        text = "\n\n".join(pieces)

        if len(text.encode("utf-8")) >= target_size:
            break

    encoding = random.choice(ENCODINGS)

    if encoding == "ascii":
        text = text.encode("ascii", errors="ignore").decode("ascii")

    elif encoding == "latin-1":
        text = text.encode("latin-1", errors="ignore").decode("latin-1")

    extension = random.choice(EXTENSIONS)

    filename = OUTPUT_DIR / f"{i:05}{extension}"

    with open(filename, "w", encoding=encoding) as f:
        f.write(text)

print(f"Generated {NUM_FILES} plaintext files.")
