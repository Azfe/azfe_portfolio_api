"""
CV Use Cases Module.

Contains use cases for retrieving and generating the complete CV.
"""

from .generate_cv_pdf import GenerateCVPDFUseCase
from .get_complete_cv import GetCompleteCVUseCase

__all__ = [
    "GetCompleteCVUseCase",
    "GenerateCVPDFUseCase",
]
