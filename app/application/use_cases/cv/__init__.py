"""
CV Use Cases Module.

Contains use cases for retrieving and generating the complete CV.
"""

from .get_complete_cv import GetCompleteCVUseCase
from .generate_cv_pdf import GenerateCVPDFUseCase

__all__ = [
    "GetCompleteCVUseCase",
    "GenerateCVPDFUseCase",
]