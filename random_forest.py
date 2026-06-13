import joblib
from collections import Counter
import sys

clf = joblib.load("model.joblib")

def histogram(data):
    counts = Counter(data)
    return [counts.get(i, 0) for i in range(256)]

with open(sys.argv[1], "rb") as f:
    f.seek(1024)
    window = f.read(1024)

features = [histogram(window)]
prediction = clf.predict(features)
probabilities = clf.predict_proba(features)

print(prediction)
print(dict(zip(clf.classes_, probabilities[0])))