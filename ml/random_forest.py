import joblib
import math
import sys
from collections import Counter

WINDOW_SIZE = 2048
THRESHOLD = 3000
NUM_WINDOWS = 5

clf = joblib.load("ml/model.joblib")


def histogram(data: bytes):
    counts = Counter(data)
    return [counts.get(i, 0) for i in range(256)]


def entropy(data: bytes):
    counts = Counter(data)
    length = len(data)
    if length == 0:
        return 0.0

    ent = 0.0
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

        all_offsets = []
        offset = THRESHOLD
        while offset <= size - WINDOW_SIZE:
            all_offsets.append(offset)
            offset += WINDOW_SIZE
        if len(all_offsets) <= NUM_WINDOWS:
            chosen_offsets = all_offsets
        else:
            step = (len(all_offsets) - 1) / (NUM_WINDOWS - 1)
            chosen_offsets = [all_offsets[int(round(i * step))] for i in range(NUM_WINDOWS)]

        features = []
        for offset in chosen_offsets:
            f.seek(offset)
            window = f.read(WINDOW_SIZE)

            hist = histogram(window)
            ent = entropy(window)

            features.append(hist + [ent])

    return features

def ml_analyze_file(path):
    try:
        features = file_features(path)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    probabilities = clf.predict_proba(features)

    scores = {label: 0.0 for label in clf.classes_}
    for window_probs in probabilities:
        for label, probability in zip(clf.classes_, window_probs):
            scores[label] += probability

    for label in scores:
        scores[label] /= len(probabilities)

    sorted_scores = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    prediction, confidence = sorted_scores[0]
    print(f"\n  prediction: {prediction} ({confidence * 100:.2f}% confidence)\n")

    print("\033[2m  votes:")

    for i, window_probs in enumerate(probabilities):
            top_idx = window_probs.argmax()
            label = clf.classes_[top_idx]
            conf = window_probs[top_idx]
    
            print(f"   window {i + 1}: {label} ({conf * 100:.2f}%)")

    print("\033[22m")
    


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ml_analyze_file(sys.argv[1])