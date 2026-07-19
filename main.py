"""
No-Drift API - Core Gateway Architecture
Copyright (c) 2026 Mozart Software Architects & Muhammad Abdullah
Licensed under the Custom Public Evaluation & Commercial Compliance License.
"""

import math
from typing import Dict, List, Any
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="No-Drift API",
    description="Custom Commercial Governance and AI Schema Protection Gateway",
    version="1.2.0"
)

# --- Schemas ---
class FeatureBaseline(BaseModel):
    feature_name: str
    expected_distribution: Dict[str, float]

class DriftAnalysisRequest(BaseModel):
    baseline: List[FeatureBaseline]
    inference_data: List[Dict[str, Any]]
    threshold: float = Field(default=0.1)

class FeatureDriftResult(BaseModel):
    feature_name: str
    psi_score: float
    drift_detected: bool
    status: str

class DriftResponse(BaseModel):
    status: str
    drift_summary: List[FeatureDriftResult]
    global_drift_detected: bool

# --- Core Business Logic ---
def calculate_psi(expected: Dict[str, float], actual: List[Any]) -> float:
    total_samples = len(actual)
    if total_samples == 0:
        return 0.0  # Prevents ZeroDivisionError if execution batch is empty

    actual_counts: Dict[str, int] = {}
    for item in actual:
        val = str(item)
        actual_counts[val] = actual_counts.get(val, 0) + 1

    psi_value = 0.0
    epsilon = 0.0001 

    for category, exp_prop in expected.items():
        act_count = actual_counts.get(category, 0)
        act_prop = act_count / total_samples

        # Apply boundary smoothing values before computing natural logs
        safe_act = max(act_prop, epsilon)
        safe_exp = max(exp_prop, epsilon)

        psi_value += (safe_act - safe_exp) * math.log(safe_act / safe_exp)

    return round(psi_value, 4)

# --- Endpoints ---
@app.post("/api/v1/verify-drift", response_model=DriftResponse, status_code=status.HTTP_200_OK)
async def verify_drift(payload: DriftAnalysisRequest):
    try:
        summary = []
        global_drift = False

        for feat in payload.baseline:
            observations = [
                row[feat.feature_name] 
                for row in payload.inference_data 
                if feat.feature_name in row
            ]

            if not observations:
                continue

            psi_score = calculate_psi(feat.expected_distribution, observations)
            is_drifted = psi_score >= payload.threshold
            
            if is_drifted:
                global_drift = True

            summary.append(FeatureDriftResult(
                feature_name=feat.feature_name,
                psi_score=psi_score,
                drift_detected=is_drifted,
                status="DRIFT_ALERT" if is_drifted else "STABLE"
            ))

        return DriftResponse(
            status="SUCCESS",
            drift_summary=summary,
            global_drift_detected=global_drift
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Governance gateway engine error: {str(e)}"
        )

@app.get("/healthz", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "healthy", "service": "No-Drift API"}