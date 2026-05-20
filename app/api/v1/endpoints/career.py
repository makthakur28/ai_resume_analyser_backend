import logging
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException

from app.schemas.career_schema import ApplicationKitResponse
from app.services.career_document_service import CareerDocumentGenerationService
from app.dependencies.services import get_career_document_service

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/generate-application-kit", response_model=ApplicationKitResponse)
async def generate_application_kit(
    file: UploadFile = File(...),
    target_role: str = Form(...),
    company_name: Optional[str] = Form(None),
    job_description: Optional[str] = Form(None),
    tone: Optional[str] = Form(None),
    career_service: CareerDocumentGenerationService = Depends(get_career_document_service)
):
    """
    Generate a complete AI Career Application Kit from a resume.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    try:
        return await career_service.generate_application_kit(
            file=file,
            target_role=target_role,
            company_name=company_name,
            job_description=job_description,
            tone=tone
        )
    except Exception as e:
        logger.error(f"Error generating application kit: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
