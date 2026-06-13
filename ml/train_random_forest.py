from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.metrics import confusion_matrix 
from sklearn.metrics import classification_report

import pandas as pd 

df = pd.read_csv(
    "dataset.csv",
    header=None
)

X = df.iloc[:, :-1]
y = df.iloc[:, -1] 

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=6
)

model = RandomForestClassifier(n_estimators=100, random_state=5)

model.fit(X_train, y_train)
predictions = model.predict(X_test)

# accuracy = accuracy_score(
#     y_test,
#     predictions
# )

# print(
#     f"Accuracy: {accuracy*100:.2f}%"
# )

print(model.classes_)

# print('-'*30)
# print(y.value_counts())

# print(X.shape)
# print(y.shape)



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