from abc import ABC, abstractmethod

from app.application.dto.cv_dto import CompleteCVResponse


class IPDFService(ABC):
    @abstractmethod
    def generate_cv_pdf(self, cv_data: CompleteCVResponse) -> bytes: ...
