"""Tests for the education router endpoints."""

from httpx import AsyncClient
import pytest

pytestmark = pytest.mark.asyncio

PREFIX = "/api/v1/education"


class TestListEducation:
    async def test_list_education_returns_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    async def test_list_education_has_required_fields(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        first = data[0]
        assert "id" in first
        assert "institution" in first
        assert "degree" in first
        assert "order_index" in first


class TestGetEducation:
    async def test_get_education_by_id(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/edu_001")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "edu_001"

    async def test_get_education_not_found(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/nonexistent")
        assert response.status_code == 404


class TestCreateEducation:
    async def test_create_education_returns_201(self, client: AsyncClient):
        payload = {
            "institution": "MIT",
            "degree": "MSc Computer Science",
            "field": "AI",
            "start_date": "2020-09-01T00:00:00",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_education_validation_missing_fields(
        self, client: AsyncClient
    ):
        response = await client.post(PREFIX, json={})
        assert response.status_code == 422


class TestUpdateEducation:
    async def test_update_returns_200(self, client: AsyncClient):
        payload = {"institution": "Updated University"}
        response = await client.put(f"{PREFIX}/edu_001", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "edu_001"

    async def test_update_education_not_found(self, client: AsyncClient):
        payload = {"institution": "Updated"}
        response = await client.put(f"{PREFIX}/nonexistent", json=payload)
        assert response.status_code == 404

    async def test_update_passes_technologies_to_use_case(self, client: AsyncClient):
        """Regression: technologies must be forwarded to EditEducationRequest."""
        from unittest.mock import AsyncMock

        from app.api.dependencies import get_edit_education_use_case
        from app.main import app as fastapi_app
        from tests.unit.api.conftest import MOCK_EDUCATION

        captured_request = {}

        async def capture_execute(request):
            captured_request["req"] = request
            return MOCK_EDUCATION[0]

        mock_uc = AsyncMock()
        mock_uc.execute = AsyncMock(side_effect=capture_execute)
        fastapi_app.dependency_overrides[get_edit_education_use_case] = (
            lambda: mock_uc
        )

        try:
            payload = {"technologies": ["Python", "FastAPI"]}
            response = await client.put(f"{PREFIX}/edu_001", json=payload)

            assert response.status_code == 200
            assert captured_request["req"].technologies == ["Python", "FastAPI"]
        finally:
            # Restore autouse override so other tests are not affected
            from tests.unit.api.conftest import MOCK_EDUCATION, _mock_edit_uc

            fastapi_app.dependency_overrides[get_edit_education_use_case] = (
                lambda: _mock_edit_uc(MOCK_EDUCATION, "education_id", MOCK_EDUCATION[0])
            )


class TestDeleteEducation:
    async def test_delete_returns_success(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/edu_001")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestReorderEducation:
    async def test_reorder_returns_list(self, client: AsyncClient):
        payload = [{"id": "edu_001", "orderIndex": 1}]
        response = await client.patch(f"{PREFIX}/reorder", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
