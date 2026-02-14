# Arquitectura del Backend

## Visión general

API REST para portfolio personal construida con **FastAPI** y **MongoDB**, siguiendo **Clean Architecture**, principios de **Hexagonal Architecture (Ports & Adapters)** y conceptos de **Domain-Driven Design (DDD)**.

El backend gestiona todos los recursos del portfolio, aplica reglas de negocio, valida datos y expone una API versionada para ser consumida por un frontend desacoplado (Astro).

**Stack principal:**

- Python 3.13  
- FastAPI 0.128  
- MongoDB (Motor 3.7 — async)  
- Pydantic 2.12 (solo en capa API)  
- pytest + pytest-asyncio  
- WeasyPrint (generación de PDF)

---

## Capas de la arquitectura

```text
┌──────────────────────────────────────────────────────────┐
│                    API (FastAPI)                          │
│ Routers · Schemas · Middlewares · Exception Handlers      │
└────────────────────────┬─────────────────────────────────┘
                         │ depende de
┌────────────────────────▼─────────────────────────────────┐
│               APPLICATION (Use Cases)                    │
│            DTOs · Orquestación de negocio                │
└────────────────────────┬─────────────────────────────────┘
                         │ depende de
┌────────────────────────▼─────────────────────────────────┐
│                  DOMAIN (Núcleo)                         │
│       Entities · Value Objects · Domain Exceptions        │
└────────────────────────▲─────────────────────────────────┘
                         │ implementa interfaces de
┌────────────────────────┴─────────────────────────────────┐
│               INFRASTRUCTURE                             │
│ Repositories · Mappers · Database (MongoDB) · PDF Service │
└──────────────────────────────────────────────────────────┘

          ┌─────────────────────────────┐
          │         SHARED              │
          │ Interfaces · Excepciones    │
          │ Tipos comunes · Utilidades  │
          └─────────────────────────────┘


**Regla de dependencia:** 

Las dependencias siempre apuntan hacia adentro.
Infrastructure implementa interfaces definidas en Shared.
Domain nunca conoce Application, API ni Infrastructure.

---

## Estructura de directorios

```text
app/
├── main.py                          # Entry point, lifespan, registros
├── config/
│   └── settings.py                  # Pydantic Settings (.env)
├── api/                             # --- Capa de Presentacion ---
│   ├── dependencies.py              # Inyeccion de dependencias (Depends)
│   ├── exception_handlers.py        # Mapeo excepciones → HTTP
│   ├── middleware.py                 # Registro de middlewares
│   ├── middlewares/
│   │   ├── logging_middleware.py     # Log de requests (omite /docs, /health)
│   │   └── process_time_middleware.py # Header X-Process-Time
│   ├── schemas/                     # Modelos Pydantic (contratos API)
│   │   ├── common_schema.py
│   │   ├── profile_schema.py
│   │   └── ...                      # 1 schema por recurso
│   └── v1/
│       ├── router.py                # Agregador de routers v1
│       └── routers/                 # 15 routers individuales
│           ├── health_router.py
│           ├── profile_router.py
│           ├── skill_router.py
│           └── ...
├── application/                     # --- Capa de Aplicacion ---
│   ├── dto/                         # Data Transfer Objects
│   │   ├── base_dto.py              # SuccessResponse, PaginationRequest
│   │   ├── skill_dto.py
│   │   ├── cv_dto.py
│   │   └── ...                      # 1 DTO por agregado
│   └── use_cases/                   # 1 archivo = 1 caso de uso
│       ├── profile/
│       │   ├── create_profile.py
│       │   ├── get_profile.py
│       │   └── update_profile.py
│       ├── skill/
│       │   ├── add_skill.py
│       │   ├── edit_skill.py
│       │   ├── delete_skill.py
│       │   └── list_skills.py
│       ├── cv/
│       │   ├── get_complete_cv.py
│       │   └── generate_cv_pdf.py
│       └── ...                      # education, work_experience, language,
│                                    # programming_language
├── domain/                          # --- Capa de Dominio ---
│   ├── entities/                    # 13 entidades (dataclass con validacion)
│   │   ├── profile.py
│   │   ├── skill.py
│   │   ├── work_experience.py
│   │   ├── education.py
│   │   ├── project.py
│   │   ├── certification.py
│   │   ├── additional_training.py
│   │   ├── contact_information.py
│   │   ├── contact_message.py
│   │   ├── social_network.py
│   │   ├── tool.py
│   │   ├── language.py
│   │   └── programming_language.py
│   ├── value_objects/               # 7 VOs inmutables (frozen dataclass)
│   │   ├── email.py                 # RFC 5322
│   │   ├── phone.py                 # E.164
│   │   ├── date_range.py
│   │   ├── contact_info.py          # Compuesto: Email + Phone
│   │   ├── skill_level.py
│   │   ├── language_proficiency.py  # CEFR (A1-C2)
│   │   └── programming_language_level.py
│   └── exceptions/
│       └── domain_errors.py         # EmptyFieldError, InvalidEmailError, etc.
├── infrastructure/                  # --- Capa de Infraestructura ---
│   ├── database/
│   │   ├── mongo_client.py          # Singleton MongoDBClient (Motor)
│   │   └── collections.py
│   ├── repositories/                # 13 implementaciones concretas
│   │   ├── profile_repository.py
│   │   ├── skill_repository.py
│   │   └── ...
│   └── mappers/                     # 13 mappers Domain ↔ MongoDB doc
│       ├── profile_mapper.py
│       ├── skill_mapper.py
│       └── ...
└── shared/                          # --- Kernel compartido ---
    ├── interfaces/
    │   ├── repository.py            # IRepository, IOrderedRepository, etc.
    │   ├── mapper.py                # IMapper[TDomain, TPersistence]
    │   └── use_case.py              # IUseCase, IQueryUseCase, ICommandUseCase
    ├── shared_exceptions/           # ApplicationException hierarchy
    ├── types/
    │   └── common_types.py
    └── utils/
        ├── date_utils.py
        └── string_utils.py
