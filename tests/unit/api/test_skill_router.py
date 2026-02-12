"""Tests for the skill router endpoints."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

PREFIX = "/api/v1/skills"


class TestListSkills:
    async def test_list_skills_returns_list(self, client: AsyncClient):
        response = await client.get(PREFIX)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    async def test_list_skills_filter_by_category(self, client: AsyncClient):
        response = await client.get(PREFIX, params={"category": "backend"})
        assert response.status_code == 200
        data = response.json()
        assert all(s["category"] == "backend" for s in data)

    async def test_list_skills_filter_by_level(self, client: AsyncClient):
        response = await client.get(PREFIX, params={"level": "expert"})
        assert response.status_code == 200
        data = response.json()
        assert all(s["level"] == "expert" for s in data)

    async def test_list_skills_ordered_by_order_index(self, client: AsyncClient):
        response = await client.get(PREFIX)
        data = response.json()
        indices = [s["order_index"] for s in data]
        assert indices == sorted(indices)


class TestGetSkill:
    async def test_get_skill_by_id(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/skill_001")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "skill_001"
        assert data["name"] == "Python"

    async def test_get_skill_not_found(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/nonexistent")
        assert response.status_code == 404


class TestCreateSkill:
    async def test_create_skill_returns_201(self, client: AsyncClient):
        payload = {
            "name": "Go",
            "category": "backend",
            "order_index": 99,
            "level": "basic",
        }
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 201

    async def test_create_skill_validation_empty_body(self, client: AsyncClient):
        response = await client.post(PREFIX, json={})
        assert response.status_code == 422

    async def test_create_skill_validation_empty_name(self, client: AsyncClient):
        payload = {"name": "", "category": "backend", "order_index": 0}
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422

    async def test_create_skill_validation_negative_order(self, client: AsyncClient):
        payload = {"name": "Go", "category": "backend", "order_index": -1}
        response = await client.post(PREFIX, json=payload)
        assert response.status_code == 422


class TestUpdateSkill:
    async def test_update_skill_returns_200(self, client: AsyncClient):
        payload = {"name": "Updated Skill"}
        response = await client.put(f"{PREFIX}/skill_001", json=payload)
        assert response.status_code == 200

    async def test_update_skill_not_found(self, client: AsyncClient):
        payload = {"name": "Test"}
        response = await client.put(f"{PREFIX}/nonexistent", json=payload)
        assert response.status_code == 404


class TestDeleteSkill:
    async def test_delete_skill_returns_200(self, client: AsyncClient):
        response = await client.delete(f"{PREFIX}/skill_001")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestSkillGroupedEndpoints:
    async def test_grouped_by_category(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/grouped/by-category")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "backend" in data

    async def test_grouped_by_level(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/grouped/by-level")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "expert" in data


class TestSkillStats:
    async def test_stats_summary(self, client: AsyncClient):
        response = await client.get(f"{PREFIX}/stats/summary")
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "by_level" in data
        assert "by_category" in data
        assert data["total"] > 0
