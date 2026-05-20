from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import FileResponse
import os
from app.schemas.resume import ResumeAnalysisResponse, OptimizeResumeResponse
from app.schemas.common import SuccessResponse
from app.services.resume_service import ResumeAnalyzerService
from app.services.resume_optimization_service import ResumeOptimizationService
from app.services.file_storage_service import FileStorageService
from app.dependencies.services import get_resume_analyzer_service, get_resume_optimization_service, get_file_storage_service
from app.exceptions.custom_exceptions import FileValidationError, AppException
from app.config.settings import settings

router = APIRouter()

def validate_upload_file(file: UploadFile):
    if file.content_type not in settings.ALLOWED_MIME_TYPES:
        raise FileValidationError(f"Invalid file type: {file.content_type}. Only PDFs are allowed.")
    if file.size and file.size > settings.MAX_UPLOAD_SIZE:
        max_mb = settings.MAX_UPLOAD_SIZE / (1024 * 1024)
        raise FileValidationError(f"File too large. Maximum allowed size is {max_mb}MB.")
    return file

@router.post("/analyze", response_model=SuccessResponse[ResumeAnalysisResponse])
async def analyze_resume(
    file: UploadFile = File(...),
    resume_service: ResumeAnalyzerService = Depends(get_resume_analyzer_service)
):
    """
    Upload a resume PDF for AI-driven analysis.
    """
    validate_upload_file(file)
    
    analysis_result = await resume_service.analyze_resume(file)
    
    return SuccessResponse(
        data=analysis_result,
        message="Resume analyzed successfully"
    )

@router.post("/optimize", response_model=SuccessResponse[OptimizeResumeResponse])
async def optimize_resume(
    file: UploadFile = File(...),
    optimization_service: ResumeOptimizationService = Depends(get_resume_optimization_service)
):
    """
    Upload a resume PDF to be extracted, AI-optimized, and regenerated as a new professional PDF.
    """
    validate_upload_file(file)
    
    optimization_result = await optimization_service.optimize_and_generate(file)
    
    return SuccessResponse(
        data=optimization_result,
        message="Resume optimized and generated successfully"
    )

@router.get("/download/{file_id}")
async def download_resume(
    file_id: str,
    file_storage: FileStorageService = Depends(get_file_storage_service)
):
    """
    Download a generated AI-optimized resume PDF by its ID.
    """
    file_path = file_storage.get_generated_path(file_id)
    if not os.path.exists(file_path):
        raise AppException(message="Resume file not found.", status_code=404)
        
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=f"Optimized_Resume_{file_id[:8]}.pdf"
    )
