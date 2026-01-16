from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

class EducationBase(BaseModel):
    """Esquema base de formación académica"""
    educational_institution: str = Field(..., description="Nombre de la institución")
    degree: str = Field(..., description="Nombre del título formativo")
    start_date: str = Field(..., description="Fecha de inicio (YYYY-MM)")
    end_date: Optional[str] = Field(None, description="Fecha de fin (YYYY-MM) o None si es actual")
    description: str = Field(..., description="Descripción de la formación")
    technical_skills: list[str] = Field(default=[], description="Tecnologías, herramientas y habilidades aprendidas")
    order: int = Field(default=0, description="Orden de visualización")

class EducationCreate(EducationBase):
    """Esquema para crear formación académica (lo que recibe el POST)"""
    pass

class EducationInDB(EducationBase):
    """Esquema de formación académica en base de datos"""
    id: str = Field(alias="_id")
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "educational_institution": "Tech Solutions S.L.",
                "degree": "Software Engineer",
                "start_date": "2023-01",
                "end_date": "2024-12",
                "description": "Desarrollo de aplicaciones web con FastAPI y React",
                "technical_skills": ["Python", "FastAPI", "React", "MongoDB", 'Scrum'],
                "order": 1,
                "created_at": "2024-01-15T10:30:00"
            }
        }

class EducationResponse(EducationBase):
    """Esquema de respuesta (lo que devuelve el API)"""
    id: str
    created_at: datetime
    
    class Config:
        populate_by_name = True