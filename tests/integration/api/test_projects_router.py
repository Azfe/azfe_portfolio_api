"""Integration tests for the projects router endpoints."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.integration

PREFIX = "/api/v1/projects"


class TestListProjects:
    async def test_list_returns_200(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200

    async def test_list_returns_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    async def test_project_response_schema(self, client: AsyncClient):
        response = await client.get(PREFIX)
        proj = response.json()[0]
        assert "id" in proj
        assert "title" in proj
        assert "description" in proj
        assert "start_date" in proj
        assert "technologies" in proj
        assert "order_index" in proj

    async def test_projects_sorted_by_order_index(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        indices = [p["order_index"] for p in data]
        assert indices == sorted(indices)

    async def test_technologies_is_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        proj = response.json()[0]
        assert isinstance(proj["technologies"], list)


class TestGetProject:
    async def test_get_project_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/proj_001")
        assert response.status_code == 200

    async def test_get_project_response_schema(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/proj_001")
        data = response.json()
        assert data["id"] == "proj_001"
        assert "title" in data

    async def test_get_nonexistent_project_returns_404(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/nonexistent")
        assert response.status_code == 404


class TestCreateProject:
    async def test_create_project_returns_201(self, client: AsyncClient):
        payload = {
            "title": "Test Project",
            "description": "A test project description with enough length",
            "start_date": "2024-01-01T00:00:00",
            "order_index": 99,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_with_all_fields(self, client: AsyncClient):
        payload = {
            "title": "Test Project",
            "description": "A test project description with enough length",
            "start_date": "2024-01-01T00:00:00",
            "end_date": "2024-12-31T00:00:00",
            "technologies": ["Python", "FastAPI"],
            "repo_url": "https://github.com/test/project",
            "live_url": "https://example.com",
            "order_index": 99,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_validation_error_missing_title(self, client: AsyncClient):
        payload = {
            "description": "Description",
            "start_date": "2024-01-01T00:00:00",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_create_validation_error_empty_description(self, client: AsyncClient):
        payload = {
            "title": "Test",
            "description": "",
            "start_date": "2024-01-01T00:00:00",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422


class TestUpdateProject:
    async def test_update_project_returns_200(self, client: AsyncClient):
        payload = {"title": "Updated Project"}
        response = await client.put(f"{PREFIX}/proj_001", json=payload)
        assert response.status_code == 200

    async def test_update_nonexistent_returns_404(self, client: AsyncClient):
        payload = {"title": "Updated"}
        response = await client.put(f"{PREFIX}/nonexistent", json=payload)
        assert response.status_code == 404


class TestDeleteProject:
    async def test_delete_project_returns_200(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/proj_001")
        assert response.status_code == 200

    async def test_delete_response_format(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/proj_001")
        data = response.json()
        assert data["success"] is True
        assert "message" in data


class TestReorderProjects:
    async def test_reorder_returns_200(self, client: AsyncClient):
        payload = [{"id": "proj_001", "orderIndex": 1}]
        response = await client.patch(f"{PREFIX}/reorder", json=payload)
        assert response.status_code == 200

    async def test_reorder_returns_list(self, client: AsyncClient):
        payload = [{"id": "proj_001", "orderIndex": 0}]
        response = await client.patch(f"{PREFIX}/reorder", json=payload)
        data = response.json()
        assert isinstance(data, list)
