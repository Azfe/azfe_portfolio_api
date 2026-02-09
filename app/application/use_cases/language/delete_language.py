"""
Delete Language Use Case.

Deletes an existing language.
"""

from typing import TYPE_CHECKING

from app.application.dto import SuccessResponse
from app.application.dto.language_dto import DeleteLanguageRequest
from app.shared.interfaces import ICommandUseCase, IOrderedRepository
from app.shared.shared_exceptions import NotFoundException

if TYPE_CHECKING:
    from app.domain.entities import Language as LanguageType


class DeleteLanguageUseCase(ICommandUseCase[DeleteLanguageRequest, SuccessResponse]):
    """Use case for deleting a language."""

    def __init__(self, language_repository: IOrderedRepository["LanguageType"]):
        self.repo = language_repository

    async def execute(self, request: DeleteLanguageRequest) -> SuccessResponse:
        deleted = await self.repo.delete(request.language_id)

        if not deleted:
            raise NotFoundException("Language", request.language_id)

        return SuccessResponse(message="Language deleted successfully")
