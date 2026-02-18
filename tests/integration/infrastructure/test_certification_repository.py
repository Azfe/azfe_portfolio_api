"""Integration tests for CertificationRepository against real MongoDB."""

from app.infrastructure.repositories import CertificationRepository

from .conftest import DT_END, PROFILE_ID, make_certification


class TestCertificationRepositoryCRUD:
    async def test_add_and_retrieve(self, certification_repo: CertificationRepository):
        cert = make_certification()
        await certification_repo.add(cert)

        fetched = await certification_repo.get_by_id(cert.id)
        assert fetched is not None
        assert fetched.title == "AWS Solutions Architect"
        assert fetched.issuer == "Amazon"

    async def test_add_with_optional_fields(
        self, certification_repo: CertificationRepository
    ):
        cert = make_certification(
            credential_id="ABC-123",
            credential_url="https://verify.example.com/abc",
            expiry_date=DT_END,
        )
        await certification_repo.add(cert)

        fetched = await certification_repo.get_by_id(cert.id)
        assert fetched is not None
        assert fetched.credential_id == "ABC-123"
        assert fetched.credential_url == "https://verify.example.com/abc"

    async def test_update(self, certification_repo: CertificationRepository):
        cert = make_certification()
        await certification_repo.add(cert)

        updated = make_certification(title="GCP Professional", issuer="Google")
        await certification_repo.update(updated)

        fetched = await certification_repo.get_by_id(cert.id)
        assert fetched is not None
        assert fetched.title == "GCP Professional"

    async def test_delete(self, certification_repo: CertificationRepository):
        cert = make_certification()
        await certification_repo.add(cert)

        assert await certification_repo.delete(cert.id) is True
        assert await certification_repo.get_by_id(cert.id) is None

    async def test_delete_nonexistent(
        self, certification_repo: CertificationRepository
    ):
        assert await certification_repo.delete("nonexistent") is False

    async def test_list_all(self, certification_repo: CertificationRepository):
        await certification_repo.add(make_certification(id="c1", order_index=0))
        await certification_repo.add(make_certification(id="c2", order_index=1))

        result = await certification_repo.list_all()
        assert len(result) == 2

    async def test_count(self, certification_repo: CertificationRepository):
        assert await certification_repo.count() == 0
        await certification_repo.add(make_certification())
        assert await certification_repo.count() == 1

    async def test_exists(self, certification_repo: CertificationRepository):
        cert = make_certification()
        await certification_repo.add(cert)

        assert await certification_repo.exists(cert.id) is True
        assert await certification_repo.exists("nonexistent") is False


class TestCertificationRepositoryOrdering:
    async def test_get_by_order_index(
        self, certification_repo: CertificationRepository
    ):
        await certification_repo.add(make_certification(id="c1", order_index=0))
        await certification_repo.add(make_certification(id="c2", order_index=1))

        result = await certification_repo.get_by_order_index(PROFILE_ID, 1)
        assert result is not None
        assert result.id == "c2"

    async def test_get_all_ordered(self, certification_repo: CertificationRepository):
        await certification_repo.add(
            make_certification(id="c2", title="GCP", order_index=1)
        )
        await certification_repo.add(
            make_certification(id="c1", title="AWS", order_index=0)
        )

        result = await certification_repo.get_all_ordered(PROFILE_ID, ascending=True)
        assert result[0].title == "AWS"
        assert result[1].title == "GCP"

    async def test_reorder_move_down(self, certification_repo: CertificationRepository):
        await certification_repo.add(
            make_certification(id="c0", title="A", order_index=0)
        )
        await certification_repo.add(
            make_certification(id="c1", title="B", order_index=1)
        )
        await certification_repo.add(
            make_certification(id="c2", title="C", order_index=2)
        )

        await certification_repo.reorder(PROFILE_ID, "c0", 2)

        result = await certification_repo.get_all_ordered(PROFILE_ID)
        assert result[0].title == "B"
        assert result[1].title == "C"
        assert result[2].title == "A"

    async def test_reorder_move_up(self, certification_repo: CertificationRepository):
        await certification_repo.add(
            make_certification(id="c0", title="A", order_index=0)
        )
        await certification_repo.add(
            make_certification(id="c1", title="B", order_index=1)
        )
        await certification_repo.add(
            make_certification(id="c2", title="C", order_index=2)
        )

        await certification_repo.reorder(PROFILE_ID, "c2", 0)

        result = await certification_repo.get_all_ordered(PROFILE_ID)
        assert result[0].title == "C"
        assert result[1].title == "A"
        assert result[2].title == "B"
