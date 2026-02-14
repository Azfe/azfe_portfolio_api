"""Integration tests for SkillRepository against real MongoDB."""


from app.infrastructure.repositories import SkillRepository

from .conftest import PROFILE_ID, make_skill


class TestSkillRepositoryCRUD:
    async def test_add_and_retrieve(self, skill_repo: SkillRepository):
        skill = make_skill()
        await skill_repo.add(skill)

        fetched = await skill_repo.get_by_id(skill.id)
        assert fetched is not None
        assert fetched.name == "Python"
        assert fetched.category == "Backend"
        assert fetched.profile_id == PROFILE_ID

    async def test_add_with_optional_fields(self, skill_repo: SkillRepository):
        skill = make_skill(level="expert")
        await skill_repo.add(skill)

        fetched = await skill_repo.get_by_id(skill.id)
        assert fetched is not None
        assert fetched.level == "expert"

    async def test_update(self, skill_repo: SkillRepository):
        skill = make_skill()
        await skill_repo.add(skill)

        updated = make_skill(name="JavaScript", category="Frontend")
        await skill_repo.update(updated)

        fetched = await skill_repo.get_by_id(skill.id)
        assert fetched is not None
        assert fetched.name == "JavaScript"
        assert fetched.category == "Frontend"

    async def test_delete_existing(self, skill_repo: SkillRepository):
        skill = make_skill()
        await skill_repo.add(skill)

        assert await skill_repo.delete(skill.id) is True
        assert await skill_repo.get_by_id(skill.id) is None

    async def test_delete_nonexistent(self, skill_repo: SkillRepository):
        assert await skill_repo.delete("nonexistent") is False

    async def test_list_all(self, skill_repo: SkillRepository):
        await skill_repo.add(make_skill(id="s1", name="Python", order_index=0))
        await skill_repo.add(make_skill(id="s2", name="JavaScript", order_index=1))

        result = await skill_repo.list_all()
        assert len(result) == 2

    async def test_count(self, skill_repo: SkillRepository):
        assert await skill_repo.count() == 0
        await skill_repo.add(make_skill())
        assert await skill_repo.count() == 1

    async def test_exists(self, skill_repo: SkillRepository):
        skill = make_skill()
        await skill_repo.add(skill)

        assert await skill_repo.exists(skill.id) is True
        assert await skill_repo.exists("nonexistent") is False

    async def test_find_by(self, skill_repo: SkillRepository):
        await skill_repo.add(
            make_skill(id="s1", name="Python", category="Backend", order_index=0)
        )
        await skill_repo.add(
            make_skill(id="s2", name="React", category="Frontend", order_index=1)
        )

        result = await skill_repo.find_by(category="Frontend")
        assert len(result) == 1
        assert result[0].name == "React"


class TestSkillRepositoryUniqueName:
    async def test_exists_by_name_true(self, skill_repo: SkillRepository):
        await skill_repo.add(make_skill(name="Python"))

        assert await skill_repo.exists_by_name(PROFILE_ID, "Python") is True

    async def test_exists_by_name_false(self, skill_repo: SkillRepository):
        assert await skill_repo.exists_by_name(PROFILE_ID, "Python") is False

    async def test_exists_by_name_different_profile(self, skill_repo: SkillRepository):
        await skill_repo.add(make_skill(name="Python"))

        assert await skill_repo.exists_by_name("other-profile", "Python") is False

    async def test_get_by_name_found(self, skill_repo: SkillRepository):
        await skill_repo.add(make_skill(name="Python"))

        result = await skill_repo.get_by_name(PROFILE_ID, "Python")
        assert result is not None
        assert result.name == "Python"

    async def test_get_by_name_not_found(self, skill_repo: SkillRepository):
        result = await skill_repo.get_by_name(PROFILE_ID, "Nonexistent")
        assert result is None


class TestSkillRepositoryOrdering:
    async def test_get_by_order_index(self, skill_repo: SkillRepository):
        await skill_repo.add(make_skill(id="s1", name="Python", order_index=0))
        await skill_repo.add(make_skill(id="s2", name="JavaScript", order_index=1))

        result = await skill_repo.get_by_order_index(PROFILE_ID, 1)
        assert result is not None
        assert result.name == "JavaScript"

    async def test_get_by_order_index_not_found(self, skill_repo: SkillRepository):
        result = await skill_repo.get_by_order_index(PROFILE_ID, 99)
        assert result is None

    async def test_get_all_ordered_ascending(self, skill_repo: SkillRepository):
        await skill_repo.add(make_skill(id="s2", name="JavaScript", order_index=1))
        await skill_repo.add(make_skill(id="s1", name="Python", order_index=0))

        result = await skill_repo.get_all_ordered(PROFILE_ID, ascending=True)
        assert len(result) == 2
        assert result[0].name == "Python"
        assert result[1].name == "JavaScript"

    async def test_get_all_ordered_descending(self, skill_repo: SkillRepository):
        await skill_repo.add(make_skill(id="s1", name="Python", order_index=0))
        await skill_repo.add(make_skill(id="s2", name="JavaScript", order_index=1))

        result = await skill_repo.get_all_ordered(PROFILE_ID, ascending=False)
        assert result[0].name == "JavaScript"
        assert result[1].name == "Python"

    async def test_reorder_move_down(self, skill_repo: SkillRepository):
        """Move item from index 0 to index 2."""
        await skill_repo.add(make_skill(id="s0", name="A", order_index=0))
        await skill_repo.add(make_skill(id="s1", name="B", order_index=1))
        await skill_repo.add(make_skill(id="s2", name="C", order_index=2))

        await skill_repo.reorder(PROFILE_ID, "s0", 2)

        result = await skill_repo.get_all_ordered(PROFILE_ID)
        assert result[0].name == "B"
        assert result[1].name == "C"
        assert result[2].name == "A"

    async def test_reorder_move_up(self, skill_repo: SkillRepository):
        """Move item from index 2 to index 0."""
        await skill_repo.add(make_skill(id="s0", name="A", order_index=0))
        await skill_repo.add(make_skill(id="s1", name="B", order_index=1))
        await skill_repo.add(make_skill(id="s2", name="C", order_index=2))

        await skill_repo.reorder(PROFILE_ID, "s2", 0)

        result = await skill_repo.get_all_ordered(PROFILE_ID)
        assert result[0].name == "C"
        assert result[1].name == "A"
        assert result[2].name == "B"

    async def test_reorder_same_position(self, skill_repo: SkillRepository):
        """Reordering to same position changes nothing."""
        await skill_repo.add(make_skill(id="s0", name="A", order_index=0))
        await skill_repo.add(make_skill(id="s1", name="B", order_index=1))

        await skill_repo.reorder(PROFILE_ID, "s0", 0)

        result = await skill_repo.get_all_ordered(PROFILE_ID)
        assert result[0].name == "A"
        assert result[1].name == "B"

    async def test_reorder_nonexistent_entity(self, skill_repo: SkillRepository):
        """Reordering a nonexistent entity does nothing."""
        await skill_repo.add(make_skill(id="s0", name="A", order_index=0))

        await skill_repo.reorder(PROFILE_ID, "nonexistent", 0)

        result = await skill_repo.get_all_ordered(PROFILE_ID)
        assert len(result) == 1
        assert result[0].name == "A"
