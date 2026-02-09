"""
Edit ProgrammingLanguage Use Case.

Updates an existing programming language.
"""

from typing import TYPE_CHECKING

from app.application.dto.programming_language_dto import (
    EditProgrammingLanguageRequest,
    ProgrammingLanguageResponse,
)
from app.shared.interfaces import ICommandUseCase, IOrderedRepository
from app.shared.shared_exceptions import NotFoundException

if TYPE_CHECKING:
    from app.domain.entities import ProgrammingLanguage as ProgrammingLanguageType


class EditProgrammingLanguageUseCase(
    ICommandUseCase[EditProgrammingLanguageRequest, ProgrammingLanguageResponse]
):
    """Use case for editing a programming language."""

    def __init__(
        self,
        programming_language_repository: IOrderedRepository[
            "ProgrammingLanguageType"
        ],
    ):
        self.repo = programming_language_repository

    async def execute(
        self, request: EditProgrammingLanguageRequest
    ) -> ProgrammingLanguageResponse:
        programming_language = await self.repo.get_by_id(
            request.programming_language_id
        )

        if not programming_language:
            raise NotFoundException(
                "ProgrammingLanguage", request.programming_language_id
            )

        programming_language.update_info(
            name=request.name,
            level=request.level,
        )

        updated = await self.repo.update(programming_language)

        return ProgrammingLanguageResponse.from_entity(updated)
