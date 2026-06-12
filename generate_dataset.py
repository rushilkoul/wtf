import csv
from pathlib import Path
from collections import Counter

def histogram(data):
    counts = Counter(data)
    return [counts.get(i, 0) for i in range(256)]

WINDOW_SIZE = 1024
HEADER_SKIP = 1024
MIN_SIZE = HEADER_SKIP + WINDOW_SIZE

full_file = open("dataset_full.csv", "w", newline="")
headerless_file = open("dataset_headerless.csv", "w", newline="")

full_writer = csv.writer(full_file)
headerless_writer = csv.writer(headerless_file)

skipped = 0
written = 0

for folder in Path("dataset").iterdir():
    if not folder.is_dir():
        continue
    label = folder.name

    for file in folder.iterdir():
        if not file.is_file():
            continue

        size = file.stat().st_size
        if size < MIN_SIZE:
            skipped += 1
            continue

        with open(file, "rb") as f:
            head = f.read(WINDOW_SIZE)
            f.seek(HEADER_SKIP)
            body = f.read(WINDOW_SIZE)

        full_writer.writerow(histogram(head) + [label])
        headerless_writer.writerow(histogram(body) + [label])
        written += 1

full_file.close()
headerless_file.close()

print(f"wrote {written} rows, skipped {skipped} files (too small)")