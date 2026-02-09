"""
LanguageProficiency Value Object.

Represents a proficiency level for spoken/written languages using the
Common European Framework of Reference (CEFR/MCER) scale.

Value Object Principles:
- Immutability: Cannot be changed after creation
- Self-validation: Only valid levels allowed
- Equality by value: Two LanguageProficiencies are equal if levels match
- Ordered: Levels can be compared (A1 < A2 < B1 < B2 < C1 < C2)
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ..exceptions import InvalidLanguageProficiencyError


class LanguageProficiencyEnum(Enum):
    """Enumeration of valid CEFR language proficiency levels."""

    A1 = "a1"
    A2 = "a2"
    B1 = "b1"
    B2 = "b2"
    C1 = "c1"
    C2 = "c2"

    def __str__(self) -> str:
        return self.value

    def __lt__(self, other) -> bool:
        """Allow ordering of proficiency levels."""
        if not isinstance(other, LanguageProficiencyEnum):
            return NotImplemented

        order = {
            LanguageProficiencyEnum.A1: 1,
            LanguageProficiencyEnum.A2: 2,
            LanguageProficiencyEnum.B1: 3,
            LanguageProficiencyEnum.B2: 4,
            LanguageProficiencyEnum.C1: 5,
            LanguageProficiencyEnum.C2: 6,
        }
        return order[self] < order[other]

    def display_name(self) -> str:
        """Get display-friendly name."""
        names = {
            LanguageProficiencyEnum.A1: "A1 - Beginner",
            LanguageProficiencyEnum.A2: "A2 - Elementary",
            LanguageProficiencyEnum.B1: "B1 - Intermediate",
            LanguageProficiencyEnum.B2: "B2 - Upper Intermediate",
            LanguageProficiencyEnum.C1: "C1 - Advanced",
            LanguageProficiencyEnum.C2: "C2 - Proficient",
        }
        return names[self]


@dataclass(frozen=True)
class LanguageProficiency:
    """
    LanguageProficiency Value Object representing language proficiency (CEFR).

    Attributes:
        level: The language proficiency enumeration

    Business Rules:
        - Must be one of: a1, a2, b1, b2, c1, c2
        - Immutable after creation
        - Can be compared/ordered
    """

    level: LanguageProficiencyEnum

    @staticmethod
    def create(value: str) -> LanguageProficiency:
        """
        Factory method to create a LanguageProficiency from string.

        Args:
            value: Proficiency level string (case-insensitive)

        Returns:
            A new LanguageProficiency instance

        Raises:
            InvalidLanguageProficiencyError: If value is not a valid level
        """
        normalized = value.lower().strip()

        try:
            enum_level = LanguageProficiencyEnum(normalized)
            return LanguageProficiency(level=enum_level)
        except ValueError:
            raise InvalidLanguageProficiencyError(value) from None

    @staticmethod
    def try_create(value: str) -> LanguageProficiency | None:
        """
        Try to create a LanguageProficiency, returning None if invalid.

        Args:
            value: Proficiency level string

        Returns:
            LanguageProficiency instance or None if invalid
        """
        try:
            return LanguageProficiency.create(value)
        except InvalidLanguageProficiencyError:
            return None

    @staticmethod
    def a1() -> LanguageProficiency:
        """Create an A1 (Beginner) proficiency."""
        return LanguageProficiency(level=LanguageProficiencyEnum.A1)

    @staticmethod
    def a2() -> LanguageProficiency:
        """Create an A2 (Elementary) proficiency."""
        return LanguageProficiency(level=LanguageProficiencyEnum.A2)

    @staticmethod
    def b1() -> LanguageProficiency:
        """Create a B1 (Intermediate) proficiency."""
        return LanguageProficiency(level=LanguageProficiencyEnum.B1)

    @staticmethod
    def b2() -> LanguageProficiency:
        """Create a B2 (Upper Intermediate) proficiency."""
        return LanguageProficiency(level=LanguageProficiencyEnum.B2)

    @staticmethod
    def c1() -> LanguageProficiency:
        """Create a C1 (Advanced) proficiency."""
        return LanguageProficiency(level=LanguageProficiencyEnum.C1)

    @staticmethod
    def c2() -> LanguageProficiency:
        """Create a C2 (Proficient) proficiency."""
        return LanguageProficiency(level=LanguageProficiencyEnum.C2)

    @staticmethod
    def all_levels() -> list[LanguageProficiency]:
        """
        Get all valid proficiency levels in order.

        Returns:
            List of all LanguageProficiency instances from A1 to C2
        """
        return [
            LanguageProficiency.a1(),
            LanguageProficiency.a2(),
            LanguageProficiency.b1(),
            LanguageProficiency.b2(),
            LanguageProficiency.c1(),
            LanguageProficiency.c2(),
        ]

    def is_a1(self) -> bool:
        """Check if this is A1 level."""
        return self.level == LanguageProficiencyEnum.A1

    def is_a2(self) -> bool:
        """Check if this is A2 level."""
        return self.level == LanguageProficiencyEnum.A2

    def is_b1(self) -> bool:
        """Check if this is B1 level."""
        return self.level == LanguageProficiencyEnum.B1

    def is_b2(self) -> bool:
        """Check if this is B2 level."""
        return self.level == LanguageProficiencyEnum.B2

    def is_c1(self) -> bool:
        """Check if this is C1 level."""
        return self.level == LanguageProficiencyEnum.C1

    def is_c2(self) -> bool:
        """Check if this is C2 level."""
        return self.level == LanguageProficiencyEnum.C2

    def is_at_least(self, other: LanguageProficiency) -> bool:
        """
        Check if this proficiency is at least as high as another.

        Args:
            other: Another LanguageProficiency to compare

        Returns:
            True if this level >= other level
        """
        return self.level.value >= other.level.value

    def to_string(self) -> str:
        """Get the string value of the proficiency."""
        return self.level.value

    def display_name(self) -> str:
        """Get display-friendly name (e.g. 'B2 - Upper Intermediate')."""
        return self.level.display_name()

    def __str__(self) -> str:
        """String representation for display."""
        return self.level.value

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"LanguageProficiency.{self.level.name.lower()}()"

    def __eq__(self, other) -> bool:
        """Equality comparison."""
        if not isinstance(other, LanguageProficiency):
            return False
        return self.level == other.level

    def __lt__(self, other) -> bool:
        """Less than comparison for ordering."""
        if not isinstance(other, LanguageProficiency):
            return NotImplemented
        return self.level < other.level

    def __le__(self, other) -> bool:
        """Less than or equal comparison."""
        if not isinstance(other, LanguageProficiency):
            return NotImplemented
        return self == other or self < other

    def __gt__(self, other) -> bool:
        """Greater than comparison."""
        if not isinstance(other, LanguageProficiency):
            return NotImplemented
        return not self <= other

    def __ge__(self, other) -> bool:
        """Greater than or equal comparison."""
        if not isinstance(other, LanguageProficiency):
            return NotImplemented
        return self == other or self > other

    def __hash__(self) -> int:
        """Hash for use in sets and dicts."""
        return hash(self.level)
