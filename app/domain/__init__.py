"""
Domain Layer Module.

This module contains the core business logic following DDD principles.
It is completely independent of infrastructure, frameworks, and external libraries.

The domain layer includes:
- Entities: Rich business objects with identity
- Value Objects: Immutable objects without identity
- Exceptions: Domain-specific error types
- Business Rules: Encoded in entity behavior

For detailed documentation, see README.md in this directory.
"""

# Export entities for easy importing
from .entities import (
    AdditionalTraining,
    Certification,
    ContactInformation,
    ContactMessage,
    Education,
    Profile,
    Project,
    Skill,
    SocialNetwork,
    Tool,
    WorkExperience,
)

# Export exceptions
from .exceptions import (
    DomainError,
    DuplicateValueError,
    EmptyFieldError,
    InvalidCategoryError,
    InvalidCompanyError,
    InvalidDateRangeError,
    InvalidDescriptionError,
    InvalidEmailError,
    InvalidInstitutionError,
    InvalidIssuerError,
    InvalidLengthError,
    InvalidNameError,
    InvalidOrderIndexError,
    InvalidPhoneError,
    InvalidPlatformError,
    InvalidProviderError,
    InvalidRoleError,
    InvalidSkillLevelError,
    InvalidTitleError,
    InvalidURLError,
)

# Export value objects
from .value_objects import (
    ContactInfo,
    DateRange,
    Email,
    Phone,
    SkillLevel,
    SkillLevelEnum,
)

__all__ = [
    # Entities
    "Profile",
    "WorkExperience",
    "Skill",
    "Education",
    "Project",
    "Certification",
    "AdditionalTraining",
    "ContactInformation",
    "ContactMessage",
    "SocialNetwork",
    "Tool",
    # Value Objects
    "DateRange",
    "Email",
    "Phone",
    "SkillLevel",
    "SkillLevelEnum",
    "ContactInfo",
    # Exceptions
    "DomainError",
    "InvalidEmailError",
    "InvalidPhoneError",
    "InvalidURLError",
    "InvalidDateRangeError",
    "InvalidOrderIndexError",
    "InvalidSkillLevelError",
    "EmptyFieldError",
    "InvalidLengthError",
    "DuplicateValueError",
    "InvalidTitleError",
    "InvalidNameError",
    "InvalidDescriptionError",
    "InvalidRoleError",
    "InvalidCompanyError",
    "InvalidInstitutionError",
    "InvalidIssuerError",
    "InvalidProviderError",
    "InvalidCategoryError",
    "InvalidPlatformError",
]

__version__ = "0.1.0"
