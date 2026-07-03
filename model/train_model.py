import pandas as pd
import numpy as np
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    precision_score,
    recall_score,
    f1_score
)

# ===============================
# 1. LOAD DATASET
# ===============================

df = pd.read_excel("data/survey_cleaned.xlsx")


# Clean column names
df.columns = (
    df.columns
    .str.strip()
    .str.replace("\n", "", regex=False)
)
df.drop(
    columns=["risk_score", "health_risk"],
    inplace=True,
    errors="ignore"
)
print("Columns:")
print(df.columns.tolist())

df["No_Familymembers"] = pd.to_numeric(
    df["No_Familymembers"],
    errors="coerce"
)

df["No_Familymembers"] = df["No_Familymembers"].fillna(
    df["No_Familymembers"].median()
) 

# ===============================
# AGE CONVERSION
# ===============================

# Clean age values
df["age"] = (
    df["age"]
    .astype(str)
    .str.strip()
    .str.replace(" years", "", regex=False)
    .str.replace(" Years", "", regex=False)
    .str.replace("YEAR", "", regex=False)
    .str.replace("Year", "", regex=False)
    .str.replace("years", "", regex=False)
)

# Convert age ranges to numbers
age_map = {
    "18–24": 21,
    "18-24": 21,

    "25–34": 30,
    "25-34": 30,

    "35–44": 40,
    "35-44": 40,

    "45–54": 50,
    "45-54": 50,

    "55+": 60,
    "55 +": 60,
    "55 and above": 60,
    "Above 55": 60
}

df["age"] = df["age"].replace(age_map)

# Convert to numeric
df["age"] = pd.to_numeric(df["age"], errors="coerce")

if df["age"].isna().sum() > 0:
    print("\n⚠ Unknown age values found:")
    print(df.loc[df["age"].isna(), "age"].unique())

df = df.dropna(subset=["age"])
df["age"] = df["age"].astype(int)

print("\nAge values converted successfully.")
print(df["age"].head())


# ===============================
# BMI
# ===============================

df["BMI"] = df["weight"] / ((df["height"] / 100) ** 2)

# ===============================
# BMI SCORE
# ===============================

def bmi_score(bmi):

    if bmi < 18.5:
        return 1      # Underweight

    elif bmi < 25:
        return 0      # Normal

    elif bmi < 30:
        return 1      # Overweight

    else:
        return 2      # Obese


df["bmi_score"] = df["BMI"].apply(bmi_score)

print("\nBMI Score Distribution")
print(df["bmi_score"].value_counts())


# ===============================
# DISEASE LABELS
# ===============================

df["Medical_Condition"] = df["Medical_Conditions"].astype(str)

df["diabetes"] = df["Medical_Conditions"].str.contains(
    "Diabetes",
    case=False,
    na=False
).astype(int)

df["cholesterol"] = df["Medical_Conditions"].str.contains(
    "Cholesterol",
    case=False,
    na=False
).astype(int)

df["bp"] = df["Medical_Conditions"].str.contains(
    "High Blood",
    case=False,
    na=False
).astype(int)

df["thyroid"] = df["Medical_Conditions"].str.contains(
    "Thyroid",
    case=False,
    na=False
).astype(int)


# ===============================
# FRUIT SCORE
# ===============================

def fruit_score(fruit):

    fruit = str(fruit).lower()

    if "daily" in fruit:
        return 0

    elif "2" in fruit or "3" in fruit:
        return 1

    elif "once" in fruit:
        return 2

    elif "rare" in fruit or "never" in fruit:
        return 3

    return 1


df["fruit_score"] = df["fruit_Intake"].apply(fruit_score)

print("\nFruit Score Distribution")
print(df["fruit_score"].value_counts())

# ===============================
# VEGETABLE SCORE
# ===============================

def vegetable_score(veg):

    veg = str(veg).lower()

    if "every meal" in veg:
        return 0

    elif "once" in veg:
        return 1

    elif "2" in veg or "3" in veg:
        return 2

    elif "rare" in veg:
        return 3

    return 1


df["vegetable_score"] = df["Vegetable_Intake"].apply(vegetable_score)

print("\nVegetable Score Distribution")
print(df["vegetable_score"].value_counts())

# ===============================
# MEAL SCORE
# ===============================

def meal_score(meals):

    meals = str(meals).lower()

    if meals.startswith("3"):
        return 0

    elif meals.startswith("2"):
        return 1

    elif meals.startswith("4") or meals.startswith("5"):
        return 1

    elif meals.startswith("1"):
        return 3

    return 1


