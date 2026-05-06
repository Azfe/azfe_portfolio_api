from pathlib import Path

import weasyprint
from jinja2 import Environment, FileSystemLoader

from app.application.dto.cv_dto import CompleteCVResponse
from app.application.services.pdf_service import IPDFService

_TEMPLATES_DIR = Path(__file__).parent / "templates"
_jinja_env = Environment(loader=FileSystemLoader(str(_TEMPLATES_DIR)), autoescape=True)


class WeasyPrintPDFService(IPDFService):
    def generate_cv_pdf(self, cv_data: CompleteCVResponse) -> bytes:
        template = _jinja_env.get_template("cv_template.html")
        html_str = template.render(cv=cv_data)
        return weasyprint.HTML(string=html_str).write_pdf()
