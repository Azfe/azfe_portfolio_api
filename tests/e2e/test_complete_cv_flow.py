"""
E2E tests for the complete CV flow.

These tests exercise the full stack (API → Use Cases → Repositories → MongoDB)
without any mocks or dependency overrides. They require a running MongoDB instance.

Test flow:
    1. Create resources via POST endpoints
    2. Read back via GET endpoints and validate
    3. Aggregate via GET /cv and validate
    4. Update and delete resources, verify consistency
"""

from httpx import AsyncClient
import pytest

pytestmark = pytest.mark.e2e

PREFIX = "/api/v1"

# =====================================================================
# TEST DATA
# =====================================================================

PROFILE_DATA = {"name": "Alex Zapata", "headline": "Full Stack Developer"}

SKILL_PYTHON = {
    "name": "Python",
    "category": "backend",
    "order_index": 0,
    "level": "expert",
}

SKILL_REACT = {
    "name": "React",
    "category": "frontend",
    "order_index": 1,
    "level": "advanced",
}

EDUCATION_DATA = {
    "institution": "Universidad Complutense",
    "degree": "BSc Computer Science",
    "field": "Computer Science",
    "start_date": "2018-09-01T00:00:00",
    "order_index": 0,
}

EXPERIENCE_DATA = {
    "role": "Senior Developer",
    "company": "Tech Corp",
    "start_date": "2022-01-01T00:00:00",
    "order_index": 0,
}

CERTIFICATION_DATA = {
    "title": "AWS Solutions Architect",
    "issuer": "Amazon",
    "issue_date": "2024-01-15T00:00:00",
    "order_index": 0,
}

TRAINING_DATA = {
    "title": "Docker Mastery",
    "provider": "Udemy",
    "completion_date": "2024-01-15T00:00:00",
    "order_index": 0,
}

TOOL_DATA = {"name": "VS Code", "category": "ide", "order_index": 0}

SOCIAL_DATA = {
    "platform": "github",
    "url": "https://github.com/alexzapata",
    "order_index": 0,
}

CONTACT_INFO_DATA = {"email": "alex@example.com"}


# =====================================================================
# HELPER
# =====================================================================


async def _create_profile(client: AsyncClient) -> dict:
    """Create profile and return response data."""
    resp = await client.post(f"{PREFIX}/profile", json=PROFILE_DATA)
    assert resp.status_code == 201, f"Profile creation failed: {resp.text}"
    return resp.json()


# =====================================================================
# TEST CLASSES
# =====================================================================


class TestCVCreationFlow:
    """Test the core CV creation flow: profile → skills → education → experience → CV."""

    async def test_full_cv_creation_and_aggregation(self, client: AsyncClient):
        """Create all CV resources and verify they aggregate correctly."""
        # 1. Create profile
        profile = await _create_profile(client)
        assert profile["name"] == "Alex Zapata"
        assert "id" in profile

        # 2. Create skills
        resp = await client.post(f"{PREFIX}/skills", json=SKILL_PYTHON)
        assert resp.status_code == 201
        skill_python = resp.json()
        assert skill_python["name"] == "Python"

        resp = await client.post(f"{PREFIX}/skills", json=SKILL_REACT)
        assert resp.status_code == 201
        skill_react = resp.json()
        assert skill_react["name"] == "React"

        # 3. Create education
        resp = await client.post(f"{PREFIX}/education", json=EDUCATION_DATA)
        assert resp.status_code == 201
        education = resp.json()
        assert education["institution"] == "Universidad Complutense"

        # 4. Create work experience
        resp = await client.post(f"{PREFIX}/work-experiences", json=EXPERIENCE_DATA)
        assert resp.status_code == 201
        experience = resp.json()
        assert experience["role"] == "Senior Developer"

        # 5. Get complete CV
        resp = await client.get(f"{PREFIX}/cv")
        assert resp.status_code == 200
        cv = resp.json()

        # Verify profile is present
        assert cv["profile"]["name"] == "Alex Zapata"

        # Verify skills are present and ordered
        assert len(cv["skills"]) == 2
        assert cv["skills"][0]["name"] == "Python"
        assert cv["skills"][0]["order_index"] <= cv["skills"][1]["order_index"]

        # Verify education is present
        assert len(cv["education"]) >= 1

        # Verify fields NOT aggregated by GetCompleteCVUseCase are empty/null
        assert cv["contact_info"] is None
        assert cv["tools"] == []
        assert cv["certifications"] == []
        assert cv["additional_training"] == []
        assert cv["social_networks"] == []


