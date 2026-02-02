"""
Education Use Cases Module.

Contains all use cases related to education management.
"""

from .add_education import AddEducationUseCase
from .edit_education import EditEducationUseCase
from .delete_education import DeleteEducationUseCase

__all__ = [
    "AddEducationUseCase",
    "EditEducationUseCase",
    "DeleteEducationUseCase",
]