df["meal_score"] = df["meals_per_day"].apply(meal_score)

print("\nMeal Score Distribution")
print(df["meal_score"].value_counts())

# ===============================
# FATIGUE SCORE
# ===============================

def fatigue_score(x):

    x = str(x).lower()

    if "never" in x:
        return 0

    elif "rarely" in x:
        return 1

    elif "sometimes" in x:
        return 2

    elif "often" in x:
        return 3

    elif "always" in x:
        return 4

    return 1


df["fatigue_score"] = df["Fatigue_Status"].apply(fatigue_score)

print("\nFatigue Score Distribution")
print(df["fatigue_score"].value_counts())

# ===============================
# SUNLIGHT SCORE
# ===============================

def sunlight_score(x):

    x = str(x).lower()

    if "more than 1 hour" in x:
        return 0

    elif "30" in x:
        return 1

    elif "15" in x:
        return 2

    elif "mostly indoors" in x:
        return 3

    return 1


df["sunlight_score"] = df["Sunlight_Exposure"].apply(sunlight_score)

print("\nSunlight Score Distribution")
print(df["sunlight_score"].value_counts())

# ===============================
# PROTEIN SCORE
# ===============================

def protein_score(x):

    x = str(x).lower()

    score = 0

    protein_sources = [
        "fish",
        "chicken",
        "eggs",
        "beans",
        "milk",
        "tofu",
        "soya",
        "meat",
        "cheese",
        "almond"
    ]

    for item in protein_sources:
        if item in x:
            score += 1

    if score >= 5:
        return 0

    elif score >= 3:
        return 1

    elif score >= 1:
        return 2

    return 3


df["protein_score"] = df["Protein_Foods"].apply(protein_score)

print("\nProtein Score Distribution")
print(df["protein_score"].value_counts())


# ===============================
# ADDICTION
# ===============================

def map_addiction(x):

    x = str(x).lower()

    if "both" in x:
        return 2

    elif "alcohol" in x or "tobacco" in x:
        return 1

    return 0

df["addiction"] = df["Tobacco_Alcohol_Use"].apply(map_addiction)

# ===============================
# ACTIVITY SCORE
# ===============================

def activity_score(activity):

    activity = str(activity).lower()

    if "heavy physical work" in activity:
        return 0

    elif "moderate activity" in activity:
        return 1

    elif "light activity" in activity:
        return 2

    elif "mostly sitting" in activity:
        return 3

    return 2


df["activity_score"] = df["Activity_Level"].apply(activity_score)

print("\nActivity Score Distribution")
print(df["activity_score"].value_counts())

# ===============================
# SLEEP SCORE
# ===============================

def sleep_score(hours):

    hours = str(hours).lower().strip()

    if "7" in hours or "8" in hours:
        return 0

    elif "6" in hours:
        return 1

    elif "more than 8" in hours:
        return 1

    elif "less than 6" in hours:
        return 2

    return 1


df["sleep_score"] = df["Sleep_Hours"].apply(sleep_score)

print("\nSleep Score Distribution")
print(df["sleep_score"].value_counts())

# ===============================
# DISEASE SCORE
# ===============================

def disease_score(condition):

    condition = str(condition).lower()

    if "none" in condition:
        return 0

    elif "cholesterol" in condition:
        return 1

    elif "thyroid" in condition:
        return 1

    elif "high blood" in condition:
        return 2

    elif "diabetes" in condition:
        return 2

    return 0


df["disease_score"] = df["Medical_Conditions"].apply(disease_score)

print(df["disease_score"].value_counts())

# ===============================
# CREATE RISK SCORE
# ===============================
df["risk_score"] = (
    df["bmi_score"]
    + df["disease_score"]
    + df["activity_score"]
    + df["sleep_score"]
    + df["fruit_score"]
    + df["vegetable_score"]
    + df["meal_score"]
    + df["fatigue_score"]
    + df["sunlight_score"]
    + df["protein_score"]
    + df["addiction"]
)

print("\nRisk Score Distribution")
print(df["risk_score"].describe())

low = df["risk_score"].quantile(0.33)
high = df["risk_score"].quantile(0.66)

print(low, high)

# ===============================
# CREATE HEALTH RISK
# ===============================

def classify(score):

    if score <= 11:
        return 0      # Low

    elif score <= 15:
        return 1      # Medium

    else:
        return 2      # High


df["health_risk"] = df["risk_score"].apply(classify)

