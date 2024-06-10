from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Train the model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=newsgroups.target_names))
