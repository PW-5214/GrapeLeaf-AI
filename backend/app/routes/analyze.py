"""FastAPI routes for nutrient analysis — supports model_type selection."""

from __future__ import annotations
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from app.models.schemas import SampleInput, AnalysisResponse, AnalysisSummary, ModelsListResponse, ModelInfo
from app.services.classifier import classify_sample
from app.services.ml_service import predict_vine_status, list_available_models

router = APIRouter(prefix="/api", tags=["analyze"])


@router.get("/models", response_model=ModelsListResponse)
async def get_available_models() -> ModelsListResponse:
    """Return metadata for all available trained ML models."""
    raw = list_available_models()
    return ModelsListResponse(models=[ModelInfo(**m) for m in raw])


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_sample(body: SampleInput) -> AnalysisResponse:
    """
    Classify all submitted nutrient values against October Pruning Reference Standards.
    Runs ML Vine Status prediction using the user-selected model (rf or xgb).
    """
    nutrient_dict = {
        "N":      body.nutrients.N,
        "NO3":    body.nutrients.NO3,
        "NH4_N":  body.nutrients.NH4_N,
        "P":      body.nutrients.P,
        "K":      body.nutrients.K,
        "Ca":     body.nutrients.Ca,
        "Mg":     body.nutrients.Mg,
        "S":      body.nutrients.S,
        "Fe":     body.nutrients.Fe,
        "Mn":     body.nutrients.Mn,
        "Zn":     body.nutrients.Zn,
        "Cu":     body.nutrients.Cu,
        "Boron":  body.nutrients.Boron,
        "Mo":     body.nutrients.Mo,
        "Na":     body.nutrients.Na,
        "Cl":     body.nutrients.Cl,
    }

    results    = classify_sample(nutrient_dict)
    ml_result  = predict_vine_status(nutrient_dict, model_key=body.model_type)

    low        = sum(1 for r in results if r.status == "Low")
    optimum    = sum(1 for r in results if r.status == "Optimum")
    high       = sum(1 for r in results if r.status == "High")
    safe       = sum(1 for r in results if r.status == "Safe")
    above_safe = sum(1 for r in results if r.status == "Above Safe Limit")
    unavail    = sum(1 for r in results if r.status == "Data Unavailable")
    attention  = low + high + above_safe

    summary = AnalysisSummary(
        total_analyzed=len(results) - unavail,
        low=low,
        optimum=optimum,
        high=high,
        safe=safe,
        above_safe_limit=above_safe,
        data_unavailable=unavail,
        attention_required=attention,
    )

    return AnalysisResponse(
        sample_id=body.sample_id,
        crop=body.crop,
        location=body.location,
        season=body.season,
        season_warning=(body.season != "October"),
        analyzed_at=datetime.now(timezone.utc).isoformat(),
        results=results,
        summary=summary,
        ml_prediction=ml_result,
    )
