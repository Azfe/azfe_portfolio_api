"""Tests for Tool Entity."""

import pytest

from app.domain.entities.tool import Tool
from app.domain.exceptions import (
    EmptyFieldError,
    InvalidCategoryError,
    InvalidLengthError,
    InvalidNameError,
    InvalidOrderIndexError,
    InvalidURLError,
)


@pytest.mark.entity
class TestToolCreation:
    """Test Tool creation."""

    def test_create_with_required_fields(self, profile_id):
        t = Tool.create(
            profile_id=profile_id,
            name="Docker",
            category="Container",
            order_index=0,
        )
        assert t.name == "Docker"
        assert t.category == "Container"
        assert t.icon_url is None

    def test_create_with_icon_url(self, profile_id):
        t = Tool.create(
            profile_id=profile_id,
            name="Docker",
            category="Container",
            order_index=0,
            icon_url="https://cdn.example.com/docker.png",
        )
        assert t.icon_url == "https://cdn.example.com/docker.png"


@pytest.mark.entity
@pytest.mark.business_rule
class TestToolValidation:
    """Test Tool validation rules."""

    def test_empty_name_raises_error(self, profile_id):
        with pytest.raises(InvalidNameError):
            Tool.create(
                profile_id=profile_id,
                name="",
                category="Container",
                order_index=0,
            )

    def test_name_too_long_raises_error(self, profile_id):
        with pytest.raises(InvalidLengthError):
            Tool.create(
                profile_id=profile_id,
                name="x" * 51,
                category="Container",
                order_index=0,
            )

    def test_empty_category_raises_error(self, profile_id):
        with pytest.raises(InvalidCategoryError):
            Tool.create(
                profile_id=profile_id,
                name="Docker",
                category="",
                order_index=0,
            )

    def test_category_too_long_raises_error(self, profile_id):
        with pytest.raises(InvalidLengthError):
            Tool.create(
                profile_id=profile_id,
                name="Docker",
                category="x" * 51,
                order_index=0,
            )

    def test_invalid_icon_url_raises_error(self, profile_id):
        with pytest.raises(InvalidURLError):
            Tool.create(
                profile_id=profile_id,
                name="Docker",
                category="Container",
                order_index=0,
                icon_url="not-a-url",
            )

    def test_empty_icon_url_becomes_none(self, profile_id):
        t = Tool.create(
            profile_id=profile_id,
            name="Docker",
            category="Container",
            order_index=0,
            icon_url="   ",
        )
        assert t.icon_url is None

    def test_negative_order_index_raises_error(self, profile_id):
        with pytest.raises(InvalidOrderIndexError):
            Tool.create(
                profile_id=profile_id,
                name="Docker",
                category="Container",
                order_index=-1,
            )

    def test_empty_profile_id_raises_error(self):
        with pytest.raises(EmptyFieldError):
            Tool.create(
                profile_id="",
                name="Docker",
                category="Container",
                order_index=0,
            )


@pytest.mark.entity
class TestToolUpdate:
    """Test Tool updates."""

    def _make(self, profile_id):
        return Tool.create(
            profile_id=profile_id,
            name="Docker",
            category="Container",
            order_index=0,
        )

    def test_update_info(self, profile_id):
        t = self._make(profile_id)
        t.update_info(name="Podman", category="Container Runtime")
        assert t.name == "Podman"
        assert t.category == "Container Runtime"

    def test_update_info_invalid_name_raises(self, profile_id):
        t = self._make(profile_id)
        with pytest.raises(InvalidNameError):
            t.update_info(name="")

    def test_update_info_with_icon_url(self, profile_id):
        t = self._make(profile_id)
        t.update_info(icon_url="https://cdn.example.com/icon.png")
        assert t.icon_url == "https://cdn.example.com/icon.png"

    def test_remove_icon(self, profile_id):
        t = Tool.create(
            profile_id=profile_id,
            name="Docker",
            category="Container",
            order_index=0,
            icon_url="https://cdn.example.com/docker.png",
        )
        t.remove_icon()
        assert t.icon_url is None

    def test_update_order(self, profile_id):
        t = self._make(profile_id)
        t.update_order(5)
        assert t.order_index == 5

    def test_update_order_negative_raises(self, profile_id):
        t = self._make(profile_id)
        with pytest.raises(InvalidOrderIndexError):
            t.update_order(-1)
