import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_scam(text: str):
    prompt = f"""
You are a cybersecurity expert.

Analyze the message below.

Return ONLY valid JSON.

Format:

{{
  "risk_score": 0,
  "fraud_type": "",
  "explanation": "",
  "recommendation": ""
}}

Message:
{text}
"""

    response = model.generate_content(prompt)

    cleaned = (
        response.text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    return json.loads(cleaned)

def analyze_currency(image_path: str):
   with Image.open(image_path) as img:
    image = img.copy()
    prompt = """
You are a counterfeit currency detection expert.

Analyze this currency note image.

Return ONLY valid JSON in this format:

{
  "status": "",
  "confidence": "",
  "security_features": [],
  "recommendation": ""
}

Rules:
- status should be "Likely Genuine", "Suspicious", or "Unable to Determine".
- confidence should be a percentage like "92%".
- security_features should list visible security features or missing features.
- Do not include markdown.
"""

    response = model.generate_content([prompt, image])

    cleaned = (
        response.text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    return json.loads(cleaned)
   
def chat_with_ai(question: str):
    prompt = f"""
You are AI Fraud Shield Assistant.

Your role:
- Answer questions about cyber fraud.
- Explain phishing, OTP scams, UPI fraud, fake websites, digital arrest scams and counterfeit currency.
- Give short, practical advice.
- If unsure, clearly say so.
- Keep responses under 150 words.

Question:
{question}
"""

    response = model.generate_content(prompt)

    return response.text 