"""Tests for the contact messages router endpoints."""

from httpx import AsyncClient
import pytest

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

    async def test_stats_has_date_fields(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/stats/summary")
        data = response.json()
        assert "today" in data
        assert "this_week" in data
        assert "this_month" in data

    async def test_stats_has_by_day(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/stats/summary")
        data = response.json()
        assert "by_day" in data
        assert isinstance(data["by_day"], dict)
        assert len(data["by_day"]) == 7

    async def test_stats_total_matches_list(self, client: AsyncClient):
        list_response = await client.get(PREFIX)
        stats_response = await client.get(f"{PREFIX}/stats/summary")
        total_list = len(list_response.json())
        total_stats = stats_response.json()["total"]
        assert total_list == total_stats

    async def test_stats_date_counts_are_non_negative(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/stats/summary")
        data = response.json()
        assert data["today"] >= 0
        assert data["this_week"] >= 0
        assert data["this_month"] >= 0


class TestRecentMessages:
    async def test_recent_returns_list(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/recent/5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 5

    async def test_recent_sorted_desc(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/recent/10")
        data = response.json()
        dates = [m["created_at"] for m in data if m.get("created_at")]
        assert dates == sorted(dates, reverse=True)

    async def test_recent_limit_1(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/recent/1")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 1

    async def test_recent_large_limit_capped(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/recent/100")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 50
