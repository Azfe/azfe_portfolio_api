"""
Edit Language Use Case.

Updates an existing language.
"""

from typing import TYPE_CHECKING

from app.application.dto.language_dto import EditLanguageRequest, LanguageResponse
from app.shared.interfaces import ICommandUseCase, IOrderedRepository
from app.shared.shared_exceptions import NotFoundException

if TYPE_CHECKING:
    from app.domain.entities import Language as LanguageType


class EditLanguageUseCase(ICommandUseCase[EditLanguageRequest, LanguageResponse]):
    """Use case for editing a language."""

    def __init__(self, language_repository: IOrderedRepository["LanguageType"]):
        self.repo = language_repository

    async def execute(self, request: EditLanguageRequest) -> LanguageResponse:
        language = await self.repo.get_by_id(request.language_id)

        if not language:
            raise NotFoundException("Language", request.language_id)

        language.update_info(
            name=request.name,
            proficiency=request.proficiency,
        )

        updated = await self.repo.update(language)

        return LanguageResponse.from_entity(updated)
