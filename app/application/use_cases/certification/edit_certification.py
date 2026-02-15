"""
Edit Certification Use Case.

Updates an existing certification.
"""

from typing import TYPE_CHECKING

from app.application.dto import CertificationResponse, EditCertificationRequest
from app.shared.interfaces import ICommandUseCase, IOrderedRepository
from app.shared.shared_exceptions import NotFoundException

if TYPE_CHECKING:
    from app.domain.entities import Certification as CertificationType


class EditCertificationUseCase(ICommandUseCase[EditCertificationRequest, CertificationResponse]):
    """
    Use case for editing a certification.

    Business Rules:
    - Certification must exist
    - Only provided fields are updated
    - Validations are performed by the entity

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

    async def execute(self, request: EditCertificationRequest) -> CertificationResponse:
        """
        Execute the use case.

        Args:
            request: Edit certification request with fields to update

        Returns:
            CertificationResponse with updated certification data

        Raises:
            NotFoundException: If certification doesn't exist
            DomainError: If validation fails
        """
        # Get existing certification
        certification = await self.certification_repo.get_by_id(request.certification_id)

        if not certification:
            raise NotFoundException("Certification", request.certification_id)

        # Update info (entity validates)
        certification.update_info(
            title=request.title,
            issuer=request.issuer,
            issue_date=request.issue_date,
            expiry_date=request.expiry_date,
            credential_id=request.credential_id,
            credential_url=request.credential_url,
        )

        # Persist changes
        updated_certification = await self.certification_repo.update(certification)

        # Convert to DTO and return
        return CertificationResponse.from_entity(updated_certification)