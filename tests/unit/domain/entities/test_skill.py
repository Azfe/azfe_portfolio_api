"""
Tests for Skill Entity.
"""

import pytest

from app.domain.entities.skill import Skill
from app.domain.exceptions import (
    InvalidLengthError,
    InvalidNameError,
    InvalidSkillLevelError,
)


@pytest.mark.entity
class TestSkillCreation:
    """Test Skill creation."""

    def test_create_with_required_fields(self, profile_id):
        """Should create skill with required fields."""
        skill = Skill.create(
            profile_id=profile_id, name="Python", order_index=0
        )

        assert skill.name == "Python"
        assert skill.order_index == 0

    def test_create_with_level(self, profile_id):
        """Should create with level."""
        skill = Skill.create(
            profile_id=profile_id,
            name="Python",
            order_index=0,
            level="intermediate",
        )

        assert skill.level == "intermediate"


@pytest.mark.entity
@pytest.mark.business_rule
class TestSkillValidation:
    """Test Skill validation rules."""

    def test_empty_name_raises_error(self, profile_id):
        """Should raise error for empty name."""
        with pytest.raises((InvalidNameError, InvalidLengthError)):
            Skill.create(
                profile_id=profile_id, name="", order_index=0
            )

    def test_name_too_long_raises_error(self, profile_id):
        """Should raise error for name > 50 chars."""
        with pytest.raises(InvalidLengthError):
            Skill.create(
                profile_id=profile_id,
                name="x" * 51,
                order_index=0,
            )

    def test_invalid_level_raises_error(self, profile_id):
        """Should raise error for invalid level."""
        with pytest.raises(InvalidSkillLevelError):
            Skill.create(
                profile_id=profile_id,
                name="Python",
                order_index=0,
                level="master",
            )


@pytest.mark.entity
class TestSkillUpdate:
    """Test Skill updates."""

    def test_update_info(self, profile_id):
        """Should update skill info."""
        skill = Skill.create(
            profile_id=profile_id, name="Python", order_index=0
        )

        skill.update_info(name="Advanced Python", level="advanced")

        assert skill.name == "Advanced Python"
        assert skill.level == "advanced"
