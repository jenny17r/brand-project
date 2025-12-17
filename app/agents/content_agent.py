from typing import Dict, List
import ollama
from app.utils.json_utils import extract_json


class ContentAgent:
    """
    Generates platform-specific marketing content using Brand Persona only
    """

    async def generate(self, payload: Dict):

        platforms: List[str] = payload.get("platforms", ["Instagram"])
        tone = payload.get("tone")

        if not tone or tone == "None":
            tone_instruction = (
                "Infer a suitable brand tone based on the business description."
            )
        else:
            tone_instruction = f"Use this brand tone strictly: {tone}"

        prompt = f"""
You are a professional marketing copywriter.

Create social media content for the following brand.

Business Name: {payload['business_name']}
Business Type: {payload['business_type']}
Description: {payload['description']}
Target Audience: {payload.get('target_audience', 'General audience')}

Platforms to generate content for:
{platforms}

Tone Instruction:
{tone_instruction}

STRICT RULES:
- Generate content separately for EACH platform
- For each platform, generate EXACTLY 3 caption options
- CTA must NOT be empty
- Captions must match the platform style
- Respond ONLY in valid JSON
- Do NOT include markdown
- Do NOT include explanations

JSON format:
{{
  "platforms": {{
    "Instagram": {{
      "captions": ["", "", ""],
      "cta": "",
      "hashtags": []
    }},
    "LinkedIn": {{
      "captions": ["", "", ""],
      "cta": "",
      "hashtags": []
    }}
  }}
}}
"""

        response = ollama.chat(
            model="qwen2.5:1.5b-instruct-q4_0"
,
            messages=[{"role": "user", "content": prompt}]
        )

        raw_output = response["message"]["content"]
        content_data = extract_json(raw_output)

        return content_data
