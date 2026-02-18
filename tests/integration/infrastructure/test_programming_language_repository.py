"""Integration tests for ProgrammingLanguageRepository against real MongoDB."""

from app.infrastructure.repositories import ProgrammingLanguageRepository

from .conftest import PROFILE_ID, make_programming_language


class TestProgrammingLanguageRepositoryCRUD:
    async def test_add_and_retrieve(
        self, programming_language_repo: ProgrammingLanguageRepository
    ):
        plang = make_programming_language()
        await programming_language_repo.add(plang)

        fetched = await programming_language_repo.get_by_id(plang.id)
        assert fetched is not None
        assert fetched.name == "Python"

    async def test_add_with_level(
        self, programming_language_repo: ProgrammingLanguageRepository
    ):
        plang = make_programming_language(level="expert")
        await programming_language_repo.add(plang)

        fetched = await programming_language_repo.get_by_id(plang.id)
        assert fetched is not None
        assert fetched.level == "expert"

    async def test_update(
        self, programming_language_repo: ProgrammingLanguageRepository
    ):
        plang = make_programming_language()
        await programming_language_repo.add(plang)

        updated = make_programming_language(name="JavaScript", level="advanced")
        await programming_language_repo.update(updated)

        fetched = await programming_language_repo.get_by_id(plang.id)
        assert fetched is not None
        assert fetched.name == "JavaScript"

    async def test_delete(
        self, programming_language_repo: ProgrammingLanguageRepository
    ):
        plang = make_programming_language()
        await programming_language_repo.add(plang)

        assert await programming_language_repo.delete(plang.id) is True
        assert await programming_language_repo.get_by_id(plang.id) is None

    async def test_delete_nonexistent(
        self, programming_language_repo: ProgrammingLanguageRepository
    ):
        assert await programming_language_repo.delete("nonexistent") is False

    async def test_list_all(
        self, programming_language_repo: ProgrammingLanguageRepository
    ):
        await programming_language_repo.add(
            make_programming_language(id="pl1", name="Python", order_index=0)
        )
        await programming_language_repo.add(
            make_programming_language(id="pl2", name="JavaScript", order_index=1)
        )

        result = await programming_language_repo.list_all()
        assert len(result) == 2

    async def test_count(
        self, programming_language_repo: ProgrammingLanguageRepository
    ):
        assert await programming_language_repo.count() == 0
        await programming_language_repo.add(make_programming_language())
        assert await programming_language_repo.count() == 1

    async def test_exists(
        self, programming_language_repo: ProgrammingLanguageRepository
    ):
        plang = make_programming_language()
        await programming_language_repo.add(plang)

        assert await programming_language_repo.exists(plang.id) is True
        assert await programming_language_repo.exists("nonexistent") is False


class TestProgrammingLanguageRepositoryOrdering:
    async def test_get_by_order_index(
        self, programming_language_repo: ProgrammingLanguageRepository
    ):
        await programming_language_repo.add(
            make_programming_language(id="pl1", order_index=0)
        )
        await programming_language_repo.add(
            make_programming_language(id="pl2", order_index=1)
        )

        result = await programming_language_repo.get_by_order_index(PROFILE_ID, 1)
        assert result is not None
        assert result.id == "pl2"

    async def test_get_all_ordered(
        self, programming_language_repo: ProgrammingLanguageRepository
    ):
        await programming_language_repo.add(
            make_programming_language(id="pl2", name="JS", order_index=1)
        )
        await programming_language_repo.add(
            make_programming_language(id="pl1", name="Python", order_index=0)
        )

        result = await programming_language_repo.get_all_ordered(
            PROFILE_ID, ascending=True
        )
        assert result[0].name == "Python"
        assert result[1].name == "JS"

    async def test_reorder_move_down(
        self, programming_language_repo: ProgrammingLanguageRepository
    ):
        await programming_language_repo.add(
            make_programming_language(id="pl0", name="A", order_index=0)
        )
        await programming_language_repo.add(
            make_programming_language(id="pl1", name="B", order_index=1)
        )
        await programming_language_repo.add(
            make_programming_language(id="pl2", name="C", order_index=2)
        )

        await programming_language_repo.reorder(PROFILE_ID, "pl0", 2)

        result = await programming_language_repo.get_all_ordered(PROFILE_ID)
        assert result[0].name == "B"
        assert result[1].name == "C"
        assert result[2].name == "A"

    async def test_reorder_move_up(
        self, programming_language_repo: ProgrammingLanguageRepository
    ):
        await programming_language_repo.add(
            make_programming_language(id="pl0", name="A", order_index=0)
        )
        await programming_language_repo.add(
            make_programming_language(id="pl1", name="B", order_index=1)
        )
        await programming_language_repo.add(
            make_programming_language(id="pl2", name="C", order_index=2)
        )

        await programming_language_repo.reorder(PROFILE_ID, "pl2", 0)

        result = await programming_language_repo.get_all_ordered(PROFILE_ID)
        assert result[0].name == "C"
        assert result[1].name == "A"
        assert result[2].name == "B"
