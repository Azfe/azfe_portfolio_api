# Interfaces Documentation (Ports)

## Overview

This module contains **interface definitions** (Ports) following **Clean Architecture** and **Hexagonal Architecture** (Ports & Adapters) patterns.

Interfaces define **contracts** that concrete implementations must follow, enabling:

- ✅ **Dependency Inversion Principle**: High-level modules depend on abstractions
- ✅ **Testability**: Easy to mock and test in isolation
- ✅ **Flexibility**: Swap implementations without changing business logic
- ✅ **Independence**: Domain/Application layers don't depend on infrastructure

## Architecture Overview

```text
┌─────────────────────────────────────────────────────────┐
│                    Application Layer                     │
│  (Use Cases depend on Repository INTERFACES)            │
└──────────────┬──────────────────────────┬───────────────┘
               │                          │
               │ Depends on               │ Depends on
               ▼                          ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│   Repository Interfaces  │  │   Mapper Interfaces      │
│   (Ports - Abstract)     │  │   (Ports - Abstract)     │
└──────────┬───────────────┘  └──────────┬───────────────┘
           │                              │
           │ Implemented by               │ Implemented by
           ▼                              ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│  Repository Impls        │  │   Mapper Impls           │
│  (Adapters - Concrete)   │  │   (Adapters - Concrete)  │
│  MongoDB / PostgreSQL    │  │   Entity ↔ Document      │
└──────────────────────────┘  └──────────────────────────┘
```

**Key Principle**: The arrow of dependency always points **inward** toward abstractions.

## Interface Categories

### 1. Repository Interfaces (`repository.py`)

Repository interfaces define the contract for **data persistence**.

#### Generic Repository: `IRepository[T]`

The base repository interface that all specific repositories extend.

**Methods:**

```python
async def add(entity: T) -> T
async def update(entity: T) -> T
async def delete(entity_id: str) -> bool
async def get_by_id(entity_id: str) -> Optional[T]
async def list_all(skip: int, limit: int, sort_by: str, ascending: bool) -> List[T]
async def count(filters: Dict[str, Any]) -> int
async def exists(entity_id: str) -> bool
async def find_by(**filters) -> List[T]
```

**Usage:**
```python
from app.shared.interfaces import IRepository
from app.domain.entities import Profile

class ProfileRepository(IRepository[Profile]):
    async def add(self, entity: Profile) -> Profile:
        # MongoDB implementation
        ...
```

#### Specialized Repositories

**IProfileRepository** - Profile-specific operations
- `get_profile()` - Get the single profile
- `profile_exists()` - Check if profile exists

**IOrderedRepository[T]** - For entities with orderIndex
- `get_by_order_index()` - Get by order
- `get_all_ordered()` - Get sorted by order
- `reorder()` - Reorder entities

**IContactMessageRepository** - Message-specific operations
- `get_pending_messages()` - Get pending messages
- `get_messages_by_status()` - Filter by status
- `mark_as_read()` - Mark as read
- `mark_as_replied()` - Mark as replied

**IUniqueNameRepository[T]** - For entities with unique names
- `exists_by_name()` - Check name uniqueness
- `get_by_name()` - Get by name

**ISocialNetworkRepository** - Social network operations
- `exists_by_platform()` - Check platform uniqueness
- `get_by_platform()` - Get by platform

#### Type Aliases for Convenience

```python
ProfileRepository = IProfileRepository
WorkExperienceRepository = IOrderedRepository[WorkExperience]
SkillRepository = IUniqueNameRepository[Skill]
EducationRepository = IOrderedRepository[Education]
ProjectRepository = IOrderedRepository[Project]
CertificationRepository = IOrderedRepository[Certification]
AdditionalTrainingRepository = IOrderedRepository[AdditionalTraining]
ContactInformationRepository = IRepository[ContactInformation]
ContactMessageRepository = IContactMessageRepository
SocialNetworkRepository = ISocialNetworkRepository
ToolRepository = IUniqueNameRepository[Tool]
```

---

