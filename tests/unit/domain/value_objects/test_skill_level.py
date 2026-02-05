"""
Tests for SkillLevel Value Object.
"""

import pytest

from app.domain.exceptions import InvalidSkillLevelError
from app.domain.value_objects.skill_level import SkillLevel


@pytest.mark.value_object
class TestSkillLevelCreation:
    """Test SkillLevel creation."""

    @pytest.mark.parametrize("level", ["basic", "intermediate", "advanced", "expert"])
    def test_create_valid_levels(self, level):
        """Should create valid levels."""
        skill_level = SkillLevel.create(level)

        assert skill_level.to_string() == level


@pytest.mark.value_object
class TestSkillLevelValidation:
    """Test SkillLevel validation."""

    def test_invalid_level_raises_error(self):
        """Should raise error for invalid level."""
        with pytest.raises(InvalidSkillLevelError):
            SkillLevel.create("master")

    @pytest.mark.parametrize("invalid", ["beginner", "pro", "novice", ""])
    def test_various_invalid_levels(self, invalid):
        """Should reject invalid levels."""
        with pytest.raises(InvalidSkillLevelError):
            SkillLevel.create(invalid)


@pytest.mark.value_object
class TestSkillLevelComparison:
    """Test SkillLevel comparison."""

    def test_levels_ordered(self):
        """Should maintain order."""
        basic = SkillLevel.create("basic")
        intermediate = SkillLevel.create("intermediate")
        advanced = SkillLevel.create("advanced")
        expert = SkillLevel.create("expert")

        assert basic < intermediate < advanced < expert


@pytest.mark.value_object
class TestSkillLevelEquality:
    """Test SkillLevel equality."""

    def test_same_level_equals(self):
        """Should be equal for same level."""
        level1 = SkillLevel.create("intermediate")
        level2 = SkillLevel.create("intermediate")

        assert level1 == level2


@pytest.mark.value_object
class TestSkillLevelImmutability:
    """Test SkillLevel immutability."""

    def test_immutable(self):
        """Should not allow modification."""
        level = SkillLevel.create("basic")

        with pytest.raises(AttributeError):
            level.level = SkillLevel.create("expert").level
