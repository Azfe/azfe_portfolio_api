"""Tests for the language router endpoints."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

PREFIX = "/api/v1/languages"


class TestListLanguages:
    async def test_list_returns_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3

    async def test_filter_by_proficiency(self, client: AsyncClient):
        response = await client.get(PREFIX, params={"proficiency": "c2"})
        assert response.status_code == 200
        data = response.json()
        assert all(lang["proficiency"] == "c2" for lang in data)

    async def test_has_required_fields(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        first = data[0]
        assert "id" in first
        assert "name" in first
        assert "proficiency" in first
        assert "order_index" in first


class TestGetLanguage:
    async def test_get_by_id(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/lang_001")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Español"

    async def test_not_found(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/nonexistent")
        assert response.status_code == 404


class TestCreateLanguage:
    async def test_create_returns_201(self, client: AsyncClient):
        payload = {"name": "Deutsch", "order_index": 5, "proficiency": "a1"}
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Deutsch"

    async def test_validation_empty_body(self, client: AsyncClient):
        response = await client.post(PREFIX, json={})
        assert response.status_code == 422

    async def test_validation_empty_name(self, client: AsyncClient):
        payload = {"name": "", "order_index": 0}
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_validation_negative_order(self, client: AsyncClient):
        payload = {"name": "Deutsch", "order_index": -1}
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422


class TestUpdateLanguage:
    async def test_update_returns_200(self, client: AsyncClient):
        payload = {"name": "Español (Castellano)"}
        response = await client.put(f"{PREFIX}/lang_001", json=payload)
        assert response.status_code == 200

    async def test_update_not_found(self, client: AsyncClient):
        payload = {"name": "Test"}
        response = await client.put(f"{PREFIX}/nonexistent", json=payload)
        assert response.status_code == 404


class TestDeleteLanguage:
    async def test_delete_returns_200(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/lang_001")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    async def test_delete_not_found(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/nonexistent")
        assert response.status_code == 404
