from pydantic import BaseModel
from typing import Optional, List

class GenerateRequest(BaseModel):
    business_name: Optional[str] = None
    business_type: str
    location: Optional[str] = None
    target_audience: Optional[str] = None
    tone: Optional[str] = None
    outputs: List[str]
