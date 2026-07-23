import os
import json
import base64
import re

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found.")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
    default_headers={
        "HTTP-Referer": "https://ai-fraud-shield-two.vercel.app",
        "X-Title": "AI Fraud Shield",
    },
)

TEXT_MODEL = "openai/gpt-oss-20b:free"
VISION_MODEL = "qwen/qwen2.5-vl-72b-instruct:free"


def clean_json_response(text: str):
    """Extract JSON safely."""

    if not text:
        return {}

    cleaned = text.replace("```json", "").replace("```", "").strip()

    match = re.search(r"\{.*\}", cleaned, re.DOTALL)

    if match:
        cleaned = match.group(0)

    try:
        return json.loads(cleaned)
    except Exception:
        return {}


def encode_image(image_path: str):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


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

        response = client.chat.completions.create(
            model=TEXT_MODEL,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI fraud detection expert."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response.choices[0].message.content or ""

        data = clean_json_response(content)

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
        
def analyze_currency(image_path: str):

    try:

        image_base64 = encode_image(image_path)

        extension = os.path.splitext(image_path)[1].lower()

        mime = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
        }.get(extension, "image/jpeg")

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

1. status must be exactly one of:
- Authentic
- Likely Genuine
- Suspicious
- Likely Counterfeit

2. confidence must be exactly one of:
- Low
- Medium
- High

3. security_features must explain all visible security features in detail.

4. recommendation must provide advice to the user.

5. Return JSON only.

6. No markdown.
"""

        response = client.chat.completions.create(
            model=VISION_MODEL,
            temperature=0.2,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime};base64,{image_base64}"
                            },
                        },
                    ],
                }
            ],
        )

        content = response.choices[0].message.content or ""

        data = clean_json_response(content)

        return {
            "status": data.get("status", "Suspicious"),
            "confidence": data.get("confidence", "Medium"),
            "security_features": data.get(
                "security_features",
                "Unable to identify security features with sufficient confidence.",
            ),
            "recommendation": data.get(
                "recommendation",
                "Have the currency verified by a bank or authorized authority before accepting or using it.",
            ),
        }

    except Exception as e:

        return {
            "status": "Error",
            "confidence": "Low",
            "security_features": str(e),
            "recommendation": "Please try another image.",
        }


def chat_with_ai(question: str):

    prompt = f"""
You are AI Fraud Shield Assistant.

Rules:

- Answer in less than 150 words.
- Give practical fraud prevention advice.
- Keep the answer concise.
- If applicable, include safety tips.

Question:

{question}
"""

    try:

        response = client.chat.completions.create(
            model=TEXT_MODEL,
            temperature=0.4,
            messages=[
                {
                    "role": "system",
                    "content": "You are AI Fraud Shield Assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return (response.choices[0].message.content or "").strip()

    except Exception as e:
        return str(e)