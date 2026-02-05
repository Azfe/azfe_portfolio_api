"""
Shared Module.

This module contains code shared across all architectural layers:
- Interfaces: Contracts (Ports) for repositories, use cases, mappers
- Types: Common type definitions and type aliases
- Utils: Utility functions and helpers
- Exceptions: Base exceptions for the application layer

The shared module follows the Dependency Rule:
- Can be imported by any layer
- Should not depend on any specific layer
- Contains only abstractions and generic utilities

Structure:
    shared/
    ├── interfaces/     # Abstract interfaces (Ports)
    ├── types/          # Common types and type aliases
    ├── utils/          # Generic utility functions
    ├── exceptions/     # Application-level exceptions
    └── __init__.py     # This file
"""

# Import interfaces for easy access
from .interfaces import (  # Repository interfaces; Use case interfaces; Mapper interfaces
    ICommandUseCase,
    IContactMessageRepository,
    IDTOMapper,
    IMapper,
    IOrderedRepository,
    IProfileRepository,
    IQueryUseCase,
    IRepository,
    ISocialNetworkRepository,
    IUniqueNameRepository,
    IUseCase,
    IValidator,
    IValueObjectMapper,
)

__all__ = [
    # Repository interfaces
    "IRepository",
    "IProfileRepository",
    "IOrderedRepository",
    "IContactMessageRepository",
    "IUniqueNameRepository",
    "ISocialNetworkRepository",
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

__version__ = "0.1.0"
