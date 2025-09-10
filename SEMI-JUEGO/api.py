from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict

from formulas import list_formulas_for_api, calculate_by_id, PREFIXES

app = FastAPI(title="API Calculadora de Telecomunicaciones", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CalculatePayload(BaseModel):
    formula_id: str = Field(..., description="Identificador de la fórmula")
    values: Dict[str, float] = Field(..., description="Valores numéricos en SI")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/prefixes")
def prefixes():
    return PREFIXES

@app.get("/formulas")
def formulas():
    return list_formulas_for_api()

@app.post("/calculate")
def calculate(payload: CalculatePayload):
    try:
        return calculate_by_id(payload.formula_id, payload.values)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
