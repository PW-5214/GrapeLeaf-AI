"""
Classifier unit tests covering all required edge cases.
Run with: pytest tests/ -v
"""

import pytest
from app.services.classifier import classify_sample, STATUS_LOW, STATUS_OPTIMUM, STATUS_HIGH, STATUS_SAFE, STATUS_ABOVE_SAFE, STATUS_UNAVAILABLE


def nutrients(**kwargs):
    """Helper: returns dict with all keys None, overriding with kwargs."""
    base = {k: None for k in [
        "N", "NO3", "NH4_N", "P", "K", "Ca", "Mg", "S",
        "Fe", "Mn", "Zn", "Cu", "Boron", "Mo", "Na", "Cl"
    ]}
    base.update(kwargs)
    return base


def get_result(results, key):
    for r in results:
        if r.nutrient_key == key:
            return r
    return None


# ─── Nitrogen classification tests ────────────────────────────────────────────
# Ref: 1.31 – 2.40 %

class TestNitrogenClassification:
    def test_low(self):
        r = get_result(classify_sample(nutrients(N=1.0)), "N")
        assert r.status == STATUS_LOW

    def test_optimum_midrange(self):
        r = get_result(classify_sample(nutrients(N=1.8)), "N")
        assert r.status == STATUS_OPTIMUM

    def test_high(self):
        r = get_result(classify_sample(nutrients(N=3.0)), "N")
        assert r.status == STATUS_HIGH

    def test_exact_minimum_boundary(self):
        """Exact ref_min should be Optimum (inclusive)."""
        r = get_result(classify_sample(nutrients(N=1.31)), "N")
        assert r.status == STATUS_OPTIMUM

    def test_exact_maximum_boundary(self):
        """Exact ref_max should be Optimum (inclusive)."""
        r = get_result(classify_sample(nutrients(N=2.40)), "N")
        assert r.status == STATUS_OPTIMUM

    def test_just_below_minimum(self):
        r = get_result(classify_sample(nutrients(N=1.30)), "N")
        assert r.status == STATUS_LOW

    def test_just_above_maximum(self):
        r = get_result(classify_sample(nutrients(N=2.41)), "N")
        assert r.status == STATUS_HIGH

    def test_missing_value(self):
        r = get_result(classify_sample(nutrients(N=None)), "N")
        assert r.status == STATUS_UNAVAILABLE
        assert r.entered_value is None


# ─── Phosphorus (0.41 – 0.80 %) ───────────────────────────────────────────────

class TestPhosphorusClassification:
    def test_low(self):
        r = get_result(classify_sample(nutrients(P=0.10)), "P")
        assert r.status == STATUS_LOW

    def test_optimum(self):
        r = get_result(classify_sample(nutrients(P=0.60)), "P")
        assert r.status == STATUS_OPTIMUM

    def test_high(self):
        r = get_result(classify_sample(nutrients(P=1.20)), "P")
        assert r.status == STATUS_HIGH

    def test_exact_min_boundary(self):
        r = get_result(classify_sample(nutrients(P=0.41)), "P")
        assert r.status == STATUS_OPTIMUM

    def test_exact_max_boundary(self):
        r = get_result(classify_sample(nutrients(P=0.80)), "P")
        assert r.status == STATUS_OPTIMUM


# ─── Copper (5.01 – 10.00 ppm) ─────────────────────────────────────────────

class TestCopperClassification:
    def test_exact_min_boundary(self):
        r = get_result(classify_sample(nutrients(Cu=5.01)), "Cu")
        assert r.status == STATUS_OPTIMUM

    def test_exact_max_boundary(self):
        r = get_result(classify_sample(nutrients(Cu=10.00)), "Cu")
        assert r.status == STATUS_OPTIMUM

    def test_just_below_min(self):
        r = get_result(classify_sample(nutrients(Cu=5.00)), "Cu")
        assert r.status == STATUS_LOW


# ─── Sodium safe-limit tests ──────────────────────────────────────────────────
# Safe limit < 0.5 %

class TestSodiumClassification:
    def test_below_safe_limit(self):
        r = get_result(classify_sample(nutrients(Na=0.30)), "Na")
        assert r.status == STATUS_SAFE

    def test_exactly_at_safe_limit(self):
        """Na = 0.5 should be Above Safe Limit (>= threshold)."""
        r = get_result(classify_sample(nutrients(Na=0.5)), "Na")
        assert r.status == STATUS_ABOVE_SAFE

    def test_above_safe_limit(self):
        r = get_result(classify_sample(nutrients(Na=0.8)), "Na")
        assert r.status == STATUS_ABOVE_SAFE

    def test_missing_na(self):
        r = get_result(classify_sample(nutrients(Na=None)), "Na")
        assert r.status == STATUS_UNAVAILABLE


