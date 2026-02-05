"""
Shared Interfaces Module.

This module contains all interface definitions (Ports) following Clean Architecture
and Hexagonal Architecture (Ports & Adapters) patterns.

Interfaces define contracts that implementations must follow, enabling:
- Dependency Inversion Principle
- Testability (easy to mock)
- Flexibility (swap implementations)
- Independence (domain doesn't depend on infrastructure)

Available Interfaces:
- Repository Interfaces: Data persistence contracts
- Use Case Interfaces: Application business logic contracts
- Mapper Interfaces: Data conversion contracts

The domain and application layers depend on these interfaces,
while the infrastructure layer provides concrete implementations.
"""

# Mapper interfaces
from .mapper import IDTOMapper, IMapper, IValueObjectMapper

# Repository interfaces
from .repository import (  # Type aliases
    AdditionalTrainingRepository,
    CertificationRepository,
    ContactInformationRepository,
    ContactMessageRepository,
    EducationRepository,
    IContactMessageRepository,
    IOrderedRepository,
    IProfileRepository,
    IRepository,
    ISocialNetworkRepository,
    IUniqueNameRepository,
    ProfileRepository,
    ProjectRepository,
    SkillRepository,
    SocialNetworkRepository,
    ToolRepository,
    WorkExperienceRepository,
)

# Use case interfaces
from .use_case import ICommandUseCase, IQueryUseCase, IUseCase, IValidator

__all__ = [
    # Repository interfaces
    "IRepository",
    "IProfileRepository",
    "IOrderedRepository",
    "IContactMessageRepository",
    "IUniqueNameRepository",
    "ISocialNetworkRepository",
    # Repository type aliases
    "ProfileRepository",
    "WorkExperienceRepository",
    "SkillRepository",
    "EducationRepository",
    "ProjectRepository",
    "CertificationRepository",
    "AdditionalTrainingRepository",
    "ContactInformationRepository",
    "ContactMessageRepository",
    "SocialNetworkRepository",
    "ToolRepository",
    # Use case interfaces
    "IUseCase",
    "IQueryUseCase",
    "ICommandUseCase",
    "IValidator",
    # Mapper interfaces
    "IMapper",
    "IDTOMapper",
    "IValueObjectMapper",
]
