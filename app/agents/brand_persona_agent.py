from typing import Dict
from app.db.database import SessionLocal
from app.db.models import BrandPersonaModel
import json
import ollama
import re


def extract_json(text: str):
    """
    Extract JSON from LLM output even if:
    - It contains extra text
    - Markdown fences
    - Single quotes
    - Comments
    """
    # Remove Markdown fences
    cleaned = text.replace("```json", "").replace("```", "").strip()

    # Try direct JSON load
    try:
        return json.loads(cleaned)
    except:
        pass

    # Find JSON with regex
    match = re.search(r"\{[\s\S]*\}", cleaned)
    if match:
        json_str = match.group()

        # Replace single quotes with double quotes
        json_str = json_str.replace("'", '"')

        return json.loads(json_str)

    raise ValueError("Could not extract JSON from model output.")


class BrandPersonaAgent:

    async def generate(self, payload: Dict):

        # ----------- INPUT HANDLING -----------------------
        raw_name = payload.get("business_name")
        business_name = raw_name.strip() if isinstance(raw_name, str) else ""

        business_type = payload.get("business_type")
        location = payload.get("location", "your area")
        target_audience = payload.get("target_audience", "local customers")
        tone = payload.get("tone", "friendly")

        # Decide if AI needs to generate a business name
        if business_name == "":
            name_instruction = "You MUST create a unique, attractive, brandable business name."
            business_name_placeholder = "AI_GENERATE_NAME"
        else:
            name_instruction = f"Use this exact business name: {business_name}"
            business_name_placeholder = business_name

        # ----------- IMPROVED JSON-STRICT PROMPT -----------------------
        prompt = f"""
        Act as a professional brand persona generator.

        {name_instruction}

        Business Type: {business_type}
        Location: {location}
        Target Audience: {target_audience}
        Tone: {tone}

        Respond ONLY in VALID JSON.
        No explanations. No markdown. No comments.

        JSON OUTPUT FORMAT:

        {{
            "business_name": "",
            "business_type": "{business_type}",
            "tone": "{tone}",
            "tagline": "",
            "color_palette": ["#hex1", "#hex2", "#hex3"],
            "description": ""
        }}
        """

        # ----------- CALL OLLAMA (phi3:mini) -----------------------
        response = ollama.chat(
            model="phi3:mini",
            messages=[{"role": "user", "content": prompt}]
        )

        llm_output = response["message"]["content"]

        # ----------- SAFE JSON PARSING ------------------------------
        persona_data = extract_json(llm_output)

        # ----------- SAVE TO DATABASE -------------------------------
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

        # ----------- RETURN RESPONSE -------------------------------
        return {
            "brand_persona_id": new_persona.id,
            "brand_persona": persona_data
        }
