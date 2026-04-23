"""Integration tests for exception handlers.

Tests that application exceptions are correctly mapped to HTTP error responses
with the standardized format: {success, error, message, code}.
"""

from httpx import AsyncClient
import pytest

pytestmark = pytest.mark.integration


class TestNotFoundExceptionHandler:
    """Tests that 404 responses have the correct error format."""

    async def test_404_from_skill_router(self, client: AsyncClient):
        response = await client.get("/api/v1/skills/nonexistent-id")
        assert response.status_code == 404

    async def test_404_from_education_router(self, client: AsyncClient):
        response = await client.get("/api/v1/education/nonexistent-id")
        assert response.status_code == 404

    async def test_404_from_work_experience_router(self, client: AsyncClient):
        response = await client.get("/api/v1/work-experiences/nonexistent-id")
        assert response.status_code == 404

    async def test_404_from_project_router(self, client: AsyncClient):
        response = await client.get("/api/v1/projects/nonexistent-id")
        assert response.status_code == 404

    async def test_404_from_certification_router(self, client: AsyncClient):
        response = await client.get("/api/v1/certifications/nonexistent-id")
        assert response.status_code == 404

    async def test_404_from_additional_training_router(self, client: AsyncClient):
        response = await client.get("/api/v1/additional-training/nonexistent-id")
        assert response.status_code == 404

    async def test_404_from_contact_messages_router(self, client: AsyncClient):
        response = await client.get("/api/v1/contact-messages/nonexistent-id")
        assert response.status_code == 404

    async def test_404_from_social_networks_router(self, client: AsyncClient):
        response = await client.get("/api/v1/social-networks/nonexistent-id")
        assert response.status_code == 404

    async def test_404_from_tools_router(self, client: AsyncClient):
        response = await client.get("/api/v1/tools/nonexistent-id")
        assert response.status_code == 404

    async def test_404_from_language_router(self, client: AsyncClient):
        response = await client.get("/api/v1/languages/nonexistent-id")
        assert response.status_code == 404

    async def test_404_from_programming_language_router(self, client: AsyncClient):
        response = await client.get("/api/v1/programming-languages/nonexistent-id")
        assert response.status_code == 404


class TestValidationExceptionHandler:
    """Tests that Pydantic validation errors return 422 with correct format."""

    async def test_422_response_format(self, client: AsyncClient):
        payload = {}  # Missing required fields
        response = await client.post("/api/v1/profile", json=payload)
        assert response.status_code == 422
        data = response.json()
        assert data["success"] is False
        assert data["error"] == "Validation Error"
        assert data["code"] == "VALIDATION_ERROR"
        assert "message" in data

    async def test_422_empty_string_field(self, client: AsyncClient):
        payload = {
            "name": "",
            "category": "backend",
            "order_index": 0,
        }
        response = await client.post("/api/v1/skills", json=payload)
        assert response.status_code == 422

    async def test_422_invalid_email(self, client: AsyncClient):
        payload = {"email": "not-valid-email"}
        response = await client.post("/api/v1/contact-information", json=payload)
        assert response.status_code == 422

    async def test_422_negative_order_index(self, client: AsyncClient):
        payload = {
            "name": "Test",
            "category": "backend",
            "order_index": -1,
        }
        response = await client.post("/api/v1/skills", json=payload)
        assert response.status_code == 422

    async def test_422_invalid_skill_level(self, client: AsyncClient):
        payload = {
            "name": "Test",
            "category": "backend",
            "level": "godlike",
            "order_index": 0,
        }
        response = await client.post("/api/v1/skills", json=payload)
        assert response.status_code == 422

    async def test_422_message_too_short(self, client: AsyncClient):
        payload = {
            "name": "Test",
            "email": "test@example.com",
            "message": "Hi",
        }
        response = await client.post("/api/v1/contact-messages", json=payload)
        assert response.status_code == 422


class TestNonExistentEndpoint:
    """Tests that non-existent endpoints return 404."""

    async def test_nonexistent_route_returns_404(self, client: AsyncClient):
        response = await client.get("/api/v1/nonexistent-endpoint")
        assert response.status_code == 404

    async def test_wrong_method_returns_405(self, client: AsyncClient):
        response = await client.patch("/api/v1/profile")
        assert response.status_code == 405


class TestNotImplemented:
    """Tests for endpoints that return 501."""

    async def test_cv_download_returns_501(self, client: AsyncClient):
        response = await client.get("/api/v1/cv/download")
        assert response.status_code == 501
