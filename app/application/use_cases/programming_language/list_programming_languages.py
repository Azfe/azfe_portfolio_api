"""
List ProgrammingLanguages Use Case.

Retrieves all programming languages for a profile.
"""

from typing import TYPE_CHECKING

from app.application.dto.programming_language_dto import (
    ListProgrammingLanguagesRequest,
    ProgrammingLanguageListResponse,
)
from app.shared.interfaces import IOrderedRepository, IQueryUseCase

if TYPE_CHECKING:
    from app.domain.entities import ProgrammingLanguage as ProgrammingLanguageType


class ListProgrammingLanguagesUseCase(
    IQueryUseCase[ListProgrammingLanguagesRequest, ProgrammingLanguageListResponse]
):
    """Use case for listing all programming languages."""

    def __init__(
        self,
        programming_language_repository: IOrderedRepository[
            "ProgrammingLanguageType"
        ],
    ):
        self.repo = programming_language_repository

    async def execute(
        self, request: ListProgrammingLanguagesRequest
    ) -> ProgrammingLanguageListResponse:
        programming_languages = await self.repo.get_all_ordered(
            profile_id=request.profile_id,
            ascending=request.ascending,
        )

        return ProgrammingLanguageListResponse.from_entities(programming_languages)
