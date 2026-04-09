from fastapi import APIRouter
from services.llm_service import llm_service

router = APIRouter()

@router.get("/{session_id}")
async def get_history(session_id: str):
    history = llm_service.get_history(session_id)
    # Filter out system prompt for the frontend
    filtered_history = [msg for msg in history if msg["role"] != "system"]
    return {"session_id": session_id, "history": filtered_history}
