"""
Extended tests for Skill Entity.

Covers uncovered lines: update_order(), remove_level(), level with whitespace
normalization to None, empty profile_id validation, and __repr__.
"""

import pytest

from app.domain.entities.skill import Skill
from app.domain.exceptions import (
    EmptyFieldError,
    InvalidLengthError,
    InvalidNameError,
    InvalidOrderIndexError,
    InvalidSkillLevelError,
)


@pytest.mark.entity
class TestSkillLevelNormalization:
    """Test level field normalization."""

    def test_whitespace_level_normalized_to_none(self, profile_id):
        """Level with only whitespace should be stored as None."""
        skill = Skill.create(profile_id=profile_id, name="Python", order_index=0, level="   ")

        assert skill.level is None

    def test_level_normalized_to_lowercase(self, profile_id):
        """Level string should be normalized to lowercase."""
        skill = Skill.create(profile_id=profile_id, name="Python", order_index=0, level="ADVANCED")

        assert skill.level == "advanced"

    def test_none_level_stays_none(self, profile_id):
        """None level should remain None."""
        skill = Skill.create(profile_id=profile_id, name="Python", order_index=0, level=None)

        assert skill.level is None


@pytest.mark.entity
@pytest.mark.business_rule
class TestSkillValidationEdgeCases:
    """Test validation edge cases not covered in base tests."""

    def test_empty_profile_id_raises_error(self):
        """Empty profile_id should raise EmptyFieldError."""
        with pytest.raises(EmptyFieldError):
            Skill.create(profile_id="", name="Python", order_index=0)

    def test_whitespace_profile_id_raises_error(self):
        """Whitespace-only profile_id should raise EmptyFieldError."""
        with pytest.raises(EmptyFieldError):
            Skill.create(profile_id="   ", name="Python", order_index=0)

    def test_whitespace_name_raises_error(self, profile_id):
        """Whitespace-only name should raise InvalidNameError."""
        with pytest.raises(InvalidNameError):
            Skill.create(profile_id=profile_id, name="   ", order_index=0)

    def test_negative_order_index_raises_error(self, profile_id):
        """Negative order_index should raise InvalidOrderIndexError."""
        with pytest.raises(InvalidOrderIndexError):
            Skill.create(profile_id=profile_id, name="Python", order_index=-1)


@pytest.mark.entity
class TestSkillUpdateOrder:
    """Test update_order() method."""

    def test_update_order_changes_index(self, profile_id):
        """Should update order_index."""
        skill = Skill.create(profile_id=profile_id, name="Python", order_index=0)

        skill.update_order(5)

        assert skill.order_index == 5

    def test_update_order_negative_raises_error(self, profile_id):
        """Negative order_index should raise InvalidOrderIndexError."""
        skill = Skill.create(profile_id=profile_id, name="Python", order_index=0)

        with pytest.raises(InvalidOrderIndexError):
            skill.update_order(-1)

    def test_update_order_updates_timestamp(self, profile_id):
        """update_order() should update the updated_at timestamp."""
        skill = Skill.create(profile_id=profile_id, name="Python", order_index=0)
        before = skill.updated_at

        skill.update_order(2)

        assert skill.updated_at >= before


@pytest.mark.entity
class TestSkillRemoveLevel:
    """Test remove_level() method."""

    def test_remove_level_clears_level(self, profile_id):
        """remove_level() should set level to None."""
        skill = Skill.create(
            profile_id=profile_id, name="Python", order_index=0, level="expert"
        )

        skill.remove_level()

        assert skill.level is None

    def test_remove_level_updates_timestamp(self, profile_id):
        """remove_level() should update the updated_at timestamp."""
        skill = Skill.create(
            profile_id=profile_id, name="Python", order_index=0, level="basic"
        )
        before = skill.updated_at

        skill.remove_level()

        assert skill.updated_at >= before


@pytest.mark.entity
class TestSkillUpdateInfo:
    """Extended tests for update_info()."""

    def test_update_info_validates_new_level(self, profile_id):
        """Updating with an invalid level should raise InvalidSkillLevelError."""
        skill = Skill.create(profile_id=profile_id, name="Python", order_index=0)

        with pytest.raises(InvalidSkillLevelError):
            skill.update_info(level="guru")

    def test_update_info_validates_new_name(self, profile_id):
        """Updating with empty name should raise InvalidNameError."""
        skill = Skill.create(profile_id=profile_id, name="Python", order_index=0)

        with pytest.raises(InvalidNameError):
            skill.update_info(name="")

    def test_update_info_with_no_args_is_safe(self, profile_id):
        """Calling update_info() with no args should not change anything except timestamp."""
        skill = Skill.create(
            profile_id=profile_id, name="Python", order_index=0, level="expert"
        )

        skill.update_info()

        assert skill.name == "Python"
        assert skill.level == "expert"


@pytest.mark.entity
class TestSkillRepr:
    """Test __repr__ method."""

    def test_repr_contains_name_and_level(self, profile_id):
        """__repr__ should include id, name and level."""
        skill = Skill.create(
            profile_id=profile_id, name="Docker", order_index=1, level="advanced"
        )

        result = repr(skill)

        assert "Skill" in result
        assert "Docker" in result
        assert "advanced" in result
