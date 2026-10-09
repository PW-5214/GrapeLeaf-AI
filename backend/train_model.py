"""
Train 5 Vine Status Classifiers for GrapeLeaf AI:
  1. Random Forest       (200 trees)
  2. XGBoost             (300 estimators)
  3. CatBoost            (300 iterations)
  4. LightGBM            (300 estimators)
  5. Gradient Boosting   (150 estimators)

4 Classification Classes (Priority order):
  1. Toxicity Risk      – Na >= 0.5% OR Cl >= 0.5%
  2. Nutrient Deficient – Any primary nutrient (N,P,K,Ca,Mg) below reference min
  3. Nutrient Excess    – Any primary nutrient (N,P,K) above reference max
  4. Balanced / Optimal – All primary nutrients within reference range

Outputs:
  app/models/vine_classifier_rf.joblib
  app/models/vine_classifier_xgb.joblib
  app/models/vine_classifier_catboost.joblib
  app/models/vine_classifier_lightgbm.joblib
  app/models/vine_classifier_gradient_boosting.joblib

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
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
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
        "standards_version": "Petiole Reference Standards",
        "classification_labels": ALL_CLASSES,
    }
    joblib.dump(bundle, path)
    print(f"  [SAVED] {path}")
    return path


def evaluate_encoded_model(name, model_key, pipeline, X_train, X_test,
                           y_train_enc, y_test_enc, X_all, y_all_enc,
                           le, y_raw_labels):
    print_separator(f"Model: {name}")
    pipeline.fit(X_train, y_train_enc)

    y_pred_enc = pipeline.predict(X_test)
    acc = accuracy_score(y_test_enc, y_pred_enc)
    print(f"\n  Test Accuracy : {acc * 100:.2f}%")

    y_pred_labels = le.inverse_transform(y_pred_enc)
    print("\n  Classification Report:\n")
    print(classification_report(y_raw_labels, y_pred_labels, target_names=sorted(le.classes_), zero_division=0))

    labels = sorted(le.classes_)
    cm = confusion_matrix(y_raw_labels, y_pred_labels, labels=labels)
    print("  Confusion Matrix (rows=actual, cols=predicted):")
    header = f"{'':28s}" + "".join(f"{l[:10]:>14s}" for l in labels)
    print(f"  {header}")
    for i, lbl in enumerate(labels):
        row_str = f"  {lbl:28s}" + "".join(f"{v:>14d}" for v in cm[i])
        print(row_str)

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(pipeline, X_all, y_all_enc, cv=cv, scoring="accuracy", n_jobs=-1)
    cv_mean, cv_std = cv_scores.mean(), cv_scores.std()
    print(f"\n  5-Fold CV Accuracy : {cv_mean*100:.2f}% (+/- {cv_std*100:.2f}%)")
    print(f"  Fold scores        : {[f'{s*100:.2f}%' for s in cv_scores]}")

    # Feature importances
    clf = pipeline.named_steps["classifier"]
    if hasattr(clf, "feature_importances_"):
        imps = clf.feature_importances_
    elif hasattr(clf, "get_feature_importance"):
        imps = clf.get_feature_importance()
    else:
        imps = np.zeros(len(FEATURE_NAMES))

    importances = dict(zip(FEATURE_NAMES, [float(x) for x in imps]))
    print("\n  Feature Importances (top 6):")
    for feat, imp in sorted(importances.items(), key=lambda x: -x[1])[:6]:
        bar = "#" * int(min(imp * 80, 40))
        print(f"    {feat:10s}  {imp:.4f}  {bar}")

    save_model_bundle(
        pipeline, name, model_key,
        acc, cv_mean, cv_std,
        le.classes_.tolist(),
        le=le,
        feature_importances=importances,
    )
    return {"name": name, "accuracy": acc, "cv_mean": cv_mean, "cv_std": cv_std}


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


def build_xgb_pipeline(num_classes: int):
    return Pipeline([
        ("imputer",    SimpleImputer(strategy="median")),
        ("scaler",     StandardScaler()),
        ("classifier", XGBClassifier(
            n_estimators=300,
            max_depth=8,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            eval_metric="mlogloss",
            num_class=num_classes,
            random_state=42,
            n_jobs=-1,
            verbosity=0,
        )),
    ])


def build_catboost_pipeline():
    return Pipeline([
        ("imputer",    SimpleImputer(strategy="median")),
        ("scaler",     StandardScaler()),
        ("classifier", CatBoostClassifier(
            iterations=300,
            depth=6,
            learning_rate=0.1,
            loss_function="MultiClass",
            random_seed=42,
            verbose=0,
            thread_count=-1,
        )),
    ])


def build_lightgbm_pipeline():
    return Pipeline([
        ("imputer",    SimpleImputer(strategy="median")),
        ("scaler",     StandardScaler()),
        ("classifier", LGBMClassifier(
            n_estimators=300,
            max_depth=8,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1,
            verbose=-1,
        )),
    ])


def build_gb_pipeline():
    return Pipeline([
        ("imputer",    SimpleImputer(strategy="median")),
        ("scaler",     StandardScaler()),
        ("classifier", GradientBoostingClassifier(
            n_estimators=150,
            max_depth=5,
            learning_rate=0.1,
            random_state=42,
        )),
    ])


def print_comparison(results: dict):
    print_separator("MODEL COMPARISON SUMMARY (ALL 5 ENGINES)")
    print(f"  {'Model':<34s}  {'Test Acc':>10s}  {'CV Mean':>10s}  {'CV Std':>8s}")
    print(f"  {'-'*34}  {'-'*10}  {'-'*10}  {'-'*8}")
    best_key, best_cv = None, -1
    for key, r in results.items():
        print(f"  {r['name']:<34s}  {r['accuracy']*100:>9.2f}%  {r['cv_mean']*100:>9.2f}%  {r['cv_std']*100:>7.2f}%")
        if r["cv_mean"] > best_cv:
            best_cv, best_key = r["cv_mean"], key
    print(f"\n  Top Performing Model (by CV accuracy): {results[best_key]['name']}")


def train_and_export():
    os.makedirs(MODEL_DIR, exist_ok=True)
    df = load_data()

    X = df[FEATURE_NAMES]
    y = df["Vine_Status"]

    le = LabelEncoder()
    y_enc = le.fit_transform(y)
    num_classes = len(le.classes_)

    X_train, X_test, y_train_enc, y_test_enc, y_train_raw, y_test_raw = train_test_split(
        X, y_enc, y, test_size=0.20, random_state=42, stratify=y_enc
    )
    print(f"\n[SPLIT] Train: {len(X_train):,}  |  Test: {len(X_test):,}")

    results = {}

    # ── 1. Random Forest (string classes) ─────────────────────────────────────
    print_separator("Model: Random Forest")
    rf_pipe = build_rf_pipeline()
    rf_pipe.fit(X_train, y_train_raw)
    rf_pred = rf_pipe.predict(X_test)
    rf_acc = accuracy_score(y_test_raw, rf_pred)
    print(f"\n  Test Accuracy : {rf_acc * 100:.2f}%")
    print("\n  Classification Report:\n")
    print(classification_report(y_test_raw, rf_pred, target_names=sorted(y.unique()), zero_division=0))

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    rf_cv_scores = cross_val_score(rf_pipe, X, y, cv=cv, scoring="accuracy", n_jobs=-1)
    rf_cv_mean, rf_cv_std = rf_cv_scores.mean(), rf_cv_scores.std()
    print(f"\n  5-Fold CV Accuracy : {rf_cv_mean*100:.2f}% (+/- {rf_cv_std*100:.2f}%)")

    rf_model = rf_pipe.named_steps["classifier"]
    rf_importances = dict(zip(FEATURE_NAMES, [float(v) for v in rf_model.feature_importances_]))
    save_model_bundle(
        rf_pipe, "Random Forest (200 trees)", "rf",
        rf_acc, rf_cv_mean, rf_cv_std,
        sorted(rf_pipe.classes_.tolist()),
        feature_importances=rf_importances,
    )
    results["rf"] = {"name": "Random Forest (200 trees)", "accuracy": rf_acc, "cv_mean": rf_cv_mean, "cv_std": rf_cv_std}

    # ── 2. XGBoost ────────────────────────────────────────────────────────────
    xgb_pipe = build_xgb_pipeline(num_classes)
    results["xgb"] = evaluate_encoded_model(
        "XGBoost (300 estimators)", "xgb", xgb_pipe,
        X_train, X_test, y_train_enc, y_test_enc, X, y_enc,
        le, y_test_raw
    )

    # ── 3. CatBoost ───────────────────────────────────────────────────────────
    cb_pipe = build_catboost_pipeline()
    results["catboost"] = evaluate_encoded_model(
        "CatBoost (300 iterations)", "catboost", cb_pipe,
        X_train, X_test, y_train_enc, y_test_enc, X, y_enc,
        le, y_test_raw
    )

    # ── 4. LightGBM ───────────────────────────────────────────────────────────
    lgb_pipe = build_lightgbm_pipeline()
    results["lightgbm"] = evaluate_encoded_model(
        "LightGBM (300 estimators)", "lightgbm", lgb_pipe,
        X_train, X_test, y_train_enc, y_test_enc, X, y_enc,
        le, y_test_raw
    )

    # ── 5. Gradient Boosting ──────────────────────────────────────────────────
    gb_pipe = build_gb_pipeline()
    results["gradient_boosting"] = evaluate_encoded_model(
        "Gradient Boosting (150 estimators)", "gradient_boosting", gb_pipe,
        X_train, X_test, y_train_enc, y_test_enc, X, y_enc,
        le, y_test_raw
    )

    print_comparison(results)
    print("\n[DONE] All 5 models saved successfully to app/models/:")
    for key in results:
        print(f"  vine_classifier_{key}.joblib  -> {results[key]['name']}")
    print("\nUsers can now select any of the 5 models in the GrapeLeaf AI UI.")


if __name__ == "__main__":
    train_and_export()
