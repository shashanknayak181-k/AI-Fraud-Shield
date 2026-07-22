import os
import json
import re
from dotenv import load_dotenv
from PIL import Image
from google import genai

# ----------------------------------
# Load Environment Variables
# ----------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found.")

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-2.0-flash"

# ==========================================
# Utility Functions
# ==========================================

def clean_json_response(text: str):
    """Extract and parse JSON safely from Gemini response."""

    if not text:
        return {}

    cleaned = (
        text.replace("```json", "")
        .replace("```", "")
        .strip()
    )

    # Extract JSON object if Gemini adds extra text
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)

    if match:
        cleaned = match.group(0)

    try:
        return json.loads(cleaned)
    except Exception:
        return {}


# ==========================================
# Scam Detection
# ==========================================

def analyze_scam(text: str):

    prompt = f"""
You are an expert cybercrime analyst.

Analyze the following message.

Return ONLY valid JSON.

{{
  "risk_score": 0,
  "fraud_type": "",
  "explanation": "",
  "recommendation": ""
}}

Rules:
- risk_score must be between 0 and 100.
- Return JSON only.
- No markdown.
- No explanation outside JSON.

Message:
{text}
"""

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        data = clean_json_response(response.text)

        return {
            "risk_score": data.get("risk_score", 0),
            "fraud_type": data.get("fraud_type", "Unknown"),
            "explanation": data.get(
                "explanation",
                "Unable to analyze."
            ),
            "recommendation": data.get(
                "recommendation",
                "Exercise caution."
            )
        }

    except Exception as e:

        return {
            "risk_score": 0,
            "fraud_type": "Error",
            "explanation": str(e),
            "recommendation": "Please try again."
        }


# ==========================================
# Currency Detection
# ==========================================

def analyze_currency(image_path: str):

    try:

        image = Image.open(image_path)

        prompt = """
You are an RBI currency authentication expert.

Analyze this Indian currency note carefully.

Return ONLY valid JSON.

{
  "status": "",
  "confidence": "",
  "security_features": "",
  "recommendation": ""
}

Rules:

1. status MUST be exactly one of:
- Authentic
- Likely Genuine
- Suspicious
- Likely Counterfeit

2. confidence MUST be exactly one of:
- Low
- Medium
- High

3. security_features MUST always contain a detailed paragraph explaining the visible security features.

4. recommendation MUST always contain user advice.

5. Return JSON ONLY.

6. Do not use markdown.

7. Do not use ```json.
"""

        response = client.models.generate_content(
            model=MODEL,
            contents=[
                prompt,
                image
            ]
        )

        data = clean_json_response(response.text)

        return {
            "status": data.get(
                "status",
                "Suspicious"
            ),
            "confidence": data.get(
                "confidence",
                "Medium"
            ),
            "security_features": data.get(
                "security_features",
                "Unable to identify security features with sufficient confidence."
            ),
            "recommendation": data.get(
                "recommendation",
                "Have the currency verified by a bank or authorized authority before accepting or using it."
            )
        }

    except Exception as e:

        return {
            "status": "Error",
            "confidence": "Low",
            "security_features": str(e),
            "recommendation": "Please try another image."
        }


# ==========================================
# AI Chat
# ==========================================

def chat_with_ai(question: str):

    prompt = f"""
You are AI Fraud Shield Assistant.

Answer in less than 150 words.

Question:

{question}
"""

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text

    except Exception as e:

        return str(e)