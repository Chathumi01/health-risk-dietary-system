import pandas as pd
import numpy as np
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report



# 1. LOAD DATASET
df = pd.read_excel("data/survey_cleaned.xlsx")
df.columns = df.columns.str.strip()
print(df.columns.tolist())

# Calculate BMI from height(cm) and weight(kg)
df["BMI"] = df["weight"] / ((df["height"] / 100) ** 2)

# Create BMI classes
df["bmi_score"] = df["BMI"].apply(
    lambda x: 2 if x >= 30 else 1 if x >= 25 else 0
)


# 2. ADD SNP (SIMULATED)

df['mthfr'] = np.random.randint(0, 3, size=len(df))
df['fto'] = np.random.randint(0, 2, size=len(df))
df['apoe'] = np.random.randint(0, 2, size=len(df))


# 3. CREATE DISEASE LABELS

df["Medical_Condition"] = df["Medical_Conditions"].astype(str)

df["diabetes"] = df["Medical_Conditions"].apply(
    lambda x: 1 if "Diabetes" in str(x) else 0
)

df["cholesterol"] = df["Medical_Conditions"].apply(
    lambda x: 1 if "Cholesterol" in str(x) else 0
)

df["bp"] = df["Medical_Conditions"].apply(
    lambda x: 1 if "High Blood" in str(x) else 0
)

df["thyroid"] = df["Medical_Conditions"].apply(
    lambda x: 1 if "Thyroid" in str(x) else 0
)


# 4. ADD ADDICTION LABEL

def map_addiction(x):
    x = str(x).lower()

    if "both" in x:
        return 2
    elif "alcohol" in x or "tobacco" in x:
        return 1
    else:
        return 0

df["addiction"] = df["Tobacco_Alcohol_Use"].apply(map_addiction)


# 5. TARGET VARIABLE

target_col = "bmi_score"
df = df.dropna(subset=[target_col])

X = df.drop(columns=[target_col])
y = df[target_col]

print("TRAINING COLUMNS:")
print(X.columns.tolist())

joblib.dump(X.columns.tolist(), "model/training_columns.pkl")


# 6. ENCODE CATEGORICAL DATA

for col in X.select_dtypes(include=["object"]).columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))


# 7. TRAIN / TEST SPLIT

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)


# 8. TRAIN MODEL 

model = RandomForestClassifier(
    n_estimators=50,
    max_depth=2,          
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42
)

model.fit(X_train, y_train)


# 9. EVALUATION

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("\nTest Accuracy:", accuracy)


# 10. CROSS VALIDATION

cv_scores = cross_val_score(model, X, y, cv=5)

print("Cross-validation scores:", cv_scores)
print("Mean CV Accuracy:", cv_scores.mean())


# 11. CLASSIFICATION REPORT

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# 12. CONFUSION MATRIX

cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6,4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")

plt.savefig("results/confusion_matrix.png")
plt.close()


# 13. SAVE MODEL

joblib.dump(model, "model/rf_model.pkl")

print("\n✅ Model trained and saved successfully!")