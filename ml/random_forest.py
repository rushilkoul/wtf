import joblib
from collections import Counter
import sys
import math 

clf = joblib.load("model.joblib")

def histogram(data):
    counts = Counter(data)
    return [counts.get(i, 0) for i in range(256)]

def entropy(data):
    counts = Counter(data)
    length = len(data)
    return -sum((c / length) * math.log2(c / length) for c in counts.values())

with open(sys.argv[1], "rb") as f:
    f.seek(1024)
    window = f.read(1024)

features =  [histogram(window) + [entropy(window)]]
# features.append([entropy(window)])
# print(features)

prediction = clf.predict(features)
probabilities = clf.predict_proba(features)

print(prediction)
print(dict(zip(clf.classes_, probabilities[0])))



