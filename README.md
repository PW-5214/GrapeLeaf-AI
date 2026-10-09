# GrapeLeaf AI – Smart Petiole/Leaf Nutrient Analysis and Farmer Advisory System

GrapeLeaf AI is a full-stack, viticulture-focused decision support application built to analyze grape petiole and leaf nutrient laboratory values against official **Petiole Reference Standards**.

---

## 🍇 Architecture & Features

- **Frontend**: React 19, TypeScript, Vite, Tailwind CSS v4, Lucide React icons, Responsive navigation, Accessible status badges (color + label + icon).
- **Backend**: Python 3.11, FastAPI, Pydantic v2 schemas, ReportLab PDF generator, Pytest (41 tests).
- **5-Model Ensemble ML Engine**: Supports **Random Forest** (200 trees), **XGBoost** (300 estimators), **CatBoost** (300 iterations), **LightGBM** (300 estimators), and **Gradient Boosting** (150 estimators) classification alongside rule-based reference limits.
- **Reviewer Comparison Notebook**: Comprehensive Jupyter Notebook (`Petiole_Nutrient_Model_Comparison.ipynb` & `notebooks/`) with cross-validation comparisons, confusion matrices, class distribution plots, and feature importance rankings.
- **Classification Engine**: Transparent reference classification:
  - Nutrients with min–max: **Low** (< min), **Optimum** (min ≤ val ≤ max, inclusive boundaries), **High** (> max).
  - Sodium (Na) & Chloride (Cl): **Safe** (< 0.5%), **Above Safe Limit** (≥ 0.5%).
  - Missing/invalid values: **Data Unavailable** (never converted to zero or Low).
- **PDF Report**: 3-page structured report with executive summary, complete results table, grouped observations, precautions, next steps, and educational disclaimer.
- **Dataset Privacy**: The internal research dataset `Petiole_Leaf_Analysis_5000.csv` is maintained strictly inside the private backend directory `backend/app/data/` and is never exposed through API routes or frontend bundles.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 2. Backend Setup & Start
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```
Backend API will be live at `http://127.0.0.1:8000`.
Interactive API documentation: `http://127.0.0.1:8000/api/docs`.

### 3. Frontend Setup & Start
```bash
cd frontend
npm install
npm run dev
```
Frontend application will be live at `http://127.0.0.1:5173`.

---

## 🧪 Running Tests

```bash
cd backend
python -m pytest tests/ -v
```
All 43 tests cover boundary conditions, missing values, Na/Cl limits, recommendation logic, API routes, all 5 ML models, and dataset non-exposure.

---

## 📄 Application Pages

1. **Home (`/`)**: Hero section with vineyard identity, how it works, petiole science, features, precautions, and disclaimer.
2. **Analyze Sample (`/analyze`)**: Form supporting all 16 parameters (N, NO3, NH4-N, P, K, Ca, Mg, S, Fe, Mn, Zn, Cu, Boron, Mo, Na, Cl), season selection with October advisory warning, and sample pre-fill.
3. **My Report (`/report`)**: Summary cards (Total Analyzed, Optimum, Low, High, Safe, Above Safe Limit, Requiring Attention), filterable results table, educational next steps, and instant PDF download.
4. **Reference Standards (`/standards`)**: Reference table with macronutrient, micronutrient, and salinity category filtering, and agronomic variability factors.
5. **About GrapeLeaf AI (`/about`)**: Viticulture mission, architectural principles, privacy design, and technology stack.

---

## ⚖️ Educational Disclaimer

This application provides educational decision support based on entered values and configured reference standards. It is not a substitute for professional agricultural advice. Verify recommendations with a qualified agricultural expert before taking corrective action. No guaranteed yield improvement, disease detection, or crop recovery is promised or implied.
