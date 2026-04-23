"""Integration tests for the profile router endpoints."""

from httpx import AsyncClient
import pytest

pytestmark = pytest.mark.integration

PREFIX = "/api/v1/profile"


class TestGetProfile:
    async def test_get_profile_returns_200(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200

    async def test_get_profile_response_schema(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        assert "id" in data
        assert "name" in data
        assert "headline" in data

    async def test_get_profile_has_timestamps(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        assert "created_at" in data
        assert "updated_at" in data


class TestCreateProfile:
    async def test_create_profile_returns_201(self, client: AsyncClient):
        payload = {
            "name": "Test User",
            "headline": "Test Developer",
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_profile_with_all_fields(self, client: AsyncClient):
        payload = {
            "name": "Test User",
            "headline": "Test Developer",
            "bio": "A test bio",
            "location": "Test City",
            "avatar_url": "https://example.com/avatar.jpg",
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201
        data = response.json()
        assert "id" in data

    async def test_create_profile_validation_error_empty_name(
        self, client: AsyncClient
    ):
        payload = {
            "name": "",
            "headline": "Test Developer",
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_create_profile_validation_error_missing_fields(
        self, client: AsyncClient
    ):
        payload = {}
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_validation_error_response_format(self, client: AsyncClient):
        payload = {}
        response = await client.post(PREFIX, json=payload)
        data = response.json()
        assert data["success"] is False
        assert data["error"] == "Validation Error"
        assert data["code"] == "VALIDATION_ERROR"
        assert "message" in data


class TestUpdateProfile:
    async def test_update_profile_returns_200(self, client: AsyncClient):
        payload = {"name": "Updated Name"}
        response = await client.put(PREFIX, json=payload)
        assert response.status_code == 200

    async def test_update_profile_response_schema(self, client: AsyncClient):
        payload = {"headline": "Updated Headline"}
        response = await client.put(PREFIX, json=payload)
        data = response.json()
        assert "id" in data
        assert "name" in data


class TestDeleteProfile:
    async def test_delete_profile_returns_200(self, client: AsyncClient):
        response = await client.delete(PREFIX)
        assert response.status_code == 200

    async def test_delete_profile_response_message(self, client: AsyncClient):
        response = await client.delete(PREFIX)
        data = response.json()
        assert data["success"] is True
        assert "message" in data
