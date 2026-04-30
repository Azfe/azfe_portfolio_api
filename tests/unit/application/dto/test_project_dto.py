"""Tests for Project DTOs."""

import pytest

from app.application.dto.project_dto import ProjectListResponse, ProjectResponse

from .conftest import DT, DT2, DT_END, DT_START, make_entity

# Fixed dates — deterministic regardless of when tests run.
# The calculated field is_ongoing is driven by the mock return value,
# not by re-implementing the domain logic here.
DATE_START = DT_START  # 2024-01-01
DATE_END = DT_END  # 2024-12-31

LONG_DESCRIPTION = (
    "A comprehensive web application built with FastAPI and MongoDB "
    "that demonstrates clean architecture and domain-driven design."
)


def _make_project_entity(**overrides):
    """Build a MagicMock project entity with sensible defaults."""
    defaults = {
        "id": "proj-1",
        "profile_id": "p-1",
        "title": "Portfolio Backend",
        "description": LONG_DESCRIPTION,
        "start_date": DATE_START,
        "order_index": 0,
        "end_date": DATE_END,
        "live_url": "https://azfe.dev",
        "repo_url": "https://github.com/azfe/portfolio",
        "technologies": ["Python", "FastAPI", "MongoDB"],
    }
    # Separate the special _is_ongoing control key before passing to make_entity
    is_ongoing_value = overrides.pop("_is_ongoing", False)
    defaults.update(overrides)
    entity = make_entity(**defaults)
    entity.is_ongoing.return_value = is_ongoing_value
    return entity


class TestProjectResponseFromEntity:
    @pytest.mark.unit
    def test_maps_all_fields(self):
        entity = _make_project_entity()
        resp = ProjectResponse.from_entity(entity)

        assert resp.id == "proj-1"
        assert resp.profile_id == "p-1"
        assert resp.title == "Portfolio Backend"
        assert resp.description == LONG_DESCRIPTION
        assert resp.start_date == DATE_START
        assert resp.order_index == 0
        assert resp.end_date == DATE_END
        assert resp.live_url == "https://azfe.dev"
        assert resp.repo_url == "https://github.com/azfe/portfolio"
        assert resp.technologies == ["Python", "FastAPI", "MongoDB"]
        assert resp.created_at == DT
        assert resp.updated_at == DT2

    @pytest.mark.unit
    def test_returns_correct_type(self):
        entity = _make_project_entity()
        resp = ProjectResponse.from_entity(entity)

        assert isinstance(resp, ProjectResponse)

    @pytest.mark.unit
    def test_timestamps_preserved(self):
        entity = _make_project_entity()
        resp = ProjectResponse.from_entity(entity)

        assert resp.created_at == DT
        assert resp.updated_at == DT2

    @pytest.mark.unit
    def test_none_end_date(self):
        entity = _make_project_entity(end_date=None, _is_ongoing=True)
        resp = ProjectResponse.from_entity(entity)

        assert resp.end_date is None

    @pytest.mark.unit
    def test_none_live_url(self):
        entity = _make_project_entity(live_url=None)
        resp = ProjectResponse.from_entity(entity)

        assert resp.live_url is None

    @pytest.mark.unit
    def test_none_repo_url(self):
        entity = _make_project_entity(repo_url=None)
        resp = ProjectResponse.from_entity(entity)

        assert resp.repo_url is None

    @pytest.mark.unit
    def test_empty_technologies(self):
        entity = _make_project_entity(technologies=[])
        resp = ProjectResponse.from_entity(entity)

        assert resp.technologies == []

    @pytest.mark.unit
    def test_all_optional_fields_absent(self):
        entity = _make_project_entity(
            end_date=None,
            live_url=None,
            repo_url=None,
            technologies=[],
            _is_ongoing=True,
        )
        resp = ProjectResponse.from_entity(entity)

        assert resp.end_date is None
        assert resp.live_url is None
        assert resp.repo_url is None
        assert resp.technologies == []

    @pytest.mark.unit
    def test_required_fields_always_present(self):
        entity = _make_project_entity(
            end_date=None,
            live_url=None,
            repo_url=None,
            technologies=[],
            _is_ongoing=True,
        )
        resp = ProjectResponse.from_entity(entity)

        assert resp.id == "proj-1"
        assert resp.profile_id == "p-1"
        assert resp.title == "Portfolio Backend"
        assert resp.description == LONG_DESCRIPTION
        assert resp.start_date == DATE_START
        assert resp.order_index == 0

    @pytest.mark.unit
    def test_different_order_index(self):
        entity = _make_project_entity(order_index=5)
        resp = ProjectResponse.from_entity(entity)

        assert resp.order_index == 5

    @pytest.mark.unit
    def test_start_date_preserved(self):
        entity = _make_project_entity(start_date=DATE_END)
        resp = ProjectResponse.from_entity(entity)

        assert resp.start_date == DATE_END


