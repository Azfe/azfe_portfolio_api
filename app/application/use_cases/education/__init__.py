"""
Education Use Cases Module.

Contains all use cases related to education management.
"""

from .add_education import AddEducationUseCase
from .delete_education import DeleteEducationUseCase
from .edit_education import EditEducationUseCase

__all__ = [
    "AddEducationUseCase",
    "EditEducationUseCase",
    "DeleteEducationUseCase",
]
