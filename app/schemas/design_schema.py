from pydantic import BaseModel
from typing import List
class DesignOutput(BaseModel):
    design_style: str
    layout_description: str
    typography: str
    color_usage: List[str]
    stable_diffusion_prompt: str
