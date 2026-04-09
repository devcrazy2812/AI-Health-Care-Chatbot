from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.chat import router as chat_router
from api.predict import router as predict_router
from api.history import router as history_router

app = FastAPI(
    title="AI Healthcare Assistant API",
    description="Backend API for managing chatting and medical prediction. Developed by devcrazy AKA Abhay Goyal.",
    version="1.0.0"
)

# Allow CORS for React frontend (default typical ports)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, restrict this to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(predict_router, prefix="/api/predict", tags=["predict"])
app.include_router(history_router, prefix="/api/history", tags=["history"])

@app.get("/")
def health_check():
    return {"status": "ok", "message": "API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
