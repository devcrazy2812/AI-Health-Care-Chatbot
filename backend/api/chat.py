from fastapi import APIRouter, HTTPException
from models.schemas import ChatRequest, ChatResponse
from services.llm_service import llm_service

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        response = llm_service.generate_response(
            session_id=request.session_id,
            user_message=request.message
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
