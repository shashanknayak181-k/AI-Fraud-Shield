import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

print("=" * 60)
print("Gemini Service Starting...")
print("API Key Found :", API_KEY is not None)

if API_KEY:
    print("API Key Prefix:", API_KEY[:10])
else:
    print("ERROR: GEMINI_API_KEY not found.")

print("=" * 60)

if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not found.")

# -----------------------------
# Configure Gemini
# -----------------------------
genai.configure(api_key=API_KEY)

# -----------------------------
# Load Model
# -----------------------------
model = genai.GenerativeModel("gemini-2.5-flash")


# ===========================================================
# Scam Detection
# ===========================================================
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
        response = model.generate_content(prompt)

        cleaned = (
            response.text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(cleaned)

    except Exception as e:
        return {"error": str(e)}


# ===========================================================
# Currency Detection
# ===========================================================
def analyze_currency(image_path: str):

    try:
        image = Image.open(image_path)

        prompt = """
You are a counterfeit currency detection expert.

Analyze this currency note image.

Return ONLY valid JSON.

{
  "status": "",
  "confidence": "",
  "security_features": [],
  "recommendation": ""
}
"""

        response = model.generate_content([prompt, image])

        cleaned = (
            response.text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(cleaned)

    except Exception as e:
        return {"error": str(e)}


# ===========================================================
# AI Chat Assistant
# ===========================================================
def chat_with_ai(question: str):

    prompt = f"""
You are AI Fraud Shield Assistant.

Answer briefly.

Question:
{question}
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return str(e)