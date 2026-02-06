# Application Layer Documentation

## Overview

The **Application Layer** contains the **business logic** of the application in the form of **Use Cases**. This layer orchestrates the flow between domain entities, repositories, and external services.

Following **Clean Architecture**, the application layer:

- ✅ Depends on **domain interfaces** (not implementations)
- ✅ Is **independent** of frameworks and infrastructure
- ✅ Contains **business operations** (use cases)
- ✅ Uses **DTOs** for input/output
- ✅ Handles **application-level exceptions**

## Structure

```text
application/
├── use_cases/
│   ├── profile/         # Profile management
│   │   ├── get_profile.py
│   │   ├── create_profile.py
│   │   └── update_profile.py
│   ├── experience/      # Work experience management
│   │   ├── add_experience.py
│   │   ├── edit_experience.py
│   │   ├── delete_experience.py
│   │   └── list_experiences.py
│   ├── skill/           # Skill management
│   │   └── __init__.py  # All skill use cases
│   ├── education/       # Education management
│   │   └── __init__.py  # All education use cases
│   └── cv/              # CV aggregation
│       └── __init__.py  # CV use cases
└── dto/                 # Data Transfer Objects
    ├── base_dto.py
    ├── profile_dto.py
    ├── experience_dto.py
    ├── skill_dto.py
    ├── education_dto.py
    └── cv_dto.py
```

## Use Cases

### Profile Use Cases

#### ✅ GetProfileUseCase

**Type**: Query (read-only)

**Purpose**: Retrieve the single profile

**Input**: `GetProfileRequest` (empty)

**Output**: `ProfileResponse`

**Business Rules**:
- Only one profile exists in the system
- Returns NotFoundException if no profile exists

**Example**:
```python
use_case = GetProfileUseCase(profile_repo)
response = await use_case.execute(GetProfileRequest())
print(response.name)  # "John Doe"
```

#### ✅ CreateProfileUseCase
**Type**: Command (write)

**Purpose**: Create the single profile

**Input**: `CreateProfileRequest`

**Output**: `ProfileResponse`

**Business Rules**:
- Only ONE profile can exist
- All required fields must be provided
- Validation is performed by entity

**Example**:
```python
use_case = CreateProfileUseCase(profile_repo)
request = CreateProfileRequest(
    name="John Doe",
    headline="Software Engineer"
)
response = await use_case.execute(request)
```

#### ✅ UpdateProfileUseCase
**Type**: Command (write)

**Purpose**: Update profile information

**Input**: `UpdateProfileRequest`

**Output**: `ProfileResponse`

**Business Rules**:
- Profile must exist
- Partial updates supported
- Validation is performed by entity

---

### Experience Use Cases

#### ✅ AddExperienceUseCase
**Type**: Command

**Purpose**: Add new work experience

**Input**: `AddExperienceRequest`

**Output**: `WorkExperienceResponse`

**Business Rules**:
- orderIndex must be unique per profile
- Date range must be valid

#### ✅ EditExperienceUseCase
**Type**: Command

**Purpose**: Update existing experience

**Input**: `EditExperienceRequest`

**Output**: `WorkExperienceResponse`

**Business Rules**:
- Experience must exist
- Partial updates supported

#### ✅ DeleteExperienceUseCase
**Type**: Command

**Purpose**: Delete work experience

**Input**: `DeleteExperienceRequest`

**Output**: `SuccessResponse`

**Business Rules**:
- Experience must exist
- Deletion is permanent

#### ✅ ListExperiencesUseCase
**Type**: Query

**Purpose**: List all experiences

**Input**: `ListExperiencesRequest`

**Output**: `WorkExperienceListResponse`

**Business Rules**:
- Ordered by orderIndex
- Sort direction configurable

---

### Skill Use Cases

#### ✅ AddSkillUseCase
**Type**: Command

**Purpose**: Add new skill

**Business Rules**:
- Name must be unique per profile
- orderIndex must be unique

#### ✅ EditSkillUseCase
**Type**: Command

**Purpose**: Update skill

**Business Rules**:
- Name uniqueness validated on change

#### ✅ DeleteSkillUseCase
**Type**: Command

**Purpose**: Delete skill

#### ✅ ListSkillsUseCase
**Type**: Query

**Purpose**: List all skills

**Features**:
- Optional category filter
- Sorted by orderIndex
- Returns unique categories

---

### Education Use Cases

#### ✅ AddEducationUseCase
**Type**: Command

**Purpose**: Add education entry

**Business Rules**:
- orderIndex must be unique

#### ✅ EditEducationUseCase
**Type**: Command

**Purpose**: Update education

#### ✅ DeleteEducationUseCase
**Type**: Command

**Purpose**: Delete education

---

### CV Use Cases

#### ✅ GetCompleteCVUseCase
**Type**: Query

**Purpose**: Aggregate complete CV data

**Output**: `CompleteCVResponse`

**Aggregates**:
- Profile (required)
- Work Experiences (ordered)
- Skills (ordered)
- Education (ordered)

**Business Rules**:
- Profile must exist
- Empty lists returned if no data