class TestCVWithAllResources:
    """Test creating ALL resource types and verifying via CV and individual endpoints."""

    async def test_create_all_resources_and_verify(self, client: AsyncClient):
        """Create every resource type and verify they exist."""
        # Profile (required first)
        await _create_profile(client)

        # Skills
        resp = await client.post(f"{PREFIX}/skills", json=SKILL_PYTHON)
        assert resp.status_code == 201

        # Education
        resp = await client.post(f"{PREFIX}/education", json=EDUCATION_DATA)
        assert resp.status_code == 201

        # Work experience
        resp = await client.post(f"{PREFIX}/work-experiences", json=EXPERIENCE_DATA)
        assert resp.status_code == 201

        # Certifications
        resp = await client.post(f"{PREFIX}/certifications", json=CERTIFICATION_DATA)
        assert resp.status_code == 201

        # Additional training
        resp = await client.post(f"{PREFIX}/additional-training", json=TRAINING_DATA)
        assert resp.status_code == 201

        # Tools
        resp = await client.post(f"{PREFIX}/tools", json=TOOL_DATA)
        assert resp.status_code == 201

        # Social networks
        resp = await client.post(f"{PREFIX}/social-networks", json=SOCIAL_DATA)
        assert resp.status_code == 201

        # Contact information
        resp = await client.post(
            f"{PREFIX}/contact-information", json=CONTACT_INFO_DATA
        )
        assert resp.status_code == 201

        # --- Verify CV aggregation ---
        resp = await client.get(f"{PREFIX}/cv")
        assert resp.status_code == 200
        cv = resp.json()

        assert cv["profile"]["name"] == "Alex Zapata"
        assert len(cv["skills"]) >= 1
        assert len(cv["education"]) >= 1

        # --- Verify individual endpoints return the created resources ---
        resp = await client.get(f"{PREFIX}/skills")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

        resp = await client.get(f"{PREFIX}/certifications")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

        resp = await client.get(f"{PREFIX}/tools")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

        resp = await client.get(f"{PREFIX}/social-networks")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

        resp = await client.get(f"{PREFIX}/additional-training")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

        resp = await client.get(f"{PREFIX}/contact-information")
        assert resp.status_code == 200
        assert "email" in resp.json()


class TestCVEmptyProfile:
    """Test CV with only a profile and no other resources."""

    async def test_cv_with_empty_lists(self, client: AsyncClient):
        """A profile with no skills/education/etc should return empty lists."""
        await _create_profile(client)

        resp = await client.get(f"{PREFIX}/cv")
        assert resp.status_code == 200
        cv = resp.json()

        assert cv["profile"]["name"] == "Alex Zapata"
        assert cv["skills"] == []
        assert cv["education"] == []
        assert cv["contact_info"] is None
        assert cv["tools"] == []


class TestCVDownloadPDF:
    """Test the CV PDF download endpoint."""

    async def test_download_returns_501(self, client: AsyncClient):
        """PDF generation is not yet implemented — should return 501."""
        await _create_profile(client)

        resp = await client.get(f"{PREFIX}/cv/download")
        assert resp.status_code == 501


