"""Integration tests for ContactInformationRepository against real MongoDB."""

from app.infrastructure.repositories import ContactInformationRepository

from .conftest import PROFILE_ID, make_contact_information


class TestContactInformationRepositoryCRUD:
    async def test_add_and_retrieve(
        self, contact_info_repo: ContactInformationRepository
    ):
        info = make_contact_information()
        await contact_info_repo.add(info)

        fetched = await contact_info_repo.get_by_id(info.id)
        assert fetched is not None
        assert fetched.email == "test@example.com"
        assert fetched.profile_id == PROFILE_ID

    async def test_add_with_optional_fields(
        self, contact_info_repo: ContactInformationRepository
    ):
        info = make_contact_information(
            phone="+34612345678",
            linkedin="https://linkedin.com/in/user",
            github="https://github.com/user",
            website="https://example.com",
        )
        await contact_info_repo.add(info)

        fetched = await contact_info_repo.get_by_id(info.id)
        assert fetched is not None
        assert fetched.phone == "+34612345678"
        assert fetched.linkedin == "https://linkedin.com/in/user"
        assert fetched.github == "https://github.com/user"
        assert fetched.website == "https://example.com"

    async def test_update(self, contact_info_repo: ContactInformationRepository):
        info = make_contact_information()
        await contact_info_repo.add(info)

        updated = make_contact_information(email="updated@example.com")
        await contact_info_repo.update(updated)

        fetched = await contact_info_repo.get_by_id(info.id)
        assert fetched is not None
        assert fetched.email == "updated@example.com"

    async def test_delete(self, contact_info_repo: ContactInformationRepository):
        info = make_contact_information()
        await contact_info_repo.add(info)

        assert await contact_info_repo.delete(info.id) is True
        assert await contact_info_repo.get_by_id(info.id) is None

    async def test_delete_nonexistent(
        self, contact_info_repo: ContactInformationRepository
    ):
        assert await contact_info_repo.delete("nonexistent") is False

    async def test_list_all(self, contact_info_repo: ContactInformationRepository):
        await contact_info_repo.add(
            make_contact_information(id="ci1", email="a@example.com")
        )
        await contact_info_repo.add(
            make_contact_information(
                id="ci2", email="b@example.com", profile_id="profile-2"
            )
        )

        result = await contact_info_repo.list_all()
        assert len(result) == 2

    async def test_count(self, contact_info_repo: ContactInformationRepository):
        assert await contact_info_repo.count() == 0
        await contact_info_repo.add(make_contact_information())
        assert await contact_info_repo.count() == 1

    async def test_exists(self, contact_info_repo: ContactInformationRepository):
        info = make_contact_information()
        await contact_info_repo.add(info)

        assert await contact_info_repo.exists(info.id) is True
        assert await contact_info_repo.exists("nonexistent") is False


class TestContactInformationRepositorySpecific:
    async def test_get_by_profile_id_found(
        self, contact_info_repo: ContactInformationRepository
    ):
        await contact_info_repo.add(make_contact_information())

        result = await contact_info_repo.get_by_profile_id(PROFILE_ID)
        assert result is not None
        assert result.email == "test@example.com"

    async def test_get_by_profile_id_not_found(
        self, contact_info_repo: ContactInformationRepository
    ):
        result = await contact_info_repo.get_by_profile_id("nonexistent-profile")
        assert result is None
