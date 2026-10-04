"""API integration tests for GrapeLeaf AI."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "GrapeLeaf AI"}


def test_get_standards():
    response = client.get("/api/standards")
    assert response.status_code == 200
    data = response.json()
    assert data["reference_period"] == "October Pruning"
    assert len(data["nutrients"]) == 16
    keys = [n["nutrient_key"] for n in data["nutrients"]]
    assert "N" in keys
    assert "Na" in keys
    assert "Cl" in keys


def test_analyze_sample_october():
    payload = {
        "sample_id": "TEST-101",
        "crop": "Grape",
        "location": "Nashik Valley",
        "season": "October",
        "nutrients": {
            "N": 1.8,
            "NO3": 850,
            "NH4_N": 600,
            "P": 0.55,
            "K": 1.50,
            "Ca": 0.90,
            "Mg": 0.65,
            "S": 0.20,
            "Fe": 60,
            "Mn": 70,
            "Zn": 65,
            "Cu": 7.5,
            "Boron": 45,
            "Mo": 0.35,
            "Na": 0.25,
            "Cl": 0.30,
        },
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["sample_id"] == "TEST-101"
    assert data["season_warning"] is False
    assert data["summary"]["total_analyzed"] == 16
    assert data["summary"]["low"] == 0
    assert data["summary"]["high"] == 0
    assert data["summary"]["above_safe_limit"] == 0
    assert data["summary"]["optimum"] == 14
    assert data["summary"]["safe"] == 2


def test_analyze_sample_non_october_warning():
    payload = {
        "sample_id": "TEST-APRIL",
        "crop": "Grape",
        "location": "Sangli",
        "season": "April",
        "nutrients": {"N": 1.0},
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["season_warning"] is True
    assert data["summary"]["low"] == 1
    assert data["summary"]["data_unavailable"] == 15


def test_pdf_download():
    payload = {
        "sample_id": "PDF-TEST",
        "crop": "Grape",
        "location": "Pune",
        "season": "October",
        "nutrients": {
            "N": 1.10,  # Low
            "P": 0.50,  # Optimum
            "K": 2.50,  # High
            "Na": 0.60, # Above Safe Limit
            "Cl": 0.20, # Safe
        },
    }
    response = client.post("/api/report/pdf", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 1000
    assert response.content.startswith(b"%PDF")


def test_dataset_non_exposure():
    """Verify that no internal CSV path or raw dataset endpoint exists."""
    resp1 = client.get("/api/dataset")
    assert resp1.status_code == 404

    resp2 = client.get("/api/data")
    assert resp2.status_code == 404

    resp3 = client.get("/Petiole_Leaf_Analysis_5000.csv")
    assert resp3.status_code == 404
