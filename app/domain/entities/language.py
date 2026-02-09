"""
Language Entity.

Represents a spoken/written language in the portfolio.

Business Rules Applied:
- RB-L01: name is required (1-50 chars)
- RB-L02: proficiency is optional (a1, a2, b1, b2, c1, c2 — CEFR scale)
- RB-L03: orderIndex is required and must be >= 0
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime

from ..exceptions import (
    EmptyFieldError,
    InvalidLanguageProficiencyError,
    InvalidLengthError,
    InvalidNameError,
    InvalidOrderIndexError,
)

# Valid CEFR proficiency levels
VALID_PROFICIENCIES = {"a1", "a2", "b1", "b2", "c1", "c2"}


@dataclass
class Language:
    """
    Language entity representing a spoken/written language proficiency.

    Languages are ordered and can have CEFR proficiency levels.
    """

    id: str
    profile_id: str
    name: str
    order_index: int
    proficiency: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # Constants
    MAX_NAME_LENGTH = 50

    def __post_init__(self):
        """Validate entity invariants after initialization."""
        self._validate_profile_id()
        self._validate_name()
        self._validate_proficiency()
        self._validate_order_index()

    @staticmethod
    def create(
        profile_id: str,
        name: str,
        order_index: int,
        proficiency: str | None = None,
    ) -> "Language":
        """
        Factory method to create a new Language.

        Args:
            profile_id: Reference to the Profile
            name: Language name (e.g., "English", "Spanish")
            order_index: Position in the ordered list
            proficiency: CEFR proficiency level (a1, a2, b1, b2, c1, c2)

        Returns:
            A new Language instance with generated UUID
        """
        return Language(
            id=str(uuid.uuid4()),
            profile_id=profile_id,
            name=name,
            order_index=order_index,
            proficiency=proficiency,
        )

    def update_info(
        self,
        name: str | None = None,
        proficiency: str | None = None,
    ) -> None:
        """
        Update language information.

        Args:
            name: New name (optional)
            proficiency: New CEFR proficiency level (optional)
        """
        if name is not None:
            self.name = name
            self._validate_name()

        if proficiency is not None:
            self.proficiency = proficiency
            self._validate_proficiency()

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

    def remove_proficiency(self) -> None:
        """Remove the proficiency level."""
        self.proficiency = None
        self._mark_as_updated()

    def _validate_profile_id(self) -> None:
        """Validate profile_id exists."""
        if not self.profile_id or not self.profile_id.strip():
            raise EmptyFieldError("profile_id")

    def _validate_name(self) -> None:
        """Validate name field according to business rules."""
        if not self.name or not self.name.strip():
            raise InvalidNameError("Language name cannot be empty")

        if len(self.name) > self.MAX_NAME_LENGTH:
            raise InvalidLengthError("name", max_length=self.MAX_NAME_LENGTH)

    def _validate_proficiency(self) -> None:
        """Validate proficiency field if provided."""
        if self.proficiency is not None:
            if self.proficiency.strip() == "":
                self.proficiency = None
            elif self.proficiency.lower() not in VALID_PROFICIENCIES:
                raise InvalidLanguageProficiencyError(self.proficiency)
            else:
                # Normalize to lowercase
                self.proficiency = self.proficiency.lower()

    def _validate_order_index(self) -> None:
        """Validate order index."""
        if self.order_index < 0:
            raise InvalidOrderIndexError(self.order_index)

    def _mark_as_updated(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Language(id={self.id}, name={self.name}, proficiency={self.proficiency})"
