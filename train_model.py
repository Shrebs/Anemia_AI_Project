import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix


# ---------------- LOAD DATASET ---------------- #

df = pd.read_csv("anemia.csv")


# ---------------- FEATURES & TARGET ---------------- #

X = df.drop("Result", axis=1)
y = df["Result"]

print("Features:")
print(X.head())

print("\nTarget:")
print(y.head())


# ---------------- TRAIN-TEST SPLIT ---------------- #

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining data shape:", X_train.shape)
print("Testing data shape:", X_test.shape)


# =========================================================
# RANDOM FOREST MODEL
# ========================================================= #

print("\n----- RANDOM FOREST -----")

# Create model
rf_model = RandomForestClassifier(random_state=42)

# Train model
rf_model.fit(X_train, y_train)

# Predictions
rf_y_pred = rf_model.predict(X_test)

# Accuracy
rf_accuracy = accuracy_score(y_test, rf_y_pred)

print("Random Forest Accuracy:", rf_accuracy)

# Confusion Matrix
rf_cm = confusion_matrix(y_test, rf_y_pred)

print("Random Forest Confusion Matrix:")
print(rf_cm)


# =========================================================
# LOGISTIC REGRESSION MODEL
# ========================================================= #

print("\n----- LOGISTIC REGRESSION -----")

# Create model
lr_model = LogisticRegression()

# Train model
lr_model.fit(X_train, y_train)

# Predictions
lr_y_pred = lr_model.predict(X_test)

# Accuracy
lr_accuracy = accuracy_score(y_test, lr_y_pred)

print("Logistic Regression Accuracy:", lr_accuracy)

# Confusion Matrix
lr_cm = confusion_matrix(y_test, lr_y_pred)

print("Logistic Regression Confusion Matrix:")
print(lr_cm)


# =========================================================
# FEATURE IMPORTANCE
# ========================================================= #

importance = rf_model.feature_importances_

features = X.columns

plt.bar(features, importance)

plt.title("Feature Importance")
plt.xlabel("Features")
plt.ylabel("Importance")

plt.show()