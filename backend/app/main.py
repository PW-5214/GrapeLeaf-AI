"""
GrapeLeaf AI – FastAPI Application Entry Point

Security notes:
  - CSV dataset is in backend/app/data/ and is NEVER served through any API.
  - All farmer data is transient (not stored).
  - CORS is restricted to local development by default.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.analyze import router as analyze_router
from app.routes.report import router as report_router
from app.routes.standards import router as standards_router

app = FastAPI(
    title="GrapeLeaf AI",
    description=(
        "Smart Petiole/Leaf Nutrient Analysis and Farmer Advisory System. "
        "Provides educational decision support based on October Pruning Reference Standards."
    ),
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url=None,
)

# CORS – restrict to local frontend in development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(analyze_router)
app.include_router(report_router)
app.include_router(standards_router)


@app.get("/api/health", tags=["health"])
async def health_check():
    return {"status": "ok", "service": "GrapeLeaf AI"}
