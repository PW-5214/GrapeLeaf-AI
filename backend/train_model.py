"""
Train BOTH Random Forest and XGBoost Vine Status Classifiers.

4 Classification Classes (Priority order):
  1. Toxicity Risk      – Na >= 0.5% OR Cl >= 0.5%
  2. Nutrient Deficient – Any primary nutrient (N,P,K,Ca,Mg) below reference min
  3. Nutrient Excess    – Any primary nutrient (N,P,K) above reference max
  4. Balanced / Optimal – All primary nutrients within reference range

Outputs:
  app/models/vine_classifier_rf.joblib   – Random Forest pipeline
  app/models/vine_classifier_xgb.joblib  – XGBoost pipeline

Run from backend/ directory:
  python train_model.py
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from xgboost import XGBClassifier
import joblib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.config.standards import CSV_COLUMN_MAP

# ─── Paths ────────────────────────────────────────────────────────────────────
_BASE = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_PATH = os.path.join(_BASE, "app", "data", "Petiole_Leaf_Analysis_5000.csv")
if not os.path.exists(RAW_DATA_PATH):
    RAW_DATA_PATH = os.path.join(os.path.dirname(_BASE), "Petiole_Leaf_Analysis_5000.csv")

OUTPUT_LABELED_PATH = os.path.join(_BASE, "app", "data", "Petiole_Leaf_Analysis_Labeled.csv")
MODEL_DIR = os.path.join(_BASE, "app", "models")

# ─── Features ─────────────────────────────────────────────────────────────────
FEATURE_NAMES = [
    "N", "NO3", "NH4_N", "P", "K", "Ca", "Mg", "S",
    "Fe", "Mn", "Zn", "Cu", "Boron", "Mo", "Na", "Cl",
]

# ─── Labeling standards ───────────────────────────────────────────────────────
STANDARDS = {
    "N":     {"min": 1.31, "max": 2.40},
    "P":     {"min": 0.41, "max": 0.80},
    "K":     {"min": 1.11, "max": 2.20},
    "Ca":    {"min": 0.74, "max": 1.14},
    "Mg":    {"min": 0.51, "max": 0.80},
    "Na":    {"safe_limit": 0.5},
    "Cl":    {"safe_limit": 0.5},
}
PRIMARY_DEFICIENCY_CHECK = ["N", "P", "K", "Ca", "Mg"]
PRIMARY_EXCESS_CHECK     = ["N", "P", "K"]

CLASS_TOXICITY  = "Toxicity Risk"
CLASS_DEFICIENT = "Nutrient Deficient"
CLASS_EXCESS    = "Nutrient Excess"
CLASS_BALANCED  = "Balanced / Optimal"
ALL_CLASSES     = [CLASS_BALANCED, CLASS_DEFICIENT, CLASS_EXCESS, CLASS_TOXICITY]


def assign_vine_status(row: pd.Series) -> str:
    na, cl = row.get("Na"), row.get("Cl")
    if (pd.notna(na) and na >= STANDARDS["Na"]["safe_limit"]) or \
       (pd.notna(cl) and cl >= STANDARDS["Cl"]["safe_limit"]):
        return CLASS_TOXICITY
    for n in PRIMARY_DEFICIENCY_CHECK:
        v = row.get(n)
        if pd.notna(v) and v < STANDARDS[n]["min"]:
            return CLASS_DEFICIENT
    for n in PRIMARY_EXCESS_CHECK:
        v = row.get(n)
        if pd.notna(v) and v > STANDARDS[n]["max"]:
            return CLASS_EXCESS
    return CLASS_BALANCED


def print_separator(title: str = ""):
    print("\n" + "=" * 62)
    if title:
        print(f"  {title}")
        print("=" * 62)


def load_data():
    print(f"\n[DATA] Loading: {RAW_DATA_PATH}")
    df_raw = pd.read_csv(RAW_DATA_PATH)
    print(f"[DATA] Loaded {len(df_raw):,} records")

    rename_map = {k: v for k, v in CSV_COLUMN_MAP.items() if k != v}
    df = df_raw.rename(columns=rename_map)
    df["Vine_Status"] = df[FEATURE_NAMES].apply(assign_vine_status, axis=1)

    print("\n[DATA] Class Distribution:")
    counts = df["Vine_Status"].value_counts()
    for cls, cnt in counts.items():
        bar = "#" * int(cnt / len(df) * 40)
        print(f"  {cls:25s}  {cnt:5d}  ({cnt/len(df)*100:.1f}%)  {bar}")

    df.to_csv(OUTPUT_LABELED_PATH, index=False)
    print(f"\n[DATA] Labeled dataset saved -> {OUTPUT_LABELED_PATH}")
    return df


def evaluate_model(name, pipeline, X_train, X_test, y_train, y_test, X_all, y_all):
    print_separator(f"Model: {name}")
    pipeline.fit(X_train, y_train)

    y_pred  = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n  Test Accuracy : {accuracy * 100:.2f}%")
    print(f"\n  Classification Report:\n")
    print(classification_report(y_test, y_pred, target_names=sorted(y_all.unique()), zero_division=0))

    # Confusion matrix
    labels = sorted(y_all.unique())
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    print("  Confusion Matrix (rows=actual, cols=predicted):")
    header = f"{'':28s}" + "".join(f"{l[:10]:>14s}" for l in labels)
    print(f"  {header}")
    for i, lbl in enumerate(labels):
        row_str = f"  {lbl:28s}" + "".join(f"{v:>14d}" for v in cm[i])
        print(row_str)

    # CV
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(pipeline, X_all, y_all, cv=cv, scoring="accuracy", n_jobs=-1)
    print(f"\n  5-Fold CV Accuracy : {cv_scores.mean()*100:.2f}% (+/- {cv_scores.std()*100:.2f}%)")
    print(f"  Fold scores        : {[f'{s*100:.2f}%' for s in cv_scores]}")

    return accuracy, cv_scores.mean(), cv_scores.std()


def build_rf_pipeline():
    return Pipeline([
        ("imputer",    SimpleImputer(strategy="median")),
        ("scaler",     StandardScaler()),
        ("classifier", RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        )),
    ])


def build_xgb_pipeline(num_classes: int, label_encoder: LabelEncoder):
    return Pipeline([
        ("imputer",    SimpleImputer(strategy="median")),
        ("scaler",     StandardScaler()),
        ("classifier", XGBClassifier(
            n_estimators=300,
            max_depth=8,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            use_label_encoder=False,
            eval_metric="mlogloss",
            num_class=num_classes,
            random_state=42,
            n_jobs=-1,
            verbosity=0,
        )),
    ])


def save_model_bundle(pipeline, name, model_key, accuracy, cv_mean, cv_std,
                      classes, le=None, feature_importances=None):
    os.makedirs(MODEL_DIR, exist_ok=True)
    path = os.path.join(MODEL_DIR, f"vine_classifier_{model_key}.joblib")
    bundle = {
        "pipeline":          pipeline,
        "model_key":         model_key,
        "model_name":        name,
        "classes":           classes,
        "feature_names":     FEATURE_NAMES,
        "accuracy":          float(accuracy),
        "cv_mean":           float(cv_mean),
        "cv_std":            float(cv_std),
        "label_encoder":     le,
        "feature_importance": feature_importances or {},
        "standards_version": "October Pruning Reference Standards",
        "classification_labels": ALL_CLASSES,
    }
    joblib.dump(bundle, path)
    print(f"\n  [SAVED] {path}")
    return path


def print_comparison(results: dict):
    print_separator("MODEL COMPARISON SUMMARY")
    print(f"  {'Model':<30s}  {'Test Acc':>10s}  {'CV Mean':>10s}  {'CV Std':>8s}")
    print(f"  {'-'*30}  {'-'*10}  {'-'*10}  {'-'*8}")
    best_key, best_cv = None, -1
    for key, r in results.items():
        print(f"  {r['name']:<30s}  {r['accuracy']*100:>9.2f}%  {r['cv_mean']*100:>9.2f}%  {r['cv_std']*100:>7.2f}%")
        if r["cv_mean"] > best_cv:
            best_cv, best_key = r["cv_mean"], key
    print(f"\n  Best model (by CV accuracy): {results[best_key]['name']}")


def train_and_export():
    os.makedirs(MODEL_DIR, exist_ok=True)
    df = load_data()

    X = df[FEATURE_NAMES]
    y = df["Vine_Status"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"\n[SPLIT] Train: {len(X_train):,}  |  Test: {len(X_test):,}")

    results = {}

    # ── 1. Random Forest ──────────────────────────────────────────────────────
    rf_pipe = build_rf_pipeline()
    rf_acc, rf_cv_mean, rf_cv_std = evaluate_model(
        "Random Forest", rf_pipe, X_train, X_test, y_train, y_test, X, y
    )

    rf_model = rf_pipe.named_steps["classifier"]
    rf_importances = dict(zip(FEATURE_NAMES, rf_model.feature_importances_.tolist()))
    print("\n  Feature Importances (top 8):")
    for feat, imp in sorted(rf_importances.items(), key=lambda x: -x[1])[:8]:
        bar = "#" * int(imp * 80)
        print(f"    {feat:10s}  {imp:.4f}  {bar}")

    save_model_bundle(
        rf_pipe, "Random Forest (200 trees)", "rf",
        rf_acc, rf_cv_mean, rf_cv_std,
        sorted(rf_pipe.classes_.tolist()),
        feature_importances=rf_importances,
    )
    results["rf"] = {"name": "Random Forest (200 trees)", "accuracy": rf_acc, "cv_mean": rf_cv_mean, "cv_std": rf_cv_std}

    # ── 2. XGBoost ────────────────────────────────────────────────────────────
    # XGBoost needs integer labels → use LabelEncoder
    le = LabelEncoder()
    y_train_enc = le.fit_transform(y_train)
    y_test_enc  = le.transform(y_test)
    y_all_enc   = le.transform(y)

    num_classes = len(le.classes_)
    xgb_pipe = build_xgb_pipeline(num_classes, le)

    print_separator("Model: XGBoost")
    xgb_pipe.fit(X_train, y_train_enc)

    y_pred_enc = xgb_pipe.predict(X_test)
    xgb_acc = accuracy_score(y_test_enc, y_pred_enc)
    print(f"\n  Test Accuracy : {xgb_acc * 100:.2f}%")

    # Decode back for readable report
    y_pred_labels = le.inverse_transform(y_pred_enc)
    print(f"\n  Classification Report:\n")
    print(classification_report(y_test, y_pred_labels, target_names=sorted(y.unique()), zero_division=0))

    labels = sorted(y.unique())
    cm = confusion_matrix(y_test, y_pred_labels, labels=labels)
    print("  Confusion Matrix (rows=actual, cols=predicted):")
    header = f"{'':28s}" + "".join(f"{l[:10]:>14s}" for l in labels)
    print(f"  {header}")
    for i, lbl in enumerate(labels):
        row_str = f"  {lbl:28s}" + "".join(f"{v:>14d}" for v in cm[i])
        print(row_str)

    # CV on encoded labels
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(xgb_pipe, X, y_all_enc, cv=cv, scoring="accuracy", n_jobs=-1)
    xgb_cv_mean, xgb_cv_std = cv_scores.mean(), cv_scores.std()
    print(f"\n  5-Fold CV Accuracy : {xgb_cv_mean*100:.2f}% (+/- {xgb_cv_std*100:.2f}%)")
    print(f"  Fold scores        : {[f'{s*100:.2f}%' for s in cv_scores]}")

    # XGBoost feature importance
    xgb_model = xgb_pipe.named_steps["classifier"]
    xgb_importances = dict(zip(FEATURE_NAMES, xgb_model.feature_importances_.tolist()))
    print("\n  Feature Importances (top 8):")
    for feat, imp in sorted(xgb_importances.items(), key=lambda x: -x[1])[:8]:
        bar = "#" * int(imp * 80)
        print(f"    {feat:10s}  {imp:.4f}  {bar}")

    save_model_bundle(
        xgb_pipe, "XGBoost (300 estimators)", "xgb",
        xgb_acc, xgb_cv_mean, xgb_cv_std,
        le.classes_.tolist(),   # original string class names
        le=le,
        feature_importances=xgb_importances,
    )
    results["xgb"] = {"name": "XGBoost (300 estimators)", "accuracy": xgb_acc, "cv_mean": xgb_cv_mean, "cv_std": xgb_cv_std}

    print_comparison(results)
    print("\n[DONE] Both models saved successfully.")
    print(f"  vine_classifier_rf.joblib  -> Random Forest")
    print(f"  vine_classifier_xgb.joblib -> XGBoost")
    print(f"\nUsers can now select their preferred model in the GrapeLeaf AI UI.")


if __name__ == "__main__":
    train_and_export()
