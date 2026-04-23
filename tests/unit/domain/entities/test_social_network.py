"""Tests for SocialNetwork Entity."""

import pytest

from app.domain.entities.social_network import SocialNetwork
from app.domain.exceptions import (
    EmptyFieldError,
    InvalidLengthError,
    InvalidOrderIndexError,
    InvalidPlatformError,
    InvalidURLError,
)


@pytest.mark.entity
class TestSocialNetworkCreation:
    """Test SocialNetwork creation."""

    def test_create_with_required_fields(self, profile_id):
        sn = SocialNetwork.create(
            profile_id=profile_id,
            platform="LinkedIn",
            url="https://linkedin.com/in/user",
            order_index=0,
        )
        assert sn.platform == "LinkedIn"
        assert sn.url == "https://linkedin.com/in/user"
        assert sn.username is None

    def test_create_with_username(self, profile_id):
        sn = SocialNetwork.create(
            profile_id=profile_id,
            platform="GitHub",
            url="https://github.com/user",
            order_index=0,
            username="user123",
        )
        assert sn.username == "user123"


@pytest.mark.entity
@pytest.mark.business_rule
class TestSocialNetworkValidation:
    """Test SocialNetwork validation rules."""

    def test_empty_platform_raises_error(self, profile_id):
        with pytest.raises(InvalidPlatformError):
            SocialNetwork.create(
                profile_id=profile_id,
                platform="",
                url="https://example.com",
                order_index=0,
            )

    def test_platform_too_long_raises_error(self, profile_id):
        with pytest.raises(InvalidLengthError):
            SocialNetwork.create(
                profile_id=profile_id,
                platform="x" * 51,
                url="https://example.com",
                order_index=0,
            )

    def test_empty_url_raises_error(self, profile_id):
        with pytest.raises(EmptyFieldError):
            SocialNetwork.create(
                profile_id=profile_id,
                platform="LinkedIn",
                url="",
                order_index=0,
            )

    def test_invalid_url_raises_error(self, profile_id):
        with pytest.raises(InvalidURLError):
            SocialNetwork.create(
                profile_id=profile_id,
                platform="LinkedIn",
                url="not-a-url",
                order_index=0,
            )

    def test_username_too_long_raises_error(self, profile_id):
        with pytest.raises(InvalidLengthError):
            SocialNetwork.create(
                profile_id=profile_id,
                platform="LinkedIn",
                url="https://linkedin.com/in/user",
                order_index=0,
                username="x" * 101,
            )

    def test_empty_username_becomes_none(self, profile_id):
        sn = SocialNetwork.create(
            profile_id=profile_id,
            platform="LinkedIn",
            url="https://linkedin.com/in/user",
            order_index=0,
            username="   ",
        )
        assert sn.username is None

    def test_negative_order_index_raises_error(self, profile_id):
        with pytest.raises(InvalidOrderIndexError):
            SocialNetwork.create(
                profile_id=profile_id,
                platform="LinkedIn",
                url="https://linkedin.com/in/user",
                order_index=-1,
            )

    def test_empty_profile_id_raises_error(self):
        with pytest.raises(EmptyFieldError):
            SocialNetwork.create(
                profile_id="",
                platform="LinkedIn",
                url="https://linkedin.com/in/user",
                order_index=0,
            )


@pytest.mark.entity
class TestSocialNetworkUpdate:
    """Test SocialNetwork updates."""

    def _make(self, profile_id):
        return SocialNetwork.create(
            profile_id=profile_id,
            platform="LinkedIn",
            url="https://linkedin.com/in/user",
            order_index=0,
        )

    def test_update_info(self, profile_id):
        sn = self._make(profile_id)
        sn.update_info(
            platform="GitHub",
            url="https://github.com/user",
            username="user123",
        )
        assert sn.platform == "GitHub"
        assert sn.url == "https://github.com/user"
        assert sn.username == "user123"

    def test_update_info_invalid_platform_raises(self, profile_id):
        sn = self._make(profile_id)
        with pytest.raises(InvalidPlatformError):
            sn.update_info(platform="")

    def test_update_info_invalid_url_raises(self, profile_id):
        sn = self._make(profile_id)
        with pytest.raises(InvalidURLError):
            sn.update_info(url="not-valid")

    def test_update_order(self, profile_id):
        sn = self._make(profile_id)
        sn.update_order(3)
        assert sn.order_index == 3

    def test_update_order_negative_raises(self, profile_id):
        sn = self._make(profile_id)
        with pytest.raises(InvalidOrderIndexError):
            sn.update_order(-1)
