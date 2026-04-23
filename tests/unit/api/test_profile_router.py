"""Tests for the profile router endpoints."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

PREFIX = "/api/v1/profile"


class TestGetProfile:
    async def test_get_profile_returns_200(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200

    async def test_get_profile_has_required_fields(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        assert "id" in data
        assert "name" in data
        assert "headline" in data


class TestCreateProfile:
    async def test_create_profile_returns_201(self, client: AsyncClient):
        payload = {
            "name": "Test User",
            "headline": "Test Developer",
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_profile_validation_missing_name(self, client: AsyncClient):
        payload = {"headline": "Test Developer"}
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_create_profile_validation_empty_name(self, client: AsyncClient):
        payload = {"name": "", "headline": "Test Developer"}
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422


class TestUpdateProfile:
    async def test_update_profile_returns_200(self, client: AsyncClient):
        payload = {"name": "Updated Name"}
        response = await client.put(PREFIX, json=payload)
        assert response.status_code == 200


class TestDeleteProfile:
    async def test_delete_profile_returns_200(self, client: AsyncClient):
        response = await client.delete(PREFIX)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
