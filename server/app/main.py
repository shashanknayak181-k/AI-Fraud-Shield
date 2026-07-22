from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.scam import router as scam_router
from app.routes.currency import router as currency_router
from app.routes.assistant import router as assistant_router
app = FastAPI(
    title="AI Fraud Shield API",
    version="1.0.0"
)

# Allow React frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(scam_router)
app.include_router(currency_router)
app.include_router(assistant_router)

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "AI Fraud Shield Backend Running 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }