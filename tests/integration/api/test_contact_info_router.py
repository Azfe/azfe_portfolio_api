"""Integration tests for the contact information router endpoints."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.integration

PREFIX = "/api/v1/contact-information"


class TestGetContactInfo:
    async def test_get_contact_info_returns_200(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200

    async def test_contact_info_response_schema(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        assert "id" in data
        assert "email" in data


class TestCreateContactInfo:
    async def test_create_contact_info_returns_201(self, client: AsyncClient):
        payload = {
            "email": "test@example.com",
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_with_all_fields(self, client: AsyncClient):
        payload = {
            "email": "test@example.com",
            "phone": "+34 666 777 888",
            "linkedin": "https://linkedin.com/in/test",
            "github": "https://github.com/test",
            "website": "https://example.com",
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_validation_error_invalid_email(self, client: AsyncClient):
        payload = {"email": "not-an-email"}
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_create_validation_error_missing_email(self, client: AsyncClient):
        payload = {}
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422


class TestUpdateContactInfo:
    async def test_update_contact_info_returns_200(self, client: AsyncClient):
        payload = {"email": "updated@example.com"}
        response = await client.put(PREFIX, json=payload)
        assert response.status_code == 200


class TestDeleteContactInfo:
    async def test_delete_contact_info_returns_200(self, client: AsyncClient):
        response = await client.delete(PREFIX)
        assert response.status_code == 200

    async def test_delete_response_has_message(self, client: AsyncClient):
        response = await client.delete(PREFIX)
        data = response.json()
        assert "message" in data
