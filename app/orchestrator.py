from app.agents.brand_persona_agent import BrandPersonaAgent
from app.agents.design_agent import DesignAgent
from app.agents.image_generation_agent import ImageGenerationAgent
from app.db.database import SessionLocal
from app.db.models import BrandPersonaModel


class Orchestrator:

    def __init__(self):
        self.brand_persona_agent = BrandPersonaAgent()
        self.design_agent = DesignAgent()
        self.image_agent = ImageGenerationAgent()

    async def handle_request(self, payload: dict):

        results = {}
        outputs = payload.get("outputs", [])
        print("🔹 Outputs requested:", outputs)


        # 1️⃣ BRAND PERSONA
        if "brand_persona" in outputs:
            results["brand_persona"] = await self.brand_persona_agent.generate(payload)

        # Fetch latest persona ONCE
        persona = None
        if "design" in outputs or "image" in outputs:
            db = SessionLocal()
            persona = (
                db.query(BrandPersonaModel)
                .order_by(BrandPersonaModel.id.desc())
                .first()
            )
            db.close()
        print("🔹 Running Design Agent")

        # 2️⃣ DESIGN AGENT
        if "design" in outputs and persona:
            design_result = await self.design_agent.generate({
                "business_name": persona.business_name,
                "business_type": persona.business_type,
                "tone": persona.tone,
                "description": persona.description,
                "color_palette": persona.color_palette
            })
            results["design"] = design_result
        print("🔹 Running image Agent")

       # 3️⃣ IMAGE GENERATION (depends on DESIGN)
        if "image" in outputs:
            if "design" not in results:
                raise ValueError(
                    "Image generation requires design output. "
                    "Include 'design' in outputs."
                )

            design_prompt = results["design"]["stable_diffusion_prompt"]

            image_result = await self.image_agent.generate({
                "prompt": design_prompt,
                "size": "1024x1024"
            })
            print(" Image Agent Result:", image_result)

            results["image"] = image_result
