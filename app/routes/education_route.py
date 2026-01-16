from fastapi import APIRouter, HTTPException, status
from app.schemas.education_schema import EducationCreate, EducationResponse
from app.database.database import get_database
from bson import ObjectId
from typing import List
from datetime import datetime, timezone

router = APIRouter(
    prefix="/education",
    tags=["Education"]
)

# Helper para convertir ObjectId a string
def education_helper(education) -> dict:
    return {
        "id": str(education["_id"]),
        "educational_institution": education["educational_institution"],
        "degree": education["degree"],
        "start_date": education["start_date"],
        "end_date": education.get("end_date"),
        "description": education["description"],
        "technical_skills": education.get("technical_skills", []),
        "order": education.get("order", 0),
        "created_at": education.get("created_at")
    }

@router.get("/", response_model=List[EducationResponse], summary="Listar toda la formación académica")
async def get_education():
    """
    Obtiene todas las formaciones académicas ordenadas por 'order'.
    """
    db = get_database()
    educations = []
    
    # Buscar todas las formaciones académicas, ordenadas por 'order'
    cursor = db.education.find().sort("order", 1)
    
    async for education in cursor:
        educations.append(education_helper(education))
    
    return educations

@router.get("/{education_id}", response_model=EducationResponse, summary="Obtener una formación académica por ID")
async def get_education(education_id: str):
    """
    Obtiene una formación académica específica por su ID.
    """
    db = get_database()
    
    # Validar que el ID sea válido
    if not ObjectId.is_valid(education_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID inválido"
        )
    
    education = await db.education.find_one({"_id": ObjectId(education_id)})
    
    if not education:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Formación académica con ID {education_id} no encontrada"
        )
    
    return education_helper(education)

@router.post("/", response_model=EducationResponse, status_code=status.HTTP_201_CREATED, summary="Crear nueva formación académica")
async def create_education(education: EducationCreate):
    """
    Crea una nueva formación académica.
    """
    db = get_database()
    
    # Preparar documento para insertar
    education_dict = education.model_dump()
    education_dict["created_at"] = datetime.now(timezone.utc)
    
    # Insertar en MongoDB
    result = await db.education.insert_one(education_dict)
    
    # Obtener el documento insertado
    new_education = await db.education.find_one({"_id": result.inserted_id})
    
    return education_helper(new_education)

