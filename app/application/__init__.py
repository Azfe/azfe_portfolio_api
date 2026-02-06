"""
Application Layer Module.

This layer contains the use cases (application business logic) and DTOs.

The application layer:
- Orchestrates the flow of data between entities and repositories
- Implements use cases (business operations)
- Depends on domain interfaces, not infrastructure
- Uses DTOs for input/output
- Handles application-level exceptions

Structure:
    application/
    ├── use_cases/     # Use case implementations
    ├── dto/           # Data Transfer Objects
    └── __init__.py    # This file
"""

__version__ = "0.1.0"
