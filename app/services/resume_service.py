from fastapi import UploadFile
from app.schemas.resume import ResumeAnalysisResponse
from app.services.pdf_extractor import PDFExtractorService
from app.integrations.groq_client import GroqClient
from app.prompts.resume_analyzer import RESUME_ANALYZER_SYSTEM_PROMPT
from app.core.logging import logger

class ResumeAnalyzerService:
    def __init__(self, pdf_extractor: PDFExtractorService, groq_client: GroqClient):
        self.pdf_extractor = pdf_extractor
        self.groq_client = groq_client

    async def analyze_resume(self, file: UploadFile) -> ResumeAnalysisResponse:
        """
        Coordinates the extraction of text from a PDF and its analysis via Groq LLM.
        """
        logger.info(f"Starting analysis for resume: {file.filename}")
        
        # 1. Extract Text
        resume_text = await self.pdf_extractor.extract_text(file)
        
        # 2. Prepare User Prompt
        user_prompt = f"Here is the text extracted from the candidate's resume:\n\n{resume_text}\n\nPlease analyze it and provide the JSON output."
        
        # 3. Call LLM via Groq Client
        llm_response_dict = await self.groq_client.generate_json(
            system_prompt=RESUME_ANALYZER_SYSTEM_PROMPT,
            user_prompt=user_prompt
        )
        
        # 4. Validate and Parse with Pydantic
        logger.info(f"Successfully received analysis for {file.filename}, validating schema.")
        analysis = ResumeAnalysisResponse(**llm_response_dict)
        
        return analysis
