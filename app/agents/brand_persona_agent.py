from typing import Dict
from app.db.database import SessionLocal
from app.db.models import BrandPersonaModel
from app.utils.json_utils import extract_json
import json
import ollama


# -----------------------------
# Schema Guard / Validator
# -----------------------------

def validate_and_fix_persona(persona: dict, fallback_tone: str, business_type: str):
    """
    Validates persona JSON from LLM.
    Fixes non-critical fields.
    Fails fast on critical identity fields.
    """

    fixed = persona.copy()

    # 🔴 Critical fields → MUST exist
    for key in ["business_name", "description"]:
        if key not in fixed or not fixed[key]:
            raise ValueError(f"Missing critical key in persona JSON: {key}")

    # 🟡 Controlled fields (system-owned)
    fixed["business_type"] = business_type
    fixed["tone"] = fixed.get("tone") or fallback_tone or "friendly"

    # 🟢 Optional fields with safe defaults
    if not fixed.get("tagline"):
        fixed["tagline"] = ""

    if not isinstance(fixed.get("color_palette"), list):
        fixed["color_palette"] = ["#000000", "#FFFFFF", "#CCCCCC"]

    return fixed


# -----------------------------
# Brand Persona Agent
# -----------------------------

class BrandPersonaAgent:

    async def generate(self, payload: Dict):

        # --- Input normalization ---
        raw_name = payload.get("business_name")
        business_name = raw_name.strip() if isinstance(raw_name, str) else ""

        business_type = payload.get("business_type", "business")
        location = payload.get("location", "your area")
        target_audience = payload.get("target_audience", "local customers")
        tone = payload.get("tone") or "friendly"

        # --- Name rule ---
        if business_name == "":
            name_instruction = (
                "You MUST create a unique, attractive, brandable business name."
            )
        else:
            name_instruction = f"Use this exact business name: {business_name}"

        # --- Prompt ---
        prompt = f"""
You are a professional brand persona generator.

{name_instruction}

Business Type: {business_type}
Location: {location}
Target Audience: {target_audience}
Tone: {tone}

Rules:
- Respond ONLY with valid JSON
- No explanations
- No markdown
- No comments
- Use double quotes everywhere

JSON format:
{{
  "business_name": "",
  "business_type": "{business_type}",
  "tone": "{tone}",
  "tagline": "",
  "color_palette": ["#hex1", "#hex2", "#hex3"],
  "description": ""
}}
"""

        # --- LLM Call ---
        response = ollama.chat(
            model="qwen2.5:1.5b-instruct-q4_0",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_output = response["message"]["content"]

        # --- Extract JSON ---
        persona_data = extract_json(raw_output)

        # --- Validate & Self-heal ---
        persona_data = validate_and_fix_persona(
            persona=persona_data,
            fallback_tone=tone,
            business_type=business_type
        )

        # --- Persist to DB ---
        db = SessionLocal()
        new_persona = BrandPersonaModel(
            business_name=persona_data["business_name"],
            business_type=persona_data["business_type"],
            tone=persona_data["tone"],
            tagline=persona_data["tagline"],
            color_palette=json.dumps(persona_data["color_palette"]),
            description=persona_data["description"]
        )

        db.add(new_persona)
        db.commit()
        db.refresh(new_persona)
        db.close()

        return {
            "brand_persona_id": new_persona.id,
            "brand_persona": persona_data
        }