```

---

## Flujos clave del sistema

### 1. Obtener el perfil completo (GET /profile)

```text
Cliente → API Router → GetProfileUseCase → ProfileRepository → MongoDB
       ← API Router ← DTO/Schema ← Mapper
```

### 2. Actualizar el perfil (PUT /profile)

```text
Cliente → API Router → UpdateProfileUseCase → Validaciones Dominio
        → Repository → Mapper → MongoDB
       ← API Router ← Schema
```

### 3. Añadir experiencia laboral (POST /experiences)

```text
Cliente → API Router → CreateExperienceUseCase
        → Entidades (Experience, DateRange)
        → Validaciones Dominio → Repository → MongoDB
       ← API Router ← Schema
```

### 4. Obtener CV completo (GET /cv)

```text
Cliente → API Router → GetCompleteCvUseCase
        → Múltiples repositorios → MongoDB
        → Mappers → Entidad agregada CompleteCV
       ← API Router ← Schema
```

### 5. Generar PDF del CV (GET /cv/download)

```text
Cliente → API Router → GenerateCvPdfUseCase
        → Obtiene CV completo
        → Render HTML (Jinja2)
        → CSS del frontend o específico
        → Servicio PDF (WeasyPrint)
       ← API Router (application/pdf)
```

### 6. Enviar mensaje de contacto (POST /contact)

```text
Cliente → API Router → CreateContactMessageUseCase
        → Entidad ContactMessage → Validaciones
        → Repository → MongoDB
       ← API Router ← Schema
```

## Flujo de una petición

Ejemplo: `GET /api/v1/skills?category=backend`

```text
1. Request HTTP
       │
2. ProcessTimeMiddleware / LoggingMiddleware
       │
3. skill_router.py
   ├── Valida query params con Pydantic Schema
   ├── Depends() → get_list_skills_use_case()
   │       └── get_skill_repository(db) → SkillRepository
   │               └── get_database() → AsyncIOMotorDatabase
   │
4. ListSkillsUseCase.execute(ListSkillsRequest)
   ├── Llama a repo.get_all_ordered(profile_id, ascending)
   └── Devuelve SkillListResponse.from_entities(skills)
       │
