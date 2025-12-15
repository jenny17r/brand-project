from pydantic import BaseModel

class BrandPersona(BaseModel):
    business_name: str
    business_type: str
    tone: str
    tagline: str
    color_palette: list
    description: str

