"""Unit tests for CertificationMapper."""

from app.domain.entities import Certification
from app.infrastructure.mappers.certification_mapper import CertificationMapper

from .conftest import DT_CREATED, DT_EXPIRY, DT_ISSUE, DT_UPDATED


class TestCertificationMapperToDomain:
    def setup_method(self):
        self.mapper = CertificationMapper()

    def test_required_fields_only(self):
        doc = {
            "_id": "c-1",
            "profile_id": "p-1",
            "title": "AWS SAA",
            "issuer": "Amazon",
            "issue_date": DT_ISSUE,
            "order_index": 0,
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)

        assert entity.id == "c-1"
        assert entity.title == "AWS SAA"
        assert entity.issuer == "Amazon"
        assert entity.expiry_date is None
        assert entity.credential_id is None
        assert entity.credential_url is None

    def test_all_fields(self):
        doc = {
            "_id": "c-1",
            "profile_id": "p-1",
            "title": "AWS SAA",
            "issuer": "Amazon",
            "issue_date": DT_ISSUE,
            "order_index": 0,
            "expiry_date": DT_EXPIRY,
            "credential_id": "CRED-123",
            "credential_url": "https://aws.com/cert/123",
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)

        assert entity.expiry_date == DT_EXPIRY
        assert entity.credential_id == "CRED-123"
        assert entity.credential_url == "https://aws.com/cert/123"


class TestCertificationMapperToPersistence:
    def setup_method(self):
        self.mapper = CertificationMapper()

    def test_excludes_none_optionals(self):
        entity = Certification(
            id="c-1",
            profile_id="p-1",
            title="AWS SAA",
            issuer="Amazon",
            issue_date=DT_ISSUE,
            order_index=0,
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)

        assert "expiry_date" not in doc
        assert "credential_id" not in doc
        assert "credential_url" not in doc

    def test_includes_optionals_when_set(self):
        entity = Certification(
            id="c-1",
            profile_id="p-1",
            title="AWS SAA",
            issuer="Amazon",
            issue_date=DT_ISSUE,
            order_index=0,
            expiry_date=DT_EXPIRY,
            credential_id="CRED-123",
            credential_url="https://aws.com/cert/123",
            created_at=DT_CREATED,
            updated_at=DT_UPDATED,
        )
        doc = self.mapper.to_persistence(entity)

        assert doc["expiry_date"] == DT_EXPIRY
        assert doc["credential_id"] == "CRED-123"
        assert doc["credential_url"] == "https://aws.com/cert/123"

    def test_round_trip(self):
        doc = {
            "_id": "c-1",
            "profile_id": "p-1",
            "title": "AWS SAA",
            "issuer": "Amazon",
            "issue_date": DT_ISSUE,
            "order_index": 0,
            "expiry_date": DT_EXPIRY,
            "credential_id": "CRED-123",
            "credential_url": "https://aws.com/cert/123",
            "created_at": DT_CREATED,
            "updated_at": DT_UPDATED,
        }
        entity = self.mapper.to_domain(doc)
        result = self.mapper.to_persistence(entity)
        assert result == doc