# ─── Chloride safe-limit tests ────────────────────────────────────────────────

class TestChlorideClassification:
    def test_below_safe_limit(self):
        r = get_result(classify_sample(nutrients(Cl=0.20)), "Cl")
        assert r.status == STATUS_SAFE

    def test_exactly_at_safe_limit(self):
        r = get_result(classify_sample(nutrients(Cl=0.5)), "Cl")
        assert r.status == STATUS_ABOVE_SAFE

    def test_above_safe_limit(self):
        r = get_result(classify_sample(nutrients(Cl=0.7)), "Cl")
        assert r.status == STATUS_ABOVE_SAFE

    def test_missing_cl(self):
        r = get_result(classify_sample(nutrients(Cl=None)), "Cl")
        assert r.status == STATUS_UNAVAILABLE


# ─── Mixed status across all nutrients ───────────────────────────────────────

class TestMixedStatuses:
    def test_multiple_statuses(self):
        """Verify summary counts are correct for a mixed sample."""
        sample = nutrients(
            N=1.0,       # Low
            NO3=900,     # Optimum
            NH4_N=None,  # Unavailable
            P=1.0,       # High
            Na=0.3,      # Safe
            Cl=0.6,      # Above Safe
        )
        results = classify_sample(sample)
        statuses = {r.nutrient_key: r.status for r in results}
        assert statuses["N"] == STATUS_LOW
        assert statuses["NO3"] == STATUS_OPTIMUM
        assert statuses["NH4_N"] == STATUS_UNAVAILABLE
        assert statuses["P"] == STATUS_HIGH
        assert statuses["Na"] == STATUS_SAFE
        assert statuses["Cl"] == STATUS_ABOVE_SAFE


# ─── Missing value – never classified as Low ─────────────────────────────────

class TestMissingValuesSafety:
    def test_none_not_classified_as_low(self):
        """Critical: missing values must NOT become Low or zero."""
        for key in ["N", "NO3", "NH4_N", "P", "K", "Ca", "Mg", "S",
                    "Fe", "Mn", "Zn", "Cu", "Boron", "Mo"]:
            r = get_result(classify_sample(nutrients()), key)
            assert r.status == STATUS_UNAVAILABLE, \
                f"Expected Unavailable for missing {key}, got {r.status}"

    def test_all_missing_returns_all_unavailable(self):
        results = classify_sample(nutrients())
        for r in results:
            assert r.status == STATUS_UNAVAILABLE


# ─── Recommendation text checks ──────────────────────────────────────────────

class TestRecommendationLogic:
    def test_low_recommendation_contains_professional(self):
        r = get_result(classify_sample(nutrients(N=1.0)), "N")
        assert "agricultural professional" in r.recommendation.lower()

    def test_high_recommendation_avoids_additional_application(self):
        r = get_result(classify_sample(nutrients(N=3.0)), "N")
        assert "unnecessary" in r.recommendation.lower() or "verify" in r.recommendation.lower()

    def test_optimum_recommendation_mentions_monitoring(self):
        r = get_result(classify_sample(nutrients(N=1.8)), "N")
        assert "monitor" in r.recommendation.lower() or "continue" in r.recommendation.lower()

    def test_above_safe_recommendation_mentions_soil_testing(self):
        r = get_result(classify_sample(nutrients(Na=0.6)), "Na")
        assert "soil testing" in r.recommendation.lower() or "professional" in r.recommendation.lower()


# ─── Molybdenum (0.25 – 0.50 ppm) boundary ───────────────────────────────────

class TestMolybdenumBoundary:
    def test_exact_min(self):
        r = get_result(classify_sample(nutrients(Mo=0.25)), "Mo")
        assert r.status == STATUS_OPTIMUM

    def test_exact_max(self):
        r = get_result(classify_sample(nutrients(Mo=0.50)), "Mo")
        assert r.status == STATUS_OPTIMUM

    def test_low(self):
        r = get_result(classify_sample(nutrients(Mo=0.10)), "Mo")
        assert r.status == STATUS_LOW

    def test_high(self):
        r = get_result(classify_sample(nutrients(Mo=0.80)), "Mo")
        assert r.status == STATUS_HIGH
