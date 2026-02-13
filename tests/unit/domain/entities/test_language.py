"""
Tests for Language Entity.
"""

import pytest

from app.domain.entities.language import Language
from app.domain.exceptions import (
    EmptyFieldError,
    InvalidLanguageProficiencyError,
    InvalidLengthError,
    InvalidNameError,
    InvalidOrderIndexError,
)


@pytest.mark.entity
class TestLanguageCreation:
    """Test Language creation."""

    def test_create_with_required_fields(self, profile_id):
        """Should create language with required fields."""
        lang = Language.create(profile_id=profile_id, name="English", order_index=0)

        assert lang.name == "English"
        assert lang.order_index == 0
        assert lang.proficiency is None
        assert lang.profile_id == profile_id
        assert lang.id is not None

    def test_create_with_proficiency(self, profile_id):
        """Should create with CEFR proficiency."""
        lang = Language.create(
            profile_id=profile_id,
            name="Spanish",
            order_index=1,
            proficiency="c1",
        )

        assert lang.proficiency == "c1"

    def test_create_normalizes_proficiency_to_lowercase(self, profile_id):
        """Should normalize proficiency to lowercase."""
        lang = Language.create(
            profile_id=profile_id,
            name="French",
            order_index=0,
            proficiency="B2",
        )

        assert lang.proficiency == "b2"

    def test_create_sets_timestamps(self, profile_id):
        """Should set created_at and updated_at."""
        lang = Language.create(profile_id=profile_id, name="German", order_index=0)

        assert lang.created_at is not None
        assert lang.updated_at is not None

    def test_create_generates_unique_ids(self, profile_id):
        """Should generate unique IDs."""
        lang1 = Language.create(profile_id=profile_id, name="English", order_index=0)
        lang2 = Language.create(profile_id=profile_id, name="Spanish", order_index=1)

        assert lang1.id != lang2.id


@pytest.mark.entity
@pytest.mark.business_rule
class TestLanguageValidation:
    """Test Language validation rules."""

    def test_empty_name_raises_error(self, profile_id):
        """Should raise error for empty name."""
        with pytest.raises((InvalidNameError, InvalidLengthError)):
            Language.create(profile_id=profile_id, name="", order_index=0)

    def test_whitespace_name_raises_error(self, profile_id):
        """Should raise error for whitespace-only name."""
        with pytest.raises((InvalidNameError, InvalidLengthError)):
            Language.create(profile_id=profile_id, name="   ", order_index=0)

    def test_name_too_long_raises_error(self, profile_id):
        """Should raise error for name > 50 chars."""
        with pytest.raises(InvalidLengthError):
            Language.create(profile_id=profile_id, name="x" * 51, order_index=0)

    def test_empty_profile_id_raises_error(self):
        """Should raise error for empty profile_id."""
        with pytest.raises(EmptyFieldError):
            Language.create(profile_id="", name="English", order_index=0)

    def test_invalid_proficiency_raises_error(self, profile_id):
        """Should raise error for invalid CEFR proficiency."""
        with pytest.raises(InvalidLanguageProficiencyError):
            Language.create(
                profile_id=profile_id,
                name="English",
                order_index=0,
                proficiency="native",
            )

    def test_negative_order_index_raises_error(self, profile_id):
        """Should raise error for negative order index."""
        with pytest.raises(InvalidOrderIndexError):
            Language.create(profile_id=profile_id, name="English", order_index=-1)

    def test_empty_proficiency_string_becomes_none(self, profile_id):
        """Should treat empty string proficiency as None."""
        lang = Language.create(
            profile_id=profile_id,
            name="English",
            order_index=0,
            proficiency="  ",
        )

        assert lang.proficiency is None

    @pytest.mark.parametrize("valid_proficiency", ["a1", "a2", "b1", "b2", "c1", "c2"])
    def test_all_valid_proficiencies_accepted(self, profile_id, valid_proficiency):
        """Should accept all valid CEFR levels."""
        lang = Language.create(
            profile_id=profile_id,
            name="English",
            order_index=0,
            proficiency=valid_proficiency,
        )

        assert lang.proficiency == valid_proficiency


@pytest.mark.entity
class TestLanguageUpdate:
    """Test Language updates."""

    def test_update_info_name(self, profile_id):
        """Should update name."""
        lang = Language.create(profile_id=profile_id, name="English", order_index=0)
        old_updated = lang.updated_at

        lang.update_info(name="British English")

        assert lang.name == "British English"
        assert lang.updated_at >= old_updated

    def test_update_info_proficiency(self, profile_id):
        """Should update proficiency."""
        lang = Language.create(profile_id=profile_id, name="English", order_index=0)

        lang.update_info(proficiency="c2")

        assert lang.proficiency == "c2"

    def test_update_info_both(self, profile_id):
        """Should update name and proficiency together."""
        lang = Language.create(
            profile_id=profile_id,
            name="English",
            order_index=0,
            proficiency="a1",
        )

        lang.update_info(name="Spanish", proficiency="b2")

        assert lang.name == "Spanish"
        assert lang.proficiency == "b2"

    def test_update_order(self, profile_id):
        """Should update order index."""
        lang = Language.create(profile_id=profile_id, name="English", order_index=0)

        lang.update_order(3)

        assert lang.order_index == 3

    def test_remove_proficiency(self, profile_id):
        """Should remove proficiency."""
        lang = Language.create(
            profile_id=profile_id,
            name="English",
            order_index=0,
            proficiency="c1",
        )

        lang.remove_proficiency()

        assert lang.proficiency is None

    def test_update_with_invalid_name_raises_error(self, profile_id):
        """Should raise error when updating to invalid name."""
        lang = Language.create(profile_id=profile_id, name="English", order_index=0)

        with pytest.raises((InvalidNameError, InvalidLengthError)):
            lang.update_info(name="")

    def test_update_with_invalid_proficiency_raises_error(self, profile_id):
        """Should raise error when updating to invalid proficiency."""
        lang = Language.create(profile_id=profile_id, name="English", order_index=0)

        with pytest.raises(InvalidLanguageProficiencyError):
            lang.update_info(proficiency="fluent")


@pytest.mark.entity
class TestLanguageRepr:
    """Test Language string representation."""

    def test_repr(self, profile_id):
        """Should return readable repr."""
        lang = Language.create(
            profile_id=profile_id,
            name="English",
            order_index=0,
            proficiency="c2",
        )

        result = repr(lang)

        assert "English" in result
        assert "c2" in result