**Example**:
```python
use_case = GetCompleteCVUseCase(
    profile_repo,
    experience_repo,
    skill_repo,
    education_repo
)
cv = await use_case.execute(GetCompleteCVRequest())
print(f"CV for {cv.profile.name}")
print(f"Experiences: {len(cv.experiences)}")
print(f"Skills: {len(cv.skills)}")
```

#### ✅ GenerateCVPDFUseCase
**Type**: Query

**Purpose**: Generate CV as PDF

**Status**: ⚠️ Placeholder (not yet implemented)

**Future Implementation**:
- PDF generation with template engine
- Multiple format options
- File storage/cloud upload

---

## DTOs (Data Transfer Objects)

DTOs are simple data containers for transferring data between layers.

### Base DTOs

**SuccessResponse**
```python
@dataclass
class SuccessResponse:
    success: bool = True
    message: str = "Operation completed successfully"
```

**ErrorResponse**
```python
@dataclass
class ErrorResponse:
    success: bool = False
    message: str
    errors: list[str]
```

**PaginationRequest**
```python
@dataclass
class PaginationRequest:
    skip: int = 0
    limit: int = 100
    sort_by: Optional[str] = None
    ascending: bool = True
```

### Entity-Specific DTOs

Each entity has:
- **Request DTOs**: For input (Create, Update, List, etc.)
- **Response DTOs**: For output
- **from_entity()** class method for conversion

**Example**:
```python
@dataclass
class ProfileResponse:
    id: str
    name: str
    headline: str
    # ... more fields
    
    @classmethod
    def from_entity(cls, entity) -> "ProfileResponse":
        return cls(
            id=entity.id,
            name=entity.name,
            # ... map fields
        )
```

---

## Design Patterns

### 1. Use Case Pattern

Each use case:
- Implements `IUseCase`, `IQueryUseCase`, or `ICommandUseCase`
- Has single responsibility
- Depends on repository interfaces
- Returns DTOs

```python
class SomeUseCase(ICommandUseCase[SomeRequest, SomeResponse]):
    def __init__(self, repo: ISomeRepository):
        self.repo = repo
    
    async def execute(self, request: SomeRequest) -> SomeResponse:
        # 1. Validate
        # 2. Get/Create entities
        # 3. Business logic
        # 4. Persist
        # 5. Return DTO
```

### 2. CQRS Pattern

**Queries** (read-only):
- Implement `IQueryUseCase`
- Don't modify state
- Can be cached

**Commands** (write):
- Implement `ICommandUseCase`
- Modify state
- Validate business rules

### 3. DTO Pattern

**Benefits**:
- ✅ Decouples API from domain
- ✅ Explicit contracts
- ✅ Easy serialization
- ✅ Validation at boundaries

---

## Dependency Flow

```
API Layer
    ↓ depends on
Use Cases (Application Layer)
    ↓ depends on
Repository Interfaces (Shared)
    ↑ implemented by
Repositories (Infrastructure Layer)
```

**Key**: Use cases depend on **interfaces**, not **implementations**.

---

## Exception Handling

Use cases throw **application-level exceptions**:

```python
from app.shared.exceptions import (
    NotFoundException,
    DuplicateException,
    BusinessRuleViolationException,
)

# In use case
if not entity:
    raise NotFoundException("Entity", entity_id)

if await repo.exists_by_name(name):
    raise DuplicateException("Entity", "name", name)
```

These exceptions are caught in the API layer and converted to HTTP responses.

---

## Testing Use Cases

Use cases are easy to test with mock repositories:

```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_get_profile_use_case():
    # Arrange
    mock_repo = AsyncMock(spec=IProfileRepository)
    mock_repo.get_profile.return_value = Profile.create(
        name="Test",
        headline="Tester"
    )
    
    use_case = GetProfileUseCase(mock_repo)
    
    # Act
    response = await use_case.execute(GetProfileRequest())
    
    # Assert
    assert response.name == "Test"
    mock_repo.get_profile.assert_called_once()
```

---

## Best Practices

### ✅ Do

1. **Keep use cases focused**: One responsibility per use case
2. **Depend on interfaces**: Not concrete implementations
3. **Validate in entities**: Let domain handle business rules
4. **Use DTOs**: Don't expose entities to API
5. **Handle exceptions**: Convert domain errors to application errors
6. **Document business rules**: Clear docstrings

### ❌ Don't

1. **Don't put UI logic**: Keep it framework-agnostic
2. **Don't depend on infrastructure**: Use interfaces
3. **Don't skip validation**: Even if API validates
4. **Don't expose entities**: Always return DTOs
5. **Don't catch domain exceptions**: Let them bubble up

---

## Future Enhancements

Potential additions:

- **Validation layer**: Pre-use-case request validation
- **Event publishing**: Domain events after operations
- **Transactions**: UnitOfWork pattern
- **Caching**: Query result caching
- **Audit logging**: Track all operations
- **Rate limiting**: Prevent abuse

---

**Last Updated**: February 2025  
**Maintainer**: Azfe Development Team