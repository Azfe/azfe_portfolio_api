from io import BytesIO
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa

from app.application.dto.cv_dto import CompleteCVResponse
from app.application.services.pdf_service import IPDFService

_TEMPLATES_DIR = Path(__file__).parent / "templates"
_jinja_env = Environment(loader=FileSystemLoader(str(_TEMPLATES_DIR)), autoescape=True)


class WeasyPrintPDFService(IPDFService):  # nombre mantenido para no alterar imports externos
    def generate_cv_pdf(self, cv_data: CompleteCVResponse) -> bytes:
        template = _jinja_env.get_template("cv_template.html")
        html_str = template.render(cv=cv_data)
        buffer = BytesIO()
        pisa.CreatePDF(html_str, dest=buffer)
        return buffer.getvalue()
