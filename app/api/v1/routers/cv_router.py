from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.api.schemas.additional_training_schema import AdditionalTrainingResponse
from app.api.schemas.certification_schema import CertificationResponse
from app.api.schemas.contact_info_schema import ContactInformationResponse
from app.api.schemas.cv_schema import CVCompleteResponse
from app.api.schemas.education_schema import EducationResponse
from app.api.schemas.profile_schema import ProfileResponse
from app.api.schemas.projects_schema import ProjectResponse
from app.api.schemas.skill_schema import SkillResponse
from app.api.schemas.social_networks_schema import SocialNetworkResponse
from app.api.schemas.tools_schema import ToolResponse
from app.api.schemas.work_experience_schema import WorkExperienceResponse

router = APIRouter(prefix="/cv", tags=["CV"])

# TODO: Reemplazar con datos reales de todos los repositorios
MOCK_CV_COMPLETE = CVCompleteResponse(
    profile=ProfileResponse(
        id="profile_001",
        name="Juan Pérez García",
        headline="Full Stack Developer & Software Engineer",
        bio="Desarrollador Full Stack apasionado por crear soluciones escalables y mantener código limpio. Especializado en Python, FastAPI, React y arquitecturas limpias. Con más de 5 años de experiencia en desarrollo web y APIs RESTful.",
        location="Valencia, España (Remoto)",
        avatar_url="https://example.com/images/profile.jpg",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    contact_info=ContactInformationResponse(
        id="contact_001",
        email="juan.perez@example.com",
        phone="+34 600 000 000",
        linkedin="https://linkedin.com/in/juanperez",
        github="https://github.com/juanperez",
        website="https://juanperez.dev",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    social_networks=[
        SocialNetworkResponse(
            id="social_001",
            platform="github",
            url="https://github.com/juanperez",
            username="juanperez",
            order_index=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        SocialNetworkResponse(
            id="social_002",
            platform="linkedin",
            url="https://linkedin.com/in/juanperez",
            username="juanperez",
            order_index=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ],
    work_experiences=[
        WorkExperienceResponse(
            id="exp_001",
            role="Senior Full Stack Developer",
            company="Tech Solutions S.L.",
            start_date=datetime(2021, 1, 1),
            end_date=None,
            description="Desarrollo de aplicaciones web escalables usando FastAPI y React. Implementación de arquitectura Clean Architecture en proyectos empresariales. Liderazgo técnico de equipo de 4 desarrolladores junior.",
            responsibilities=[
                "Desarrollo de aplicaciones web escalables",
                "Implementación de Clean Architecture",
                "Liderazgo técnico de equipo",
            ],
            order_index=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        WorkExperienceResponse(
            id="exp_002",
            role="Full Stack Developer",
            company="StartupXYZ",
            start_date=datetime(2019, 3, 1),
            end_date=datetime(2020, 12, 31),
            description="Desarrollo del MVP de una plataforma fintech desde cero. Implementación de sistema de pagos con Stripe.",
            responsibilities=[
                "Desarrollo del MVP desde cero",
                "Implementación de sistema de pagos con Stripe",
            ],
            order_index=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ],
    projects=[
        ProjectResponse(
            id="proj_001",
            title="Portfolio Personal con Clean Architecture",
            description="Portfolio web profesional desarrollado con Astro en el frontend y FastAPI en el backend, siguiendo principios de Clean Architecture. Incluye sistema de gestión de contenido dinámico con MongoDB y generación automática de CV en PDF.",
            start_date=datetime(2024, 1, 1),
            end_date=None,
            technologies=["Astro", "FastAPI", "MongoDB", "Tailwind CSS", "Docker"],
            repo_url="https://github.com/juanperez/portfolio",
            live_url="https://juanperez.dev",
            order_index=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        ProjectResponse(
            id="proj_002",
            title="E-commerce API REST",
            description="API REST completa para e-commerce con sistema de autenticación JWT, gestión de productos, carrito de compras y procesamiento de pagos con Stripe.",
            start_date=datetime(2023, 6, 1),
            end_date=datetime(2024, 2, 15),
            technologies=[
                "Python",
                "FastAPI",
                "PostgreSQL",
                "Stripe",
                "Redis",
                "Docker",
            ],
            repo_url="https://github.com/juanperez/ecommerce-api",
            live_url=None,
            order_index=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ],
    skills=[
        SkillResponse(
            id="skill_001",
            name="Python",
            level="expert",
            category="backend",
            order_index=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        SkillResponse(
            id="skill_002",
            name="FastAPI",
            level="expert",
            category="backend",
            order_index=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        SkillResponse(
            id="skill_003",
            name="React",
            level="advanced",
            category="frontend",
            order_index=2,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        SkillResponse(
            id="skill_004",
            name="MongoDB",
            level="advanced",
            category="database",
            order_index=3,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        SkillResponse(
            id="skill_005",
            name="PostgreSQL",
            level="advanced",
            category="database",
            order_index=4,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ],
    tools=[
        ToolResponse(
            id="tool_001",
            name="VS Code",
            category="ide",
            order_index=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        ToolResponse(
            id="tool_002",
            name="Docker",
            category="containerization",
            order_index=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        ToolResponse(
            id="tool_003",
            name="Git",
            category="version_control",
            order_index=2,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        ToolResponse(
            id="tool_004",
            name="Postman",
            category="testing_tools",
            order_index=3,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ],
    education=[
        EducationResponse(
            id="edu_001",
            institution="Universidad Politécnica de Valencia",
            degree="Grado en Ingeniería Informática",
            field="Ingeniería del Software",
            start_date=datetime(2015, 9, 1),
            end_date=datetime(2019, 6, 30),
            description="Especialización en Ingeniería del Software y Arquitecturas de Software. Nota media: 8.5/10",
            order_index=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
    ],
    additional_training=[
        AdditionalTrainingResponse(
            id="train_001",
            title="Clean Architecture y Domain-Driven Design en Python",
            provider="Udemy",
            completion_date=datetime(2023, 4, 15),
            duration="40 horas",
            description="Curso avanzado sobre arquitecturas limpias, DDD y principios SOLID aplicados a Python",
            order_index=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        AdditionalTrainingResponse(
            id="train_002",
            title="Advanced React Patterns",
            provider="Frontend Masters",
            completion_date=datetime(2023, 7, 1),
            duration="30 horas",
            description="Patrones avanzados de React: Hooks, Context, Performance",
            order_index=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ],
    certifications=[
        CertificationResponse(
            id="cert_001",
            title="AWS Certified Solutions Architect - Associate",
            issuer="Amazon Web Services",
            issue_date=datetime(2023, 6, 15),
            expiry_date=datetime(2026, 6, 15),
            credential_id="AWS-SA-123456789",
            credential_url="https://www.credly.com/badges/aws-saa-123456789",
            order_index=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
    ],
)


@router.get(
    "",
    response_model=CVCompleteResponse,
    summary="Obtener CV completo",
    description="Obtiene TODA la información del CV para mostrar en el portfolio",
)
async def get_complete_cv():
    """
    Retorna el CV completo con TODAS las secciones del portfolio.

    Este endpoint combina información de todas las entidades relacionadas con Profile:

    **Información Personal:**
    - Profile (único en el sistema)
    - ContactInformation (1-a-1 con Profile)
    - SocialNetworks (muchos)

    **Experiencia Profesional:**
    - WorkExperiences (muchos)
    - Projects (muchos)

    **Habilidades:**
    - Skills / TechnicalSkills (muchos)
    - Tools (muchos)

    **Formación:**
    - Education (muchos)
    - AdditionalTraining (muchos)
    - Certifications (muchos)

    Returns:
        CVCompleteResponse: Objeto con toda la información del portfolio

    TODO: Implementar con GetCompleteCVUseCase
    """
    return MOCK_CV_COMPLETE


@router.get(
    "/download",
    summary="Descargar CV en PDF",
    description="Genera y descarga el CV en formato PDF profesional",
    response_class=FileResponse,
)
async def download_cv_pdf():
    """
    Genera un PDF del CV completo y lo retorna para descarga.

    Returns:
        FileResponse: Archivo PDF descargable

    Raises:
        HTTPException 501: Mientras no esté implementado

    TODO: Implementar con GenerateCVPDFUseCase
    """
    raise HTTPException(
        status_code=501,
        detail="Funcionalidad de descarga PDF aún no implementada. Próximamente disponible.",
    )
