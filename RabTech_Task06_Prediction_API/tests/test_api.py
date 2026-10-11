import math
from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import app as prediction_app  # noqa: E402

client = TestClient(prediction_app.app)

VALID_PAYLOAD = {
    "customer_segment": "Consumer",
    "city": "Chennai",
    "category": "Electronics",
    "quantity": 2,
    "unit_price": 799.0,
    "discount_pct": 10.0,
}


def test_health_endpoint_returns_200_and_model_source():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model_source"] in {"task03_clean_dataset", "synthetic_fallback"}


def test_root_endpoint_describes_api():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["predict"] == "POST /predict"


def test_predict_returns_schema_and_probabilities():
    response = client.post("/predict", json=VALID_PAYLOAD)
    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"predicted_status", "probabilities", "model_source"}
    assert body["predicted_status"] in body["probabilities"]
    assert body["model_source"] in {"task03_clean_dataset", "synthetic_fallback"}
    assert body["probabilities"]
    assert all(0.0 <= p <= 1.0 for p in body["probabilities"].values())
    assert math.isclose(sum(body["probabilities"].values()), 1.0, abs_tol=0.00002)


def test_predict_rejects_invalid_values_with_422():
    payload = {**VALID_PAYLOAD, "quantity": 0}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_rejects_missing_fields_with_422():
    payload = {key: value for key, value in VALID_PAYLOAD.items() if key != "city"}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_model_has_at_least_two_classes_and_probability_api():
    assert len(prediction_app.model_classes) >= 2
    assert hasattr(prediction_app.model, "predict_proba")
