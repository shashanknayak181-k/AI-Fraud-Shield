from fastapi import APIRouter
from pydantic import BaseModel
from app.services.gemini_service import analyze_scam

router = APIRouter(
    prefix="/scam",
    tags=["Scam Detector"]
)


class ScamRequest(BaseModel):
    text: str


@router.post("/analyze-text")
def analyze(request: ScamRequest):
    return analyze_scam(request.text)