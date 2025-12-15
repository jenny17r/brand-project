from pydantic import BaseModel
from typing import Any, Dict, Optional

class GenerateResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
