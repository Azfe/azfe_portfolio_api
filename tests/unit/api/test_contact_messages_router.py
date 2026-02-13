"""Tests for the contact messages router endpoints."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

PREFIX = "/api/v1/contact-messages"


class TestListMessages:
    async def test_list_messages_returns_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    async def test_list_messages_has_required_fields(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        first = data[0]
        assert "id" in first
        assert "name" in first
        assert "email" in first
        assert "message" in first


class TestGetMessage:
    async def test_get_message_by_id(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/msg_001")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "msg_001"

    async def test_get_message_not_found(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/nonexistent")
        assert response.status_code == 404


class TestCreateMessage:
    async def test_create_message_returns_201(self, client: AsyncClient):
        payload = {
            "name": "Test User",
            "email": "test@example.com",
            "message": "This is a test message with enough characters to pass validation.",
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_validation_invalid_email(self, client: AsyncClient):
        payload = {
            "name": "Test",
            "email": "not-valid",
            "message": "This is a test message with enough characters.",
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_create_validation_message_too_short(self, client: AsyncClient):
        payload = {
            "name": "Test",
            "email": "test@example.com",
            "message": "Short",
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_create_validation_empty(self, client: AsyncClient):
        response = await client.post(PREFIX, json={})
        assert response.status_code == 422


class TestDeleteMessage:
    async def test_delete_returns_success(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/msg_001")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestMessageStats:
    async def test_stats_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/stats/summary")
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert data["total"] > 0


class TestRecentMessages:
    async def test_recent_returns_list(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/recent/5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 5
