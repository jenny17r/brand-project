from app.agents.brand_persona_agent import BrandPersonaAgent
from app.agents.content_agent import ContentAgent
from app.agents.campaign_agent import CampaignAgent
from app.db.database import SessionLocal
from app.db.models import BrandPersonaModel


class Orchestrator:

    def __init__(self):
        self.brand_persona_agent = BrandPersonaAgent()
        self.content_agent = ContentAgent()
        self.campaign_agent = CampaignAgent()

    async def handle_request(self, payload: dict):

        print("🔹 RAW PAYLOAD:", payload)
        outputs = payload.get("outputs", [])
        print("🔹 OUTPUTS RECEIVED:", outputs)

        results = {}

        # 1️⃣ BRAND PERSONA
        if "brand_persona" in outputs:
            results["brand_persona"] = await self.brand_persona_agent.generate(payload)

        # 🔥 FIX: Fetch persona if ANY downstream agent needs it
        persona = None
        if "content" in outputs or "campaign" in outputs:
            db = SessionLocal()
            persona = (
                db.query(BrandPersonaModel)
                .order_by(BrandPersonaModel.id.desc())
                .first()
            )
            db.close()

        # 3️⃣ CONTENT AGENT
        if "content" in outputs and persona:
            results["content"] = await self.content_agent.generate({
                "business_name": persona.business_name,
                "business_type": persona.business_type,
                "tone": persona.tone,
                "description": persona.description,
                "target_audience": payload.get("target_audience"),
                "platforms": payload.get("platforms", ["Instagram"])
            })

        # 4️⃣ CAMPAIGN AGENT
        if "campaign" in outputs and persona:
            results["campaign"] = await self.campaign_agent.generate({
                "business_name": persona.business_name,
                "location": payload.get("location"),
                "campaign_type": payload.get("campaign_type"),
                "campaign_days": payload.get("campaign_days"),
                "platforms": payload.get("platforms")
            })


        return results
