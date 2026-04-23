"""
Add ProgrammingLanguage Use Case.

Adds a new programming language to the profile.
"""

from typing import TYPE_CHECKING

from app.application.dto.programming_language_dto import (
    AddProgrammingLanguageRequest,
    ProgrammingLanguageResponse,
)
from app.domain.entities import ProgrammingLanguage
from app.shared.interfaces import ICommandUseCase, IOrderedRepository

if TYPE_CHECKING:
    from app.domain.entities import ProgrammingLanguage as ProgrammingLanguageType


class AddProgrammingLanguageUseCase(
    ICommandUseCase[AddProgrammingLanguageRequest, ProgrammingLanguageResponse]
):
    """Use case for adding a programming language."""

    def __init__(
        self,
        programming_language_repository: IOrderedRepository["ProgrammingLanguageType"],
    ):
        self.repo = programming_language_repository

    async def execute(
        self, request: AddProgrammingLanguageRequest
    ) -> ProgrammingLanguageResponse:
        programming_language = ProgrammingLanguage.create(
            profile_id=request.profile_id,
            name=request.name,
            order_index=request.order_index,
            level=request.level,
        )

        created = await self.repo.add(programming_language)

        return ProgrammingLanguageResponse.from_entity(created)
