"""PDF report download route."""

from __future__ import annotations
from fastapi import APIRouter
from fastapi.responses import Response
from app.models.schemas import SampleInput, AnalysisResponse, AnalysisSummary
from app.services.classifier import classify_sample
from app.services.ml_service import predict_vine_status
from app.services.pdf_generator import generate_pdf
from datetime import datetime, timezone

router = APIRouter(prefix="/api/report", tags=["report"])


@router.post("/pdf")
async def download_pdf(body: SampleInput) -> Response:
    """
    Generate and return a 3-page PDF report for the submitted sample.
    No CSV data is included in the report.
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

    results = classify_sample(nutrient_dict)
    ml_result = predict_vine_status(nutrient_dict, model_key=body.model_type)

    low = sum(1 for r in results if r.status == "Low")
    optimum = sum(1 for r in results if r.status == "Optimum")
    high = sum(1 for r in results if r.status == "High")
    safe = sum(1 for r in results if r.status == "Safe")
    above_safe = sum(1 for r in results if r.status == "Above Safe Limit")
    unavail = sum(1 for r in results if r.status == "Data Unavailable")

    analysis = AnalysisResponse(
        sample_id=body.sample_id,
        crop=body.crop,
        location=body.location,
        season=body.season,
        season_warning=(body.season != "October"),
        analyzed_at=datetime.now(timezone.utc).isoformat(),
        results=results,
        summary=AnalysisSummary(
            total_analyzed=len(results) - unavail,
            low=low,
            optimum=optimum,
            high=high,
            safe=safe,
            above_safe_limit=above_safe,
            data_unavailable=unavail,
            attention_required=low + high + above_safe,
        ),
        ml_prediction=ml_result,
    )

    pdf_bytes = generate_pdf(analysis)
    filename = f"GrapeLeafAI_Report_{body.sample_id or 'sample'}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
