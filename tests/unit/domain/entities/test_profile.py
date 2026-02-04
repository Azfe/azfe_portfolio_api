"""
Tests for Profile Entity.
"""

import pytest
from app.domain.entities.profile import Profile
from app.domain.exceptions import EmptyFieldError, InvalidLengthError, InvalidURLError


@pytest.mark.entity
class TestProfileCreation:
    """Test Profile creation."""

    def test_create_with_required_fields(self):
        """Should create profile with required fields."""
        profile = Profile.create(
            name="John Doe",
            headline="Software Engineer"
        )
        
        assert profile.name == "John Doe"
        assert profile.headline == "Software Engineer"
        assert profile.id is not None

    def test_create_with_optional_fields(self, valid_url):
        """Should create with optional fields."""
        profile = Profile.create(
            name="John Doe",
            headline="Engineer",
            bio="Developer",
            location="Barcelona",
            avatar_url=valid_url
        )
        
        assert profile.bio == "Developer"
        assert profile.location == "Barcelona"


@pytest.mark.entity
@pytest.mark.business_rule
class TestProfileValidation:
    """Test Profile validation rules."""

    def test_empty_name_raises_error(self):
        """Should raise error for empty name."""
        with pytest.raises(EmptyFieldError):
            Profile.create(name="", headline="Engineer")

    def test_empty_headline_raises_error(self):
        """Should raise error for empty headline."""
        with pytest.raises(EmptyFieldError):
            Profile.create(name="John", headline="")

    def test_name_too_long_raises_error(self):
        """Should raise error for name > 100 chars."""
        with pytest.raises(InvalidLengthError):
            Profile.create(name="x" * 101, headline="Engineer")

    def test_bio_too_long_raises_error(self):
        """Should raise error for bio > 1000 chars."""
        with pytest.raises(InvalidLengthError):
            Profile.create(name="John", headline="Engineer", bio="x" * 1001)

    def test_invalid_avatar_url_raises_error(self, invalid_url):
        """Should raise error for invalid URL."""
        with pytest.raises(InvalidURLError):
            Profile.create(name="John", headline="Engineer", avatar_url=invalid_url)


@pytest.mark.entity
class TestProfileUpdate:
    """Test Profile updates."""

    def test_update_basic_info(self):
        """Should update profile info."""
        profile = Profile.create(name="John", headline="Engineer")
        
        profile.update_basic_info(name="Jane", headline="Senior Engineer")
        
        assert profile.name == "Jane"
        assert profile.headline == "Senior Engineer"

    def test_update_avatar(self, valid_url):
        """Should update avatar."""
        profile = Profile.create(name="John", headline="Engineer")
        
        profile.update_avatar(valid_url)
        
        assert profile.avatar_url == valid_url