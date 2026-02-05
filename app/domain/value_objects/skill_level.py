"""
SkillLevel Value Object.

Represents a proficiency level for skills using a type-safe enumeration.

Value Object Principles:
- Immutability: Cannot be changed after creation
- Self-validation: Only valid levels allowed
- Equality by value: Two SkillLevels are equal if levels match
- Ordered: Levels can be compared
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ..exceptions import InvalidSkillLevelError


class SkillLevelEnum(Enum):
    """Enumeration of valid skill proficiency levels."""

    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

    def __str__(self) -> str:
        return self.value

    def __lt__(self, other) -> bool:
        """Allow ordering of skill levels."""
        if not isinstance(other, SkillLevelEnum):
            return NotImplemented

        order = {
            SkillLevelEnum.BASIC: 1,
            SkillLevelEnum.INTERMEDIATE: 2,
            SkillLevelEnum.ADVANCED: 3,
            SkillLevelEnum.EXPERT: 4,
        }
        return order[self] < order[other]

    def display_name(self) -> str:
        """Get display-friendly name."""
        return self.value.capitalize()


@dataclass(frozen=True)
class SkillLevel:
    """
    SkillLevel Value Object representing skill proficiency.

    Attributes:
        level: The skill level enumeration

    Business Rules:
        - Must be one of: basic, intermediate, advanced, expert
        - Immutable after creation
        - Can be compared/ordered

    Examples:
        >>> basic = SkillLevel.basic()
        >>> advanced = SkillLevel.advanced()
        >>> basic < advanced
        True
    """

    level: SkillLevelEnum

    @staticmethod
    def create(value: str) -> SkillLevel:
        """
        Factory method to create a SkillLevel from string.

        Args:
            value: Skill level string (case-insensitive)

        Returns:
            A new SkillLevel instance

        Raises:
            InvalidSkillLevelError: If value is not a valid level
        """
        normalized = value.lower().strip()

        try:
            enum_level = SkillLevelEnum(normalized)
            return SkillLevel(level=enum_level)
        except ValueError:
            raise InvalidSkillLevelError(value) from None

    @staticmethod
    def try_create(value: str) -> SkillLevel | None:
        """
        Try to create a SkillLevel, returning None if invalid.

        Args:
            value: Skill level string

        Returns:
            SkillLevel instance or None if invalid
        """
        try:
            return SkillLevel.create(value)
        except InvalidSkillLevelError:
            return None

    @staticmethod
    def basic() -> SkillLevel:
        """Create a BASIC skill level."""
        return SkillLevel(level=SkillLevelEnum.BASIC)

    @staticmethod
    def intermediate() -> SkillLevel:
        """Create an INTERMEDIATE skill level."""
        return SkillLevel(level=SkillLevelEnum.INTERMEDIATE)

    @staticmethod
    def advanced() -> SkillLevel:
        """Create an ADVANCED skill level."""
        return SkillLevel(level=SkillLevelEnum.ADVANCED)

    @staticmethod
    def expert() -> SkillLevel:
        """Create an EXPERT skill level."""
        return SkillLevel(level=SkillLevelEnum.EXPERT)

    @staticmethod
    def all_levels() -> list[SkillLevel]:
        """
        Get all valid skill levels in order.

        Returns:
            List of all SkillLevel instances
        """
        return [
            SkillLevel.basic(),
            SkillLevel.intermediate(),
            SkillLevel.advanced(),
            SkillLevel.expert(),
        ]

    def is_basic(self) -> bool:
        """Check if this is basic level."""
        return self.level == SkillLevelEnum.BASIC

    def is_intermediate(self) -> bool:
        """Check if this is intermediate level."""
        return self.level == SkillLevelEnum.INTERMEDIATE

    def is_advanced(self) -> bool:
        """Check if this is advanced level."""
        return self.level == SkillLevelEnum.ADVANCED

    def is_expert(self) -> bool:
        """Check if this is expert level."""
        return self.level == SkillLevelEnum.EXPERT

    def is_at_least(self, other: SkillLevel) -> bool:
        """
        Check if this level is at least as high as another.

        Args:
            other: Another SkillLevel to compare

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
        return f"SkillLevel.{self.level.name.lower()}()"

    def __eq__(self, other) -> bool:
        """Equality comparison."""
        if not isinstance(other, SkillLevel):
            return False
        return self.level == other.level

    def __lt__(self, other) -> bool:
        """Less than comparison for ordering."""
        if not isinstance(other, SkillLevel):
            return NotImplemented
        return self.level < other.level

    def __le__(self, other) -> bool:
        """Less than or equal comparison."""
        if not isinstance(other, SkillLevel):
            return NotImplemented
        return self == other or self < other

    def __gt__(self, other) -> bool:
        """Greater than comparison."""
        if not isinstance(other, SkillLevel):
            return NotImplemented
        return not self <= other

    def __ge__(self, other) -> bool:
        """Greater than or equal comparison."""
        if not isinstance(other, SkillLevel):
            return NotImplemented
        return self == other or self > other

    def __hash__(self) -> int:
        """Hash for use in sets and dicts."""
        return hash(self.level)
