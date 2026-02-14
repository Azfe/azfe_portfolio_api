"""Integration tests for EducationRepository against real MongoDB."""

from app.infrastructure.repositories import EducationRepository

from .conftest import PROFILE_ID, make_education


class TestEducationRepositoryCRUD:
    async def test_add_and_retrieve(self, education_repo: EducationRepository):
        edu = make_education()
        await education_repo.add(edu)

        fetched = await education_repo.get_by_id(edu.id)
        assert fetched is not None
        assert fetched.institution == "MIT"
        assert fetched.degree == "BSc"
        assert fetched.field == "Computer Science"

    async def test_add_with_optional_fields(self, education_repo: EducationRepository):
        edu = make_education(
            description="Study of algorithms and data structures",
            end_date=None,
        )
        await education_repo.add(edu)

        fetched = await education_repo.get_by_id(edu.id)
        assert fetched is not None
        assert fetched.description == "Study of algorithms and data structures"

    async def test_update(self, education_repo: EducationRepository):
        edu = make_education()
        await education_repo.add(edu)

        updated = make_education(institution="Stanford", degree="MSc")
        await education_repo.update(updated)

        fetched = await education_repo.get_by_id(edu.id)
        assert fetched is not None
        assert fetched.institution == "Stanford"

    async def test_delete_existing(self, education_repo: EducationRepository):
        edu = make_education()
        await education_repo.add(edu)

        assert await education_repo.delete(edu.id) is True
        assert await education_repo.get_by_id(edu.id) is None

    async def test_delete_nonexistent(self, education_repo: EducationRepository):
        assert await education_repo.delete("nonexistent") is False

    async def test_list_all(self, education_repo: EducationRepository):
        await education_repo.add(make_education(id="e1", order_index=0))
        await education_repo.add(make_education(id="e2", order_index=1))

        result = await education_repo.list_all()
        assert len(result) == 2

    async def test_count(self, education_repo: EducationRepository):
        assert await education_repo.count() == 0
        await education_repo.add(make_education())
        assert await education_repo.count() == 1

    async def test_exists(self, education_repo: EducationRepository):
        edu = make_education()
        await education_repo.add(edu)

        assert await education_repo.exists(edu.id) is True
        assert await education_repo.exists("nonexistent") is False

    async def test_find_by(self, education_repo: EducationRepository):
        await education_repo.add(
            make_education(id="e1", institution="MIT", order_index=0)
        )
        await education_repo.add(
            make_education(id="e2", institution="Stanford", order_index=1)
        )

        result = await education_repo.find_by(institution="Stanford")
        assert len(result) == 1
        assert result[0].institution == "Stanford"


class TestEducationRepositoryOrdering:
    async def test_get_by_order_index(self, education_repo: EducationRepository):
        await education_repo.add(make_education(id="e1", order_index=0))
        await education_repo.add(make_education(id="e2", order_index=1))

        result = await education_repo.get_by_order_index(PROFILE_ID, 1)
        assert result is not None
        assert result.id == "e2"

    async def test_get_by_order_index_not_found(
        self, education_repo: EducationRepository
    ):
        result = await education_repo.get_by_order_index(PROFILE_ID, 99)
        assert result is None

    async def test_get_all_ordered_ascending(self, education_repo: EducationRepository):
        await education_repo.add(
            make_education(id="e2", institution="Stanford", order_index=1)
        )
        await education_repo.add(
            make_education(id="e1", institution="MIT", order_index=0)
        )

        result = await education_repo.get_all_ordered(PROFILE_ID, ascending=True)
        assert result[0].institution == "MIT"
        assert result[1].institution == "Stanford"

    async def test_get_all_ordered_descending(
        self, education_repo: EducationRepository
    ):
        await education_repo.add(
            make_education(id="e1", institution="MIT", order_index=0)
        )
        await education_repo.add(
            make_education(id="e2", institution="Stanford", order_index=1)
        )

        result = await education_repo.get_all_ordered(PROFILE_ID, ascending=False)
        assert result[0].institution == "Stanford"
        assert result[1].institution == "MIT"

    async def test_reorder_move_down(self, education_repo: EducationRepository):
        await education_repo.add(
            make_education(id="e0", institution="A", order_index=0)
        )
        await education_repo.add(
            make_education(id="e1", institution="B", order_index=1)
        )
        await education_repo.add(
            make_education(id="e2", institution="C", order_index=2)
        )

        await education_repo.reorder(PROFILE_ID, "e0", 2)

        result = await education_repo.get_all_ordered(PROFILE_ID)
        assert result[0].institution == "B"
        assert result[1].institution == "C"
        assert result[2].institution == "A"

    async def test_reorder_move_up(self, education_repo: EducationRepository):
        await education_repo.add(
            make_education(id="e0", institution="A", order_index=0)
        )
        await education_repo.add(
            make_education(id="e1", institution="B", order_index=1)
        )
        await education_repo.add(
            make_education(id="e2", institution="C", order_index=2)
        )

        await education_repo.reorder(PROFILE_ID, "e2", 0)

        result = await education_repo.get_all_ordered(PROFILE_ID)
        assert result[0].institution == "C"
        assert result[1].institution == "A"
        assert result[2].institution == "B"
