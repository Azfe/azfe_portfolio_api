"""Tests for Certification use cases."""

from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from app.application.dto import (
    AddCertificationRequest,
    DeleteCertificationRequest,
    EditCertificationRequest,
    ListCertificationsRequest,
)
from app.application.use_cases.certification.add_certification import (
    AddCertificationUseCase,
)
from app.application.use_cases.certification.delete_certification import (
    DeleteCertificationUseCase,
)
from app.application.use_cases.certification.edit_certification import (
    EditCertificationUseCase,
)
from app.application.use_cases.certification.list_certifications import (
    ListCertificationsUseCase,
)
from app.domain.entities.certification import Certification
from app.shared.shared_exceptions import (
    BusinessRuleViolationException,
    NotFoundException,
)

pytestmark = pytest.mark.asyncio

PROFILE_ID = "profile-001"
ISSUE_DATE = datetime(2022, 3, 1)
EXPIRY_DATE = datetime(2025, 3, 1)


def _make_certification(**overrides):
    defaults = {
        "profile_id": PROFILE_ID,
        "title": "AWS Certified Solutions Architect",
        "issuer": "Amazon Web Services",
        "issue_date": ISSUE_DATE,
        "order_index": 0,
    }
    defaults.update(overrides)
    return Certification.create(**defaults)


class TestAddCertificationUseCase:
    @pytest.mark.unit
    async def test_add_certification_success(self):
        repo = AsyncMock()
        certification = _make_certification()
        repo.get_by_order_index.return_value = None
        repo.add.return_value = certification

        uc = AddCertificationUseCase(repo)
        request = AddCertificationRequest(
            profile_id=PROFILE_ID,
            title="AWS Certified Solutions Architect",
            issuer="Amazon Web Services",
            issue_date=ISSUE_DATE,
            order_index=0,
        )
        result = await uc.execute(request)

        assert result.title == "AWS Certified Solutions Architect"
        assert result.issuer == "Amazon Web Services"
        assert result.order_index == 0
        repo.get_by_order_index.assert_awaited_once_with(PROFILE_ID, 0)
        repo.add.assert_awaited_once()

    @pytest.mark.unit
    async def test_add_certification_with_optional_fields(self):
        repo = AsyncMock()
        certification = _make_certification(
            expiry_date=EXPIRY_DATE,
            credential_id="ABC-12345",
            credential_url="https://aws.amazon.com/verify/ABC-12345",
        )
        repo.get_by_order_index.return_value = None
        repo.add.return_value = certification

        uc = AddCertificationUseCase(repo)
        request = AddCertificationRequest(
            profile_id=PROFILE_ID,
            title="AWS Certified Solutions Architect",
            issuer="Amazon Web Services",
            issue_date=ISSUE_DATE,
            order_index=0,
            expiry_date=EXPIRY_DATE,
            credential_id="ABC-12345",
            credential_url="https://aws.amazon.com/verify/ABC-12345",
        )
        result = await uc.execute(request)

        assert result.expiry_date == EXPIRY_DATE
        assert result.credential_id == "ABC-12345"
        assert result.credential_url == "https://aws.amazon.com/verify/ABC-12345"

    @pytest.mark.unit
    @pytest.mark.business_rule
    async def test_add_certification_duplicate_order_index_raises(self):
        repo = AsyncMock()
        repo.get_by_order_index.return_value = _make_certification()

        uc = AddCertificationUseCase(repo)
        request = AddCertificationRequest(
            profile_id=PROFILE_ID,
            title="Another Certification",
            issuer="Google",
            issue_date=ISSUE_DATE,
            order_index=0,
        )
        with pytest.raises(BusinessRuleViolationException):
            await uc.execute(request)

        repo.add.assert_not_awaited()

    @pytest.mark.unit
    async def test_add_certification_checks_order_index_for_correct_profile(self):
        repo = AsyncMock()
        repo.get_by_order_index.return_value = None
        repo.add.return_value = _make_certification(order_index=5)

        uc = AddCertificationUseCase(repo)
        request = AddCertificationRequest(
            profile_id=PROFILE_ID,
            title="Google Cloud Professional",
            issuer="Google",
            issue_date=ISSUE_DATE,
            order_index=5,
        )
        await uc.execute(request)

        repo.get_by_order_index.assert_awaited_once_with(PROFILE_ID, 5)


class TestDeleteCertificationUseCase:
    @pytest.mark.unit
    async def test_delete_certification_success(self):
        repo = AsyncMock()
        repo.delete.return_value = True

        uc = DeleteCertificationUseCase(repo)
        result = await uc.execute(
            DeleteCertificationRequest(certification_id="cert-001")
        )

        assert result.success is True
        repo.delete.assert_awaited_once_with("cert-001")

    @pytest.mark.unit
    async def test_delete_certification_not_found_raises(self):
        repo = AsyncMock()
        repo.delete.return_value = False

        uc = DeleteCertificationUseCase(repo)
        with pytest.raises(NotFoundException):
            await uc.execute(
                DeleteCertificationRequest(certification_id="nonexistent")
            )


