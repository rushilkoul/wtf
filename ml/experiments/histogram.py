import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("dataset.csv", header=None)

labels = df.iloc[:, -1].unique()

fig, axes = plt.subplots(len(labels), 1, figsize=(10, 2 * len(labels)), sharex=True)

for ax, label in zip(axes, labels):
    subset = df[df.iloc[:, -1] == label].iloc[:, :256]
    avg_hist = subset.mean(axis=0)
    ax.bar(range(256), avg_hist, width=1)
    ax.set_title(label)
    ax.set_ylabel("avg count")

axes[-1].set_xlabel("byte value")
plt.tight_layout()
plt.savefig("hist.png", dpi=150)
plt.show()