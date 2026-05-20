import logging
from typing import Optional, List
from fastapi import UploadFile

from app.integrations.groq_client import GroqClient
from app.services.pdf_extractor import PDFExtractorService
from app.schemas.career_schema import ApplicationKitResponse
from app.prompts.career_prompts import CAREER_KIT_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

class CareerDocumentGenerationService:
    def __init__(self, groq_client: GroqClient, pdf_extraction_service: PDFExtractorService):
        self.groq_client = groq_client
        self.pdf_extraction_service = pdf_extraction_service

    async def generate_application_kit(
        self, 
        file: UploadFile, 
        target_role: str, 
        company_name: Optional[str] = None, 
        job_description: Optional[str] = None, 
        tone: Optional[str] = None
    ) -> ApplicationKitResponse:
        logger.info(f"Generating application kit for role: {target_role}")
        
        # Extract text from resume
        resume_text = await self.pdf_extraction_service.extract_text(file)
        
        # Build prompt
        user_prompt = f"Resume Content:\n{resume_text}\n\nTarget Role: {target_role}\n"
        if company_name:
            user_prompt += f"Target Company: {company_name}\n"
        if job_description:
            user_prompt += f"Job Description context: {job_description}\n"
        if tone:
            user_prompt += f"Requested Tone: {tone}\n"
            
        # Call Groq AI
        llm_response = await self.groq_client.generate_json(
            system_prompt=CAREER_KIT_SYSTEM_PROMPT,
            user_prompt=user_prompt
        )
        
        # Parse and return structured response
        return ApplicationKitResponse(**llm_response)

    # Modular methods as requested for future scaling
    async def extract_candidate_strengths(self, resume_text: str) -> List[str]:
        pass
        
    async def generate_cover_letter(self, resume_text: str, role: str) -> str:
        pass
        
    async def generate_custom_template(self, resume_text: str) -> str:
        pass
        
    async def generate_cold_email(self, resume_text: str, role: str) -> str:
        pass
        
    async def generate_linkedin_message(self, resume_text: str) -> str:
        pass
        
    async def generate_subject_lines(self, role: str) -> List[str]:
        pass
        
    async def generate_job_pitch(self, resume_text: str) -> str:
        pass
