import csv
from pathlib import Path
from collections import Counter
import random

def histogram(data):
    counts = Counter(data)
    return [counts.get(i, 0) for i in range(256)]


WINDOW_SIZE = 1024

csvfile = open("dataset.csv", "w", newline="")

writer = csv.writer(csvfile)

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

        RANDOM_SKIP = random.randint(WINDOW_SIZE, 2532)
        MIN_SIZE = RANDOM_SKIP + WINDOW_SIZE

        if size < MIN_SIZE:
            skipped += 1
            continue

        with open(file, "rb") as f:
            f.seek(RANDOM_SKIP)
            body = f.read(WINDOW_SIZE)

        writer.writerow(histogram(body) + [label])
        written += 1

csvfile.close()

print(f"wrote {written} rows, skipped {skipped} files (too small)")