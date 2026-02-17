"""Integration tests for the language router endpoints."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.integration

PREFIX = "/api/v1/languages"


class TestListLanguages:
    async def test_list_returns_200(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200

    async def test_list_returns_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    async def test_language_response_schema(self, client: AsyncClient):
        response = await client.get(PREFIX)
        lang = response.json()[0]
        assert "id" in lang
        assert "name" in lang
        assert "proficiency" in lang
        assert "order_index" in lang

    async def test_filter_by_proficiency(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}?proficiency=c2")
        assert response.status_code == 200
        data = response.json()
        assert all(lang["proficiency"] == "c2" for lang in data)

    async def test_filter_nonexistent_proficiency_returns_empty(
        self, client: AsyncClient
    ):
        response = await client.get(f"{PREFIX}?proficiency=z9")
        assert response.status_code == 200
        assert response.json() == []


class TestGetLanguage:
    async def test_get_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/lang_001")
        assert response.status_code == 200

    async def test_get_response_schema(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/lang_001")
        data = response.json()
        assert data["id"] == "lang_001"
        assert "name" in data
        assert "proficiency" in data

    async def test_get_nonexistent_returns_404(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/nonexistent")
        assert response.status_code == 404


class TestCreateLanguage:
    async def test_create_returns_201(self, client: AsyncClient):
        payload = {
            "name": "Deutsch",
            "proficiency": "a1",
            "order_index": 99,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_response_has_name(self, client: AsyncClient):
        payload = {
            "name": "Italiano",
            "proficiency": "b1",
            "order_index": 99,
        }
        response = await client.post(PREFIX, json=payload)
        data = response.json()
        assert "name" in data

    async def test_create_validation_error_missing_name(self, client: AsyncClient):
        payload = {
            "proficiency": "a1",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_create_validation_error_empty_name(self, client: AsyncClient):
        payload = {
            "name": "",
            "proficiency": "a1",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422


class TestUpdateLanguage:
    async def test_update_returns_200(self, client: AsyncClient):
        payload = {"name": "Updated Language"}
        response = await client.put(f"{PREFIX}/lang_001", json=payload)
        assert response.status_code == 200

    async def test_update_nonexistent_returns_404(self, client: AsyncClient):
        payload = {"name": "Updated"}
        response = await client.put(f"{PREFIX}/nonexistent", json=payload)
        assert response.status_code == 404


class TestDeleteLanguage:
    async def test_delete_returns_200(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/lang_001")
        assert response.status_code == 200

    async def test_delete_response_format(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/lang_001")
        data = response.json()
        assert "message" in data
