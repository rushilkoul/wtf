import csv
from pathlib import Path
from collections import Counter
import random
import math

def histogram(data):
    counts = Counter(data)
    return [counts.get(i, 0) for i in range(256)]

def entropy(data):
    counts = Counter(data)
    length = len(data)
    return -sum((c / length) * math.log2(c / length) for c in counts.values())

WINDOW_SIZE = 2048
ROWS_PER_CLASS = 1000

csvfile = open("dataset.csv", "w", newline="")

writer = csv.writer(csvfile)

skipped = 0
written = 0

for folder in Path("dataset").iterdir():
    if not folder.is_dir():
        continue
    label = folder.name

    files = [f for f in folder.iterdir() if f.is_file()]
    if not files: 
        continue

    rows_generated = 0

    while rows_generated < ROWS_PER_CLASS:
        random.shuffle(files)

        for file in files:
            if rows_generated >= ROWS_PER_CLASS:
                break
            
            size = file.stat().st_size

            THRESHOLD = 3000

            if size < (THRESHOLD + WINDOW_SIZE):
                skipped += 1
                continue

            with open(file, "rb") as f:
                max_chunks = (size - THRESHOLD) // WINDOW_SIZE
                chunks = min(max_chunks, 20);

                for _ in range(chunks):
                    RANDOM_SKIP = random.randint(THRESHOLD, size - WINDOW_SIZE)                    
                    f.seek(RANDOM_SKIP)
                    body = f.read(WINDOW_SIZE)

                    writer.writerow(histogram(body) + [entropy(body), label])
                    rows_generated += 1

                    if rows_generated >= ROWS_PER_CLASS:
                        break

    print(f"{label}: wrote {rows_generated} rows")
csvfile.close()
