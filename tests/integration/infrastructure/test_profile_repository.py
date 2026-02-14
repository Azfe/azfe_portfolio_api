"""Integration tests for ProfileRepository against real MongoDB."""

from app.infrastructure.repositories import ProfileRepository

from .conftest import make_profile


class TestProfileRepositoryAdd:
    async def test_add_and_retrieve(self, profile_repo: ProfileRepository):
        profile = make_profile()
        result = await profile_repo.add(profile)

        assert result.id == profile.id
        assert result.name == "John Doe"

        fetched = await profile_repo.get_by_id(profile.id)
        assert fetched is not None
        assert fetched.name == "John Doe"
        assert fetched.headline == "Software Developer"

    async def test_add_with_optional_fields(self, profile_repo: ProfileRepository):
        profile = make_profile(
            bio="A passionate developer",
            location="Madrid",
            avatar_url="https://example.com/avatar.jpg",
        )
        await profile_repo.add(profile)

        fetched = await profile_repo.get_by_id(profile.id)
        assert fetched is not None
        assert fetched.bio == "A passionate developer"
        assert fetched.location == "Madrid"
        assert fetched.avatar_url == "https://example.com/avatar.jpg"


class TestProfileRepositoryUpdate:
    async def test_update_existing(self, profile_repo: ProfileRepository):
        profile = make_profile()
        await profile_repo.add(profile)

        updated = make_profile(name="Jane Doe", headline="Lead Developer")
        result = await profile_repo.update(updated)
        assert result.name == "Jane Doe"

        fetched = await profile_repo.get_by_id(profile.id)
        assert fetched is not None
        assert fetched.name == "Jane Doe"
        assert fetched.headline == "Lead Developer"


class TestProfileRepositoryDelete:
    async def test_delete_existing(self, profile_repo: ProfileRepository):
        profile = make_profile()
        await profile_repo.add(profile)

        deleted = await profile_repo.delete(profile.id)
        assert deleted is True

        fetched = await profile_repo.get_by_id(profile.id)
        assert fetched is None

    async def test_delete_nonexistent(self, profile_repo: ProfileRepository):
        deleted = await profile_repo.delete("nonexistent-id")
        assert deleted is False


class TestProfileRepositoryQueries:
    async def test_get_by_id_not_found(self, profile_repo: ProfileRepository):
        result = await profile_repo.get_by_id("nonexistent-id")
        assert result is None

    async def test_list_all_empty(self, profile_repo: ProfileRepository):
        result = await profile_repo.list_all()
        assert result == []

    async def test_list_all_with_data(self, profile_repo: ProfileRepository):
        await profile_repo.add(make_profile(id="p1", name="Alice"))
        await profile_repo.add(make_profile(id="p2", name="Bob"))

        result = await profile_repo.list_all()
        assert len(result) == 2

    async def test_list_all_pagination(self, profile_repo: ProfileRepository):
        for i in range(5):
            await profile_repo.add(make_profile(id=f"p{i}", name=f"User {i}"))

        page = await profile_repo.list_all(skip=2, limit=2)
        assert len(page) == 2

    async def test_count_empty(self, profile_repo: ProfileRepository):
        count = await profile_repo.count()
        assert count == 0

    async def test_count_with_data(self, profile_repo: ProfileRepository):
        await profile_repo.add(make_profile(id="p1"))
        await profile_repo.add(make_profile(id="p2"))

        count = await profile_repo.count()
        assert count == 2

    async def test_exists_true(self, profile_repo: ProfileRepository):
        profile = make_profile()
        await profile_repo.add(profile)

        assert await profile_repo.exists(profile.id) is True

    async def test_exists_false(self, profile_repo: ProfileRepository):
        assert await profile_repo.exists("nonexistent") is False

    async def test_find_by(self, profile_repo: ProfileRepository):
        await profile_repo.add(make_profile(id="p1", name="Alice"))
        await profile_repo.add(make_profile(id="p2", name="Bob"))

        result = await profile_repo.find_by(name="Alice")
        assert len(result) == 1
        assert result[0].name == "Alice"


class TestProfileRepositorySpecific:
    async def test_get_profile_returns_none_when_empty(
        self, profile_repo: ProfileRepository
    ):
        result = await profile_repo.get_profile()
        assert result is None

    async def test_get_profile_returns_profile(self, profile_repo: ProfileRepository):
        profile = make_profile()
        await profile_repo.add(profile)

        result = await profile_repo.get_profile()
        assert result is not None
        assert result.id == profile.id

    async def test_profile_exists_false(self, profile_repo: ProfileRepository):
        assert await profile_repo.profile_exists() is False

    async def test_profile_exists_true(self, profile_repo: ProfileRepository):
        await profile_repo.add(make_profile())
        assert await profile_repo.profile_exists() is True
