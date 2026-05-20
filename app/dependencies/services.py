from fastapi import Depends
from app.services.pdf_extractor import PDFExtractorService
from app.integrations.groq_client import GroqClient
from app.services.resume_service import ResumeAnalyzerService

from app.services.template_service import TemplateService
from app.services.pdf_generation_service import PDFGenerationService
from app.services.file_storage_service import FileStorageService
from app.services.resume_optimization_service import ResumeOptimizationService

# Dependency Providers
def get_pdf_extractor() -> PDFExtractorService:
    return PDFExtractorService()

def get_groq_client() -> GroqClient:
    return GroqClient()

def get_template_service() -> TemplateService:
    return TemplateService()

def get_pdf_generation_service() -> PDFGenerationService:
    return PDFGenerationService()

def get_file_storage_service() -> FileStorageService:
    return FileStorageService()

def get_resume_analyzer_service(
    pdf_extractor: PDFExtractorService = Depends(get_pdf_extractor),
    groq_client: GroqClient = Depends(get_groq_client)
) -> ResumeAnalyzerService:
    return ResumeAnalyzerService(pdf_extractor=pdf_extractor, groq_client=groq_client)

def get_resume_optimization_service(
    pdf_extractor: PDFExtractorService = Depends(get_pdf_extractor),
    groq_client: GroqClient = Depends(get_groq_client),
    template_service: TemplateService = Depends(get_template_service),
    pdf_generation_service: PDFGenerationService = Depends(get_pdf_generation_service),
    file_storage_service: FileStorageService = Depends(get_file_storage_service)
) -> ResumeOptimizationService:
    return ResumeOptimizationService(
        pdf_extractor=pdf_extractor,
        groq_client=groq_client,
        template_service=template_service,
        pdf_generation_service=pdf_generation_service,
        file_storage_service=file_storage_service
    )

from app.services.career_document_service import CareerDocumentGenerationService

def get_career_document_service(
    pdf_extractor: PDFExtractorService = Depends(get_pdf_extractor),
    groq_client: GroqClient = Depends(get_groq_client)
) -> CareerDocumentGenerationService:
    return CareerDocumentGenerationService(
        groq_client=groq_client,
        pdf_extraction_service=pdf_extractor
    )
