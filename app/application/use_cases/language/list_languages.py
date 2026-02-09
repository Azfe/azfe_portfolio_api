"""
List Languages Use Case.

Retrieves all languages for a profile.
"""

from typing import TYPE_CHECKING

from app.application.dto.language_dto import (
    LanguageListResponse,
    ListLanguagesRequest,
)
from app.shared.interfaces import IOrderedRepository, IQueryUseCase

if TYPE_CHECKING:
    from app.domain.entities import Language as LanguageType


class ListLanguagesUseCase(
    IQueryUseCase[ListLanguagesRequest, LanguageListResponse]
):
    """Use case for listing all languages."""

    def __init__(
        self, language_repository: IOrderedRepository["LanguageType"]
    ):
        self.repo = language_repository

    async def execute(
        self, request: ListLanguagesRequest
    ) -> LanguageListResponse:
        languages = await self.repo.get_all_ordered(
            profile_id=request.profile_id,
            ascending=request.ascending,
        )

        return LanguageListResponse.from_entities(languages)
