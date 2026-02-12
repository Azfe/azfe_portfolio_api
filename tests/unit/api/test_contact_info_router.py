"""Tests for the contact information router endpoints."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

PREFIX = "/api/v1/contact-information"


class TestGetContactInfo:
    async def test_get_contact_info_returns_200(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "email" in data


class TestCreateContactInfo:
    async def test_create_returns_201(self, client: AsyncClient):
        payload = {
            "email": "test@example.com",
            "phone": "+34 600 000 000",
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_validation_invalid_email(self, client: AsyncClient):
        payload = {"email": "not-an-email"}
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_create_validation_empty(self, client: AsyncClient):
        response = await client.post(PREFIX, json={})
        assert response.status_code == 422


class TestUpdateContactInfo:
    async def test_update_returns_200(self, client: AsyncClient):
        payload = {"email": "updated@example.com"}
        response = await client.put(PREFIX, json=payload)
        assert response.status_code == 200


class TestDeleteContactInfo:
    async def test_delete_returns_200(self, client: AsyncClient):
        response = await client.delete(PREFIX)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
