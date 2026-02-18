"""Integration tests for WorkExperienceRepository against real MongoDB."""

from app.infrastructure.repositories import WorkExperienceRepository

from .conftest import PROFILE_ID, make_work_experience


class TestExperienceRepositoryCRUD:
    async def test_add_and_retrieve(self, experience_repo: WorkExperienceRepository):
        exp = make_work_experience()
        await experience_repo.add(exp)

        fetched = await experience_repo.get_by_id(exp.id)
        assert fetched is not None
        assert fetched.role == "Senior Developer"
        assert fetched.company == "Acme Corp"

    async def test_add_with_optional_fields(
        self, experience_repo: WorkExperienceRepository
    ):
        exp = make_work_experience(
            description="Led a team of 5 developers",
            responsibilities=["Code reviews", "Architecture design"],
        )
        await experience_repo.add(exp)

        fetched = await experience_repo.get_by_id(exp.id)
        assert fetched is not None
        assert fetched.description == "Led a team of 5 developers"
        assert fetched.responsibilities == ["Code reviews", "Architecture design"]

    async def test_update(self, experience_repo: WorkExperienceRepository):
        exp = make_work_experience()
        await experience_repo.add(exp)

        updated = make_work_experience(role="Lead Developer", company="TechCo")
        await experience_repo.update(updated)

        fetched = await experience_repo.get_by_id(exp.id)
        assert fetched is not None
        assert fetched.role == "Lead Developer"

    async def test_delete(self, experience_repo: WorkExperienceRepository):
        exp = make_work_experience()
        await experience_repo.add(exp)

        assert await experience_repo.delete(exp.id) is True
        assert await experience_repo.get_by_id(exp.id) is None

    async def test_delete_nonexistent(self, experience_repo: WorkExperienceRepository):
        assert await experience_repo.delete("nonexistent") is False

    async def test_list_all(self, experience_repo: WorkExperienceRepository):
        await experience_repo.add(make_work_experience(id="x1", order_index=0))
        await experience_repo.add(make_work_experience(id="x2", order_index=1))

        result = await experience_repo.list_all()
        assert len(result) == 2

    async def test_count(self, experience_repo: WorkExperienceRepository):
        assert await experience_repo.count() == 0
        await experience_repo.add(make_work_experience())
        assert await experience_repo.count() == 1

    async def test_exists(self, experience_repo: WorkExperienceRepository):
        exp = make_work_experience()
        await experience_repo.add(exp)

        assert await experience_repo.exists(exp.id) is True
        assert await experience_repo.exists("nonexistent") is False


class TestExperienceRepositoryOrdering:
    async def test_get_by_order_index(self, experience_repo: WorkExperienceRepository):
        await experience_repo.add(make_work_experience(id="x1", order_index=0))
        await experience_repo.add(make_work_experience(id="x2", order_index=1))

        result = await experience_repo.get_by_order_index(PROFILE_ID, 1)
        assert result is not None
        assert result.id == "x2"

    async def test_get_all_ordered(self, experience_repo: WorkExperienceRepository):
        await experience_repo.add(
            make_work_experience(id="x2", role="Lead", order_index=1)
        )
        await experience_repo.add(
            make_work_experience(id="x1", role="Junior", order_index=0)
        )

        result = await experience_repo.get_all_ordered(PROFILE_ID, ascending=True)
        assert result[0].role == "Junior"
        assert result[1].role == "Lead"

    async def test_reorder_move_down(self, experience_repo: WorkExperienceRepository):
        await experience_repo.add(
            make_work_experience(id="x0", role="A", order_index=0)
        )
        await experience_repo.add(
            make_work_experience(id="x1", role="B", order_index=1)
        )
        await experience_repo.add(
            make_work_experience(id="x2", role="C", order_index=2)
        )

        await experience_repo.reorder(PROFILE_ID, "x0", 2)

        result = await experience_repo.get_all_ordered(PROFILE_ID)
        assert result[0].role == "B"
        assert result[1].role == "C"
        assert result[2].role == "A"

    async def test_reorder_move_up(self, experience_repo: WorkExperienceRepository):
        await experience_repo.add(
            make_work_experience(id="x0", role="A", order_index=0)
        )
        await experience_repo.add(
            make_work_experience(id="x1", role="B", order_index=1)
        )
        await experience_repo.add(
            make_work_experience(id="x2", role="C", order_index=2)
        )

        await experience_repo.reorder(PROFILE_ID, "x2", 0)

        result = await experience_repo.get_all_ordered(PROFILE_ID)
        assert result[0].role == "C"
        assert result[1].role == "A"
        assert result[2].role == "B"