### 2. Use Case Interfaces (`use_case.py`)

Use case interfaces define the contract for **application business logic**.

#### Generic Use Case: `IUseCase[TRequest, TResponse]`

Base interface for all use cases.

**Method:**
```python
async def execute(request: TRequest) -> TResponse
```

**Usage:**
```python
from app.shared.interfaces import IUseCase
from app.application.dto import GetProfileRequest, GetProfileResponse

class GetProfileUseCase(IUseCase[GetProfileRequest, GetProfileResponse]):
    def __init__(self, profile_repo: IProfileRepository):
        self.profile_repo = profile_repo
        
    async def execute(self, request: GetProfileRequest) -> GetProfileResponse:
        profile = await self.profile_repo.get_profile()
        if not profile:
            raise NotFoundException("Profile", "single")
        return GetProfileResponse.from_entity(profile)
```

#### CQRS Interfaces

**IQueryUseCase[TRequest, TResponse]** - Read-only operations
- Never modifies state
- Can be cached aggressively
- Optimized for reads

**ICommandUseCase[TRequest, TResponse]** - Write operations
- Modifies state
- Validates business rules
- May use transactions

**Example:**
```python
from app.shared.interfaces import IQueryUseCase, ICommandUseCase

# Query (read-only)
class GetAllSkillsQuery(IQueryUseCase[GetAllSkillsRequest, GetAllSkillsResponse]):
    async def execute(self, request: GetAllSkillsRequest) -> GetAllSkillsResponse:
        skills = await self.skill_repo.list_all()
        return GetAllSkillsResponse(skills=skills)

# Command (write)
class CreateSkillCommand(ICommandUseCase[CreateSkillRequest, CreateSkillResponse]):
    async def execute(self, request: CreateSkillRequest) -> CreateSkillResponse:
        skill = Skill.create(...)
        created = await self.skill_repo.add(skill)
        return CreateSkillResponse.from_entity(created)
```

#### Validator Interface: `IValidator[TRequest]`

For input validation.

**Method:**
```python
def validate(request: TRequest) -> List[str]
```

**Usage:**
```python
from app.shared.interfaces import IValidator

class CreateProfileValidator(IValidator[CreateProfileRequest]):
    def validate(self, request: CreateProfileRequest) -> List[str]:
        errors = []
        if not request.name:
            errors.append("Name is required")
        if len(request.name) > 100:
            errors.append("Name too long")
        return errors
```

---

### 3. Mapper Interfaces (`mapper.py`)

Mapper interfaces define the contract for **data conversion** between layers.

#### Generic Mapper: `IMapper[TDomain, TPersistence]`

Converts between domain entities and persistence models.

**Methods:**

```python
def to_domain(persistence_model: TPersistence) -> TDomain
def to_persistence(domain_entity: TDomain) -> TPersistence
def to_domain_list(persistence_models: List[TPersistence]) -> List[TDomain]
def to_persistence_list(domain_entities: List[TDomain]) -> List[TPersistence]
```

**Usage:**

```python
from app.shared.interfaces import IMapper
from app.domain.entities import Profile
from typing import Dict, Any

class ProfileMapper(IMapper[Profile, Dict[str, Any]]):
    def to_domain(self, persistence_model: Dict[str, Any]) -> Profile:
        return Profile(
            id=str(persistence_model['_id']),
            name=persistence_model['name'],
            headline=persistence_model['headline'],
            # ... more fields
        )
        
    def to_persistence(self, domain_entity: Profile) -> Dict[str, Any]:
        return {
            '_id': ObjectId(domain_entity.id),
            'name': domain_entity.name,
            'headline': domain_entity.headline,
            # ... more fields
        }
```

#### DTO Mapper: `IDTOMapper[TDomain, TDTO]`

Converts between domain entities and DTOs (API layer).

**Methods:**

```python
def to_dto(domain_entity: TDomain) -> TDTO
def from_dto(dto: TDTO) -> TDomain
def to_dto_list(domain_entities: List[TDomain]) -> List[TDTO]
def from_dto_list(dtos: List[TDTO]) -> List[TDomain]
```

