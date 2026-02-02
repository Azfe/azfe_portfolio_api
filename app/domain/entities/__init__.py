"""
Domain entities module.

This module contains all domain entities following DDD principles.
Each entity is rich in behavior and maintains business invariants.
"""

from .additional_training import AdditionalTraining
from .certification import Certification
from .contact_information import ContactInformation
from .contact_message import ContactMessage
from .education import Education
from .profile import Profile
from .project import Project
from .skill import Skill
from .social_network import SocialNetwork
from .tool import Tool
from .work_experience import WorkExperience

__all__ = [
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
]
