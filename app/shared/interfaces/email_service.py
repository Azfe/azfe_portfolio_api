from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class EmailMessage:
    to: str
    subject: str
    body_html: str
    body_text: str


class IEmailService(ABC):
    @abstractmethod
    async def send(self, message: EmailMessage) -> None: ...
