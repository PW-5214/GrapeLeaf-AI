"""Pydantic models for GrapeLeaf AI API."""

from __future__ import annotations
from typing import Optional, Dict, List, Literal
from pydantic import BaseModel, Field
from datetime import datetime


# ─── Input Models ─────────────────────────────────────────────────────────────

class NutrientValues(BaseModel):
    N: Optional[float] = Field(None, description="Total Nitrogen (%)")
    NO3: Optional[float] = Field(None, description="Nitrate (ppm)")
    NH4_N: Optional[float] = Field(None, description="Ammonium-N (ppm)")
    P: Optional[float] = Field(None, description="Phosphorus (%)")
    K: Optional[float] = Field(None, description="Potassium (%)")
    Ca: Optional[float] = Field(None, description="Calcium (%)")
    Mg: Optional[float] = Field(None, description="Magnesium (%)")
    S: Optional[float] = Field(None, description="Sulfur (%)")
    Fe: Optional[float] = Field(None, description="Iron (ppm)")
    Mn: Optional[float] = Field(None, description="Manganese (ppm)")
    Zn: Optional[float] = Field(None, description="Zinc (ppm)")
    Cu: Optional[float] = Field(None, description="Copper (ppm)")
    Boron: Optional[float] = Field(None, description="Boron (ppm)")
    Mo: Optional[float] = Field(None, description="Molybdenum (ppm)")
    Na: Optional[float] = Field(None, description="Sodium (%)")
    Cl: Optional[float] = Field(None, description="Chloride (%)")


class SampleInput(BaseModel):
    sample_id: Optional[str] = Field(None, max_length=100)
    crop: str = Field(default="Grape", max_length=100)
    location: Optional[str] = Field(None, max_length=200)
    season: Literal["October", "April", "Other"] = Field(default="October")
    nutrients: NutrientValues


# ─── Result Models ─────────────────────────────────────────────────────────────

class NutrientResult(BaseModel):
    nutrient_key: str
    display_name: str
    entered_value: Optional[float]
    unit: str
    reference_range: str
    status: Literal[
        "Low", "Optimum", "High", "Safe", "Above Safe Limit", "Data Unavailable"
    ]
    explanation: str
    recommendation: str


class AnalysisSummary(BaseModel):
    total_analyzed: int
    low: int
    optimum: int
    high: int
    safe: int
    above_safe_limit: int
    data_unavailable: int
    attention_required: int


class AnalysisResponse(BaseModel):
    sample_id: Optional[str]
    crop: str
    location: Optional[str]
    season: str
    season_warning: bool
    analyzed_at: str
    results: List[NutrientResult]
    summary: AnalysisSummary


class StandardInfo(BaseModel):
    nutrient_key: str
    display_name: str
    unit: str
    reference_range: str
    description: str


class StandardsResponse(BaseModel):
    reference_period: str = "October Pruning"
    nutrients: List[StandardInfo]
