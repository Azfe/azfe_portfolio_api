"""
Extended tests for Profile Entity.

Covers uncovered lines: update_avatar(None), empty bio/location normalization,
location too long, avatar_url empty string normalization, update_basic_info with bio.
"""

import pytest

from app.domain.entities.profile import Profile
from app.domain.exceptions import EmptyFieldError, InvalidLengthError, InvalidURLError


@pytest.mark.entity
class TestProfileEmptyStringNormalization:
    """Test that empty strings are normalized to None."""

    def test_empty_bio_normalized_to_none(self):
        """Empty bio string should be stored as None."""
        profile = Profile.create(name="John", headline="Engineer", bio="")

        assert profile.bio is None

    def test_whitespace_bio_normalized_to_none(self):
        """Whitespace-only bio should be normalized to None."""
        profile = Profile.create(name="John", headline="Engineer", bio="   ")

        assert profile.bio is None

    def test_empty_location_normalized_to_none(self):
        """Empty location string should be stored as None."""
        profile = Profile.create(name="John", headline="Engineer", location="")

        assert profile.location is None

    def test_whitespace_location_normalized_to_none(self):
        """Whitespace-only location should be normalized to None."""
        profile = Profile.create(name="John", headline="Engineer", location="   ")

        assert profile.location is None

    def test_empty_avatar_url_normalized_to_none(self):
        """Empty avatar_url string should be stored as None."""
        profile = Profile.create(name="John", headline="Engineer", avatar_url="")

        assert profile.avatar_url is None


@pytest.mark.entity
@pytest.mark.business_rule
class TestProfileValidationBoundaries:
    """Test Profile field length boundaries."""

    def test_location_too_long_raises_error(self):
        """Location longer than 100 chars should raise InvalidLengthError."""
        with pytest.raises(InvalidLengthError):
            Profile.create(
                name="John",
                headline="Engineer",
                location="x" * 101,
            )

    def test_headline_too_long_raises_error(self):
        """Headline longer than 100 chars should raise InvalidLengthError."""
        with pytest.raises(InvalidLengthError):
            Profile.create(name="John", headline="x" * 101)

    def test_whitespace_name_raises_error(self):
        """Whitespace-only name should raise EmptyFieldError."""
        with pytest.raises(EmptyFieldError):
            Profile.create(name="   ", headline="Engineer")

    def test_whitespace_headline_raises_error(self):
        """Whitespace-only headline should raise EmptyFieldError."""
        with pytest.raises(EmptyFieldError):
            Profile.create(name="John", headline="   ")


@pytest.mark.entity
class TestProfileUpdateAvatar:
    """Test update_avatar() method."""

    def test_update_avatar_to_none_removes_url(self):
        """Setting avatar to None should clear it."""
        profile = Profile.create(
            name="John",
            headline="Engineer",
            avatar_url="https://example.com/avatar.jpg",
        )

        profile.update_avatar(None)

        assert profile.avatar_url is None

    def test_update_avatar_with_valid_url(self):
        """Setting avatar to a valid URL should update it."""
        profile = Profile.create(name="John", headline="Engineer")

        profile.update_avatar("https://cdn.example.com/pic.png")

        assert profile.avatar_url == "https://cdn.example.com/pic.png"

    def test_update_avatar_with_invalid_url_raises_error(self):
        """Setting avatar to an invalid URL should raise InvalidURLError."""
        profile = Profile.create(name="John", headline="Engineer")

        with pytest.raises(InvalidURLError):
            profile.update_avatar("not-a-url")

    def test_update_avatar_updates_timestamp(self):
        """update_avatar() should update the updated_at timestamp."""

        profile = Profile.create(name="John", headline="Engineer")
        before = profile.updated_at

        profile.update_avatar("https://example.com/pic.jpg")

        assert profile.updated_at >= before


@pytest.mark.entity
class TestProfileUpdateBasicInfo:
    """Extended tests for update_basic_info()."""

    def test_update_bio(self):
        """Should update bio field."""
        profile = Profile.create(name="John", headline="Engineer")

        profile.update_basic_info(bio="New bio text")

        assert profile.bio == "New bio text"

    def test_update_location(self):
        """Should update location field."""
        profile = Profile.create(name="John", headline="Engineer")

        profile.update_basic_info(location="Barcelona, Spain")

        assert profile.location == "Barcelona, Spain"

    def test_update_with_no_args_is_idempotent(self):
        """Calling update_basic_info() with no args should not change anything."""
        profile = Profile.create(
            name="John",
            headline="Engineer",
            bio="Bio",
            location="Madrid",
        )
        original_name = profile.name
        original_headline = profile.headline

        profile.update_basic_info()

        assert profile.name == original_name
        assert profile.headline == original_headline

    def test_update_name_validates_length(self):
        """Updating name with too long value should raise InvalidLengthError."""
        profile = Profile.create(name="John", headline="Engineer")

        with pytest.raises(InvalidLengthError):
            profile.update_basic_info(name="x" * 101)

    def test_update_headline_validates_length(self):
        """Updating headline with too long value should raise InvalidLengthError."""
        profile = Profile.create(name="John", headline="Engineer")

        with pytest.raises(InvalidLengthError):
            profile.update_basic_info(headline="x" * 101)


@pytest.mark.entity
class TestProfileRepr:
    """Test __repr__ method."""

    def test_repr_contains_name_and_headline(self):
        """__repr__ should include id, name, and headline."""
        profile = Profile.create(name="Alex", headline="Developer")

        result = repr(profile)

        assert "Profile" in result
        assert "Alex" in result
        assert "Developer" in result
