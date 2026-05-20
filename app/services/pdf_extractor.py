import io
from pypdf import PdfReader
from fastapi import UploadFile
from app.exceptions.custom_exceptions import PDFExtractionError
from app.core.logging import logger

class PDFExtractorService:
    @staticmethod
    async def extract_text(file: UploadFile) -> str:
        """
        Extracts text from an uploaded PDF file asynchronously.
        """
        try:
            # Read file content into memory
            content = await file.read()
            pdf_file = io.BytesIO(content)
            
            reader = PdfReader(pdf_file)
            extracted_text = ""
            
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + "\n"
                    
            if not extracted_text.strip():
                logger.warning(f"Extracted text from {file.filename} is empty.")
                raise PDFExtractionError("Could not extract any readable text from the provided PDF. It might be an image-based PDF.")
                
            return extracted_text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting PDF text from {file.filename}: {e}", exc_info=True)
            if isinstance(e, PDFExtractionError):
                raise e
            raise PDFExtractionError(f"Failed to process PDF file: {str(e)}")
        finally:
            # Reset file pointer for any subsequent reads if necessary
            await file.seek(0)
