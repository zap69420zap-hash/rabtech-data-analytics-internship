"""RabTech Task 06: payment-status prediction API.

The model trains on Task 03's cleaned synthetic retail dataset when available.
If that file is absent, a deterministic synthetic fallback keeps the demo runnable.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

import numpy as np
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

CATEGORICAL_FEATURES = ["customer_segment", "city", "category"]
NUMERIC_FEATURES = ["quantity", "unit_price", "discount_pct"]
FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES
TARGET = "payment_status"

app = FastAPI(
    title="RabTech Retail Prediction API",
    description="Demo API returning class probabilities for retail payment status.",
    version="1.0.0",
)


class PredictionRequest(BaseModel):
    customer_segment: str = Field(min_length=1, max_length=80, examples=["Consumer"])
    city: str = Field(min_length=1, max_length=100, examples=["Chennai"])
    category: str = Field(min_length=1, max_length=100, examples=["Electronics"])
    quantity: int = Field(gt=0, le=10000, examples=[2])
    unit_price: float = Field(gt=0, le=100000000, examples=[799.0])
    discount_pct: float = Field(ge=0, le=100, examples=[10.0])


class PredictionResponse(BaseModel):
    predicted_status: str
    probabilities: dict[str, float]
    model_source: Literal["task03_clean_dataset", "synthetic_fallback"]


def _fallback_data(n: int = 1200, seed: int = 42) -> pd.DataFrame:
    """Create reproducible demo data when the Task 03 CSV is unavailable."""
    rng = np.random.default_rng(seed)
    segments = np.array(["Consumer", "Corporate", "Home Office"])
    cities = np.array(["Chennai", "Bengaluru", "Mumbai", "Delhi", "Hyderabad"])
    categories = np.array(["Electronics", "Furniture", "Office Supplies", "Clothing"])
    frame = pd.DataFrame({
        "customer_segment": rng.choice(segments, n),
        "city": rng.choice(cities, n),
        "category": rng.choice(categories, n),
        "quantity": rng.integers(1, 8, n),
        "unit_price": rng.uniform(100, 5000, n).round(2),
        "discount_pct": rng.choice([0, 5, 10, 15, 20, 25], n),
    })
    # Deterministic rule creates learnable demo labels; this is not a real business rule.
    score = (
        0.7 * (frame["discount_pct"] >= 20).astype(int)
        + 0.35 * (frame["quantity"] >= 5).astype(int)
        + 0.2 * (frame["unit_price"] >= 3000).astype(int)
        + rng.normal(0, 0.8, n)
    )
    frame[TARGET] = np.where(score > 0.8, "Pending", np.where(score < -0.3, "Failed", "Paid"))
    return frame


def _find_dataset() -> Path | None:
    configured = os.getenv("TRAINING_DATA_PATH")
    candidates = [
        Path(configured) if configured else None,
        Path("/app/data/clean_dataset.csv"),
        Path(__file__).resolve().parents[1] / "RabTech_Task03_Deliverables" / "clean_dataset.csv",
        Path(__file__).resolve().parent / "clean_dataset.csv",
    ]
    for candidate in candidates:
        if candidate is not None and candidate.is_file():
            return candidate
    return None


def _load_training_data() -> tuple[pd.DataFrame, str]:
    path = _find_dataset()
    if path is not None:
        try:
            df = pd.read_csv(path)
            required = set(FEATURES + [TARGET])
            if required.issubset(df.columns):
                df = df[FEATURES + [TARGET]].dropna()
                df = df[df[TARGET].astype(str).str.strip().ne("")]
                if len(df) >= 30 and df[TARGET].nunique() >= 2:
                    return df, "task03_clean_dataset"
        except (OSError, ValueError, pd.errors.ParserError):
            pass
    return _fallback_data(), "synthetic_fallback"


def _build_model() -> tuple[Pipeline, list[str], str]:
    data, source = _load_training_data()
    x = data[FEATURES].copy()
    y = data[TARGET].astype(str)
    categorical = ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
            ("numeric", StandardScaler(), NUMERIC_FEATURES),
        ]
    )
    model = Pipeline([
        ("preprocessor", categorical),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
    ])
    model.fit(x, y)
    classes = [str(value) for value in model.named_steps["classifier"].classes_]
    return model, classes, source


model, model_classes, model_source = _build_model()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "model_source": model_source}


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "RabTech Retail Prediction API",
        "docs": "/docs",
        "predict": "POST /predict",
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    row = pd.DataFrame([request.model_dump()])[FEATURES]
    probabilities_array = model.predict_proba(row)[0]
    probabilities = {
        label: round(float(probability), 6)
        for label, probability in zip(model_classes, probabilities_array)
    }
    # Keep the rounded values summing to one (within normal floating point tolerance).
    predicted = model_classes[int(np.argmax(probabilities_array))]
    return PredictionResponse(
        predicted_status=predicted,
        probabilities=probabilities,
        model_source=model_source,
    )
