"""Tests for the global exception handlers.

Verifies that the centralized error handling produces consistent
JSON responses following the ErrorResponse schema.
"""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

PREFIX = "/api/v1"


class TestValidationErrorHandler:
    """RequestValidationError → 422 with clean format."""

    async def test_missing_required_field_returns_422(self, client: AsyncClient):
        response = await client.post(f"{PREFIX}/skills", json={})
        assert response.status_code == 422

    async def test_invalid_type_returns_422(self, client: AsyncClient):
        payload = {
            "name": "Test",
            "category": "backend",
            "order_index": "not_a_number",
        }
        response = await client.post(f"{PREFIX}/skills", json=payload)
        assert response.status_code == 422

    async def test_validation_error_has_error_format(self, client: AsyncClient):
        response = await client.post(f"{PREFIX}/skills", json={})
        data = response.json()
        assert data["success"] is False
        assert "error" in data
        assert "message" in data
        assert data["code"] == "VALIDATION_ERROR"


class TestNotFoundHandler:
    """HTTPException 404 from routers (mock data not found)."""

    async def test_skill_not_found_returns_404(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/skills/nonexistent_id")
        assert response.status_code == 404

    async def test_language_not_found_returns_404(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/languages/nonexistent_id")
        assert response.status_code == 404

    async def test_programming_language_not_found_returns_404(
        self, client: AsyncClient
    ):
        response = await client.get(f"{PREFIX}/programming-languages/nonexistent_id")
        assert response.status_code == 404

    async def test_education_not_found_returns_404(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/education/nonexistent_id")
        assert response.status_code == 404

    async def test_work_experience_not_found_returns_404(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/work-experiences/nonexistent_id")
        assert response.status_code == 404

    async def test_project_not_found_returns_404(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/projects/nonexistent_id")
        assert response.status_code == 404

    async def test_certification_not_found_returns_404(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/certifications/nonexistent_id")
        assert response.status_code == 404

    async def test_additional_training_not_found_returns_404(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/additional-training/nonexistent_id")
        assert response.status_code == 404


class TestNotImplementedHandler:
    """501 from CV download endpoint."""

    async def test_cv_download_returns_501(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/cv/download")
        assert response.status_code == 501

    async def test_cv_download_has_detail(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/cv/download")
        data = response.json()
        assert "detail" in data


class TestMethodNotAllowed:
    """Incorrect HTTP method returns 405."""

    async def test_get_on_post_only_endpoint(self, client: AsyncClient):
        response = await client.patch(f"{PREFIX}/skills/skill_001")
        assert response.status_code == 405


class TestRootEndpoint:
    """Root endpoint returns basic info."""

    async def test_root_returns_200(self, client: AsyncClient):
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data

    async def test_root_has_correct_structure(self, client: AsyncClient):
        response = await client.get("/")
        data = response.json()
        assert isinstance(data["message"], str)
        assert isinstance(data["version"], str)
        assert isinstance(data["docs"], str)
