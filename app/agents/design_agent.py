from typing import Dict
import ollama
from app.utils.json_utils import extract_json


class DesignAgent:

    async def generate(self, payload: Dict):

        prompt = f"""
        Create a marketing design plan for the following brand.

        Business Name: {payload['business_name']}
        Description: {payload['description']}
        Tone: {payload['tone']}
        Colors: {payload['color_palette']}

        Rules:
        - Respond ONLY in valid JSON
        - Do NOT include markdown
        - Do NOT include explanations

        JSON format:
        {{
            "design_style": "",
            "layout_description": "",
            "typography": "",
            "color_usage": [],
            "stable_diffusion_prompt": ""
        }}
        """

        response = ollama.chat(
            model="phi3:mini",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_output = response["message"]["content"]

        design_data = extract_json(raw_output)

        return design_data
