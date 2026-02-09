"""
Value Objects Module.

Value Objects are immutable objects that are defined by their attributes
rather than a unique identity. They encapsulate domain concepts and ensure
consistency through validation.

Implemented Value Objects:
- DateRange: Represents a period with start and end dates
- Email: Validated email address (RFC 5322 simplified)
- Phone: Validated phone number (E.164 format)
- SkillLevel: Type-safe skill proficiency enumeration
- ContactInfo: Composite of Email and optional Phone

Value Objects follow these principles:
1. Immutability: Once created, cannot be changed (frozen dataclasses)
2. Equality by value: Two VOs are equal if all attributes match
3. Self-validation: Validate on construction
4. Side-effect free: All operations return new instances
5. No identity: Unlike entities, VOs have no ID
"""

from .contact_info import ContactInfo
from .date_range import DateRange
from .email import Email
from .language_proficiency import LanguageProficiency, LanguageProficiencyEnum
from .phone import Phone
from .programming_language_level import (
    ProgrammingLanguageLevel,
    ProgrammingLanguageLevelEnum,
)
from .skill_level import SkillLevel, SkillLevelEnum

__all__ = [
    "DateRange",
    "Email",
    "Phone",
    "SkillLevel",
    "SkillLevelEnum",
    "ProgrammingLanguageLevel",
    "ProgrammingLanguageLevelEnum",
    "LanguageProficiency",
    "LanguageProficiencyEnum",
    "ContactInfo",
]
