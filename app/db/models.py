from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.db.database import Base

class BrandPersonaModel(Base):
    __tablename__ = "brand_personas"

    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String(255))
    business_type = Column(String(255))
    tone = Column(String(100))
    tagline = Column(String(255))
    color_palette = Column(String(1000))  # stored as JSON string
    description = Column(Text)
class GeneratedImageModel(Base):
    __tablename__ = "generated_images"

    id = Column(Integer, primary_key=True, index=True)
    brand_persona_id = Column(Integer, nullable=False)
    prompt = Column(Text, nullable=False)
    image_path = Column(String(255), nullable=False)