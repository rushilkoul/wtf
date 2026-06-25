import csv
import math
import random
from collections import Counter
from pathlib import Path

WINDOW_SIZE = 2048
THRESHOLD = 3000

ROWS_PER_CLASS = 1000
TRAIN_RATIO = 0.8
WINDOWS_PER_FILE = 3

random.seed(21)


def histogram(data):
    counts = Counter(data)

    hist = []

    for i in range(256):
        hist.append(counts.get(i, 0))

    return hist


def entropy(data):
    counts = Counter(data)
    length = len(data)

    ent = 0

    for count in counts.values():
        probability = count / length
        ent -= probability * math.log2(probability)

    return ent


def gather_files():
    files_by_label = {}

    for folder in Path("dataset").iterdir():
        if not folder.is_dir():
            continue

        files = []

        for file in folder.iterdir():
            if not file.is_file():
                continue

            if file.stat().st_size < THRESHOLD + WINDOW_SIZE:
                continue

            files.append(file)

        if files:
            random.shuffle(files)
            files_by_label[folder.name] = files

    return files_by_label


def split_files(files_by_label):
    train = {}
    test = {}

    for label, files in files_by_label.items():
        split = max(1, int(len(files) * TRAIN_RATIO))

        if split >= len(files):
            split = len(files) - 1

        train[label] = files[:split]
        test[label] = files[split:]

        print(f"{label}: {len(train[label])} train, {len(test[label])} test")

    return train, test


def generate_dataset(dataset, output_file):
    csvfile = open(output_file, "w", newline="")
    writer = csv.writer(csvfile)

    for label in dataset:
        print(f"\ngenerating {label}...")

        files = dataset[label]

        rows_generated = 0

        samples_per_file = {}
        available_offsets = {}

        for file in files:
            samples_per_file[file] = 0

            size = file.stat().st_size

            offsets = []

            offset = THRESHOLD

            while offset <= size - WINDOW_SIZE:
                offsets.append(offset)
                offset += WINDOW_SIZE

            random.shuffle(offsets)
            available_offsets[file] = offsets

        while rows_generated < ROWS_PER_CLASS:

            random.shuffle(files)

            generated_this_pass = False

            for file in files:

                if rows_generated >= ROWS_PER_CLASS:
                    break

                if samples_per_file[file] >= WINDOWS_PER_FILE:
                    continue

                if len(available_offsets[file]) == 0:
                    continue

                offset = available_offsets[file].pop()

                with open(file, "rb") as f:
                    f.seek(offset)
                    body = f.read(WINDOW_SIZE)

                hist = histogram(body)
                ent = entropy(body)

                row = hist.copy()
                row.append(ent)
                row.append(label)

                writer.writerow(row)

                samples_per_file[file] += 1
                rows_generated += 1
                generated_this_pass = True

            if not generated_this_pass:
                print(f"{label}: no more unique samples available")
                break

        print(f"{label}: wrote {rows_generated} rows")

    csvfile.close()

files_by_label = gather_files()

train_files, test_files = split_files(files_by_label)

print("\ngenerating training dataset...")
generate_dataset(train_files, "train.csv")

print("\ngenerating testing dataset...")
generate_dataset(test_files, "test.csv")

print("\ndone")