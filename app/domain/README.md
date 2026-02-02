# Domain Layer Documentation

## Overview

This directory contains the **Domain Layer** of the Portfolio Backend, following **Domain-Driven Design (DDD)** and **Clean Architecture** principles.

The domain layer is the **heart of the business logic** and is completely **independent** of:

- Infrastructure (databases, frameworks, external services)
- Application layer concerns (use cases, DTOs)
- Presentation layer (API, controllers)

## Structure

```text
domain/
├── entities/           # Rich domain entities with behavior
├── value_objects/      # Immutable value objects (see issue #3.2.2)
├── exceptions/         # Domain-specific exceptions
└── README.md          # This file
```

## Entities

Entities are the core building blocks of the domain. Each entity:

- Has a **unique identity** (UUID)
- Contains **business logic and validation**
- Maintains **invariants** (rules that must always be true)
- Is **rich in behavior**, not just a data container
- Is **framework-agnostic** (uses Python dataclasses, not Pydantic or DB models)

### Available Entities

1. **Profile** (`profile.py`)
   - Represents the portfolio owner's professional profile
   - Only ONE profile can exist in the system
   - Contains: name, headline, bio, location, avatar

2. **WorkExperience** (`work_experience.py`)
   - Professional work experience entries
   - Maintains temporal coherence (startDate < endDate)
   - Includes responsibilities and ordering

3. **Skill** (`skill.py`)
   - Technical or professional skills
   - Categorized with optional proficiency levels
   - Unique by name per profile

4. **Education** (`education.py`)
   - Formal education entries
   - Institution, degree, field of study
   - Temporal coherence maintained

5. **Project** (`project.py`)
   - Professional projects
   - Includes technologies, URLs, and descriptions
   - Special rule: description must be detailed if no URLs provided

6. **Certification** (`certification.py`)
   - Professional certifications
   - Can have expiry dates and credential verification

7. **AdditionalTraining** (`additional_training.py`)
   - Courses, workshops, and training
   - Non-formal education and professional development

8. **ContactInformation** (`contact_information.py`)
   - Official contact details
   - Email, phone, social links
   - Only ONE per profile

9. **ContactMessage** (`contact_message.py`)
   - Messages from visitors via contact form
   - Append-only (no updates after creation)
   - Status tracking: pending, read, replied

10. **SocialNetwork** (`social_network.py`)
    - Social media profile links
    - Unique by platform per profile

11. **Tool** (`tool.py`)
    - Technologies, frameworks, software used
    - Categorized with optional icons

## Design Principles

### 1. Factory Methods

All entities use static factory methods for creation:

```python
profile = Profile.create(
    name="John Doe",
    headline="Software Engineer"
)
```

### 2. Explicit Validation

Entities validate themselves in `__post_init__`:

```python
def __post_init__(self):
    self._validate_name()
    self._validate_email()
    # ... other validations
```

### 3. Business Rules Enforcement

Domain logic is embedded in entity methods:

```python
def is_current_position(self) -> bool:
    """Check if this is a current position."""
    return self.end_date is None
```

### 4. Immutability Where Appropriate
- Entities maintain updated_at timestamps
- Value Objects (coming in issue #3.2.2) are immutable

## Business Rules Reference

All entities implement business rules documented in:
- `docs/business_rules.md`
- See each entity's docstring for specific rules applied

### Key Rules:
- **Uniqueness**: Profile is unique, Skills/Tools unique by name, SocialNetwork unique by platform
- **Temporal Coherence**: End dates must be after start dates
- **Ordering**: All ordered entities must have unique orderIndex per profile
- **URL Validation**: All URLs must follow RFC 3986
- **Email Validation**: Standard email format validation
- **Length Constraints**: All text fields have min/max length requirements

## Exceptions

All domain exceptions inherit from `DomainError`:

```python
from app.domain.exceptions import (
    DomainError,
    EmptyFieldError,
    InvalidEmailError,
    InvalidDateRangeError,
    # ... etc
)
```

### Exception Hierarchy:
- `DomainError` (base)
  - `EmptyFieldError`
  - `InvalidLengthError`
  - `InvalidEmailError`
  - `InvalidPhoneError`
  - `InvalidURLError`
  - `InvalidDateRangeError`
  - `InvalidOrderIndexError`
  - And more...

## Usage Examples

### Creating an Entity

```python
from app.domain.entities import WorkExperience
from datetime import datetime

experience = WorkExperience.create(
    profile_id="123e4567-e89b-12d3-a456-426614174000",
    role="Senior Developer",
    company="Tech Corp",
    start_date=datetime(2020, 1, 1),
    order_index=1,
    description="Leading backend development"
)
```

### Updating an Entity

```python
experience.update_info(
    role="Lead Developer",
    description="Leading the entire engineering team"
)
```

### Validation

```python
try:
    skill = Skill.create(
        profile_id="123e4567-e89b-12d3-a456-426614174000",
        name="",  # Invalid!
        category="Programming",
        order_index=1
    )
except InvalidNameError as e:
    print(f"Validation failed: {e.message}")
```

## Testing

All entities should be tested in isolation (unit tests):

```python
def test_profile_creation():
    profile = Profile.create(
        name="John Doe",
        headline="Developer"
    )
    assert profile.id is not None
    assert profile.name == "John Doe"
```

See `tests/unit/domain/` for complete test suite.

## Dependencies

The domain layer has **ZERO** external dependencies:
- No database imports
- No FastAPI imports
- No Pydantic models
- Only Python standard library (dataclasses, datetime, uuid, re)

This ensures:
- ✅ **Testability**: Easy to unit test
- ✅ **Portability**: Can be used in any Python context
- ✅ **Maintainability**: Changes to infrastructure don't affect domain
- ✅ **Clarity**: Business logic is pure and explicit

## Next Steps

After implementing entities (issue #3.2.1):
1. **Issue #3.2.2**: Implement Value Objects (DateRange, ContactInfo, etc.)
2. **Issue #3.3.x**: Implement Repository interfaces and implementations
3. **Issue #3.4.x**: Implement Use Cases in the Application layer

## Notes

- All entities use **UUID v4** for IDs (generated at domain level)
- All dates use **datetime** objects (UTC)
- All timestamps (`created_at`, `updated_at`) are auto-managed
- Entities are **framework-agnostic** but will be mapped to MongoDB documents in the infrastructure layer

---

**Last Updated**: January 2025  
**Maintainer**: Azfe Development Team