class TestEditCertificationUseCase:
    @pytest.mark.unit
    async def test_edit_certification_success(self):
        repo = AsyncMock()
        certification = _make_certification()
        repo.get_by_id.return_value = certification
        repo.update.return_value = certification

        uc = EditCertificationUseCase(repo)
        request = EditCertificationRequest(
            certification_id="cert-001",
            title="Updated Certification Title",
        )
        result = await uc.execute(request)

        assert result.title == "Updated Certification Title"
        repo.get_by_id.assert_awaited_once_with("cert-001")
        repo.update.assert_awaited_once()

    @pytest.mark.unit
    async def test_edit_certification_updates_multiple_fields(self):
        repo = AsyncMock()
        certification = _make_certification()
        repo.get_by_id.return_value = certification
        repo.update.return_value = certification

        uc = EditCertificationUseCase(repo)
        request = EditCertificationRequest(
            certification_id="cert-001",
            title="New Certification Name",
            issuer="New Issuer",
            credential_id="NEW-ID-999",
        )
        result = await uc.execute(request)

        assert result.title == "New Certification Name"
        assert result.issuer == "New Issuer"
        assert result.credential_id == "NEW-ID-999"

    @pytest.mark.unit
    async def test_edit_certification_not_found_raises(self):
        repo = AsyncMock()
        repo.get_by_id.return_value = None

        uc = EditCertificationUseCase(repo)
        request = EditCertificationRequest(
            certification_id="nonexistent",
            title="Updated Title",
        )
        with pytest.raises(NotFoundException):
            await uc.execute(request)

        repo.update.assert_not_awaited()

    @pytest.mark.unit
    async def test_edit_certification_partial_update_preserves_existing_fields(self):
        repo = AsyncMock()
        certification = _make_certification(
            title="Original Title",
            issuer="Original Issuer",
            credential_id="ORIG-001",
            credential_url="https://example.com/verify/ORIG-001",
        )
        repo.get_by_id.return_value = certification
        repo.update.return_value = certification

        uc = EditCertificationUseCase(repo)
        request = EditCertificationRequest(
            certification_id="cert-001",
            title="Updated Title",
        )
        result = await uc.execute(request)

        assert result.title == "Updated Title"
        assert result.issuer == "Original Issuer"
        assert result.credential_id == "ORIG-001"
        assert result.credential_url == "https://example.com/verify/ORIG-001"

    @pytest.mark.unit
    async def test_edit_certification_with_expiry_date(self):
        repo = AsyncMock()
        certification = _make_certification()
        repo.get_by_id.return_value = certification
        repo.update.return_value = certification

        uc = EditCertificationUseCase(repo)
        request = EditCertificationRequest(
            certification_id="cert-001",
            expiry_date=EXPIRY_DATE,
        )
        result = await uc.execute(request)

        assert result.expiry_date == EXPIRY_DATE


class TestListCertificationsUseCase:
    @pytest.mark.unit
    async def test_list_certifications_returns_empty_list(self):
        repo = AsyncMock()
        repo.find_by.return_value = []

        uc = ListCertificationsUseCase(repo)
        result = await uc.execute(
            ListCertificationsRequest(profile_id=PROFILE_ID)
        )

        assert result.certifications == []
        assert result.total == 0
        repo.find_by.assert_awaited_once_with(profile_id=PROFILE_ID)

    @pytest.mark.unit
    async def test_list_certifications_returns_all_items(self):
        repo = AsyncMock()
        certifications = [
            _make_certification(title="Cert A", order_index=0),
            _make_certification(title="Cert B", order_index=1),
            _make_certification(title="Cert C", order_index=2),
        ]
        repo.find_by.return_value = certifications

        uc = ListCertificationsUseCase(repo)
        result = await uc.execute(
            ListCertificationsRequest(profile_id=PROFILE_ID)
        )

        assert result.total == 3
        assert len(result.certifications) == 3

    @pytest.mark.unit
    async def test_list_certifications_sorted_ascending_by_default(self):
        repo = AsyncMock()
        certifications = [
            _make_certification(title="Cert C", order_index=2),
            _make_certification(title="Cert A", order_index=0),
            _make_certification(title="Cert B", order_index=1),
        ]
        repo.find_by.return_value = certifications

        uc = ListCertificationsUseCase(repo)
        result = await uc.execute(
            ListCertificationsRequest(profile_id=PROFILE_ID, ascending=True)
        )

        order_indices = [c.order_index for c in result.certifications]
        assert order_indices == sorted(order_indices)

    @pytest.mark.unit
    async def test_list_certifications_sorted_descending_when_requested(self):
        repo = AsyncMock()
        certifications = [
            _make_certification(title="Cert A", order_index=0),
            _make_certification(title="Cert B", order_index=1),
            _make_certification(title="Cert C", order_index=2),
        ]
        repo.find_by.return_value = certifications

        uc = ListCertificationsUseCase(repo)
        result = await uc.execute(
            ListCertificationsRequest(profile_id=PROFILE_ID, ascending=False)
        )

        order_indices = [c.order_index for c in result.certifications]
        assert order_indices == sorted(order_indices, reverse=True)

    @pytest.mark.unit
    async def test_list_certifications_includes_is_expired_field(self):
        repo = AsyncMock()
        # issue_date must be before expiry_date; both in the past so is_expired() returns True
        old_issue_date = datetime(2018, 1, 1)
        past_expiry = datetime(2019, 1, 1)
        cert_expired = _make_certification(
            title="Expired Cert",
            issue_date=old_issue_date,
            order_index=0,
            expiry_date=past_expiry,
        )
        cert_no_expiry = _make_certification(
            title="No Expiry Cert",
            order_index=1,
        )
        repo.find_by.return_value = [cert_expired, cert_no_expiry]

        uc = ListCertificationsUseCase(repo)
        result = await uc.execute(
            ListCertificationsRequest(profile_id=PROFILE_ID)
        )

        assert result.certifications[0].is_expired is True
        assert result.certifications[1].is_expired is False
