"""Tests for Project Entity."""

from datetime import datetime

import pytest

from app.domain.entities.project import Project
from app.domain.exceptions import (
    EmptyFieldError,
    InvalidDateRangeError,
    InvalidDescriptionError,
    InvalidLengthError,
    InvalidOrderIndexError,
    InvalidTitleError,
    InvalidURLError,
)

LONG_DESC = "A" * 100  # minimum for description without URLs


@pytest.mark.entity
class TestProjectCreation:
    """Test Project creation."""

    def test_create_with_required_fields(self, profile_id):
        p = Project.create(
            profile_id=profile_id,
            title="Portfolio",
            description=LONG_DESC,
            start_date=datetime(2023, 1, 1),
            order_index=0,
        )
        assert p.title == "Portfolio"
        assert p.description == LONG_DESC
        assert p.end_date is None
        assert p.technologies == []

    def test_create_with_all_fields(self, profile_id):
        p = Project.create(
            profile_id=profile_id,
            title="Portfolio",
            description="Full-stack portfolio website",
            start_date=datetime(2023, 1, 1),
            order_index=0,
            end_date=datetime(2023, 6, 1),
            live_url="https://example.com",
            repo_url="https://github.com/user/repo",
            technologies=["Python", "FastAPI"],
        )
        assert p.live_url == "https://example.com"
        assert p.repo_url == "https://github.com/user/repo"
        assert len(p.technologies) == 2

    def test_create_generates_uuid(self, profile_id):
        p = Project.create(
            profile_id=profile_id,
            title="Test",
            description=LONG_DESC,
            start_date=datetime(2023, 1, 1),
            order_index=0,
        )
        assert p.id is not None


@pytest.mark.entity
@pytest.mark.business_rule
class TestProjectValidation:
    """Test Project validation rules."""

    def test_empty_title_raises_error(self, profile_id):
        with pytest.raises(InvalidTitleError):
            Project.create(
                profile_id=profile_id,
                title="",
                description=LONG_DESC,
                start_date=datetime(2023, 1, 1),
                order_index=0,
            )

    def test_title_too_long_raises_error(self, profile_id):
        with pytest.raises(InvalidLengthError):
            Project.create(
                profile_id=profile_id,
                title="x" * 101,
                description=LONG_DESC,
                start_date=datetime(2023, 1, 1),
                order_index=0,
            )

    def test_empty_description_raises_error(self, profile_id):
        with pytest.raises(InvalidDescriptionError):
            Project.create(
                profile_id=profile_id,
                title="Test",
                description="",
                start_date=datetime(2023, 1, 1),
                order_index=0,
            )

    def test_description_too_short_raises_error(self, profile_id):
        with pytest.raises(InvalidLengthError):
            Project.create(
                profile_id=profile_id,
                title="Test",
                description="Short",
                start_date=datetime(2023, 1, 1),
                order_index=0,
            )

    def test_description_too_long_raises_error(self, profile_id):
        with pytest.raises(InvalidLengthError):
            Project.create(
                profile_id=profile_id,
                title="Test",
                description="x" * 2001,
                start_date=datetime(2023, 1, 1),
                order_index=0,
            )

    def test_description_insufficient_without_urls(self, profile_id):
        """RB-PR09: description < 100 chars without URLs raises error."""
        with pytest.raises(InvalidDescriptionError):
            Project.create(
                profile_id=profile_id,
                title="Test",
                description="A" * 50,  # > 10 but < 100, no URLs
                start_date=datetime(2023, 1, 1),
                order_index=0,
            )

    def test_short_description_ok_with_urls(self, profile_id):
        """RB-PR09: short description is OK if URLs are provided."""
        p = Project.create(
            profile_id=profile_id,
            title="Test",
            description="A short project description here.",
            start_date=datetime(2023, 1, 1),
            order_index=0,
            live_url="https://example.com",
        )
        assert p.has_urls() is True

    def test_end_date_before_start_raises_error(self, profile_id):
        with pytest.raises(InvalidDateRangeError):
            Project.create(
                profile_id=profile_id,
                title="Test",
                description=LONG_DESC,
                start_date=datetime(2023, 6, 1),
                order_index=0,
                end_date=datetime(2023, 1, 1),
            )

    def test_invalid_live_url_raises_error(self, profile_id):
        with pytest.raises(InvalidURLError):
            Project.create(
                profile_id=profile_id,
                title="Test",
                description=LONG_DESC,
                start_date=datetime(2023, 1, 1),
                order_index=0,
                live_url="not-a-url",
            )

    def test_invalid_repo_url_raises_error(self, profile_id):
        with pytest.raises(InvalidURLError):
            Project.create(
                profile_id=profile_id,
                title="Test",
                description=LONG_DESC,
                start_date=datetime(2023, 1, 1),
                order_index=0,
                repo_url="ftp://invalid",
            )

    def test_negative_order_index_raises_error(self, profile_id):
        with pytest.raises(InvalidOrderIndexError):
            Project.create(
                profile_id=profile_id,
                title="Test",
                description=LONG_DESC,
                start_date=datetime(2023, 1, 1),
                order_index=-1,
            )

    def test_too_many_technologies_raises_error(self, profile_id):
        with pytest.raises(InvalidLengthError):
            Project.create(
                profile_id=profile_id,
                title="Test",
                description=LONG_DESC,
                start_date=datetime(2023, 1, 1),
                order_index=0,
                technologies=[f"Tech{i}" for i in range(21)],
            )

    def test_empty_technology_item_raises_error(self, profile_id):
        with pytest.raises(EmptyFieldError):
            Project.create(
                profile_id=profile_id,
                title="Test",
                description=LONG_DESC,
                start_date=datetime(2023, 1, 1),
                order_index=0,
                technologies=["Python", ""],
            )


