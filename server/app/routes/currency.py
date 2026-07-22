import os
import tempfile

from fastapi import APIRouter, UploadFile, File
from app.services.gemini_service import analyze_currency

router = APIRouter(
    prefix="/currency",
    tags=["Currency Detector"]
)


@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
        temp.write(await file.read())
        temp_path = temp.name

    try:
        result = analyze_currency(temp_path)
        return result

    finally:
        os.remove(temp_path)