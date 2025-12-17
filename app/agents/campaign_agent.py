from typing import Dict, List
import ollama
from app.utils.json_utils import extract_json
from app.rag.retriever import FestivalRetriever


class CampaignAgent:
    """
    Plans a multi-day marketing campaign using Brand Persona + RAG
    """

    def __init__(self):
        self.retriever = FestivalRetriever()

    async def generate(self, payload: Dict):

        campaign_days = payload.get("campaign_days", 7)
        campaign_type = payload.get("campaign_type", "campaign")
        platforms = payload.get("platforms", ["Instagram"])
        location = payload.get("location", "")

        # 🔹 STEP 1: RAG – retrieve festival knowledge
        festival_context = []
        if campaign_type:
            festival_context = self.retriever.search(
                query=f"{campaign_type} festival in {location} for cafe promotion",
                limit=3
            )

        # 🔹 STEP 2: Convert RAG output to readable context
        festival_text = ""
        if festival_context:
            lines = []
            for f in festival_context:
                lines.append(
                    f"- {f['name']} ({f['region']}): {f['description']} | Marketing angles: {', '.join(f['marketing_angles'])}"
                )
            festival_text = "\n".join(lines)
        else:
            festival_text = "No specific festival data found."

        # 🔹 STEP 3: Build prompt (NO JSON ARRAYS INSIDE f-string)
        prompt = f"""
You are a senior digital marketing strategist.

Brand Details:
Business Name: {payload.get('business_name')}
Business Type: {payload.get('business_type')}
Brand Description: {payload.get('description')}
Brand Tone: {payload.get('tone', 'Infer suitable tone')}

Campaign Type:
{campaign_type}

Campaign Duration:
{campaign_days} days

Platforms:
{", ".join(platforms)}

Festival Knowledge (from knowledge base):
{festival_text}

STRICT RULES:
- Campaign duration MUST be exactly {campaign_days} days
- Create ONE entry per day (day 1 to day {campaign_days})
- EACH platform MUST have {campaign_days} objects
- Do NOT skip days
- Use unique themes per day
- Respond ONLY with valid JSON
- Use double quotes for all keys and string values
- Do NOT include markdown, comments, or explanations

Required JSON structure:
{{
  "campaign_name": "",
  "campaign_goal": "",
  "duration_days": {campaign_days},
  "platforms": {{
    "<platform_name>": [
      {{
        "day": 1,
        "theme": "",
        "content_type": "",
        "posting_time": ""
      }}
    ]
  }}
}}
"""

        # 🔹 STEP 4: Call LLM
        response = ollama.chat(
            model="qwen2.5:1.5b-instruct-q4_0",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_output = response["message"]["content"]

        print("\n🔴 RAW CAMPAIGN OUTPUT FROM LLM:\n")
        print(raw_output)
        print("\n🔴 END RAW OUTPUT\n")

        campaign_data = extract_json(raw_output)


        return campaign_data

