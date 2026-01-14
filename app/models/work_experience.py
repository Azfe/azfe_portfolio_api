from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

class ExperienceBase(BaseModel):
    """Esquema base de experiencia laboral"""
    company: str = Field(..., description="Nombre de la empresa")
    position: str = Field(..., description="Cargo o posición")
    start_date: str = Field(..., description="Fecha de inicio (YYYY-MM)")
    end_date: Optional[str] = Field(None, description="Fecha de fin (YYYY-MM) o None si es actual")
    description: str = Field(..., description="Descripción del trabajo")
    technologies: list[str] = Field(default=[], description="Tecnologías utilizadas")
    order: int = Field(default=0, description="Orden de visualización")

class ExperienceCreate(ExperienceBase):
    """Esquema para crear experiencia (lo que recibe el POST)"""
    pass

class ExperienceInDB(ExperienceBase):
    """Esquema de experiencia en base de datos"""
    id: str = Field(alias="_id")
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "company": "Tech Solutions S.L.",
                "position": "Software Engineer",
                "start_date": "2023-01",
                "end_date": "2024-12",
                "description": "Desarrollo de aplicaciones web con FastAPI y React",
                "technologies": ["Python", "FastAPI", "React", "MongoDB"],
                "order": 1,
                "created_at": "2024-01-15T10:30:00"
            }
        }

class ExperienceResponse(ExperienceBase):
    """Esquema de respuesta (lo que devuelve el API)"""
    id: str
    created_at: datetime
    
    class Config:
        populate_by_name = True