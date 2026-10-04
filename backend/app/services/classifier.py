"""
Transparent rule-based nutrient classification engine.

Rules:
  - Nutrients with min/max range:
      value < ref_min  → "Low"
      ref_min <= value <= ref_max → "Optimum"
      value > ref_max  → "High"
  - Na and Cl (safe-limit nutrients):
      value < 0.5  → "Safe"
      value >= 0.5 → "Above Safe Limit"
  - Missing or invalid value → "Data Unavailable"
"""

from __future__ import annotations
from typing import Optional
from app.config.standards import OCTOBER_STANDARDS, NUTRIENT_ORDER
from app.models.schemas import NutrientResult


STATUS_LOW = "Low"
STATUS_OPTIMUM = "Optimum"
STATUS_HIGH = "High"
STATUS_SAFE = "Safe"
STATUS_ABOVE_SAFE = "Above Safe Limit"
STATUS_UNAVAILABLE = "Data Unavailable"


def _format_range(std: dict) -> str:
    if std["is_safe_limit"]:
        return f"Less than {std['safe_limit']} {std['unit']}"
    return f"{std['ref_min']}–{std['ref_max']} {std['unit']}"


def _classify_nutrient(key: str, value: Optional[float]) -> NutrientResult:
    std = OCTOBER_STANDARDS[key]
    display_name = std["display_name"]
    unit = std["unit"]
    ref_range = _format_range(std)

    # Missing or invalid
    if value is None:
        return NutrientResult(
            nutrient_key=key,
            display_name=display_name,
            entered_value=None,
            unit=unit,
            reference_range=ref_range,
            status=STATUS_UNAVAILABLE,
            explanation="No value was provided for this nutrient.",
            recommendation="If this nutrient is important for your crop assessment, consider obtaining the measurement through laboratory analysis.",
        )

    # Safe-limit nutrients (Na, Cl)
    if std["is_safe_limit"]:
        limit = std["safe_limit"]
        if value < limit:
            return NutrientResult(
                nutrient_key=key,
                display_name=display_name,
                entered_value=value,
                unit=unit,
                reference_range=ref_range,
                status=STATUS_SAFE,
                explanation=f"The entered value ({value} {unit}) is below the safe limit of {limit} {unit}.",
                recommendation="Continue regular monitoring. Maintain balanced irrigation and soil management practices.",
            )
        else:
            return NutrientResult(
                nutrient_key=key,
                display_name=display_name,
                entered_value=value,
                unit=unit,
                reference_range=ref_range,
                status=STATUS_ABOVE_SAFE,
                explanation=f"The entered value ({value} {unit}) meets or exceeds the safe limit of {limit} {unit}. Elevated levels may indicate salinity concerns.",
                recommendation=(
                    "Consult a qualified agricultural professional for further assessment. "
                    "Consider soil testing and irrigation-water testing to evaluate salinity conditions. "
                    "Review current irrigation sources and soil amendment practices."
                ),
            )

    # Standard min/max nutrients
    ref_min = std["ref_min"]
    ref_max = std["ref_max"]

    if value < ref_min:
        return NutrientResult(
            nutrient_key=key,
            display_name=display_name,
            entered_value=value,
            unit=unit,
            reference_range=ref_range,
            status=STATUS_LOW,
            explanation=f"The entered value ({value} {unit}) is below the reference range of {ref_min}–{ref_max} {unit}.",
            recommendation=(
                "Review soil conditions, crop growth stage, and fertilizer history. "
                "Consult a qualified agricultural professional before making any amendments. "
                "Consider verification through appropriate laboratory re-testing."
            ),
        )
    elif value <= ref_max:
        return NutrientResult(
            nutrient_key=key,
            display_name=display_name,
            entered_value=value,
            unit=unit,
            reference_range=ref_range,
            status=STATUS_OPTIMUM,
            explanation=f"The entered value ({value} {unit}) is within the reference range of {ref_min}–{ref_max} {unit}.",
            recommendation=(
                "Continue balanced nutrient management practices. "
                "Monitor crop and soil conditions regularly to maintain this status."
            ),
        )
    else:
        return NutrientResult(
            nutrient_key=key,
            display_name=display_name,
            entered_value=value,
            unit=unit,
            reference_range=ref_range,
            status=STATUS_HIGH,
            explanation=f"The entered value ({value} {unit}) is above the reference range of {ref_min}–{ref_max} {unit}.",
            recommendation=(
                "Avoid unnecessary additional application of this nutrient until the result is verified. "
                "Review fertilizer history and consider re-testing to confirm. "
                "Consult an agricultural professional."
            ),
        )


def classify_sample(nutrients: dict) -> list[NutrientResult]:
    """
    Classify all nutrients in a sample.
    nutrients: dict mapping internal key → Optional[float]
    Returns results in NUTRIENT_ORDER.
    """
    results = []
    for key in NUTRIENT_ORDER:
        value = nutrients.get(key)
        results.append(_classify_nutrient(key, value))
    return results
