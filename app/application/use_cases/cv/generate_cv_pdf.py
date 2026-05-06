import asyncio

from app.application.dto import (
    GenerateCVPDFRequest,
    GenerateCVPDFResponse,
    GetCompleteCVRequest,
)
from app.application.services.pdf_service import IPDFService
from app.shared.interfaces import IQueryUseCase

from .get_complete_cv import GetCompleteCVUseCase


class GenerateCVPDFUseCase(IQueryUseCase[GenerateCVPDFRequest, GenerateCVPDFResponse]):
    def __init__(self, get_cv_use_case: GetCompleteCVUseCase, pdf_service: IPDFService):
        self.get_cv_use_case = get_cv_use_case
        self.pdf_service = pdf_service

    async def execute(self, _request: GenerateCVPDFRequest) -> GenerateCVPDFResponse:
        cv_data = await self.get_cv_use_case.execute(GetCompleteCVRequest())
        # WeasyPrint is synchronous; run in thread pool to avoid blocking the event loop
        pdf_bytes = await asyncio.to_thread(self.pdf_service.generate_cv_pdf, cv_data)
        return GenerateCVPDFResponse(success=True, pdf_bytes=pdf_bytes)
