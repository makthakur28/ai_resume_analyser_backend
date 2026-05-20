import uuid
import asyncio
from fastapi import UploadFile
from app.schemas.resume import OptimizeResumeResponse, StructuredResume
from app.services.pdf_extractor import PDFExtractorService
from app.integrations.groq_client import GroqClient
from app.services.template_service import TemplateService
from app.services.pdf_generation_service import PDFGenerationService
from app.services.file_storage_service import FileStorageService
from app.prompts.resume_optimizer import RESUME_OPTIMIZER_SYSTEM_PROMPT
from app.core.logging import logger

class ResumeOptimizationService:
    def __init__(
        self, 
        pdf_extractor: PDFExtractorService, 
        groq_client: GroqClient,
        template_service: TemplateService,
        pdf_generation_service: PDFGenerationService,
        file_storage_service: FileStorageService
    ):
        self.pdf_extractor = pdf_extractor
        self.groq_client = groq_client
        self.template_service = template_service
        self.pdf_generation_service = pdf_generation_service
        self.file_storage = file_storage_service

    async def optimize_and_generate(self, file: UploadFile) -> OptimizeResumeResponse:
        """
        Full pipeline: Upload -> Extract -> Optimize(Groq) -> Render HTML -> Generate PDF -> Return URLs
        """
        file_id = str(uuid.uuid4())
        logger.info(f"Starting optimization pipeline for {file.filename}, assigned ID: {file_id}")
        
        # 1. Extract Text
        resume_text = await self.pdf_extractor.extract_text(file)
        
        # 2. AI Optimization via Groq
        user_prompt = f"Optimize and structure the following resume text:\n\n{resume_text}"
        llm_response = await self.groq_client.generate_json(
            system_prompt=RESUME_OPTIMIZER_SYSTEM_PROMPT,
            user_prompt=user_prompt
        )
        
        # Parse into structured schema
        structured_resume = StructuredResume(**llm_response)
        logger.info("Successfully structured and optimized resume via LLM.")
        
        # 3. HTML Template Rendering
        # This is a CPU bound task, running in executor if needed, but it's fast enough
        html_content = self.template_service.render_resume(structured_resume)
        
        # 4. PDF Generation
        pdf_path = self.file_storage.get_generated_path(file_id)
        # Running WeasyPrint in a thread pool since it's blocking
        await asyncio.to_thread(self.pdf_generation_service.generate_pdf, html_content, pdf_path)
        
        return OptimizeResumeResponse(
            success=True,
            file_id=file_id,
            download_url=f"/api/v1/resume/download/{file_id}",
            preview_url=f"/api/v1/resume/download/{file_id}",
            ats_score=95, # In a real scenario, this could be calculated by the LLM
            optimized_sections=["Summary", "Experience", "Skills"],
            recommendations=["Consider adding quantifiable metrics to Project X."]
        )
