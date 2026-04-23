from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from app.api.dependencies import (
    get_generate_cv_pdf_use_case,
    get_get_complete_cv_use_case,
)
from app.api.schemas.cv_schema import CVCompleteResponse
from app.application.dto import GenerateCVPDFRequest, GetCompleteCVRequest
from app.application.use_cases import GenerateCVPDFUseCase, GetCompleteCVUseCase

router = APIRouter(prefix="/cv", tags=["CV"])


@router.get(
    "",
    response_model=CVCompleteResponse,
    summary="Obtener CV completo",
    description="Obtiene TODA la información del CV para mostrar en el portfolio",
)
async def get_complete_cv(
    use_case: GetCompleteCVUseCase = Depends(get_get_complete_cv_use_case),
):
    result = await use_case.execute(GetCompleteCVRequest())
    return result


@router.get(
    "/download",
    summary="Descargar CV en PDF",
    description="Genera y descarga el CV en formato PDF profesional",
    response_class=FileResponse,
)
async def download_cv_pdf(
    use_case: GenerateCVPDFUseCase = Depends(get_generate_cv_pdf_use_case),
):
    result = await use_case.execute(GenerateCVPDFRequest())
    if not result.success:
        raise HTTPException(status_code=500, detail=result.message)
    raise HTTPException(
        status_code=501,
        detail=result.message,
    )