5. SkillRepository.get_all_ordered()
   ├── collection.find({profile_id}).sort(order_index)
   └── SkillMapper.to_domain(doc) por cada documento
       │
6. Response ← SkillListResponse (DTO → JSON)
```

Si ocurre un error en cualquier punto:

```text
DomainError           → exception_handlers → 400 Bad Request
NotFoundException     → exception_handlers → 404 Not Found
DuplicateException    → exception_handlers → 409 Conflict
ValidationException   → exception_handlers → 422 Unprocessable Entity
Exception (generico)  → exception_handlers → 500 Internal Server Error
```

Formato estandarizado de error:

```json
{
  "success": false,
  "error": "Not Found",
  "message": "Skill with id 'xyz' not found",
  "code": "NOT_FOUND"
}
```

---

## Inyección de dependencias

Toda la DI esta centralizada en `app/api/dependencies.py` usando `Depends()` de FastAPI:

```text
get_database()
  └── get_skill_repository(db)
        └── get_add_skill_use_case(repo)
              └── Router endpoint (via Depends)
```

Los routers nunca instancian repositorios ni acceden a la base de datos directamente.

---

## Modelo de dominio

### Relaciones entre entidades

```text
Profile (1 unica instancia)
├── WorkExperience      (N, ordenado por order_index)
├── Education           (N, ordenado)
├── Project             (N, ordenado)
├── Certification       (N, ordenado)
├── AdditionalTraining  (N, ordenado)
├── ProgrammingLanguage (N, ordenado)
├── Language            (N, ordenado)
├── Skill               (N, nombre unico por perfil)
├── Tool                (N, nombre unico por perfil)
├── SocialNetwork       (N, plataforma unica por perfil)
├── ContactInformation  (1)
└── ContactMessage      (N, sin perfil asociado)
```

### Jerarquía de interfaces de repositorio

```text
IRepository[T]                          # CRUD generico
├── IProfileRepository                  # get_profile(), profile_exists()
├── IOrderedRepository[T]               # get_all_ordered(), reorder()
│   usado por: WorkExperience, Education, Project,
│              Certification, AdditionalTraining,
│              ProgrammingLanguage, Language
├── IUniqueNameRepository[T]            # exists_by_name(), get_by_name()
│   usado por: Skill, Tool
├── IContactMessageRepository           # get_pending_messages(), mark_as_read()
└── ISocialNetworkRepository            # exists_by_platform()
```

### Entidades

Las entidades son `@dataclass` con validación en `__post_init__` y factory method `create()`:

```python
@dataclass
class Skill:
    id: str
    profile_id: str
    name: str
    category: str
    order_index: int
    level: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        self._validate_name()
        self._validate_category()
        # ...

    @staticmethod
    def create(**kwargs) -> "Skill":
        return Skill(id=str(uuid.uuid4()), **kwargs)
