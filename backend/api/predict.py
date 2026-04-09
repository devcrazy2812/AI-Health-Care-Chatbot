from fastapi import APIRouter, HTTPException
from models.schemas import DiseasePredictionRequest, DiseasePredictionResponse
from services.ml_service import ml_service

router = APIRouter()

@router.post("/", response_model=DiseasePredictionResponse)
async def predict_endpoint(request: DiseasePredictionRequest):
    try:
        response = ml_service.predict(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
