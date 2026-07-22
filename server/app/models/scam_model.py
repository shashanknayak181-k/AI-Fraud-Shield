from pydantic import BaseModel


class ScamRequest(BaseModel):
    text: str


class ScamResponse(BaseModel):
    risk_score: int
    scam_type: str
    explanation: str
    recommendation: str