print("\nHealth Risk Distribution")
print(df["health_risk"].value_counts())
# ===============================
# TARGET
# ===============================

target_col = "health_risk"

y = df[target_col]

X = df.drop(
    columns=[
        target_col,
        "risk_score",
        "BMI",
        "bmi_score",

        # Remove original text columns
        "fruit_Intake",
        "Vegetable_Intake",
        "Protein_Foods",
        "Activity_Level",
        "Sleep_Hours",
        "Fatigue_Status",
        "Sunlight_Exposure",
        "Medical_Conditions",
        "Medical_Condition"
    ],
    errors="ignore"
)
print("\nHealth Risk Distribution")
print(y.value_counts())


print("\nTraining Columns:")
print(X.columns.tolist())

joblib.dump(
    X.columns.tolist(),
    "model/training_columns.pkl"
)
print("\n===== COLUMN DATA TYPES =====")
print(X.dtypes)
# ===============================
# ENCODING

# FILL MISSING VALUES
# ===============================

for col in X.columns:

    # Text columns
    if pd.api.types.is_object_dtype(X[col]) or pd.api.types.is_string_dtype(X[col]):

        X[col] = X[col].fillna("Unknown")

    # Numeric columns
    elif pd.api.types.is_numeric_dtype(X[col]):

        X[col] = X[col].fillna(X[col].median())

    # Any other datatype
    else:

        X[col] = X[col].fillna("Unknown")

# One-hot encoding
X = pd.get_dummies(
    X,
    drop_first=True,
    dtype=int
)

# ===============================
# TRAIN TEST SPLIT
# ===============================

X_train,X_test,y_train,y_test = train_test_split(

    X,
    y,

    test_size=0.30,

    random_state=42,

    stratify=y

)

# ===============================
# MODEL
# ===============================

model = RandomForestClassifier(
    n_estimators=1000,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    max_features="sqrt",
    bootstrap=True,
    class_weight="balanced_subsample",
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)
# ===============================
# PREDICTION
# ===============================

y_pred = model.predict(X_test)

# ===============================
# METRICS
# ===============================

print("\nAccuracy :",accuracy_score(y_test,y_pred))

print("\nPrecision :",precision_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
))

print("\nRecall :",recall_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
))

print("\nF1 Score :",f1_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
))

print("\nClassification Report\n")

print(

    classification_report(

        y_test,

        y_pred,

        zero_division=0

    )

)

# ===============================
# CROSS VALIDATION
# ===============================

cv = StratifiedKFold(
    n_splits=10,
    shuffle=True,
    random_state=42
)

scores = cross_val_score(
    model,
    X,
    y,
    cv=cv,
    scoring="f1_weighted"
)

print(scores)
print(scores.mean())
print(scores.std())

# ===============================
# CONFUSION MATRIX
# ===============================

cm = confusion_matrix(

    y_test,

    y_pred

)

plt.figure(figsize=(6,5))

sns.heatmap(

    cm,

    annot=True,

    fmt="d",

    cmap="Blues"

)

plt.xlabel("Predicted")

plt.ylabel("Actual")

plt.title("Confusion Matrix")

plt.tight_layout()

plt.savefig(

    "results/confusion_matrix.png"

)

plt.close()

# ===============================
# FEATURE IMPORTANCE
# ===============================

importance = pd.DataFrame({

    "Feature":X.columns,

    "Importance":model.feature_importances_

})

importance = importance.sort_values(

    "Importance",

    ascending=False

)

print("\nTop Features")

print(importance.head(15))

importance.to_csv(

    "results/feature_importance.csv",

    index=False

)
plt.figure(figsize=(10,6))

top15 = importance.head(15)

plt.barh(top15["Feature"], top15["Importance"])

plt.gca().invert_yaxis()

plt.xlabel("Importance")

plt.title("Top 15 Feature Importance")

plt.tight_layout()

plt.savefig("results/feature_importance.png")

plt.close()
# ===============================
# SAVE MODEL
# ===============================

MODEL_PATH = "model/rf_model.pkl"

joblib.dump(model, MODEL_PATH)

print(f"\nModel saved to {MODEL_PATH}")

print("\nModel Saved Successfully")

# ===============================
# DATASET INFO
# ===============================

print("\n===== COLUMN NAMES =====")
print(df.columns.tolist())

print("\n===== FIRST 5 ROWS =====")
print(df.head())

print("\n===== DATA TYPES =====")
print(df.dtypes)