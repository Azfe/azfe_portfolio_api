"""Tests for the projects router endpoints."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

PREFIX = "/api/v1/projects"


class TestListProjects:
    async def test_list_projects_returns_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    async def test_list_projects_has_required_fields(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        first = data[0]
        assert "id" in first
        assert "title" in first
        assert "order_index" in first


class TestGetProject:
    async def test_get_project_by_id(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/proj_001")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "proj_001"

    async def test_get_project_not_found(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/nonexistent")
        assert response.status_code == 404


class TestCreateProject:
    async def test_create_project_returns_201(self, client: AsyncClient):
        payload = {
            "title": "New Project",
            "description": "A long enough description for a project that needs at least some text to pass validation checks properly.",
            "start_date": "2024-01-01T00:00:00",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_project_validation_empty(self, client: AsyncClient):
        response = await client.post(PREFIX, json={})
        assert response.status_code == 422


class TestUpdateProject:
    async def test_update_project_not_found(self, client: AsyncClient):
        payload = {"title": "Updated"}
        response = await client.put(f"{PREFIX}/nonexistent", json=payload)
        assert response.status_code == 404


class TestDeleteProject:
    async def test_delete_returns_success(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/proj_001")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
