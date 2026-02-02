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
    Profile,
    WorkExperience,
    Skill,
    Education,
    Project,
    Certification,
    AdditionalTraining,
    ContactInformation,
    ContactMessage,
    SocialNetwork,
    Tool,
)

# Export value objects
from .value_objects import (
    DateRange,
    Email,
    Phone,
    SkillLevel,
    SkillLevelEnum,
    ContactInfo,
)

# Export exceptions
from .exceptions import (
    DomainError,
    InvalidEmailError,
    InvalidPhoneError,
    InvalidURLError,
    InvalidDateRangeError,
    InvalidOrderIndexError,
    InvalidSkillLevelError,
    EmptyFieldError,
    InvalidLengthError,
    DuplicateValueError,
    InvalidTitleError,
    InvalidNameError,
    InvalidDescriptionError,
    InvalidRoleError,
    InvalidCompanyError,
    InvalidInstitutionError,
    InvalidIssuerError,
    InvalidProviderError,
    InvalidCategoryError,
    InvalidPlatformError,
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