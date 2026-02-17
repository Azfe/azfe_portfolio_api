"""
Delete Certification Use Case.

Deletes an existing certification.
"""

from typing import TYPE_CHECKING

from app.application.dto import DeleteCertificationRequest, SuccessResponse
from app.shared.interfaces import ICommandUseCase, IOrderedRepository
from app.shared.shared_exceptions import NotFoundException

if TYPE_CHECKING:
    from app.domain.entities import Certification as CertificationType


class DeleteCertificationUseCase(
    ICommandUseCase[DeleteCertificationRequest, SuccessResponse]
):
    """
    Use case for deleting a certification.

    Business Rules:
    - Certification must exist
    - Deletion is permanent

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

    async def execute(self, request: DeleteCertificationRequest) -> SuccessResponse:
        """
        Execute the use case.

        Args:
            request: Delete certification request with certification ID

        Returns:
            SuccessResponse confirming deletion

        Raises:
            NotFoundException: If certification doesn't exist
        """
        # Attempt to delete
        deleted = await self.certification_repo.delete(request.certification_id)

        if not deleted:
            raise NotFoundException("Certification", request.certification_id)

        return SuccessResponse(message="Certification deleted successfully")
