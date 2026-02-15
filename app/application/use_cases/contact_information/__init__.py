"""
ContactInformation Use Cases Module.

Contains all use cases related to contact information management.
"""

from .create_contact_information import CreateContactInformationUseCase
from .delete_contact_information import DeleteContactInformationUseCase
from .get_contact_information import GetContactInformationUseCase
from .update_contact_information import UpdateContactInformationUseCase

__all__ = [
    "GetContactInformationUseCase",
    "CreateContactInformationUseCase",
    "UpdateContactInformationUseCase",
    "DeleteContactInformationUseCase",
]
