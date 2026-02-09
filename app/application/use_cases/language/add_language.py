"""
Add Language Use Case.

Adds a new language to the profile.
"""

from typing import TYPE_CHECKING

from app.application.dto.language_dto import AddLanguageRequest, LanguageResponse
from app.domain.entities import Language
from app.shared.interfaces import ICommandUseCase, IOrderedRepository

if TYPE_CHECKING:
    from app.domain.entities import Language as LanguageType


class AddLanguageUseCase(ICommandUseCase[AddLanguageRequest, LanguageResponse]):
    """Use case for adding a language."""

    def __init__(self, language_repository: IOrderedRepository["LanguageType"]):
        self.repo = language_repository

    async def execute(self, request: AddLanguageRequest) -> LanguageResponse:
        language = Language.create(
            profile_id=request.profile_id,
            name=request.name,
            order_index=request.order_index,
            proficiency=request.proficiency,
        )

        created = await self.repo.add(language)

        return LanguageResponse.from_entity(created)
