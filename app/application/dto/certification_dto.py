"""
Certification DTOs.

Data Transfer Objects for Certification use cases.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AddCertificationRequest:
    """Request to add a certification."""

    profile_id: str
    title: str
    issuer: str
    issue_date: datetime
    order_index: int
    expiry_date: datetime | None = None
    credential_id: str | None = None
    credential_url: str | None = None


@dataclass
class EditCertificationRequest:
    """Request to edit a certification."""

    certification_id: str
    title: str | None = None
    issuer: str | None = None
    issue_date: datetime | None = None
    expiry_date: datetime | None = None
    credential_id: str | None = None
    credential_url: str | None = None


@dataclass
class DeleteCertificationRequest:
    """Request to delete a certification."""

    certification_id: str


@dataclass
class ListCertificationsRequest:
    """Request to list certifications."""

    profile_id: str
    ascending: bool = True  # Default: by order_index ASC


@dataclass
class CertificationResponse:
    """Response containing certification data."""

    id: str
    profile_id: str
    title: str
    issuer: str
    issue_date: datetime
    order_index: int
    expiry_date: datetime | None
    credential_id: str | None
    credential_url: str | None
    created_at: datetime
    updated_at: datetime
    is_expired: bool

    @classmethod
    def from_entity(cls, entity) -> "CertificationResponse":
        """Create DTO from domain entity."""
        return cls(
            id=entity.id,
            profile_id=entity.profile_id,
            title=entity.title,
            issuer=entity.issuer,
            issue_date=entity.issue_date,
            order_index=entity.order_index,
            expiry_date=entity.expiry_date,
            credential_id=entity.credential_id,
            credential_url=entity.credential_url,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_expired=entity.is_expired(),
        )


@dataclass
class CertificationListResponse:
    """Response containing list of certifications."""

    certifications: list[CertificationResponse]
    total: int

    @classmethod
    def from_entities(cls, entities) -> "CertificationListResponse":
        """Create DTO from list of domain entities."""
        return cls(
            certifications=[CertificationResponse.from_entity(e) for e in entities],
            total=len(entities),
        )
