import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier

# 1. Adversarial Attacks
# Let's create a simple binary classification model and show how adversarial attacks can fool it.

# Generate synthetic data
X, y = make_moons(n_samples=1000, noise=0.3, random_state=42)

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train a logistic regression model
clf = LogisticRegression()
clf.fit(X_train, y_train)

# Evaluate the model
y_pred = clf.predict(X_test)
initial_accuracy = accuracy_score(y_test, y_pred)
print(f"Initial Model Accuracy: {initial_accuracy * 100:.2f}%")

# Adversarial example creation (FGSM)
def fgsm_attack(model, X, epsilon):
    # Calculate gradients
    grad = np.zeros_like(X)
    for i in range(len(X)):
        grad[i] = np.sign(X[i])
    # Apply perturbation
    X_adv = X + epsilon * grad
    return X_adv

epsilon = 0.1
X_test_adv = fgsm_attack(clf, X_test, epsilon)

# Evaluate the model on adversarial examples
y_pred_adv = clf.predict(X_test_adv)
adversarial_accuracy = accuracy_score(y_test, y_pred_adv)
print(f"Model Accuracy on Adversarial Examples: {adversarial_accuracy * 100:.2f}%")

# Plot original vs adversarial examples
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title("Original Test Data")
plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test)
plt.subplot(1, 2, 2)
plt.title("Adversarial Test Data")
plt.scatter(X_test_adv[:, 0], X_test_adv[:, 1], c=y_test)
plt.show()

# 2. Data Poisoning
# Injecting malicious data into the training set to corrupt the model.

# Add poison data points
X_poison = np.random.normal(loc=3, scale=0.1, size=(50, 2))
y_poison = np.ones(50)  # Assuming the target class is 1
X_train_poisoned = np.vstack((X_train, X_poison))
y_train_poisoned = np.hstack((y_train, y_poison))

# Train a new model on poisoned data
clf_poisoned = LogisticRegression()
clf_poisoned.fit(X_train_poisoned, y_train_poisoned)

# Evaluate the poisoned model
y_pred_poisoned = clf_poisoned.predict(X_test)
poisoned_accuracy = accuracy_score(y_test, y_pred_poisoned)
print(f"Model Accuracy with Poisoned Data: {poisoned_accuracy * 100:.2f}%")

# 3. Model Theft
# Simulating model stealing by training a surrogate model on the outputs of the target model.

# Assume attacker queries the target model and gets responses
X_attack = np.random.uniform(low=-3, high=3, size=(500, 2))
y_attack = clf.predict(X_attack)

# Attacker trains a surrogate model
surrogate_model = KNeighborsClassifier(n_neighbors=3)
surrogate_model.fit(X_attack, y_attack)

# Evaluate surrogate model
y_surrogate_pred = surrogate_model.predict(X_test)
surrogate_accuracy = accuracy_score(y_test, y_surrogate_pred)
print(f"Surrogate Model Accuracy: {surrogate_accuracy * 100:.2f}%")

# 4. Privacy Concerns
# Differential privacy to protect sensitive training data.

from diffprivlib.models import LogisticRegression as DPLogisticRegression

# Train a differentially private model
dp_clf = DPLogisticRegression(epsilon=1.0)
dp_clf.fit(X_train, y_train)

# Evaluate the differentially private model
y_dp_pred = dp_clf.predict(X_test)
dp_accuracy = accuracy_score(y_test, y_dp_pred)
print(f"Differentially Private Model Accuracy: {dp_accuracy * 100:.2f}%")
