"""Integration tests for the CV router endpoints."""

from httpx import AsyncClient
import pytest

pytestmark = pytest.mark.integration

PREFIX = "/api/v1/cv"


class TestGetCompleteCV:
    async def test_get_cv_returns_200(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200

    async def test_cv_has_all_sections(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        assert "profile" in data
        assert "contact_info" in data
        assert "work_experiences" in data
        assert "projects" in data
        assert "skills" in data
        assert "tools" in data
        assert "education" in data
        assert "certifications" in data
        assert "additional_training" in data
        assert "social_networks" in data

    async def test_cv_profile_has_fields(self, client: AsyncClient):
        response = await client.get(PREFIX)
        profile = response.json()["profile"]
        assert "name" in profile
        assert "headline" in profile

    async def test_cv_lists_are_arrays(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        assert isinstance(data["work_experiences"], list)
        assert isinstance(data["skills"], list)
        assert isinstance(data["education"], list)
        assert isinstance(data["tools"], list)
        assert isinstance(data["projects"], list)
        assert isinstance(data["certifications"], list)
        assert isinstance(data["additional_training"], list)
        assert isinstance(data["social_networks"], list)

    async def test_cv_lists_have_items(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        assert len(data["skills"]) > 0
        assert len(data["work_experiences"]) > 0
        assert len(data["tools"]) > 0

    async def test_cv_contact_info_has_email(self, client: AsyncClient):
        response = await client.get(PREFIX)
        contact = response.json()["contact_info"]
        assert "email" in contact

    async def test_cv_skills_have_correct_schema(self, client: AsyncClient):
        response = await client.get(PREFIX)
        skills = response.json()["skills"]
        skill = skills[0]
        assert "id" in skill
        assert "name" in skill
        assert "category" in skill


class TestDownloadCVPDF:
    async def test_download_returns_501(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/download")
        assert response.status_code == 501
