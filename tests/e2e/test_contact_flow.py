"""
E2E tests for the contact message flow.

Tests the public contact form submission and admin management of messages
through the full stack (API → Use Cases → Repositories → MongoDB).
"""

from httpx import AsyncClient
import pytest

pytestmark = pytest.mark.e2e

PREFIX = "/api/v1/contact-messages"

CONTACT_MESSAGE = {
    "name": "John Doe",
    "email": "john@example.com",
    "message": "Hello! I'd like to connect with you about a project.",
}


class TestContactMessageFlow:
    """Test the complete contact message lifecycle."""

    async def test_create_and_list_messages(self, client: AsyncClient):
        """Create a message via public form and verify it appears in admin list."""
        # Create message (public endpoint)
        resp = await client.post(PREFIX, json=CONTACT_MESSAGE)
        assert resp.status_code == 201
        data = resp.json()
        assert data["success"] is True
        assert "message" in data

        # List messages (admin endpoint)
        resp = await client.get(PREFIX)
        assert resp.status_code == 200
        messages = resp.json()
        assert len(messages) >= 1
        msg = messages[0]
        assert msg["name"] == "John Doe"
        assert msg["email"] == "john@example.com"
        assert msg["status"] == "pending"
        assert "id" in msg

    async def test_get_message_by_id(self, client: AsyncClient):
        """Create a message and retrieve it by ID."""
        # Create
        await client.post(PREFIX, json=CONTACT_MESSAGE)

        # Get list to find the ID
        resp = await client.get(PREFIX)
        messages = resp.json()
        msg_id = messages[0]["id"]

        # Get by ID
        resp = await client.get(f"{PREFIX}/{msg_id}")
        assert resp.status_code == 200
        msg = resp.json()
        assert msg["id"] == msg_id
        assert msg["name"] == "John Doe"

    async def test_delete_message(self, client: AsyncClient):
        """Create a message, delete it, verify it's gone."""
        # Create
        await client.post(PREFIX, json=CONTACT_MESSAGE)

        # Get ID
        resp = await client.get(PREFIX)
        msg_id = resp.json()[0]["id"]

        # Delete
        resp = await client.delete(f"{PREFIX}/{msg_id}")
        assert resp.status_code == 200
        assert resp.json()["success"] is True

        # Verify gone
        resp = await client.get(PREFIX)
        assert len(resp.json()) == 0

    async def test_stats_summary(self, client: AsyncClient):
        """Create messages and verify stats reflect the count."""
        # Create 2 messages
        await client.post(PREFIX, json=CONTACT_MESSAGE)
        await client.post(
            PREFIX,
            json={
                "name": "Jane Smith",
                "email": "jane@example.com",
                "message": "Interested in working together on a new project!",
            },
        )

        # Check stats
        resp = await client.get(f"{PREFIX}/stats/summary")
        assert resp.status_code == 200
        stats = resp.json()
        assert stats["total"] >= 2
        assert "today" in stats
        assert "this_week" in stats
        assert "by_day" in stats

    async def test_recent_messages(self, client: AsyncClient):
        """Create messages and verify recent endpoint limits results."""
        # Create 3 messages
        for i in range(3):
            await client.post(
                PREFIX,
                json={
                    "name": f"User {i}",
                    "email": f"user{i}@example.com",
                    "message": f"This is test message number {i} for the contact form.",
                },
            )

        # Get recent with limit 2
        resp = await client.get(f"{PREFIX}/recent/2")
        assert resp.status_code == 200
        messages = resp.json()
        assert len(messages) <= 2


class TestContactMessageValidation:
    """Test validation of contact message submissions."""

    async def test_missing_name_returns_422(self, client: AsyncClient):
        resp = await client.post(
            PREFIX,
            json={
                "email": "test@example.com",
                "message": "This is a valid message body for testing.",
            },
        )
        assert resp.status_code == 422

    async def test_invalid_email_returns_422(self, client: AsyncClient):
        resp = await client.post(
            PREFIX,
            json={
                "name": "Test",
                "email": "not-an-email",
                "message": "This is a valid message body for testing.",
            },
        )
        assert resp.status_code == 422

    async def test_message_too_short_returns_422(self, client: AsyncClient):
        resp = await client.post(
            PREFIX,
            json={"name": "Test", "email": "test@example.com", "message": "Hi"},
        )
        assert resp.status_code == 422

    async def test_get_nonexistent_message_returns_404(self, client: AsyncClient):
        resp = await client.get(f"{PREFIX}/nonexistent-id-12345")
        assert resp.status_code == 404
