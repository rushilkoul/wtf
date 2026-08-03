from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.metrics import confusion_matrix 
from sklearn.metrics import classification_report

import pandas as pd 

train_df = pd.read_csv("train.csv", header=None)
test_df = pd.read_csv("test.csv", header=None)

X_train = train_df.iloc[:, :-1]
y_train = train_df.iloc[:, -1]

X_test = test_df.iloc[:, :-1]
y_test = test_df.iloc[:, -1]

model = RandomForestClassifier(
    n_estimators=300,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=5,
    n_jobs=-1
)

model.fit(X_train, y_train)
predictions = model.predict(X_test)
print(model.classes_)

print(classification_report(y_test, model.predict(X_test)))

print('-'*30)
print(confusion_matrix( y_test, predictions ))
print('-'*30)


import numpy as np

importances = model.feature_importances_
top10 = np.argsort(importances)[-10:][::-1]
for byte_val in top10:
    print(f"byte {byte_val:3d} (0x{byte_val:02x}): {importances[byte_val]:.4f}")


import joblib
joblib.dump(model, "model.joblib")