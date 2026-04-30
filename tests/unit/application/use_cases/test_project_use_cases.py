"""Tests for Project use cases."""

from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from app.application.dto import (
    AddProjectRequest,
    DeleteProjectRequest,
    EditProjectRequest,
    ListProjectsRequest,
)
from app.application.use_cases.project.add_project import AddProjectUseCase
from app.application.use_cases.project.delete_project import DeleteProjectUseCase
from app.application.use_cases.project.edit_project import EditProjectUseCase
from app.application.use_cases.project.list_projects import ListProjectsUseCase
from app.domain.entities.project import Project
from app.shared.shared_exceptions import (
    BusinessRuleViolationException,
    NotFoundException,
)

pytestmark = pytest.mark.asyncio

PROFILE_ID = "profile-001"
START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2023, 6, 30)

# Description long enough to satisfy the 100-char minimum when no URLs are provided (RB-PR09)
LONG_DESCRIPTION = (
    "A full-featured e-commerce platform built with FastAPI and React, "
    "supporting thousands of concurrent users with real-time inventory management."
)


def _make_project(**overrides):
    defaults = {
        "profile_id": PROFILE_ID,
        "title": "My Portfolio Project",
        "description": LONG_DESCRIPTION,
        "start_date": START_DATE,
        "order_index": 0,
    }
    defaults.update(overrides)
    return Project.create(**defaults)


class TestAddProjectUseCase:
    @pytest.mark.unit
    async def test_add_project_success(self):
        repo = AsyncMock()
        project = _make_project()
        repo.get_by_order_index.return_value = None
        repo.add.return_value = project

        uc = AddProjectUseCase(repo)
        request = AddProjectRequest(
            profile_id=PROFILE_ID,
            title="My Portfolio Project",
            description=LONG_DESCRIPTION,
            start_date=START_DATE,
            order_index=0,
        )
        result = await uc.execute(request)

        assert result.title == "My Portfolio Project"
        assert result.profile_id == PROFILE_ID
        assert result.order_index == 0
        repo.get_by_order_index.assert_awaited_once_with(PROFILE_ID, 0)
        repo.add.assert_awaited_once()

    @pytest.mark.unit
    async def test_add_project_with_optional_fields(self):
        repo = AsyncMock()
        project = _make_project(
            end_date=END_DATE,
            live_url="https://example.com",
            repo_url="https://github.com/user/repo",
            technologies=["Python", "FastAPI", "MongoDB"],
        )
        repo.get_by_order_index.return_value = None
        repo.add.return_value = project

        uc = AddProjectUseCase(repo)
        request = AddProjectRequest(
            profile_id=PROFILE_ID,
            title="My Portfolio Project",
            description=LONG_DESCRIPTION,
            start_date=START_DATE,
            order_index=0,
            end_date=END_DATE,
            live_url="https://example.com",
            repo_url="https://github.com/user/repo",
            technologies=["Python", "FastAPI", "MongoDB"],
        )
        result = await uc.execute(request)

        assert result.end_date == END_DATE
        assert result.live_url == "https://example.com"
        assert result.repo_url == "https://github.com/user/repo"
        assert result.technologies == ["Python", "FastAPI", "MongoDB"]

    @pytest.mark.unit
    @pytest.mark.business_rule
    async def test_add_project_duplicate_order_index_raises(self):
        repo = AsyncMock()
        repo.get_by_order_index.return_value = _make_project()

        uc = AddProjectUseCase(repo)
        request = AddProjectRequest(
            profile_id=PROFILE_ID,
            title="Another Project",
            description=LONG_DESCRIPTION,
            start_date=START_DATE,
            order_index=0,
        )
        with pytest.raises(BusinessRuleViolationException):
            await uc.execute(request)

        repo.add.assert_not_awaited()

    @pytest.mark.unit
    async def test_add_project_checks_order_index_for_correct_profile(self):
        repo = AsyncMock()
        repo.get_by_order_index.return_value = None
        repo.add.return_value = _make_project(order_index=4)

        uc = AddProjectUseCase(repo)
        request = AddProjectRequest(
            profile_id=PROFILE_ID,
            title="My Portfolio Project",
            description=LONG_DESCRIPTION,
            start_date=START_DATE,
            order_index=4,
        )
        await uc.execute(request)

        repo.get_by_order_index.assert_awaited_once_with(PROFILE_ID, 4)


class TestDeleteProjectUseCase:
    @pytest.mark.unit
    async def test_delete_project_success(self):
        repo = AsyncMock()
        repo.delete.return_value = True

        uc = DeleteProjectUseCase(repo)
        result = await uc.execute(DeleteProjectRequest(project_id="project-001"))

        assert result.success is True
        repo.delete.assert_awaited_once_with("project-001")

    @pytest.mark.unit
    async def test_delete_project_not_found_raises(self):
        repo = AsyncMock()
        repo.delete.return_value = False

        uc = DeleteProjectUseCase(repo)
        with pytest.raises(NotFoundException):
            await uc.execute(DeleteProjectRequest(project_id="nonexistent"))


