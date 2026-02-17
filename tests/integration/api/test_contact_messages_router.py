"""Integration tests for the contact messages router endpoints."""

from httpx import AsyncClient
import pytest

pytestmark = pytest.mark.integration

PREFIX = "/api/v1/contact-messages"


class TestListContactMessages:
    async def test_list_messages_returns_200(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200

    async def test_list_messages_returns_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    async def test_message_response_schema(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        msg = data[0]
        assert "id" in msg
        assert "name" in msg
        assert "email" in msg
        assert "message" in msg
        assert "status" in msg
        assert "created_at" in msg

    async def test_messages_sorted_by_date_desc(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        dates = [m["created_at"] for m in data]
        assert dates == sorted(dates, reverse=True)

    async def test_message_status_is_valid(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        valid_statuses = {"pending", "read", "replied"}
        for msg in data:
            assert msg["status"] in valid_statuses


class TestGetContactMessage:
    async def test_get_message_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/msg_001")
        assert response.status_code == 200

    async def test_get_message_response_schema(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/msg_001")
        data = response.json()
        assert data["id"] == "msg_001"
        assert "name" in data
        assert "email" in data

    async def test_get_nonexistent_message_returns_404(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/nonexistent")
        assert response.status_code == 404


class TestCreateContactMessage:
    async def test_create_message_returns_201(self, client: AsyncClient):
        payload = {
            "name": "Test User",
            "email": "test@example.com",
            "message": "Hello, this is a test message for the contact form.",
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_message_response_has_message(self, client: AsyncClient):
        payload = {
            "name": "Test User",
            "email": "test@example.com",
            "message": "Hello, this is a test message for the contact form.",
        }
        response = await client.post(PREFIX, json=payload)
        data = response.json()
        assert data["success"] is True
        assert "message" in data

    async def test_create_message_validation_error_missing_name(
        self, client: AsyncClient
    ):
        payload = {
            "email": "test@example.com",
            "message": "Hello, this is a test message for the contact form.",
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_create_message_validation_error_invalid_email(
        self, client: AsyncClient
    ):
        payload = {
            "name": "Test User",
            "email": "not-valid",
            "message": "Hello, this is a test message for the contact form.",
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_create_message_validation_error_short_message(
        self, client: AsyncClient
    ):
        payload = {
            "name": "Test User",
            "email": "test@example.com",
            "message": "Short",
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422


class TestDeleteContactMessage:
    async def test_delete_message_returns_200(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/msg_001")
        assert response.status_code == 200

    async def test_delete_message_response_format(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/msg_001")
        data = response.json()
        assert data["success"] is True
        assert "message" in data


class TestContactMessageStats:
    async def test_stats_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/stats/summary")
        assert response.status_code == 200

    async def test_stats_response_schema(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/stats/summary")
        data = response.json()
        assert "total" in data
        assert "today" in data
        assert "this_week" in data
        assert "this_month" in data
        assert "by_day" in data
        assert isinstance(data["total"], int)
        assert data["total"] > 0


class TestRecentMessages:
    async def test_recent_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/recent/5")
        assert response.status_code == 200

    async def test_recent_returns_list(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/recent/3")
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 3

    async def test_recent_respects_limit(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/recent/2")
        data = response.json()
        assert len(data) <= 2
