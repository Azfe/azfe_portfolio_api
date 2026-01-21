from pydantic import BaseModel
from typing import List
from app.api.schemas.profile_schema import ProfileResponse
from app.api.schemas.contact_info_schema import ContactInformationResponse
from app.api.schemas.social_networks_schema import SocialNetworkResponse
from app.api.schemas.projects_schema import ProjectResponse
from app.api.schemas.work_experience_schema import WorkExperienceResponse
from app.api.schemas.skill_schema import SkillResponse
from app.api.schemas.tools_schema import ToolResponse
from app.api.schemas.education_schema import EducationResponse
from app.api.schemas.additional_training_schema import AdditionalTrainingResponse
from app.api.schemas.certification_schema import CertificationResponse


class CVCompleteResponse(BaseModel):
    """
    Schema del CV completo.
    Agrupa TODA la información del portfolio.
    """
    # Información personal
    profile: ProfileResponse
    contact_info: ContactInformationResponse
    social_networks: List[SocialNetworkResponse] = []
    
    # Experiencia profesional
    work_experiences: List[WorkExperienceResponse] = []
    projects: List[ProjectResponse] = []
    
    # Habilidades
    skills: List[SkillResponse] = []
    tools: List[ToolResponse] = []
    
    # Formación
    education: List[EducationResponse] = []
    additional_training: List[AdditionalTrainingResponse] = []
    certifications: List[CertificationResponse] = []
    
    class Config:
        from_attributes = True