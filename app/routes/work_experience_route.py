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
def experience_helper(exp: dict) -> dict:
    return {
        "id": str(exp.get("_id")),
        "company": exp.get("company"), 
        "job_position": exp.get("job_position"), 
        "start_date": exp.get("start_date"), 
        "end_date": exp.get("end_date"), 
        "description": exp.get("description"), 
        "technologies": exp.get("technologies", []), 
        "order": exp.get("order", 0), 
        "created_at": exp.get("created_at").isoformat() if exp.get("created_at") else None
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
    
    # Validar que no exista otra experiencia con el mismo order 
    existing = await db.experience.find_one({"order": experience.order}) 
    if existing: 
        raise HTTPException( 
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Ya existe una experiencia con order={experience.order}" 
        )
    
    # Preparar documento para insertar
    experience_dict = experience.model_dump(by_alias=True)
    experience_dict["created_at"] = datetime.now(timezone.utc)
    
    # Insertar en MongoDB
    result = await db.experience.insert_one(experience_dict)
    
    # Obtener el documento insertado
    new_experience = await db.experience.find_one({"_id": result.inserted_id})
    
    return experience_helper(new_experience)

