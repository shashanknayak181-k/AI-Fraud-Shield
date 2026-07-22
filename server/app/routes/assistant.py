from fastapi import APIRouter
from pydantic import BaseModel
from app.services.gemini_service import chat_with_ai

router = APIRouter(
    prefix="/assistant",
    tags=["AI Assistant"]
)

class ChatRequest(BaseModel):
    question: str

@router.post("/chat")
def chat(request: ChatRequest):
    return {
        "answer": chat_with_ai(request.question)
    }
