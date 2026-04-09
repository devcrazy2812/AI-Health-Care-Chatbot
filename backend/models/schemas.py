from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    requires_symptoms: bool = False
    symptoms_context: Optional[str] = None

class DiseasePredictionRequest(BaseModel):
    age: int = Field(..., ge=0, le=120)
    sex: int = Field(..., description="1 = male, 0 = female")
    cp: int = Field(..., description="Chest pain type (0-3)")
    trestbps: int = Field(..., description="Resting blood pressure")
    chol: int = Field(..., description="Serum cholestoral in mg/dl")
    fbs: int = Field(..., description="Fasting blood sugar > 120 mg/dl (1 = true; 0 = false)")
    restecg: int = Field(..., description="Resting electrocardiographic results (0-2)")
    thalach: int = Field(..., description="Maximum heart rate achieved")
    exang: int = Field(..., description="Exercise induced angina (1 = yes; 0 = no)")
    oldpeak: float = Field(..., description="ST depression induced by exercise relative to rest")
    slope: int = Field(..., description="The slope of the peak exercise ST segment (0-2)")
    ca: int = Field(..., description="Number of major vessels (0-3) colored by flourosopy")
    thal: int = Field(..., description="Thal (0-3)")

class DiseasePredictionResponse(BaseModel):
    prediction: int
    probability: float
    risk_level: str
    recommendation: str

class SessionHistory(BaseModel):
    session_id: str
    history: List[Dict[str, str]]