**Usage:**

```python
from app.shared.interfaces import IDTOMapper
from app.domain.entities import Profile
from app.api.schemas import ProfileResponse

class ProfileDTOMapper(IDTOMapper[Profile, ProfileResponse]):
    def to_dto(self, domain_entity: Profile) -> ProfileResponse:
        return ProfileResponse(
            id=domain_entity.id,
            name=domain_entity.name,
            headline=domain_entity.headline,
            bio=domain_entity.bio,
            location=domain_entity.location,
            avatarUrl=domain_entity.avatar_url,
        )
        
    def from_dto(self, dto: ProfileResponse) -> Profile:
        # Usually used for requests, not responses
        ...
```

#### Value Object Mapper: `IValueObjectMapper[TDomain, TPrimitive]`

Converts value objects to/from primitives.

**Methods:**

```python
def to_primitive(value_object: TDomain) -> TPrimitive
def from_primitive(primitive: TPrimitive) -> TDomain
```

**Usage:**

```python
from app.shared.interfaces import IValueObjectMapper
from app.domain.value_objects import Email

class EmailMapper(IValueObjectMapper[Email, str]):
    def to_primitive(self, value_object: Email) -> str:
        return value_object.value
        
    def from_primitive(self, primitive: str) -> Email:
        return Email.create(primitive)
```

---

## Design Patterns

### 1. Repository Pattern

**Intent**: Mediate between domain and data mapping layers using a collection-like interface.

**Benefits:**

- ✅ Decouples domain from persistence
- ✅ Centralizes data access logic
- ✅ Enables testing with mock repositories
- ✅ Allows swapping storage implementations

### 2. Dependency Inversion Principle

**Intent**: High-level modules should not depend on low-level modules. Both should depend on abstractions.

```python
# ❌ Bad: Use case depends on concrete repository
class GetProfileUseCase:
    def __init__(self, mongo_profile_repo: MongoProfileRepository):
        self.repo = mongo_profile_repo  # Tight coupling!

# ✅ Good: Use case depends on interface
class GetProfileUseCase:
    def __init__(self, profile_repo: IProfileRepository):
        self.repo = profile_repo  # Loose coupling!
```

### 3. Command/Query Separation (CQRS)

**Intent**: Separate read and write operations.

**Benefits:**

- ✅ Optimized separately (reads vs writes)
- ✅ Different consistency models
- ✅ Clearer intention
- ✅ Better scalability

### 4. Port & Adapter (Hexagonal Architecture)

**Ports**: Interfaces (this module)
**Adapters**: Concrete implementations (infrastructure)

```text
Domain ← Use Cases ← [PORT] → [ADAPTER] → MongoDB
                       ↑           ↑
                   Interface   Implementation
```

---

## Testing with Interfaces

Interfaces make testing trivial through mocking:

### Example: Mocking a Repository

```python
import pytest
from app.shared.interfaces import IProfileRepository
from app.domain.entities import Profile

class MockProfileRepository(IProfileRepository):
    def __init__(self):
        self.profiles = {}
        
    async def add(self, entity: Profile) -> Profile:
        self.profiles[entity.id] = entity
        return entity
        
    async def get_profile(self) -> Profile:
        if not self.profiles:
            return None
        return list(self.profiles.values())[0]
        
    # ... implement other methods

@pytest.mark.asyncio
async def test_get_profile_use_case():
    # Arrange
    mock_repo = MockProfileRepository()
    profile = Profile.create(name="John", headline="Dev")
    await mock_repo.add(profile)
    
    use_case = GetProfileUseCase(mock_repo)
    
    # Act
    response = await use_case.execute(GetProfileRequest())
    
    # Assert
    assert response.name == "John"
```

### Example: Using pytest-mock

```python
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_with_mock(mocker):
    # Mock repository
    mock_repo = mocker.Mock(spec=IProfileRepository)
    mock_repo.get_profile = AsyncMock(return_value=Profile.create(...))
    
    # Test use case
    use_case = GetProfileUseCase(mock_repo)
    result = await use_case.execute(GetProfileRequest())
    
    # Verify
    mock_repo.get_profile.assert_called_once()
```