class TestResourceCRUDFlow:
    """Test full CRUD lifecycle of a resource (skills) through the real stack."""

    async def test_skill_crud_lifecycle(self, client: AsyncClient):
        """Create → Read → Update → Delete a skill, verify at each step."""
        await _create_profile(client)

        # CREATE
        resp = await client.post(f"{PREFIX}/skills", json=SKILL_PYTHON)
        assert resp.status_code == 201
        skill = resp.json()
        skill_id = skill["id"]
        assert skill["name"] == "Python"
        assert skill["category"] == "backend"
        assert "created_at" in skill

        # READ (list)
        resp = await client.get(f"{PREFIX}/skills")
        assert resp.status_code == 200
        skills = resp.json()
        assert any(s["id"] == skill_id for s in skills)

        # READ (by ID)
        resp = await client.get(f"{PREFIX}/skills/{skill_id}")
        assert resp.status_code == 200
        assert resp.json()["id"] == skill_id
        assert resp.json()["name"] == "Python"

        # UPDATE
        resp = await client.put(
            f"{PREFIX}/skills/{skill_id}",
            json={"name": "Python 3.13", "category": "backend"},
        )
        assert resp.status_code == 200

        # Verify update persisted
        resp = await client.get(f"{PREFIX}/skills/{skill_id}")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Python 3.13"

        # DELETE
        resp = await client.delete(f"{PREFIX}/skills/{skill_id}")
        assert resp.status_code == 200
        delete_data = resp.json()
        assert delete_data["success"] is True

        # Verify deleted (404)
        resp = await client.get(f"{PREFIX}/skills/{skill_id}")
        assert resp.status_code == 404


class TestBusinessRuleValidation:
    """Test that business rules and validation are enforced through the full stack."""

    async def test_create_skill_negative_order_index(self, client: AsyncClient):
        """Negative order_index should return 422."""
        resp = await client.post(
            f"{PREFIX}/skills",
            json={"name": "Test", "category": "backend", "order_index": -1},
        )
        assert resp.status_code == 422

    async def test_create_skill_empty_name(self, client: AsyncClient):
        """Empty name should return 422."""
        resp = await client.post(
            f"{PREFIX}/skills",
            json={"name": "", "category": "backend", "order_index": 0},
        )
        assert resp.status_code == 422

    async def test_get_nonexistent_skill(self, client: AsyncClient):
        """Getting a non-existent skill should return 404."""
        resp = await client.get(f"{PREFIX}/skills/nonexistent-id-12345")
        assert resp.status_code == 404

    async def test_error_response_format(self, client: AsyncClient):
        """Error responses should follow the standard format."""
        resp = await client.post(f"{PREFIX}/skills", json={})
        assert resp.status_code == 422
        data = resp.json()
        assert data["success"] is False
        assert "error" in data
        assert "message" in data
        assert "code" in data

    async def test_cv_without_profile_returns_404(self, client: AsyncClient):
        """Getting CV without creating a profile first should return 404."""
        resp = await client.get(f"{PREFIX}/cv")
        assert resp.status_code == 404


class TestDataConsistency:
    """Test that data remains consistent across create/delete operations."""

    async def test_deleted_skill_disappears_from_cv(self, client: AsyncClient):
        """A deleted skill should no longer appear in the CV."""
        await _create_profile(client)

        # Create 2 skills
        resp = await client.post(f"{PREFIX}/skills", json=SKILL_PYTHON)
        assert resp.status_code == 201
        skill_id = resp.json()["id"]

        resp = await client.post(f"{PREFIX}/skills", json=SKILL_REACT)
        assert resp.status_code == 201

        # Verify CV has 2 skills
        resp = await client.get(f"{PREFIX}/cv")
        assert len(resp.json()["skills"]) == 2

        # Delete one skill
        resp = await client.delete(f"{PREFIX}/skills/{skill_id}")
        assert resp.status_code == 200

        # Verify CV now has 1 skill
        resp = await client.get(f"{PREFIX}/cv")
        assert len(resp.json()["skills"]) == 1

        # Verify skills list also has 1 skill
        resp = await client.get(f"{PREFIX}/skills")
        assert len(resp.json()) == 1

    async def test_multiple_resources_accumulate(self, client: AsyncClient):
        """Creating multiple resources should all appear in their respective lists."""
        await _create_profile(client)

        # Create 3 skills
        for skill in [
            {"name": "Python", "category": "backend", "order_index": 0},
            {"name": "React", "category": "frontend", "order_index": 1},
            {"name": "PostgreSQL", "category": "database", "order_index": 2},
        ]:
            resp = await client.post(f"{PREFIX}/skills", json=skill)
            assert resp.status_code == 201

        # Verify all 3 are in the list
        resp = await client.get(f"{PREFIX}/skills")
        assert resp.status_code == 200
        assert len(resp.json()) == 3

        # Verify all 3 are in the CV
        resp = await client.get(f"{PREFIX}/cv")
        assert len(resp.json()["skills"]) == 3
