"""Integration tests for LanguageRepository against real MongoDB."""

from app.infrastructure.repositories import LanguageRepository

from .conftest import PROFILE_ID, make_language


class TestLanguageRepositoryCRUD:
    async def test_add_and_retrieve(self, language_repo: LanguageRepository):
        lang = make_language()
        await language_repo.add(lang)

        fetched = await language_repo.get_by_id(lang.id)
        assert fetched is not None
        assert fetched.name == "English"

    async def test_add_with_proficiency(self, language_repo: LanguageRepository):
        lang = make_language(proficiency="c2")
        await language_repo.add(lang)

        fetched = await language_repo.get_by_id(lang.id)
        assert fetched is not None
        assert fetched.proficiency == "c2"

    async def test_update(self, language_repo: LanguageRepository):
        lang = make_language()
        await language_repo.add(lang)

        updated = make_language(name="Spanish", proficiency="b2")
        await language_repo.update(updated)

        fetched = await language_repo.get_by_id(lang.id)
        assert fetched is not None
        assert fetched.name == "Spanish"

    async def test_delete(self, language_repo: LanguageRepository):
        lang = make_language()
        await language_repo.add(lang)

        assert await language_repo.delete(lang.id) is True
        assert await language_repo.get_by_id(lang.id) is None

    async def test_delete_nonexistent(self, language_repo: LanguageRepository):
        assert await language_repo.delete("nonexistent") is False

    async def test_list_all(self, language_repo: LanguageRepository):
        await language_repo.add(make_language(id="l1", name="English", order_index=0))
        await language_repo.add(make_language(id="l2", name="Spanish", order_index=1))

        result = await language_repo.list_all()
        assert len(result) == 2

    async def test_count(self, language_repo: LanguageRepository):
        assert await language_repo.count() == 0
        await language_repo.add(make_language())
        assert await language_repo.count() == 1

    async def test_exists(self, language_repo: LanguageRepository):
        lang = make_language()
        await language_repo.add(lang)

        assert await language_repo.exists(lang.id) is True
        assert await language_repo.exists("nonexistent") is False


class TestLanguageRepositoryOrdering:
    async def test_get_by_order_index(self, language_repo: LanguageRepository):
        await language_repo.add(make_language(id="l1", order_index=0))
        await language_repo.add(make_language(id="l2", order_index=1))

        result = await language_repo.get_by_order_index(PROFILE_ID, 1)
        assert result is not None
        assert result.id == "l2"

    async def test_get_all_ordered(self, language_repo: LanguageRepository):
        await language_repo.add(make_language(id="l2", name="Spanish", order_index=1))
        await language_repo.add(make_language(id="l1", name="English", order_index=0))

        result = await language_repo.get_all_ordered(PROFILE_ID, ascending=True)
        assert result[0].name == "English"
        assert result[1].name == "Spanish"

    async def test_reorder_move_down(self, language_repo: LanguageRepository):
        await language_repo.add(make_language(id="l0", name="A", order_index=0))
        await language_repo.add(make_language(id="l1", name="B", order_index=1))
        await language_repo.add(make_language(id="l2", name="C", order_index=2))

        await language_repo.reorder(PROFILE_ID, "l0", 2)

        result = await language_repo.get_all_ordered(PROFILE_ID)
        assert result[0].name == "B"
        assert result[1].name == "C"
        assert result[2].name == "A"

    async def test_reorder_move_up(self, language_repo: LanguageRepository):
        await language_repo.add(make_language(id="l0", name="A", order_index=0))
        await language_repo.add(make_language(id="l1", name="B", order_index=1))
        await language_repo.add(make_language(id="l2", name="C", order_index=2))

        await language_repo.reorder(PROFILE_ID, "l2", 0)

        result = await language_repo.get_all_ordered(PROFILE_ID)
        assert result[0].name == "C"
        assert result[1].name == "A"
        assert result[2].name == "B"