```

### Value Objects

Objetos inmutables (`frozen=True`) con validación interna:

| Value Object | Validacion |
|---|---|
| Email | RFC 5322, normalizacion a minusculas |
| Phone | E.164, normalizacion (quita espacios, guiones, parentesis) |
| DateRange | start_date <= end_date |
| ContactInfo | Compuesto: Email (requerido) + Phone (opcional) |
| SkillLevel | Enum: basic, intermediate, advanced, expert |
| LanguageProficiency | CEFR: a1, a2, b1, b2, c1, c2 |
| ProgrammingLanguageLevel | Enum: basic, intermediate, advanced, expert |

---

## Mappers

Cada mapper implementa `IMapper[TDomain, dict[str, Any]]` con dos métodos:

- `to_domain(dict) → Entity` — convierte documento MongoDB a entidad. Usa `_id` → `id`, `.get()` para campos opcionales.
- `to_persistence(Entity) → dict` — convierte entidad a documento. Usa `id` → `_id`, incluye campos opcionales solo si no son `None`.

---

## Excepciones

### Dominio (`domain/exceptions/`)

```text
DomainError
├── EmptyFieldError
├── InvalidLengthError
├── InvalidEmailError
├── InvalidPhoneError
├── InvalidDateRangeError
├── InvalidOrderIndexError
├── InvalidSkillLevelError
├── InvalidLanguageProficiencyError
├── InvalidProgrammingLanguageLevelError
└── DuplicateValueError
```

### Aplicacion (`shared/shared_exceptions/`)

```text
ApplicationException
├── NotFoundException              → 404
├── ValidationException            → 422
├── DuplicateException             → 409
├── UnauthorizedException          → 401
├── ForbiddenException             → 403
└── BusinessRuleViolationException → 400
```

---

## API

### Endpoints (v1)

Todos bajo el prefijo `/api/v1`:

| Grupo | Ruta | Recurso |
|---|---|---|
| Sistema | `/health` | Health check + estado DB |
| Personal | `/profile` | Perfil unico |
| Personal | `/contact-info` | Informacion de contacto |
| Personal | `/social-networks` | Redes sociales |
| Profesional | `/work-experience` | Experiencia laboral |
| Profesional | `/projects` | Proyectos del portfolio |
| Habilidades | `/skills` | Habilidades tecnicas |
| Habilidades | `/tools` | Herramientas |
| Habilidades | `/programming-languages` | Lenguajes de programacion |
| Idiomas | `/languages` | Idiomas |
| Formacion | `/education` | Formacion academica |
| Formacion | `/additional-training` | Cursos y formacion extra |
| Formacion | `/certifications` | Certificaciones |
| Contacto | `/contact-messages` | Mensajes de contacto |
| CV | `/cv` | CV completo (agregado) |

### Middlewares

1. **CORSMiddleware** — Orígenes configurables via `.env`
2. **ProcessTimeMiddleware** — Header `X-Process-Time` en cada respuesta
3. **LoggingMiddleware** — Log de request/response (omite `/docs`, `/health`)

### Documentacion auto-generada

- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI spec: `/openapi.json`

---

## Configuracion

Via `pydantic-settings` con variables de entorno:

```text
ENVIRONMENT          development | test | production
API_HOST             0.0.0.0
API_PORT             8000
MONGODB_URL          mongodb://localhost:27017
DATABASE_NAME        portfolio_db
CORS_ORIGINS         http://localhost:4321,http://localhost:3000
SECRET_KEY           (cambiar en produccion)
```

Archivos `.env`:

- `.env.development.local` — desarrollo local
- `.env.development.docker` — Docker
- `.env.test` — tests

---

## Testing

- Unit tests: dominio y casos de uso, sin DB
- Integration tests: repositorios reales con MongoDB
- E2E tests: API completa con Docker
- Herramientas: pytest, pytest-asyncio, httpx, mocks, coverage

### Organizacion

```text
tests/
├── conftest.py                  # Fixtures globales (client, test_settings, test_db)
├── unit/                        # Tests rapidos, sin DB real
│   ├── domain/
│   │   ├── entities/            # Validacion, creacion, reglas de negocio
│   │   └── value_objects/       # Inmutabilidad, igualdad, validacion
│   ├── application/
│   │   ├── dto/                 # from_entity(), PaginationRequest clamping
│   │   └── use_cases/           # Logica de negocio con repos mockeados
│   ├── infrastructure/
│   │   ├── mappers/             # to_domain(), to_persistence(), round-trip
│   │   └── repositories/       # CRUD, metodos especializados, ordenamiento
│   └── api/                     # Endpoints HTTP (happy path, 404, 422)
├── integration/                 # Tests con MongoDB real
└── e2e/                         # Flujos completos
```

### Herramientas

- **pytest** — framework principal
- **pytest-asyncio** — soporte async (mode=strict)
- **pytest-cov** — cobertura
- **pytest-mock** — mocking
- **httpx.AsyncClient** — cliente HTTP para tests de API
- **unittest.mock.AsyncMock** — mock de repositorios async

### Ejecución

```bash
# Todos los tests
make test

# Solo unitarios
make test-unit

# Con cobertura HTML
make test-cov

# Por marcador
make test-mark MARK=value_object

