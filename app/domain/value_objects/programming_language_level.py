"""
ProgrammingLanguageLevel Value Object.

Represents a proficiency level for programming languages using a type-safe enumeration.

Value Object Principles:
- Immutability: Cannot be changed after creation
- Self-validation: Only valid levels allowed
- Equality by value: Two ProgrammingLanguageLevels are equal if levels match
- Ordered: Levels can be compared
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ..exceptions import InvalidProgrammingLanguageLevelError


class ProgrammingLanguageLevelEnum(Enum):
    """Enumeration of valid programming language proficiency levels."""

    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

    def __str__(self) -> str:
        return self.value

    def __lt__(self, other) -> bool:
        """Allow ordering of programming language levels."""
        if not isinstance(other, ProgrammingLanguageLevelEnum):
            return NotImplemented

        order = {
            ProgrammingLanguageLevelEnum.BASIC: 1,
            ProgrammingLanguageLevelEnum.INTERMEDIATE: 2,
            ProgrammingLanguageLevelEnum.ADVANCED: 3,
            ProgrammingLanguageLevelEnum.EXPERT: 4,
        }
        return order[self] < order[other]

    def display_name(self) -> str:
        """Get display-friendly name."""
        return self.value.capitalize()


@dataclass(frozen=True)
class ProgrammingLanguageLevel:
    """
    ProgrammingLanguageLevel Value Object representing programming language proficiency.

    Attributes:
        level: The programming language level enumeration

    Business Rules:
        - Must be one of: basic, intermediate, advanced, expert
        - Immutable after creation
        - Can be compared/ordered
    """

    level: ProgrammingLanguageLevelEnum

    @staticmethod
    def create(value: str) -> ProgrammingLanguageLevel:
        """
        Factory method to create a ProgrammingLanguageLevel from string.

        Args:
            value: Level string (case-insensitive)

        Returns:
            A new ProgrammingLanguageLevel instance

        Raises:
            InvalidProgrammingLanguageLevelError: If value is not a valid level
        """
        normalized = value.lower().strip()

        try:
            enum_level = ProgrammingLanguageLevelEnum(normalized)
            return ProgrammingLanguageLevel(level=enum_level)
        except ValueError:
            raise InvalidProgrammingLanguageLevelError(value) from None

    @staticmethod
    def try_create(value: str) -> ProgrammingLanguageLevel | None:
        """
        Try to create a ProgrammingLanguageLevel, returning None if invalid.

        Args:
            value: Level string

        Returns:
            ProgrammingLanguageLevel instance or None if invalid
        """
        try:
            return ProgrammingLanguageLevel.create(value)
        except InvalidProgrammingLanguageLevelError:
            return None

    @staticmethod
    def basic() -> ProgrammingLanguageLevel:
        """Create a BASIC level."""
        return ProgrammingLanguageLevel(level=ProgrammingLanguageLevelEnum.BASIC)

    @staticmethod
    def intermediate() -> ProgrammingLanguageLevel:
        """Create an INTERMEDIATE level."""
        return ProgrammingLanguageLevel(level=ProgrammingLanguageLevelEnum.INTERMEDIATE)

    @staticmethod
    def advanced() -> ProgrammingLanguageLevel:
        """Create an ADVANCED level."""
        return ProgrammingLanguageLevel(level=ProgrammingLanguageLevelEnum.ADVANCED)

    @staticmethod
    def expert() -> ProgrammingLanguageLevel:
        """Create an EXPERT level."""
        return ProgrammingLanguageLevel(level=ProgrammingLanguageLevelEnum.EXPERT)

    @staticmethod
    def all_levels() -> list[ProgrammingLanguageLevel]:
        """
        Get all valid levels in order.

        Returns:
            List of all ProgrammingLanguageLevel instances
        """
        return [
            ProgrammingLanguageLevel.basic(),
            ProgrammingLanguageLevel.intermediate(),
            ProgrammingLanguageLevel.advanced(),
            ProgrammingLanguageLevel.expert(),
        ]

    def is_basic(self) -> bool:
        """Check if this is basic level."""
        return self.level == ProgrammingLanguageLevelEnum.BASIC

    def is_intermediate(self) -> bool:
        """Check if this is intermediate level."""
        return self.level == ProgrammingLanguageLevelEnum.INTERMEDIATE

    def is_advanced(self) -> bool:
        """Check if this is advanced level."""
        return self.level == ProgrammingLanguageLevelEnum.ADVANCED

    def is_expert(self) -> bool:
        """Check if this is expert level."""
        return self.level == ProgrammingLanguageLevelEnum.EXPERT

    def is_at_least(self, other: ProgrammingLanguageLevel) -> bool:
        """
        Check if this level is at least as high as another.

        Args:
            other: Another ProgrammingLanguageLevel to compare

        Returns:
            True if this level >= other level
        """
        return self.level.value >= other.level.value

    def to_string(self) -> str:
        """Get the string value of the level."""
        return self.level.value

    def display_name(self) -> str:
        """Get display-friendly name."""
        return self.level.display_name()

    def __str__(self) -> str:
        """String representation for display."""
        return self.level.value

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"ProgrammingLanguageLevel.{self.level.name.lower()}()"

    def __eq__(self, other) -> bool:
        """Equality comparison."""
        if not isinstance(other, ProgrammingLanguageLevel):
            return False
        return self.level == other.level

    def __lt__(self, other) -> bool:
        """Less than comparison for ordering."""
        if not isinstance(other, ProgrammingLanguageLevel):
            return NotImplemented
        return self.level < other.level

    def __le__(self, other) -> bool:
        """Less than or equal comparison."""
        if not isinstance(other, ProgrammingLanguageLevel):
            return NotImplemented
        return self == other or self < other

    def __gt__(self, other) -> bool:
        """Greater than comparison."""
        if not isinstance(other, ProgrammingLanguageLevel):
            return NotImplemented
        return not self <= other

    def __ge__(self, other) -> bool:
        """Greater than or equal comparison."""
        if not isinstance(other, ProgrammingLanguageLevel):
            return NotImplemented
        return self == other or self > other

    def __hash__(self) -> int:
        """Hash for use in sets and dicts."""
        return hash(self.level)
