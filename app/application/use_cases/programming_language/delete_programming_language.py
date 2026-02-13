"""
Delete ProgrammingLanguage Use Case.

Deletes an existing programming language.
"""

from typing import TYPE_CHECKING

from app.application.dto import SuccessResponse
from app.application.dto.programming_language_dto import (
    DeleteProgrammingLanguageRequest,
)
from app.shared.interfaces import ICommandUseCase, IOrderedRepository
from app.shared.shared_exceptions import NotFoundException

if TYPE_CHECKING:
    from app.domain.entities import ProgrammingLanguage as ProgrammingLanguageType


class DeleteProgrammingLanguageUseCase(
    ICommandUseCase[DeleteProgrammingLanguageRequest, SuccessResponse]
):
    """Use case for deleting a programming language."""

    def __init__(
        self,
        programming_language_repository: IOrderedRepository["ProgrammingLanguageType"],
    ):
        self.repo = programming_language_repository

    async def execute(
        self, request: DeleteProgrammingLanguageRequest
    ) -> SuccessResponse:
        deleted = await self.repo.delete(request.programming_language_id)

        if not deleted:
            raise NotFoundException(
                "ProgrammingLanguage", request.programming_language_id
            )

        return SuccessResponse(message="Programming language deleted successfully")