---

## Best Practices

### 1. Keep Interfaces Minimal

```python
# ✅ Good: Focused interface
class IProfileRepository(IRepository[Profile]):
    async def get_profile(self) -> Optional[Profile]:
        pass

# ❌ Bad: Too many methods
class IProfileRepository(IRepository[Profile]):
    async def get_profile_with_experiences(self) -> Profile:
        pass
    async def get_profile_with_skills(self) -> Profile:
        pass
    async def get_profile_with_everything(self) -> Profile:
        pass
    # Use composition instead!
```

### 2. Use Type Hints Consistently

```python
# ✅ Good
async def get_by_id(self, entity_id: str) -> Optional[Profile]:
    pass

# ❌ Bad
async def get_by_id(self, entity_id):  # No type hints
    pass
```

### 3. Document Contracts Clearly

```python
async def add(self, entity: T) -> T:
    """
    Add a new entity.
    
    Args:
        entity: The entity to add
        
    Returns:
        The added entity with generated fields
        
    Raises:
        DuplicateValueError: If unique constraint violated
    """
    pass
```

### 4. Follow Naming Conventions

- Interfaces: Start with `I` (e.g., `IRepository`)
- Methods: Use verbs (e.g., `get`, `add`, `update`, `delete`)
- Async methods: Always use `async def`
- Return types: Always specify

---

## Common Pitfalls

### ❌ Leaking Implementation Details

```python
# Bad: Exposes MongoDB specifics
class IProfileRepository(ABC):
    async def find_by_mongo_query(self, query: dict) -> List[Profile]:
        pass
```

### ❌ Too Many Methods

```python
# Bad: Interface does too much
class IProfileRepository(ABC):
    async def add(self, entity: Profile) -> Profile: pass
    async def send_email(self, email: str) -> bool: pass  # Wrong layer!
    async def log_access(self, user_id: str) -> None: pass  # Wrong layer!
```

### ❌ Synchronous Methods

```python
# Bad: Blocks async operations
class IProfileRepository(ABC):
    def get_by_id(self, entity_id: str) -> Profile:  # Should be async!
        pass
```

---

## Integration Example

Complete flow from API to Database:

```python
# 1. API Layer (FastAPI)
@router.get("/profile")
async def get_profile(use_case: GetProfileUseCase = Depends(get_profile_use_case)):
    request = GetProfileRequest()
    response = await use_case.execute(request)
    return response

# 2. Application Layer (Use Case)
class GetProfileUseCase(IUseCase[GetProfileRequest, GetProfileResponse]):
    def __init__(self, profile_repo: IProfileRepository):  # Depends on interface
        self.repo = profile_repo
        
    async def execute(self, request: GetProfileRequest) -> GetProfileResponse:
        profile = await self.repo.get_profile()  # Uses interface method
        return GetProfileResponse.from_entity(profile)

# 3. Infrastructure Layer (Repository Implementation)
class MongoProfileRepository(IProfileRepository):  # Implements interface
    def __init__(self, db):
        self.collection = db.profiles
        
    async def get_profile(self) -> Optional[Profile]:
        doc = await self.collection.find_one()
        return ProfileMapper().to_domain(doc) if doc else None
```

---

## Future Enhancements

Potential additions based on project needs:

- **IEventPublisher**: For domain events
- **IUnitOfWork**: For transaction management
- **ICache**: For caching strategies
- **ILogger**: For structured logging
- **IEmailService**: For email notifications
- **IFileStorage**: For file uploads

---

## References

- **Clean Architecture** by Robert C. Martin
- **Domain-Driven Design** by Eric Evans
- **Implementing Domain-Driven Design** by Vaughn Vernon
- **Patterns of Enterprise Application Architecture** by Martin Fowler

---

**Last Updated**: February 2026
**Maintainer**: Azfe Developer
