"""Tests for Skill use cases."""

from unittest.mock import AsyncMock

import pytest

from app.application.dto import (
    AddSkillRequest,
    DeleteSkillRequest,
    EditSkillRequest,
    ListSkillsRequest,
)
from app.application.use_cases.skill.add_skill import AddSkillUseCase
from app.application.use_cases.skill.delete_skill import DeleteSkillUseCase
from app.application.use_cases.skill.edit_skill import EditSkillUseCase
from app.application.use_cases.skill.list_skills import ListSkillsUseCase
from app.domain.entities.skill import Skill
from app.shared.shared_exceptions import DuplicateException, NotFoundException

pytestmark = pytest.mark.asyncio

PROFILE_ID = "profile-001"


def _make_skill(**overrides):
    defaults = {
        "profile_id": PROFILE_ID,
        "name": "Python",
        "order_index": 0,
        "level": "expert",
    }
    defaults.update(overrides)
    return Skill.create(**defaults)


class TestAddSkillUseCase:
    async def test_add_skill_success(self):
        repo = AsyncMock()
        skill = _make_skill()
        repo.exists_by_name.return_value = False
        repo.add.return_value = skill

        uc = AddSkillUseCase(repo)
        request = AddSkillRequest(
            profile_id=PROFILE_ID,
            name="Python",
            order_index=0,
            level="expert",
        )
        result = await uc.execute(request)

        assert result.name == "Python"
        repo.exists_by_name.assert_awaited_once_with(PROFILE_ID, "Python")
        repo.add.assert_awaited_once()

    async def test_add_skill_duplicate_name_raises(self):
        repo = AsyncMock()
        repo.exists_by_name.return_value = True

        uc = AddSkillUseCase(repo)
        request = AddSkillRequest(
            profile_id=PROFILE_ID,
            name="Python",
            order_index=0,
        )
        with pytest.raises(DuplicateException):
            await uc.execute(request)

        repo.add.assert_not_awaited()


class TestDeleteSkillUseCase:
    async def test_delete_skill_success(self):
        repo = AsyncMock()
        repo.delete.return_value = True

        uc = DeleteSkillUseCase(repo)
        result = await uc.execute(DeleteSkillRequest(skill_id="skill-001"))

        assert result.success is True
        repo.delete.assert_awaited_once_with("skill-001")

    async def test_delete_skill_not_found_raises(self):
        repo = AsyncMock()
        repo.delete.return_value = False

        uc = DeleteSkillUseCase(repo)
        with pytest.raises(NotFoundException):
            await uc.execute(DeleteSkillRequest(skill_id="nonexistent"))


class TestEditSkillUseCase:
    async def test_edit_skill_success(self):
        repo = AsyncMock()
        skill = _make_skill()
        repo.get_by_id.return_value = skill
        repo.exists_by_name.return_value = False
        repo.update.return_value = skill

        uc = EditSkillUseCase(repo)
        request = EditSkillRequest(skill_id="skill-001", name="Go")
        result = await uc.execute(request)

        assert result.name == "Go"
        repo.get_by_id.assert_awaited_once_with("skill-001")
        repo.update.assert_awaited_once()

    async def test_edit_skill_not_found_raises(self):
        repo = AsyncMock()
        repo.get_by_id.return_value = None

        uc = EditSkillUseCase(repo)
        request = EditSkillRequest(skill_id="nonexistent", name="Go")
        with pytest.raises(NotFoundException):
            await uc.execute(request)

    async def test_edit_skill_duplicate_name_raises(self):
        repo = AsyncMock()
        skill = _make_skill()
        repo.get_by_id.return_value = skill
        repo.exists_by_name.return_value = True

        uc = EditSkillUseCase(repo)
        request = EditSkillRequest(skill_id="skill-001", name="Go")
        with pytest.raises(DuplicateException):
            await uc.execute(request)

    async def test_edit_skill_same_name_no_duplicate_check(self):
        repo = AsyncMock()
        skill = _make_skill()
        repo.get_by_id.return_value = skill
        repo.update.return_value = skill

        uc = EditSkillUseCase(repo)
        request = EditSkillRequest(skill_id="skill-001", name="Python")
        await uc.execute(request)

        repo.exists_by_name.assert_not_awaited()

    @pytest.mark.unit
    async def test_edit_skill_with_order_index_calls_update_order(self):
        """When order_index is provided it must be propagated via update_order."""
        repo = AsyncMock()
        skill = _make_skill(order_index=0)
        repo.get_by_id.return_value = skill
        repo.exists_by_name.return_value = False
        repo.update.return_value = skill

        uc = EditSkillUseCase(repo)
        request = EditSkillRequest(skill_id="skill-001", order_index=5)
        await uc.execute(request)

        assert skill.order_index == 5
        repo.update.assert_awaited_once()

    @pytest.mark.unit
    async def test_edit_skill_without_order_index_does_not_change_order(self):
        """When order_index is None, update_order must NOT be called."""
        repo = AsyncMock()
        skill = _make_skill(order_index=3)
        repo.get_by_id.return_value = skill
        repo.exists_by_name.return_value = False
        repo.update.return_value = skill

        uc = EditSkillUseCase(repo)
        request = EditSkillRequest(skill_id="skill-001", name="Rust", order_index=None)
        await uc.execute(request)

        # order_index must remain unchanged
        assert skill.order_index == 3
        repo.update.assert_awaited_once()

    @pytest.mark.unit
    async def test_edit_skill_combined_name_level_order_index(self):
        """Updating name, level and order_index together must apply all changes."""
        repo = AsyncMock()
        skill = _make_skill(name="Python", level="basic", order_index=0)
        repo.get_by_id.return_value = skill
        repo.exists_by_name.return_value = False
        repo.update.return_value = skill

        uc = EditSkillUseCase(repo)
        request = EditSkillRequest(
            skill_id="skill-001",
            name="Rust",
            level="expert",
            order_index=10,
        )
        result = await uc.execute(request)

        assert skill.name == "Rust"
        assert skill.level == "expert"
        assert skill.order_index == 10
        repo.update.assert_awaited_once()
        assert result.name == "Rust"


class TestListSkillsUseCase:
    async def test_list_skills_all(self):
        repo = AsyncMock()
        skills = [_make_skill(order_index=0), _make_skill(name="Go", order_index=1)]
        repo.find_by.return_value = skills

        uc = ListSkillsUseCase(repo)
        request = ListSkillsRequest(profile_id=PROFILE_ID)
        result = await uc.execute(request)

        assert result.total == 2
        assert len(result.skills) == 2
        repo.find_by.assert_awaited_once_with(profile_id=PROFILE_ID)

    async def test_list_skills_empty(self):
        repo = AsyncMock()
        repo.find_by.return_value = []

        uc = ListSkillsUseCase(repo)
        request = ListSkillsRequest(profile_id=PROFILE_ID)
        result = await uc.execute(request)

        assert result.total == 0
        assert result.skills == []
