from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from datetime import datetime, date

from app.api.schemas.cv_schema import CVCompleteResponse
from app.api.schemas.profile_schema import ProfileResponse
from app.api.schemas.contact_info_schema import ContactInfoResponse
from app.api.schemas.social_networks_schema import SocialNetworkResponse
from app.api.schemas.projects_schema import ProjectResponse
from app.api.schemas.work_experience_schema import ExperienceResponse
from app.api.schemas.skill_schema import SkillResponse
from app.api.schemas.tools_schema import ToolResponse
from app.api.schemas.education_schema import EducationResponse
from app.api.schemas.additional_training_schema import AdditionalTrainingResponse
from app.api.schemas.certification_schema import CertificationResponse

router = APIRouter(prefix="/cv", tags=["CV"])

# TODO: Reemplazar con datos reales de todos los repositorios
MOCK_CV_COMPLETE = CVCompleteResponse(
    profile=ProfileResponse(
        id="profile_001",
        full_name="Juan Pérez García",
        headline="Full Stack Developer & Software Engineer",
        about="Desarrollador Full Stack apasionado por crear soluciones escalables y mantener código limpio. Especializado en Python, FastAPI, React y arquitecturas limpias. Con más de 5 años de experiencia en desarrollo web y APIs RESTful.",
        location="Valencia, España (Remoto)",
        profile_image="https://example.com/images/profile.jpg",
        banner_image="https://example.com/images/banner.jpg",
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    contact_info=ContactInfoResponse(
        id="contact_001",
        email="juan.perez@example.com",
        telefono="+34 600 000 000",
        ubicacion="Valencia, España",
        disponibilidad="Inmediata",
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    social_networks=[
        SocialNetworkResponse(
            id="social_001",
            plataforma="github",
            url="https://github.com/juanperez",
            usuario="juanperez",
            orden=1,
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        SocialNetworkResponse(
            id="social_002",
            plataforma="linkedin",
            url="https://linkedin.com/in/juanperez",
            usuario="juanperez",
            orden=2,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    ],
    work_experiences=[
        ExperienceResponse(
            id="exp_001",
            empresa="Tech Solutions S.L.",
            cargo="Senior Full Stack Developer",
            descripcion="Desarrollo de aplicaciones web escalables usando FastAPI y React. Implementación de arquitectura Clean Architecture en proyectos empresariales.",
            fecha_inicio=date(2021, 1, 1),
            fecha_fin=None,  # Presente
            ubicacion="Valencia, España",
            tecnologias=["Python", "FastAPI", "React", "MongoDB", "Docker"],
            logros=[
                "Implementé arquitectura Clean Architecture en 3 proyectos principales",
                "Reduje el tiempo de respuesta de la API en un 40%",
                "Lideré un equipo de 4 desarrolladores junior"
            ],
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        ExperienceResponse(
            id="exp_002",
            empresa="StartupXYZ",
            cargo="Full Stack Developer",
            descripcion="Desarrollo del MVP de una plataforma fintech desde cero",
            fecha_inicio=date(2019, 3, 1),
            fecha_fin=date(2020, 12, 31),
            ubicacion="Remoto",
            tecnologias=["Node.js", "Vue.js", "PostgreSQL", "AWS"],
            logros=[
                "Lanzamiento exitoso del MVP en 6 meses",
                "Integración de pasarela de pagos Stripe"
            ],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    ],
    projects=[
        ProjectResponse(
            id="proj_001",
            nombre="Portfolio Personal con Clean Architecture",
            descripcion="Portfolio web profesional desarrollado con Astro en el frontend y FastAPI en el backend, siguiendo principios de Clean Architecture. Incluye sistema de gestión de contenido dinámico con MongoDB y generación automática de CV en PDF.",
            descripcion_corta="Portfolio con Clean Architecture y gestión dinámica de contenido",
            tecnologias=["Astro", "FastAPI", "MongoDB", "Tailwind CSS", "Docker"],
            url_repositorio="https://github.com/juanperez/portfolio",
            url_demo="https://juanperez.dev",
            url_imagen="https://example.com/images/portfolio.jpg",
            fecha_inicio=date(2024, 1, 1),
            fecha_fin=None,  # En desarrollo
            destacado=True,
            orden=1,
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        ProjectResponse(
            id="proj_002",
            nombre="E-commerce API REST",
            descripcion="API REST completa para e-commerce con sistema de autenticación JWT, gestión de productos, carrito de compras y procesamiento de pagos con Stripe.",
            descripcion_corta="API REST para e-commerce con pagos",
            tecnologias=["Python", "FastAPI", "PostgreSQL", "Stripe", "Redis", "Docker"],
            url_repositorio="https://github.com/juanperez/ecommerce-api",
            fecha_inicio=date(2023, 6, 1),
            fecha_fin=date(2023, 12, 15),
            destacado=True,
            orden=2,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    ],
    skills=[
        SkillResponse(
            id="skill_001",
            nombre="Python",
            categoria="lenguaje",
            nivel="experto",
            años_experiencia=5,
            descripcion="Desarrollo backend con FastAPI, Django. Scripting y automatización.",
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        SkillResponse(
            id="skill_002",
            nombre="FastAPI",
            categoria="framework",
            nivel="experto",
            años_experiencia=3,
            descripcion="Desarrollo de APIs REST de alto rendimiento",
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        SkillResponse(
            id="skill_003",
            nombre="React",
            categoria="framework",
            nivel="avanzado",
            años_experiencia=3,
            descripcion="Desarrollo de interfaces modernas con hooks y context",
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        SkillResponse(
            id="skill_004",
            nombre="MongoDB",
            categoria="base_datos",
            nivel="avanzado",
            años_experiencia=4,
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        SkillResponse(
            id="skill_005",
            nombre="PostgreSQL",
            categoria="base_datos",
            nivel="avanzado",
            años_experiencia=4,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    ],
    tools=[
        ToolResponse(
            id="tool_001",
            nombre="VS Code",
            categoria="ide",
            nivel="experto",
            años_experiencia=5,
            descripcion="Editor principal para desarrollo",
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        ToolResponse(
            id="tool_002",
            nombre="Docker",
            categoria="contenedores",
            nivel="avanzado",
            años_experiencia=3,
            descripcion="Containerización y orquestación",
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        ToolResponse(
            id="tool_003",
            nombre="Git",
            categoria="versionado",
            nivel="experto",
            años_experiencia=5,
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        ToolResponse(
            id="tool_004",
            nombre="Postman",
            categoria="testing",
            nivel="avanzado",
            años_experiencia=4,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    ],
    education=[
        EducationResponse(
            id="edu_001",
            institucion="Universidad Politécnica de Valencia",
            titulo="Grado en Ingeniería Informática",
            campo_estudio="Ingeniería del Software",
            fecha_inicio=date(2015, 9, 1),
            fecha_fin=date(2019, 6, 30),
            descripcion="Especialización en Ingeniería del Software y Arquitecturas de Software",
            nota="8.5/10",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    ],
    additional_training=[
        AdditionalTrainingResponse(
            id="train_001",
            nombre="Clean Architecture y Domain-Driven Design en Python",
            institucion="Udemy",
            descripcion="Curso avanzado sobre arquitecturas limpias, DDD y principios SOLID aplicados a Python",
            duracion_horas=40,
            fecha_inicio=date(2023, 3, 1),
            fecha_fin=date(2023, 4, 15),
            url_certificado="https://udemy.com/certificate/ABC123",
            tecnologias=["Python", "FastAPI", "Design Patterns", "SOLID", "DDD"],
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        AdditionalTrainingResponse(
            id="train_002",
            nombre="Advanced React Patterns",
            institucion="Frontend Masters",
            descripcion="Patrones avanzados de React: Hooks, Context, Performance",
            duracion_horas=30,
            fecha_inicio=date(2023, 6, 1),
            fecha_fin=date(2023, 7, 1),
            tecnologias=["React", "TypeScript", "Performance"],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    ],
    certifications=[
        CertificationResponse(
            id="cert_001",
            nombre="AWS Certified Solutions Architect - Associate",
            organizacion_emisora="Amazon Web Services",
            descripcion="Certificación oficial de AWS para arquitectos de soluciones",
            fecha_emision=date(2023, 6, 15),
            fecha_expiracion=date(2026, 6, 15),
            codigo_credencial="AWS-SA-123456789",
            url_verificacion="https://aws.amazon.com/verification/123456789",
            url_insignia="https://example.com/aws-badge.png",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    ]
)


@router.get(
    "",
    response_model=CVCompleteResponse,
    summary="Obtener CV completo",
    description="Obtiene TODA la información del CV para mostrar en el portfolio"
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
    TODO: El use case debe:
        1. Obtener el Profile único
        2. Obtener ContactInformation asociada
        3. Obtener todas las SocialNetworks del profile
        4. Obtener todas las WorkExperiences ordenadas por fecha
        5. Obtener todos los Projects destacados primero, luego por orden
        6. Obtener todas las Skills agrupadas por categoría
        7. Obtener todas las Tools agrupadas por categoría
        8. Obtener toda la Education ordenada por fecha
        9. Obtener todo el AdditionalTraining ordenado por fecha
        10. Obtener todas las Certifications vigentes primero
    """
    return MOCK_CV_COMPLETE


@router.get(
    "/download",
    summary="Descargar CV en PDF",
    description="Genera y descarga el CV en formato PDF profesional",
    response_class=FileResponse
)
async def download_cv_pdf():
    """
    Genera un PDF del CV completo y lo retorna para descarga.
    
    El PDF incluirá:
    - Información personal del Profile
    - Datos de contacto
    - Enlaces a redes sociales
    - Experiencia laboral completa
    - Proyectos destacados
    - Habilidades técnicas organizadas
    - Herramientas que domina
    - Formación académica
    - Cursos y formación adicional
    - Certificaciones profesionales
    
    Returns:
        FileResponse: Archivo PDF descargable
    
    Raises:
        HTTPException 501: Mientras no esté implementado
    
    TODO: Implementar con GenerateCVPDFUseCase
    TODO: Usar librería para generar PDF (opciones):
        - reportlab: Más control, bajo nivel
        - weasyprint: HTML/CSS a PDF, más fácil
        - fpdf2: Simple y rápido
    TODO: Diseñar template profesional del CV
    TODO: Guardar PDF generado temporalmente o devolverlo en streaming
    TODO: Considerar cache del PDF (regenerar solo si hay cambios)
    """
    raise HTTPException(
        status_code=501,
        detail="Funcionalidad de descarga PDF aún no implementada. Próximamente disponible."
    )