class TestProjectResponseIsOngoing:
    """Tests focused on the `is_ongoing` calculated field."""

    @pytest.mark.unit
    def test_is_ongoing_true_when_no_end_date(self):
        """is_ongoing=True when entity has no end_date (ongoing project)."""
        entity = _make_project_entity(end_date=None, _is_ongoing=True)
        resp = ProjectResponse.from_entity(entity)

        assert resp.is_ongoing is True

    @pytest.mark.unit
    def test_is_ongoing_false_when_end_date_present(self):
        """is_ongoing=False when entity has an end_date (completed project)."""
        entity = _make_project_entity(end_date=DATE_END, _is_ongoing=False)
        resp = ProjectResponse.from_entity(entity)

        assert resp.is_ongoing is False

    @pytest.mark.unit
    def test_is_ongoing_delegates_to_entity_method(self):
        """from_entity() calls entity.is_ongoing() to compute the field."""
        entity = _make_project_entity(_is_ongoing=True)
        ProjectResponse.from_entity(entity)

        entity.is_ongoing.assert_called_once()

    @pytest.mark.unit
    def test_is_ongoing_true_type_is_bool(self):
        entity = _make_project_entity(end_date=None, _is_ongoing=True)
        resp = ProjectResponse.from_entity(entity)

        assert isinstance(resp.is_ongoing, bool)

    @pytest.mark.unit
    def test_is_ongoing_false_type_is_bool(self):
        entity = _make_project_entity(end_date=DATE_END, _is_ongoing=False)
        resp = ProjectResponse.from_entity(entity)

        assert isinstance(resp.is_ongoing, bool)


class TestProjectListResponseFromEntities:
    @pytest.mark.unit
    def test_maps_list(self):
        entities = [
            _make_project_entity(id="proj-1", title="Portfolio Backend"),
            _make_project_entity(id="proj-2", title="Portfolio Frontend"),
        ]
        resp = ProjectListResponse.from_entities(entities)

        assert resp.total == 2
        assert len(resp.projects) == 2

    @pytest.mark.unit
    def test_items_are_correctly_mapped(self):
        entities = [
            _make_project_entity(id="proj-1", title="Portfolio Backend"),
            _make_project_entity(id="proj-2", title="Portfolio Frontend"),
        ]
        resp = ProjectListResponse.from_entities(entities)

        assert resp.projects[0].title == "Portfolio Backend"
        assert resp.projects[1].title == "Portfolio Frontend"

    @pytest.mark.unit
    def test_empty_list(self):
        resp = ProjectListResponse.from_entities([])

        assert resp.total == 0
        assert resp.projects == []

    @pytest.mark.unit
    def test_returns_correct_type(self):
        resp = ProjectListResponse.from_entities([])

        assert isinstance(resp, ProjectListResponse)

    @pytest.mark.unit
    def test_single_item_list(self):
        entities = [_make_project_entity(id="proj-1")]
        resp = ProjectListResponse.from_entities(entities)

        assert resp.total == 1
        assert len(resp.projects) == 1
        assert isinstance(resp.projects[0], ProjectResponse)

    @pytest.mark.unit
    def test_items_preserve_is_ongoing_flag(self):
        """Each item in the list carries the correct is_ongoing value."""
        ongoing = _make_project_entity(
            id="proj-1", title="Active Project", end_date=None, _is_ongoing=True
        )
        completed = _make_project_entity(
            id="proj-2", title="Old Project", end_date=DATE_END, _is_ongoing=False
        )
        resp = ProjectListResponse.from_entities([ongoing, completed])

        assert resp.projects[0].is_ongoing is True
        assert resp.projects[1].is_ongoing is False

    @pytest.mark.unit
    def test_total_matches_entity_count(self):
        entities = [
            _make_project_entity(id=f"proj-{i}", title=f"Project {i}") for i in range(4)
        ]
        resp = ProjectListResponse.from_entities(entities)

        assert resp.total == 4
        assert resp.total == len(resp.projects)
