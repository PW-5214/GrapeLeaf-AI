"""
Inference service for both Random Forest and XGBoost Vine Status Classifiers.
Loads model bundles on first use and caches them in memory.
"""

from __future__ import annotations
import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Literal

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(_BASE, "models")

MODEL_PATHS: Dict[str, str] = {
    "rf":                os.path.join(MODEL_DIR, "vine_classifier_rf.joblib"),
    "xgb":               os.path.join(MODEL_DIR, "vine_classifier_xgb.joblib"),
    "catboost":          os.path.join(MODEL_DIR, "vine_classifier_catboost.joblib"),
    "lightgbm":          os.path.join(MODEL_DIR, "vine_classifier_lightgbm.joblib"),
    "gradient_boosting": os.path.join(MODEL_DIR, "vine_classifier_gradient_boosting.joblib"),
}

MODEL_DISPLAY_NAMES: Dict[str, str] = {
    "rf":                "Random Forest (200 trees)",
    "xgb":               "XGBoost (300 estimators)",
    "catboost":          "CatBoost (300 iterations)",
    "lightgbm":          "LightGBM (300 estimators)",
    "gradient_boosting": "Gradient Boosting (150 estimators)",
}

ALIAS_MAP: Dict[str, str] = {
    "cb":  "catboost",
    "lgb": "lightgbm",
    "gb":  "gradient_boosting",
}

FEATURE_NAMES = [
    "N", "NO3", "NH4_N", "P", "K", "Ca", "Mg", "S",
    "Fe", "Mn", "Zn", "Cu", "Boron", "Mo", "Na", "Cl",
]

# In-memory cache: model_key → bundle
_cache: Dict[str, Any] = {}


def _load_bundle(model_key: str) -> Optional[dict]:
    """Load and cache a model bundle by canonical key."""
    canonical_key = ALIAS_MAP.get(model_key, model_key)
    if canonical_key in _cache:
        return _cache[canonical_key]
    path = MODEL_PATHS.get(canonical_key)
    if path and os.path.exists(path):
        _cache[canonical_key] = joblib.load(path)
        return _cache[canonical_key]
    return None


def list_available_models() -> list[dict]:
    """Return metadata for all available trained models."""
    available = []
    for key, path in MODEL_PATHS.items():
        if os.path.exists(path):
            bundle = _load_bundle(key)
            available.append({
                "key":          key,
                "display_name": MODEL_DISPLAY_NAMES[key],
                "cv_accuracy":  f"{bundle['cv_mean'] * 100:.1f}%" if bundle else "N/A",
                "test_accuracy": f"{bundle['accuracy'] * 100:.1f}%" if bundle else "N/A",
                "available":    True,
            })
        else:
            available.append({
                "key":          key,
                "display_name": MODEL_DISPLAY_NAMES[key],
                "cv_accuracy":  "N/A",
                "test_accuracy": "N/A",
                "available":    False,
            })
    return available


def predict_vine_status(
    nutrients: Dict[str, Optional[float]],
    model_key: str = "rf",
) -> Optional[Dict[str, Any]]:
    """
    Predict vine status using the chosen model.

    Args:
        nutrients:  dict mapping feature name → value (None for missing)
        model_key:  'rf' for Random Forest, 'xgb' for XGBoost

    Returns:
        dict with predicted_class, confidence_score, class_probabilities, etc.
        or None if the model is not available.
    """
    canonical_key = ALIAS_MAP.get(model_key, model_key)
    bundle = _load_bundle(canonical_key)
    if bundle is None:
        return None

    # Require at least one nutrient value
    if not any(v is not None for v in nutrients.values()):
        return None

    pipeline        = bundle["pipeline"]
    feature_names   = bundle.get("feature_names", FEATURE_NAMES)
    le              = bundle.get("label_encoder")
    classes_list    = bundle["classes"]

    # Build single-row DataFrame
    row_data = {feat: [nutrients.get(feat)] for feat in feature_names}
    df_row = pd.DataFrame(row_data)

    try:
        if le is not None:
            pred_enc  = pipeline.predict(df_row)[0]
            proba     = pipeline.predict_proba(df_row)[0]
            scalar_enc = int(np.asarray(pred_enc).ravel()[0])
            pred_class = str(le.inverse_transform([scalar_enc])[0])
            class_probs = {
                str(cls_name): round(float(p), 4)
                for cls_name, p in zip(le.classes_, proba)
            }
        else:
            pred_class  = str(pipeline.predict(df_row)[0])
            proba       = pipeline.predict_proba(df_row)[0]
            class_probs = {
                str(cls_name): round(float(p), 4)
                for cls_name, p in zip(pipeline.classes_, proba)
            }

        confidence = float(max(proba))

        return {
            "predicted_class":   pred_class,
            "confidence_score":  round(confidence, 4),
            "class_probabilities": class_probs,
            "model_key":         canonical_key,
            "model_name":        MODEL_DISPLAY_NAMES.get(canonical_key, canonical_key),
            "validation_accuracy": f"{bundle.get('cv_mean', 0) * 100:.1f}%",
            "test_accuracy":       f"{bundle.get('accuracy', 0) * 100:.1f}%",
        }

    except Exception as e:
        print(f"[ml_service] Prediction error ({model_key}): {e}")
        return None
