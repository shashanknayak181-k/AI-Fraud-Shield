import os
import json
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

MODEL = "gemini-2.5-flash"

# ==========================================
# Scam Detection
# ==========================================

def analyze_scam(text: str):

    prompt = f"""
You are a cybersecurity expert.

Analyze the message below.

Return ONLY valid JSON.

{{
  "risk_score": 0,
  "fraud_type": "",
  "explanation": "",
  "recommendation": ""
}}

Message:
{text}
"""

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        cleaned = (
            response.text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(cleaned)

    except Exception as e:
        return {
            "error": str(e)
        }


# ==========================================
# Currency Detection
# ==========================================

def analyze_currency(image_path: str):

    try:

        image = Image.open(image_path)

        prompt = """
You are a counterfeit currency detection expert.

Analyze this currency note.

Return ONLY valid JSON.

{
  "status":"",
  "confidence":"",
  "security_features":[],
  "recommendation":""
}
"""

        response = client.models.generate_content(
            model=MODEL,
            contents=[
                prompt,
                image
            ]
        )

        cleaned = (
            response.text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(cleaned)

    except Exception as e:

        return {
            "error": str(e)
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