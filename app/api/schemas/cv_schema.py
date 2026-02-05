from pydantic import BaseModel

from app.api.schemas.additional_training_schema import AdditionalTrainingResponse
from app.api.schemas.certification_schema import CertificationResponse
from app.api.schemas.contact_info_schema import ContactInformationResponse
from app.api.schemas.education_schema import EducationResponse
from app.api.schemas.profile_schema import ProfileResponse
from app.api.schemas.projects_schema import ProjectResponse
from app.api.schemas.skill_schema import SkillResponse
from app.api.schemas.social_networks_schema import SocialNetworkResponse
from app.api.schemas.tools_schema import ToolResponse
from app.api.schemas.work_experience_schema import WorkExperienceResponse


class CVCompleteResponse(BaseModel):
    """
    Schema del CV completo.
    Agrupa TODA la información del portfolio.
    """

    # Información personal
    profile: ProfileResponse
    contact_info: ContactInformationResponse
    social_networks: list[SocialNetworkResponse] = []

    # Experiencia profesional
    work_experiences: list[WorkExperienceResponse] = []
    projects: list[ProjectResponse] = []

    # Habilidades
    skills: list[SkillResponse] = []
    tools: list[ToolResponse] = []

    # Formación
    education: list[EducationResponse] = []
    additional_training: list[AdditionalTrainingResponse] = []
    certifications: list[CertificationResponse] = []

    class Config:
        from_attributes = True
