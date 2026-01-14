from fastapi import APIRouter, HTTPException, status
from app.models.work_experience import ExperienceCreate, ExperienceResponse
from app.database.database import get_database
from bson import ObjectId
from typing import List
from datetime import datetime, timezone

router = APIRouter(
    prefix="/experience",
    tags=["Experience"]
)

# Helper para convertir ObjectId a string
def experience_helper(experience) -> dict:
    return {
        "id": str(experience["_id"]),
        "company": experience["company"],
        "position": experience["position"],
        "start_date": experience["start_date"],
        "end_date": experience.get("end_date"),
        "description": experience["description"],
        "technologies": experience.get("technologies", []),
        "order": experience.get("order", 0),
        "created_at": experience.get("created_at")
    }

@router.get("/", response_model=List[ExperienceResponse], summary="Listar todas las experiencias")
async def get_experiences():
    """
    Obtiene todas las experiencias laborales ordenadas por 'order'.
    """
    db = get_database()
    experiences = []
    
    # Buscar todas las experiencias, ordenadas por 'order'
    cursor = db.experience.find().sort("order", 1)
    
    async for experience in cursor:
        experiences.append(experience_helper(experience))
    
    return experiences

@router.get("/{experience_id}", response_model=ExperienceResponse, summary="Obtener una experiencia por ID")
async def get_experience(experience_id: str):
    """
    Obtiene una experiencia laboral específica por su ID.
    """
    db = get_database()
    
    # Validar que el ID sea válido
    if not ObjectId.is_valid(experience_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID inválido"
        )
    
    experience = await db.experience.find_one({"_id": ObjectId(experience_id)})
    
    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Experiencia con ID {experience_id} no encontrada"
        )
    
    return experience_helper(experience)

@router.post("/", response_model=ExperienceResponse, status_code=status.HTTP_201_CREATED, summary="Crear nueva experiencia")
async def create_experience(experience: ExperienceCreate):
    """
    Crea una nueva experiencia laboral.
    """
    db = get_database()
    
    # Preparar documento para insertar
    experience_dict = experience.model_dump()
    experience_dict["created_at"] = datetime.now(timezone.utc)
    
    # Insertar en MongoDB
    result = await db.experience.insert_one(experience_dict)
    
    # Obtener el documento insertado
    new_experience = await db.experience.find_one({"_id": result.inserted_id})
    
    return experience_helper(new_experience)

