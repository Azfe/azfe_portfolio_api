"""Tests for the programming language router endpoints."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

PREFIX = "/api/v1/programming-languages"


class TestListProgrammingLanguages:
    async def test_list_returns_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 4

    async def test_filter_by_level(self, client: AsyncClient):
        response = await client.get(PREFIX, params={"level": "expert"})
        assert response.status_code == 200
        data = response.json()
        assert all(pl["level"] == "expert" for pl in data)

    async def test_has_required_fields(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        first = data[0]
        assert "id" in first
        assert "name" in first
        assert "level" in first
        assert "order_index" in first


class TestGetProgrammingLanguage:
    async def test_get_by_id(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/pl_001")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "pl_001"
        assert data["name"] == "Python"

    async def test_not_found(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/nonexistent")
        assert response.status_code == 404


class TestCreateProgrammingLanguage:
    async def test_create_returns_201(self, client: AsyncClient):
        payload = {"name": "Java", "order_index": 10, "level": "basic"}
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Java"
        assert data["level"] == "basic"

    async def test_create_without_level(self, client: AsyncClient):
        payload = {"name": "Scala", "order_index": 11}
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_validation_empty_body(self, client: AsyncClient):
        response = await client.post(PREFIX, json={})
        assert response.status_code == 422

    async def test_validation_empty_name(self, client: AsyncClient):
        payload = {"name": "", "order_index": 0}
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_validation_negative_order(self, client: AsyncClient):
        payload = {"name": "Ruby", "order_index": -1}
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422


class TestUpdateProgrammingLanguage:
    async def test_update_returns_200(self, client: AsyncClient):
        payload = {"name": "Python 3.13"}
        response = await client.put(f"{PREFIX}/pl_001", json=payload)
        assert response.status_code == 200

    async def test_update_not_found(self, client: AsyncClient):
        payload = {"name": "Test"}
        response = await client.put(f"{PREFIX}/nonexistent", json=payload)
        assert response.status_code == 404


class TestDeleteProgrammingLanguage:
    async def test_delete_returns_200(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/pl_001")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    async def test_delete_not_found(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/nonexistent")
        assert response.status_code == 404