@pytest.mark.entity
class TestProjectUpdate:
    """Test Project updates."""

    def _make(self, profile_id):
        return Project.create(
            profile_id=profile_id,
            title="Portfolio",
            description=LONG_DESC,
            start_date=datetime(2023, 1, 1),
            order_index=0,
        )

    def test_update_info(self, profile_id):
        p = self._make(profile_id)
        new_desc = "B" * 100
        p.update_info(title="New Title", description=new_desc)
        assert p.title == "New Title"
        assert p.description == new_desc

    def test_update_urls(self, profile_id):
        p = self._make(profile_id)
        p.update_urls(
            live_url="https://example.com",
            repo_url="https://github.com/user/repo",
        )
        assert p.live_url == "https://example.com"
        assert p.repo_url == "https://github.com/user/repo"

    def test_update_urls_invalid_raises(self, profile_id):
        p = self._make(profile_id)
        with pytest.raises(InvalidURLError):
            p.update_urls(live_url="not-valid")

    def test_add_technology(self, profile_id):
        p = self._make(profile_id)
        p.add_technology("Docker")
        assert "Docker" in p.technologies

    def test_add_empty_technology_raises(self, profile_id):
        p = self._make(profile_id)
        with pytest.raises(EmptyFieldError):
            p.add_technology("")

    def test_update_technologies(self, profile_id):
        p = self._make(profile_id)
        p.update_technologies(["React", "TypeScript"])
        assert p.technologies == ["React", "TypeScript"]


@pytest.mark.entity
class TestProjectBusinessMethods:
    """Test Project business methods."""

    def test_is_ongoing_no_end_date(self, profile_id):
        p = Project.create(
            profile_id=profile_id,
            title="Test",
            description=LONG_DESC,
            start_date=datetime(2023, 1, 1),
            order_index=0,
        )
        assert p.is_ongoing() is True

    def test_is_not_ongoing_with_end_date(self, profile_id):
        p = Project.create(
            profile_id=profile_id,
            title="Test",
            description=LONG_DESC,
            start_date=datetime(2022, 1, 1),
            order_index=0,
            end_date=datetime(2023, 1, 1),
        )
        assert p.is_ongoing() is False

    def test_has_urls_with_live_url(self, profile_id):
        p = Project.create(
            profile_id=profile_id,
            title="Test",
            description="Short desc for URL project",
            start_date=datetime(2023, 1, 1),
            order_index=0,
            live_url="https://example.com",
        )
        assert p.has_urls() is True

    def test_has_no_urls(self, profile_id):
        p = Project.create(
            profile_id=profile_id,
            title="Test",
            description=LONG_DESC,
            start_date=datetime(2023, 1, 1),
            order_index=0,
        )
        assert p.has_urls() is False