# Local sin Docker
./venv/Scripts/python.exe -m pytest tests/unit/ -v
```

### Markers disponibles

- `@pytest.mark.unit`
- `@pytest.mark.integration`
- `@pytest.mark.e2e`
- `@pytest.mark.value_object`
- `@pytest.mark.business_rule`

---

## Calidad de código

| Herramienta | Función |
|---|---|
| **Black** | Formatter (line-length 88) |
| **Ruff** | Linter rápido (pycodestyle, pyflakes, pyupgrade) |
| **isort** | Ordenación de imports (perfil black) |
| **mypy** | Tipado estático |
| **Bandit** | Análisis de seguridad |
| **pre-commit** | Hooks de Git |

---

## Decisiones técnicas importantes

| Decisión | Justificación |
|----------|---------------|
| Clean Architecture | Separación estricta de responsabilidades, testabilidad, mantenibilidad |
| MongoDB | Flexibilidad para datos del CV, estructura variable, evolución sencilla |
| FastAPI | Alto rendimiento, tipado fuerte, validación automática, async |
| Pydantic solo en API | Evita acoplar dominio a la capa de presentación |
| Repository Pattern | Desacopla dominio de MongoDB |
| Use Case Pattern | Un caso de uso por acción, responsabilidad única |
| CQRS ligero | Separación entre queries y commands |
| Value Objects inmutables | Validación en construcción, seguridad y consistencia |
| DTOs entre capas | Control de datos expuestos, desacoplamiento |
| DI con Depends | Inyección simple sin frameworks externos |
| Async/Await completo | I/O no bloqueante |
| Mappers dedicados | Separación clara Domain ↔ Persistence |
| Exception handlers centralizados | Formato de error consistente |
| Single Profile constraint | Solo puede existir un perfil |
| Generación de PDF con WeasyPrint | Calidad visual, soporte CSS moderno, integración limpia |
| Logging estructurado | Requests, responses, errores, tiempos |
| Docker | Entornos reproducibles, CI/CD, dependencias del sistema |
| Versionado de API | Permite evolución sin romper clientes |

## Estrategia de logging

Logging centralizado con logging de Python.

Middlewares para:

- Requests
- Responses
- Tiempos de ejecución
- Logging de errores en handlers.

Niveles por entorno:

- dev → DEBUG
- prod → INFO/WARNING
- test → mínimo

## Generación de PDF

- Librería: WeasyPrint
- Servicio implementado en `infrastructure/pdf`
- Interfaz: `IPdfGenerator`
- Plantillas HTML en `infrastructure/pdf/templates`
- CSS específico para PDF
- Backend no depende del frontend para generar el PDF
- El PDF combina:
  - Datos del backend
  - Estilos del frontend (opcional)

## Comunicación con el frontend

El frontend (Astro):

- Renderiza el portfolio completo
- Consume la API vía HTTP
- Usa `fetch()` o utilidades de Astro
- Recibe JSON para datos
- Recibe `application/pdf` para el CV descargable
- Envía mensajes de contacto al backend

El backend habilita CORS para permitir acceso desde el dominio público

## Docker y entornos

- Desarrollo: recarga automática, logging detallado
- Testing: base de datos efímera, datos controlados
- Producción: imágenes optimizadas, seguridad reforzada

Docker garantiza:

- Entornos idénticos
- Dependencias del sistema (WeasyPrint, Cairo, Pango)
- CI/CD estable

## Versionado de API

- Todas las rutas bajo `/api/v1`
- Cambios incompatibles → `/api/v2`
- Versiones antiguas se mantienen durante transición
- Deprecación mediante headers HTTP

## Reglas internas del proyecto

(Resumen, las reglas completas están en `PROJECT_CONTEXT.md`)

- Naming conventions
- Creación de casos de uso
- Creación de entidades
- Repositorios
- Mappers
- DTOs
- Schemas
- Endpoints
- Manejo de errores
- Testing
- PDF
- Logging
- Versionado
- Estructura de capas

## Configuración

Variables gestionadas con pydantic-settings:

```code
ENVIRONMENT
API_HOST
API_PORT
MONGODB_URL
DATABASE_NAME
CORS_ORIGINS
SECRET_KEY
```

## Entornos

- `.env.development.local`
- `.env.development.docker`
- `.env.test`
