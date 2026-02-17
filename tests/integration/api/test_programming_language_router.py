"""Integration tests for the programming language router endpoints."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.integration

PREFIX = "/api/v1/programming-languages"


class TestListProgrammingLanguages:
    async def test_list_returns_200(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200

    async def test_list_returns_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    async def test_programming_language_response_schema(self, client: AsyncClient):
        response = await client.get(PREFIX)
        pl = response.json()[0]
        assert "id" in pl
        assert "name" in pl
        assert "level" in pl
        assert "order_index" in pl

    async def test_filter_by_level(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}?level=expert")
        assert response.status_code == 200
        data = response.json()
        assert all(pl["level"] == "expert" for pl in data)

    async def test_filter_nonexistent_level_returns_empty(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}?level=nonexistent")
        assert response.status_code == 200
        assert response.json() == []


class TestGetProgrammingLanguage:
    async def test_get_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/pl_001")
        assert response.status_code == 200

    async def test_get_response_schema(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/pl_001")
        data = response.json()
        assert data["id"] == "pl_001"
        assert "name" in data
        assert "level" in data

    async def test_get_nonexistent_returns_404(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/nonexistent")
        assert response.status_code == 404


class TestCreateProgrammingLanguage:
    async def test_create_returns_201(self, client: AsyncClient):
        payload = {
            "name": "Java",
            "level": "basic",
            "order_index": 99,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_response_has_name(self, client: AsyncClient):
        payload = {
            "name": "Kotlin",
            "level": "intermediate",
            "order_index": 99,
        }
        response = await client.post(PREFIX, json=payload)
        data = response.json()
        assert "name" in data

    async def test_create_validation_error_missing_name(self, client: AsyncClient):
        payload = {
            "level": "basic",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_create_validation_error_empty_name(self, client: AsyncClient):
        payload = {
            "name": "",
            "level": "basic",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422


class TestUpdateProgrammingLanguage:
    async def test_update_returns_200(self, client: AsyncClient):
        payload = {"name": "Updated PL"}
        response = await client.put(f"{PREFIX}/pl_001", json=payload)
        assert response.status_code == 200

    async def test_update_nonexistent_returns_404(self, client: AsyncClient):
        payload = {"name": "Updated"}
        response = await client.put(f"{PREFIX}/nonexistent", json=payload)
        assert response.status_code == 404


class TestDeleteProgrammingLanguage:
    async def test_delete_returns_200(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/pl_001")
        assert response.status_code == 200

    async def test_delete_response_format(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/pl_001")
        data = response.json()
        assert "message" in data
