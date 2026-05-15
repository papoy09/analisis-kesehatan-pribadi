import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from xgboost import XGBClassifier


# =====================================================
# 1. LOAD DATASET
# =====================================================
df = pd.read_csv("personalised_dataset.csv")


# =====================================================
# 2. MENENTUKAN FITUR DAN TARGET
# =====================================================
cols_to_drop = [
    "Patient_ID",
    "Blood_Pressure",
    "Health_Risk",
    "Predicted_Insurance_Cost",
    "Diet_Recommendation",
    "Exercise_Recommendation",
    "Heart_Disease_Risk",
    "Diabetes_Risk"
]

X = df.drop(columns=cols_to_drop)


# Mapping target dari teks ke angka
target_mapping = {
    "Low": 0,
    "Moderate": 1,
    "High": 2
}

y_heart = df["Heart_Disease_Risk"].map(target_mapping)
y_diabetes = df["Diabetes_Risk"].map(target_mapping)

# Menggabungkan dua target menjadi satu dataframe
y = pd.concat([y_heart, y_diabetes], axis=1)
y.columns = ["Heart_Disease_Risk", "Diabetes_Risk"]


# =====================================================
# 3. PRA-PEMROSESAN DATA
# =====================================================
# Memisahkan kolom kategorikal dan numerikal
categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
numerical_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()

# Transformer untuk data numerikal
numerical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

# Transformer untuk data kategorikal
categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

# Menggabungkan transformer
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numerical_transformer, numerical_cols),
        ("cat", categorical_transformer, categorical_cols)
    ]
)


# =====================================================
# 4. PEMBAGIAN DATA TRAIN DAN TEST
# =====================================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# =====================================================
# 5. PEMODELAN: MULTIVARIATE RANDOM FOREST
# =====================================================
rf_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", MultiOutputClassifier(
        RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )
    ))
])

print("Melatih model Multivariate Random Forest...")
rf_pipeline.fit(X_train, y_train)

y_pred_rf = rf_pipeline.predict(X_test)

print("\n--- Evaluasi Random Forest ---")
print(f"Akurasi Heart Disease: {accuracy_score(y_test['Heart_Disease_Risk'], y_pred_rf[:, 0]):.4f}")
print(f"Akurasi Diabetes: {accuracy_score(y_test['Diabetes_Risk'], y_pred_rf[:, 1]):.4f}")


# =====================================================
# 6. PEMODELAN: MULTIVARIATE XGBOOST
# =====================================================
xgb_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", MultiOutputClassifier(
        XGBClassifier(
            n_estimators=100,
            random_state=42,
            use_label_encoder=False,
            eval_metric="mlogloss"
        )
    ))
])

print("\nMelatih model Multivariate XGBoost...")
xgb_pipeline.fit(X_train, y_train)

y_pred_xgb = xgb_pipeline.predict(X_test)

print("\n--- Evaluasi XGBoost ---")
print(f"Akurasi Heart Disease: {accuracy_score(y_test['Heart_Disease_Risk'], y_pred_xgb[:, 0]):.4f}")
print(f"Akurasi Diabetes: {accuracy_score(y_test['Diabetes_Risk'], y_pred_xgb[:, 1]):.4f}")


# =====================================================
# 7. EVALUASI TAMBAHAN
# =====================================================
label_names = ["Low", "Moderate", "High"]

print("\n=== Classification Report Random Forest - Heart Disease ===")
print(classification_report(
    y_test["Heart_Disease_Risk"],
    y_pred_rf[:, 0],
    target_names=label_names
))

print("\n=== Classification Report Random Forest - Diabetes ===")
print(classification_report(
    y_test["Diabetes_Risk"],
    y_pred_rf[:, 1],
    target_names=label_names
))

print("\n=== Classification Report XGBoost - Heart Disease ===")
print(classification_report(
    y_test["Heart_Disease_Risk"],
    y_pred_xgb[:, 0],
    target_names=label_names
))

print("\n=== Classification Report XGBoost - Diabetes ===")
print(classification_report(
    y_test["Diabetes_Risk"],
    y_pred_xgb[:, 1],
    target_names=label_names
))


# =====================================================
# 8. CONFUSION MATRIX
# =====================================================
print("\n=== Confusion Matrix Random Forest - Heart Disease ===")
print(confusion_matrix(
    y_test["Heart_Disease_Risk"],
    y_pred_rf[:, 0]
))

print("\n=== Confusion Matrix Random Forest - Diabetes ===")
print(confusion_matrix(
    y_test["Diabetes_Risk"],
    y_pred_rf[:, 1]
))

print("\n=== Confusion Matrix XGBoost - Heart Disease ===")
print(confusion_matrix(
    y_test["Heart_Disease_Risk"],
    y_pred_xgb[:, 0]
))

print("\n=== Confusion Matrix XGBoost - Diabetes ===")
print(confusion_matrix(
    y_test["Diabetes_Risk"],
    y_pred_xgb[:, 1]
))


# =====================================================
# 9. SIMPAN MODEL
# =====================================================
with open("rf_model.pkl", "wb") as file:
    pickle.dump(rf_pipeline, file)

with open("xgb_model.pkl", "wb") as file:
    pickle.dump(xgb_pipeline, file)

print("\nModel berhasil dilatih dan disimpan.")
print("File yang dibuat:")
print("- rf_model.pkl")
print("- xgb_model.pkl")