from fastapi import FastAPI
from app.orchestrator import Orchestrator
from pydantic import BaseModel
from typing import List, Optional


app = FastAPI()
orchestrator = Orchestrator()


class GenerateRequest(BaseModel):
    business_name: Optional[str] = None
    business_type: Optional[str] = None
    location: Optional[str] = None
    target_audience: Optional[str] = None
    tone: Optional[str] = None
    outputs: List[str]


@app.post("/generate")
async def generate(request: GenerateRequest):
    result = await orchestrator.handle_request(request.dict())
    return {
        "success": True,
        "data": result,
        "message": "Request processed successfully"
    }

