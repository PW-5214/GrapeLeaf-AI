"""Reference standards public endpoint – no CSV data exposed."""

from __future__ import annotations
from fastapi import APIRouter
from app.models.schemas import StandardsResponse, StandardInfo
from app.config.standards import OCTOBER_STANDARDS, NUTRIENT_ORDER

router = APIRouter(prefix="/api", tags=["standards"])


@router.get("/standards", response_model=StandardsResponse)
async def get_standards() -> StandardsResponse:
    """Return October Pruning Reference Standards for display purposes."""
    nutrients = []
    for key in NUTRIENT_ORDER:
        std = OCTOBER_STANDARDS[key]
        if std["is_safe_limit"]:
            ref_range = f"Less than {std['safe_limit']} {std['unit']}"
        else:
            ref_range = f"{std['ref_min']}–{std['ref_max']} {std['unit']}"
        nutrients.append(StandardInfo(
            nutrient_key=key,
            display_name=std["display_name"],
            unit=std["unit"],
            reference_range=ref_range,
            description=std["description"],
        ))

    return StandardsResponse(
        reference_period="October Pruning",
        nutrients=nutrients,
    )
