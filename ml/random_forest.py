import joblib
import math
import sys
from collections import Counter

WINDOW_SIZE = 2048
THRESHOLD = 3000
NUM_WINDOWS = 5

clf = joblib.load("model.joblib")


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


def file_features(path):

    with open(path, "rb") as f:

        f.seek(0, 2)
        size = f.tell()

        if size < THRESHOLD + WINDOW_SIZE:
            raise ValueError("file is too small")

        first_offset = THRESHOLD
        last_offset = size - WINDOW_SIZE

        offsets = []

        if NUM_WINDOWS == 1:
            offsets.append((first_offset + last_offset) // 2)

        else:
            span = last_offset - first_offset

            for i in range(NUM_WINDOWS):
                offset = first_offset + int(
                    span * i / (NUM_WINDOWS - 1)
                )

                offsets.append(offset)

        histograms = []
        entropies = []

        for offset in offsets:

            f.seek(offset)

            window = f.read(WINDOW_SIZE)

            histograms.append(histogram(window))
            entropies.append(entropy(window))

    average_histogram = []

    for byte in range(256):

        total = 0

        for hist in histograms:
            total += hist[byte]

        average_histogram.append(total / len(histograms))

    average_entropy = sum(entropies) / len(entropies)

    features = average_histogram
    features.append(average_entropy)

    return features


try:
    features = [file_features(sys.argv[1])]

except ValueError as e:
    print(e)
    exit(1)


prediction = clf.predict(features)[0]
probabilities = clf.predict_proba(features)[0]

print(f"prediction: {prediction}")
print()

# for now also show the candidates, debugging :p
sorted_predictions = sorted(zip(clf.classes_, probabilities), key=lambda x: x[1], reverse=True)

for label, probability in sorted_predictions:
    print(f"{label:<10} {probability:.4f}")