class TestEditProjectUseCase:
    @pytest.mark.unit
    async def test_edit_project_success(self):
        repo = AsyncMock()
        project = _make_project()
        repo.get_by_id.return_value = project
        repo.update.return_value = project

        uc = EditProjectUseCase(repo)
        request = EditProjectRequest(
            project_id="project-001",
            title="Updated Project Title",
        )
        result = await uc.execute(request)

        assert result.title == "Updated Project Title"
        repo.get_by_id.assert_awaited_once_with("project-001")
        repo.update.assert_awaited_once()

    @pytest.mark.unit
    async def test_edit_project_updates_multiple_fields(self):
        repo = AsyncMock()
        project = _make_project()
        repo.get_by_id.return_value = project
        repo.update.return_value = project

        uc = EditProjectUseCase(repo)
        request = EditProjectRequest(
            project_id="project-001",
            title="New Title",
            description=LONG_DESCRIPTION,
            end_date=END_DATE,
        )
        result = await uc.execute(request)

        assert result.title == "New Title"
        assert result.description == LONG_DESCRIPTION
        assert result.end_date == END_DATE

    @pytest.mark.unit
    async def test_edit_project_not_found_raises(self):
        repo = AsyncMock()
        repo.get_by_id.return_value = None

        uc = EditProjectUseCase(repo)
        request = EditProjectRequest(
            project_id="nonexistent",
            title="Updated Title",
        )
        with pytest.raises(NotFoundException):
            await uc.execute(request)

        repo.update.assert_not_awaited()

    @pytest.mark.unit
    async def test_edit_project_partial_update_preserves_existing_fields(self):
        repo = AsyncMock()
        project = _make_project(
            title="Original Title",
            live_url="https://original.com",
            repo_url="https://github.com/original/repo",
            technologies=["Python", "Django"],
        )
        repo.get_by_id.return_value = project
        repo.update.return_value = project

        uc = EditProjectUseCase(repo)
        request = EditProjectRequest(
            project_id="project-001",
            title="New Title",
        )
        result = await uc.execute(request)

        assert result.title == "New Title"
        assert result.live_url == "https://original.com"
        assert result.repo_url == "https://github.com/original/repo"
        assert result.technologies == ["Python", "Django"]

    @pytest.mark.unit
    async def test_edit_project_updates_urls(self):
        repo = AsyncMock()
        project = _make_project()
        repo.get_by_id.return_value = project
        repo.update.return_value = project

        uc = EditProjectUseCase(repo)
        request = EditProjectRequest(
            project_id="project-001",
            live_url="https://new-live.com",
            repo_url="https://github.com/new/repo",
        )
        result = await uc.execute(request)

        assert result.live_url == "https://new-live.com"
        assert result.repo_url == "https://github.com/new/repo"

    @pytest.mark.unit
    async def test_edit_project_updates_technologies(self):
        repo = AsyncMock()
        project = _make_project(technologies=["Python"])
        repo.get_by_id.return_value = project
        repo.update.return_value = project

        uc = EditProjectUseCase(repo)
        request = EditProjectRequest(
            project_id="project-001",
            technologies=["FastAPI", "React", "MongoDB"],
        )
        result = await uc.execute(request)

        assert result.technologies == ["FastAPI", "React", "MongoDB"]


class TestListProjectsUseCase:
    @pytest.mark.unit
    async def test_list_projects_returns_empty_list(self):
        repo = AsyncMock()
        repo.find_by.return_value = []

        uc = ListProjectsUseCase(repo)
        result = await uc.execute(ListProjectsRequest(profile_id=PROFILE_ID))

        assert result.projects == []
        assert result.total == 0
        repo.find_by.assert_awaited_once_with(profile_id=PROFILE_ID)

    @pytest.mark.unit
    async def test_list_projects_returns_all_items(self):
        repo = AsyncMock()
        projects = [
            _make_project(title="Project A", order_index=0),
            _make_project(title="Project B", order_index=1),
            _make_project(title="Project C", order_index=2),
        ]
        repo.find_by.return_value = projects

        uc = ListProjectsUseCase(repo)
        result = await uc.execute(ListProjectsRequest(profile_id=PROFILE_ID))

        assert result.total == 3
        assert len(result.projects) == 3

    @pytest.mark.unit
    async def test_list_projects_sorted_ascending_by_default(self):
        repo = AsyncMock()
        projects = [
            _make_project(title="Project C", order_index=2),
            _make_project(title="Project A", order_index=0),
            _make_project(title="Project B", order_index=1),
        ]
        repo.find_by.return_value = projects

        uc = ListProjectsUseCase(repo)
        result = await uc.execute(
            ListProjectsRequest(profile_id=PROFILE_ID, ascending=True)
        )

        order_indices = [p.order_index for p in result.projects]
        assert order_indices == sorted(order_indices)

    @pytest.mark.unit
    async def test_list_projects_sorted_descending_when_requested(self):
        repo = AsyncMock()
        projects = [
            _make_project(title="Project A", order_index=0),
            _make_project(title="Project B", order_index=1),
            _make_project(title="Project C", order_index=2),
        ]
        repo.find_by.return_value = projects

        uc = ListProjectsUseCase(repo)
        result = await uc.execute(
            ListProjectsRequest(profile_id=PROFILE_ID, ascending=False)
        )

        order_indices = [p.order_index for p in result.projects]
        assert order_indices == sorted(order_indices, reverse=True)

    @pytest.mark.unit
    async def test_list_projects_includes_is_ongoing_field(self):
        repo = AsyncMock()
        project_ongoing = _make_project(
            title="Ongoing Project",
            order_index=0,
            # No end_date → is_ongoing = True
        )
        project_finished = _make_project(
            title="Finished Project",
            order_index=1,
            live_url="https://example.com",
            end_date=END_DATE,
        )
        repo.find_by.return_value = [project_ongoing, project_finished]

        uc = ListProjectsUseCase(repo)
        result = await uc.execute(ListProjectsRequest(profile_id=PROFILE_ID))

        ongoing_dto = next(p for p in result.projects if p.title == "Ongoing Project")
        finished_dto = next(p for p in result.projects if p.title == "Finished Project")

        assert ongoing_dto.is_ongoing is True
        assert finished_dto.is_ongoing is False
