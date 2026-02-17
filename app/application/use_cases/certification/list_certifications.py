"""
List Certifications Use Case.

Retrieves all certifications for a profile.
"""

from typing import TYPE_CHECKING

from app.application.dto import CertificationListResponse, ListCertificationsRequest
from app.shared.interfaces import IOrderedRepository, IQueryUseCase

if TYPE_CHECKING:
    from app.domain.entities import Certification as CertificationType


class ListCertificationsUseCase(
    IQueryUseCase[ListCertificationsRequest, CertificationListResponse]
):
    """
    Use case for listing all certifications.

    Business Rules:
    - Returns all certifications for the profile
    - Ordered by orderIndex (configurable direction)

    Dependencies:
    - IOrderedRepository[Certification]: For certification data access
    """

    def __init__(
        self, certification_repository: IOrderedRepository["CertificationType"]
    ):
        """
        Initialize use case with dependencies.

        Args:
            certification_repository: Certification repository interface
        """
        self.certification_repo = certification_repository

    async def execute(
        self, request: ListCertificationsRequest
    ) -> CertificationListResponse:
        """
        Execute the use case.

        Args:
            request: List certifications request with profile ID

        Returns:
            CertificationListResponse with list of certifications and metadata
        """
        # Get certifications
        certifications = await self.certification_repo.find_by(
            profile_id=request.profile_id
        )

        # Sort by order_index
        certifications.sort(key=lambda c: c.order_index, reverse=not request.ascending)

        # Convert to DTO and return
        return CertificationListResponse.from_entities(certifications)
