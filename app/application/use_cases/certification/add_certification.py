"""
Add Certification Use Case.

Adds a new certification to the profile.
"""

from typing import TYPE_CHECKING

from app.application.dto import AddCertificationRequest, CertificationResponse
from app.domain.entities import Certification
from app.shared.interfaces import ICommandUseCase, IOrderedRepository
from app.shared.shared_exceptions import BusinessRuleViolationException

if TYPE_CHECKING:
    from app.domain.entities import Certification as CertificationType


class AddCertificationUseCase(ICommandUseCase[AddCertificationRequest, CertificationResponse]):
    """
    Use case for adding a certification.

    Business Rules:
    - orderIndex must be unique per profile
    - Title and issuer are required
    - Date range must be valid

    Dependencies:
    - IOrderedRepository[Certification]: For certification data access
    """

    def __init__(self, certification_repository: IOrderedRepository["CertificationType"]):
        """
        Initialize use case with dependencies.

        Args:
            certification_repository: Certification repository interface
        """
        self.certification_repo = certification_repository

    async def execute(self, request: AddCertificationRequest) -> CertificationResponse:
        """
        Execute the use case.

        Args:
            request: Add certification request with certification data

        Returns:
            CertificationResponse with created certification data

        Raises:
            BusinessRuleViolationException: If orderIndex already exists
            DomainError: If validation fails
        """
        # Check orderIndex uniqueness
        existing = await self.certification_repo.get_by_order_index(
            request.profile_id, request.order_index
        )
        if existing:
            raise BusinessRuleViolationException(
                "orderIndex must be unique per profile",
                {"orderIndex": request.order_index},
            )

        # Create domain entity (validates automatically)
        certification = Certification.create(
            profile_id=request.profile_id,
            title=request.title,
            issuer=request.issuer,
            issue_date=request.issue_date,
            order_index=request.order_index,
            expiry_date=request.expiry_date,
            credential_id=request.credential_id,
            credential_url=request.credential_url,
        )

        # Persist the certification
        created_certification = await self.certification_repo.add(certification)

        # Convert to DTO and return
        return CertificationResponse.from_entity(created_certification)