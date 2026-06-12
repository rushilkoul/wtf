from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.metrics import confusion_matrix 
from sklearn.metrics import classification_report

import pandas as pd 

df = pd.read_csv(
    "dataset_headerless.csv",
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

# print(model.classes_)

# print('-'*30)
# print(y.value_counts())

# print(X.shape)
# print(y.shape)



print(classification_report(y_test, model.predict(X_test)))

print('-'*30)
print(confusion_matrix( y_test, predictions ))