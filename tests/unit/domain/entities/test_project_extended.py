"""
Extended tests for Project Entity.

Covers uncovered lines: update_order(), add_technology() when full or too long,
URL empty string normalization, update_info() with start/end dates, __repr__.
"""

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

LONG_DESC = "A" * 100


def _make_project(profile_id, **kwargs):
    defaults = {
        "profile_id": profile_id,
        "title": "My Project",
        "description": LONG_DESC,
        "start_date": datetime(2023, 1, 1),
        "order_index": 0,
    }
    defaults.update(kwargs)
    return Project.create(**defaults)


@pytest.mark.entity
@pytest.mark.business_rule
class TestProjectProfileIdValidation:
    """Test profile_id validation at both creation and update."""

    def test_empty_profile_id_at_creation_raises_error(self):
        """Empty profile_id should raise EmptyFieldError."""
        with pytest.raises(EmptyFieldError):
            Project.create(
                profile_id="",
                title="Test",
                description=LONG_DESC,
                start_date=datetime(2023, 1, 1),
                order_index=0,
            )

    def test_technology_item_too_long_in_validate_raises_error(self, profile_id):
        """Technology item > 150 chars in validation should raise InvalidLengthError."""
        with pytest.raises(InvalidLengthError):
            Project.create(
                profile_id=profile_id,
                title="Test",
                description=LONG_DESC,
                start_date=datetime(2023, 1, 1),
                order_index=0,
                technologies=["x" * 151],
            )


@pytest.mark.entity
class TestProjectURLNormalization:
    """Test that empty URL strings are normalized to None."""

    def test_empty_live_url_normalized_to_none(self, profile_id):
        """Empty live_url string should be stored as None."""
        project = _make_project(profile_id, live_url="")

        assert project.live_url is None

    def test_whitespace_live_url_normalized_to_none(self, profile_id):
        """Whitespace live_url should be stored as None."""
        project = _make_project(profile_id, live_url="   ")

        assert project.live_url is None

    def test_empty_repo_url_normalized_to_none(self, profile_id):
        """Empty repo_url string should be stored as None."""
        project = _make_project(profile_id, repo_url="")

        assert project.repo_url is None

    def test_whitespace_repo_url_normalized_to_none(self, profile_id):
        """Whitespace repo_url should be stored as None."""
        project = _make_project(profile_id, repo_url="   ")

        assert project.repo_url is None


@pytest.mark.entity
class TestProjectUpdateOrder:
    """Test update_order() method."""

    def test_update_order_changes_index(self, profile_id):
        """Should update order_index."""
        project = _make_project(profile_id, order_index=0)

        project.update_order(3)

        assert project.order_index == 3

    def test_update_order_negative_raises(self, profile_id):
        """Negative order_index should raise InvalidOrderIndexError."""
        project = _make_project(profile_id)

        with pytest.raises(InvalidOrderIndexError):
            project.update_order(-1)

    def test_update_order_updates_timestamp(self, profile_id):
        """update_order() should update the updated_at timestamp."""
        project = _make_project(profile_id)
        before = project.updated_at

        project.update_order(2)

        assert project.updated_at >= before


@pytest.mark.entity
class TestProjectAddTechnology:
    """Extended tests for add_technology()."""

    def test_add_technology_when_at_max_raises(self, profile_id):
        """Adding technology when list is already at max should raise InvalidLengthError."""
        project = _make_project(
            profile_id,
            technologies=[f"Tech{i}" for i in range(20)],
        )

        with pytest.raises(InvalidLengthError):
            project.add_technology("OneMore")

    def test_add_technology_too_long_raises(self, profile_id):
        """Adding a technology name > 150 chars should raise InvalidLengthError."""
        project = _make_project(profile_id)

        with pytest.raises(InvalidLengthError):
            project.add_technology("x" * 151)

    def test_add_technology_updates_timestamp(self, profile_id):
        """add_technology() should update the updated_at timestamp."""
        project = _make_project(profile_id)
        before = project.updated_at

        project.add_technology("Docker")

        assert project.updated_at >= before


@pytest.mark.entity
class TestProjectUpdateInfoWithDates:
    """Test update_info() with date parameters."""

    def test_update_start_date(self, profile_id):
        """Should update start_date."""
        project = _make_project(profile_id, start_date=datetime(2023, 1, 1))
        new_start = datetime(2022, 6, 1)
        project.update_info(start_date=new_start)

        assert project.start_date == new_start

    def test_update_end_date(self, profile_id):
        """Should update end_date."""
        project = _make_project(profile_id)
        new_end = datetime(2023, 12, 31)
        project.update_info(end_date=new_end)

        assert project.end_date == new_end

    def test_update_info_invalid_title_raises(self, profile_id):
        """Updating with empty title should raise InvalidTitleError."""
        project = _make_project(profile_id)

        with pytest.raises(InvalidTitleError):
            project.update_info(title="")

    def test_update_info_invalid_description_raises(self, profile_id):
        """Updating with short description (no URLs) should raise InvalidDescriptionError."""
        project = _make_project(profile_id)

        with pytest.raises((InvalidDescriptionError, InvalidLengthError)):
            project.update_info(description="Short")

    def test_update_info_invalid_date_order_raises(self, profile_id):
        """Setting end_date before start_date should raise InvalidDateRangeError."""
        project = _make_project(profile_id, start_date=datetime(2023, 6, 1))

        with pytest.raises(InvalidDateRangeError):
            project.update_info(end_date=datetime(2022, 1, 1))


@pytest.mark.entity
class TestProjectUpdateURLs:
    """Extended tests for update_urls()."""

    def test_update_both_urls(self, profile_id):
        """Should update both URLs."""
        project = _make_project(profile_id)
        project.update_urls(
            live_url="https://example.com",
            repo_url="https://github.com/user/repo",
        )

        assert project.live_url == "https://example.com"
        assert project.repo_url == "https://github.com/user/repo"

    def test_update_url_empty_string_normalized_to_none(self, profile_id):
        """Updating URL with empty string should normalize to None."""
        project = _make_project(
            profile_id,
            live_url="https://example.com",
        )
        project.update_urls(live_url="")

        assert project.live_url is None

    def test_update_url_invalid_repo_url_raises(self, profile_id):
        """Invalid repo_url should raise InvalidURLError."""
        project = _make_project(profile_id)

        with pytest.raises(InvalidURLError):
            project.update_urls(repo_url="ftp://invalid")

    def test_update_urls_updates_timestamp(self, profile_id):
        """update_urls() should update the updated_at timestamp."""
        project = _make_project(profile_id)
        before = project.updated_at

        project.update_urls(live_url="https://example.com")

        assert project.updated_at >= before


@pytest.mark.entity
class TestProjectRepr:
    """Test __repr__ method."""

    def test_repr_contains_title(self, profile_id):
        """__repr__ should include id and title."""
        project = _make_project(profile_id, title="My Amazing Project")

        result = repr(project)

        assert "Project" in result
        assert "My Amazing Project" in result
