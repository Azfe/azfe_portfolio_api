from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class ExperienceBase(BaseModel):
    """Esquema base de experiencia laboral"""
    company: str = Field(..., description="Nombre de la empresa")
    job_position: str = Field(..., description="Cargo o posición")
    start_date: str = Field(..., description="Fecha de inicio (YYYY-MM)")
    end_date: Optional[str] = Field(None, description="Fecha de fin (YYYY-MM) o None si es actual")
    description: str = Field(..., description="Descripción del trabajo")
    technologies: list[str] = Field(default=[], description="Tecnologías utilizadas")
    order: int = Field(default=0, description="Orden de visualización")
    
    @field_validator("start_date", "end_date") 
    def validate_dates(cls, v): 
        if v is None: 
            return v 
        try: 
            datetime.strptime(v, "%Y-%m") 
        except ValueError: 
            raise ValueError("Formato inválido, usa YYYY-MM") 
        return v

class ExperienceCreate(ExperienceBase):
    """Esquema para crear experiencia (lo que recibe el POST)"""
    pass    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "company": "Mi Empresa S.L.",
                "job_position": "Software Engineer",
                "start_date": "2023-01",
                "end_date": "2024-12",
                "description": "Desarrollo de aplicaciones web con Python y FastAPI",
                "technologies": ["Python", "FastAPI", "MongoDB", "React"],
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