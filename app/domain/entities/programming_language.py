"""
ProgrammingLanguage Entity.

Represents a programming language in the portfolio.

Business Rules Applied:
- RB-PL01: name is required (1-50 chars)
- RB-PL02: level is optional (basic, intermediate, advanced, expert)
- RB-PL03: orderIndex is required and must be >= 0
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime

from ..exceptions import (
    EmptyFieldError,
    InvalidLengthError,
    InvalidNameError,
    InvalidOrderIndexError,
    InvalidProgrammingLanguageLevelError,
)

# Valid programming language levels
VALID_PROGRAMMING_LANGUAGE_LEVELS = {"basic", "intermediate", "advanced", "expert"}


@dataclass
class ProgrammingLanguage:
    """
    ProgrammingLanguage entity representing a programming language proficiency.

    Programming languages are ordered and can have proficiency levels.
    """

    id: str
    profile_id: str
    name: str
    order_index: int
    level: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # Constants
    MAX_NAME_LENGTH = 50

    def __post_init__(self):
        """Validate entity invariants after initialization."""
        self._validate_profile_id()
        self._validate_name()
        self._validate_level()
        self._validate_order_index()

    @staticmethod
    def create(
        profile_id: str,
        name: str,
        order_index: int,
        level: str | None = None,
    ) -> "ProgrammingLanguage":
        """
        Factory method to create a new ProgrammingLanguage.

        Args:
            profile_id: Reference to the Profile
            name: Language name (e.g., "Python", "TypeScript")
            order_index: Position in the ordered list
            level: Proficiency level (basic, intermediate, advanced, expert)

        Returns:
            A new ProgrammingLanguage instance with generated UUID
        """
        return ProgrammingLanguage(
            id=str(uuid.uuid4()),
            profile_id=profile_id,
            name=name,
            order_index=order_index,
            level=level,
        )

    def update_info(
        self,
        name: str | None = None,
        level: str | None = None,
    ) -> None:
        """
        Update programming language information.

        Args:
            name: New name (optional)
            level: New level (optional)
        """
        if name is not None:
            self.name = name
            self._validate_name()

        if level is not None:
            self.level = level
            self._validate_level()

        self._mark_as_updated()

    def update_order(self, new_order_index: int) -> None:
        """
        Update the order index.

        Args:
            new_order_index: New position in the list
        """
        self.order_index = new_order_index
        self._validate_order_index()
        self._mark_as_updated()

    def remove_level(self) -> None:
        """Remove the proficiency level."""
        self.level = None
        self._mark_as_updated()

    def _validate_profile_id(self) -> None:
        """Validate profile_id exists."""
        if not self.profile_id or not self.profile_id.strip():
            raise EmptyFieldError("profile_id")

    def _validate_name(self) -> None:
        """Validate name field according to business rules."""
        if not self.name or not self.name.strip():
            raise InvalidNameError("Programming language name cannot be empty")

        if len(self.name) > self.MAX_NAME_LENGTH:
            raise InvalidLengthError("name", max_length=self.MAX_NAME_LENGTH)

    def _validate_level(self) -> None:
        """Validate level field if provided."""
        if self.level is not None:
            if self.level.strip() == "":
                self.level = None
            elif self.level.lower() not in VALID_PROGRAMMING_LANGUAGE_LEVELS:
                raise InvalidProgrammingLanguageLevelError(self.level)
            else:
                # Normalize to lowercase
                self.level = self.level.lower()

    def _validate_order_index(self) -> None:
        """Validate order index."""
        if self.order_index < 0:
            raise InvalidOrderIndexError(self.order_index)

    def _mark_as_updated(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"ProgrammingLanguage(id={self.id}, name={self.name}, level={self.level})"
        )
