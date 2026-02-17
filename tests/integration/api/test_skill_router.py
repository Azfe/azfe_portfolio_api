"""Integration tests for the skill router endpoints."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.integration

PREFIX = "/api/v1/skills"


class TestListSkills:
    async def test_list_skills_returns_200(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200

    async def test_list_skills_returns_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    async def test_skill_response_schema(self, client: AsyncClient):
        response = await client.get(PREFIX)
        skill = response.json()[0]
        assert "id" in skill
        assert "name" in skill
        assert "category" in skill
        assert "order_index" in skill
        assert "created_at" in skill

    async def test_skills_sorted_by_order_index(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        indices = [s["order_index"] for s in data]
        assert indices == sorted(indices)

    async def test_filter_skills_by_category(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}?category=backend")
        assert response.status_code == 200
        data = response.json()
        assert all(s["category"] == "backend" for s in data)

    async def test_filter_skills_by_level(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}?level=expert")
        assert response.status_code == 200
        data = response.json()
        assert all(s["level"] == "expert" for s in data)

    async def test_filter_skills_by_category_and_level(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}?category=backend&level=expert")
        assert response.status_code == 200
        data = response.json()
        assert all(s["category"] == "backend" and s["level"] == "expert" for s in data)

    async def test_filter_nonexistent_category_returns_empty(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}?category=nonexistent")
        assert response.status_code == 200
        data = response.json()
        assert data == []


class TestGetSkill:
    async def test_get_skill_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/skill_001")
        assert response.status_code == 200

    async def test_get_skill_response_schema(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/skill_001")
        data = response.json()
        assert data["id"] == "skill_001"
        assert "name" in data
        assert "category" in data

    async def test_get_nonexistent_skill_returns_404(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/nonexistent")
        assert response.status_code == 404


class TestCreateSkill:
    async def test_create_skill_returns_201(self, client: AsyncClient):
        payload = {
            "name": "Go",
            "category": "backend",
            "level": "basic",
            "order_index": 99,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_skill_validation_error_missing_name(self, client: AsyncClient):
        payload = {
            "category": "backend",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_create_skill_validation_error_empty_name(self, client: AsyncClient):
        payload = {
            "name": "",
            "category": "backend",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_create_skill_validation_error_negative_order(self, client: AsyncClient):
        payload = {
            "name": "Go",
            "category": "backend",
            "order_index": -1,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_create_skill_validation_error_invalid_level(self, client: AsyncClient):
        payload = {
            "name": "Go",
            "category": "backend",
            "level": "master",
            "order_index": 0,
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422


class TestUpdateSkill:
    async def test_update_skill_returns_200(self, client: AsyncClient):
        payload = {"name": "Updated Skill"}
        response = await client.put(f"{PREFIX}/skill_001", json=payload)
        assert response.status_code == 200

    async def test_update_nonexistent_skill_returns_404(self, client: AsyncClient):
        payload = {"name": "Updated"}
        response = await client.put(f"{PREFIX}/nonexistent", json=payload)
        assert response.status_code == 404


class TestDeleteSkill:
    async def test_delete_skill_returns_200(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/skill_001")
        assert response.status_code == 200

    async def test_delete_skill_response_format(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/skill_001")
        data = response.json()
        assert data["success"] is True
        assert "message" in data


class TestReorderSkills:
    async def test_reorder_skills_returns_200(self, client: AsyncClient):
        payload = [
            {"id": "skill_001", "orderIndex": 1},
            {"id": "skill_002", "orderIndex": 0},
        ]
        response = await client.patch(f"{PREFIX}/reorder", json=payload)
        assert response.status_code == 200

    async def test_reorder_skills_returns_list(self, client: AsyncClient):
        payload = [{"id": "skill_001", "orderIndex": 0}]
        response = await client.patch(f"{PREFIX}/reorder", json=payload)
        data = response.json()
        assert isinstance(data, list)


class TestSkillsGroupedByCategory:
    async def test_grouped_by_category_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/grouped/by-category")
        assert response.status_code == 200

    async def test_grouped_by_category_is_dict(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/grouped/by-category")
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0

    async def test_grouped_by_category_has_backend(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/grouped/by-category")
        data = response.json()
        assert "backend" in data
        assert isinstance(data["backend"], list)


class TestSkillsGroupedByLevel:
    async def test_grouped_by_level_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/grouped/by-level")
        assert response.status_code == 200

    async def test_grouped_by_level_is_dict(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/grouped/by-level")
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0


class TestSkillsStats:
    async def test_stats_returns_200(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/stats/summary")
        assert response.status_code == 200

    async def test_stats_response_schema(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/stats/summary")
        data = response.json()
        assert "total" in data
        assert "by_level" in data
        assert "by_category" in data
        assert isinstance(data["total"], int)
        assert data["total"] > 0
