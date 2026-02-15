"""
ContactMessage Use Cases Module.

Contains all use cases related to contact message management.
"""

from .create_contact_message import CreateContactMessageUseCase
from .delete_contact_message import DeleteContactMessageUseCase
from .list_contact_messages import ListContactMessagesUseCase

__all__ = [
    "CreateContactMessageUseCase",
    "ListContactMessagesUseCase",
    "DeleteContactMessageUseCase",
]
