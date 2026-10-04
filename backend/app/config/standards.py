"""
Central configuration for October Pruning Reference Standards.
This is the single source of truth for all classification and display logic.
Do NOT replace these values with external sources without expert validation.
"""

from typing import Optional

# ─── Nutrient definitions ───────────────────────────────────────────────────
# Each entry: (display_name, unit, min, max, is_safe_limit)
# is_safe_limit=True means: safe < threshold, above_safe >= threshold (Na, Cl)

OCTOBER_STANDARDS = {
    "N": {
        "display_name": "Nitrogen",
        "unit": "%",
        "ref_min": 1.31,
        "ref_max": 2.40,
        "is_safe_limit": False,
        "description": "Total Nitrogen – essential for vegetative growth and leaf development.",
    },
    "NO3": {
        "display_name": "Nitrate",
        "unit": "ppm",
        "ref_min": 700,
        "ref_max": 1200,
        "is_safe_limit": False,
        "description": "Nitrate Nitrogen – primary inorganic nitrogen form absorbed by roots.",
    },
    "NH4_N": {
        "display_name": "Ammonium-N",
        "unit": "ppm",
        "ref_min": 500,
        "ref_max": 800,
        "is_safe_limit": False,
        "description": "Ammonium Nitrogen – another inorganic nitrogen form available to plants.",
    },
    "P": {
        "display_name": "Phosphorus",
        "unit": "%",
        "ref_min": 0.41,
        "ref_max": 0.80,
        "is_safe_limit": False,
        "description": "Phosphorus – vital for energy transfer, root development, and fruiting.",
    },
    "K": {
        "display_name": "Potassium",
        "unit": "%",
        "ref_min": 1.11,
        "ref_max": 2.20,
        "is_safe_limit": False,
        "description": "Potassium – regulates water balance, fruit quality, and disease resistance.",
    },
    "Ca": {
        "display_name": "Calcium",
        "unit": "%",
        "ref_min": 0.74,
        "ref_max": 1.14,
        "is_safe_limit": False,
        "description": "Calcium – essential for cell wall strength and fruit firmness.",
    },
    "Mg": {
        "display_name": "Magnesium",
        "unit": "%",
        "ref_min": 0.51,
        "ref_max": 0.80,
        "is_safe_limit": False,
        "description": "Magnesium – central atom in chlorophyll; needed for photosynthesis.",
    },
    "S": {
        "display_name": "Sulfur",
        "unit": "%",
        "ref_min": 0.14,
        "ref_max": 0.27,
        "is_safe_limit": False,
        "description": "Sulfur – important for protein synthesis and enzyme activity.",
    },
    "Fe": {
        "display_name": "Iron",
        "unit": "ppm",
        "ref_min": 40,
        "ref_max": 80,
        "is_safe_limit": False,
        "description": "Iron – required for chlorophyll synthesis; deficiency causes leaf yellowing.",
    },
    "Mn": {
        "display_name": "Manganese",
        "unit": "ppm",
        "ref_min": 40,
        "ref_max": 100,
        "is_safe_limit": False,
        "description": "Manganese – involved in photosynthesis and enzyme activation.",
    },
    "Zn": {
        "display_name": "Zinc",
        "unit": "ppm",
        "ref_min": 40,
        "ref_max": 100,
        "is_safe_limit": False,
        "description": "Zinc – essential for hormone production and shoot growth.",
    },
    "Cu": {
        "display_name": "Copper",
        "unit": "ppm",
        "ref_min": 5.01,
        "ref_max": 10.00,
        "is_safe_limit": False,
        "description": "Copper – involved in enzyme reactions and lignin formation.",
    },
    "Boron": {
        "display_name": "Boron",
        "unit": "ppm",
        "ref_min": 30,
        "ref_max": 70,
        "is_safe_limit": False,
        "description": "Boron – required for cell wall formation and pollen germination.",
    },
    "Mo": {
        "display_name": "Molybdenum",
        "unit": "ppm",
        "ref_min": 0.25,
        "ref_max": 0.50,
        "is_safe_limit": False,
        "description": "Molybdenum – needed for nitrogen metabolism and enzyme function.",
    },
    "Na": {
        "display_name": "Sodium",
        "unit": "%",
        "safe_limit": 0.5,
        "is_safe_limit": True,
        "description": "Sodium – naturally present in soil; elevated levels may indicate salinity issues.",
    },
    "Cl": {
        "display_name": "Chloride",
        "unit": "%",
        "safe_limit": 0.5,
        "is_safe_limit": True,
        "description": "Chloride – naturally occurring; high levels may affect sensitive crops.",
    },
}

# Ordered list of nutrient keys for consistent display
NUTRIENT_ORDER = [
    "N", "NO3", "NH4_N", "P", "K", "Ca", "Mg", "S",
    "Fe", "Mn", "Zn", "Cu", "Boron", "Mo", "Na", "Cl",
]

# CSV column name mapping → internal key
CSV_COLUMN_MAP = {
    "N": "N",
    "NO3": "NO3",
    "NH4-N": "NH4_N",
    "p": "P",
    "K": "K",
    "Ca": "Ca",
    "Mg": "Mg",
    "S": "S",
    "Fe": "Fe",
    "Mn": "Mn",
    "Zn": "Zn",
    "Cu": "Cu",
    "Boron": "Boron",
    "Mo": "Mo",
    "Na": "Na",
    "Cl": "Cl",
}
