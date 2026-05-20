class AppException(Exception):
    """Base exception for application errors."""
    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class FileValidationError(AppException):
    """Raised when an uploaded file fails validation (size, type, etc)."""
    def __init__(self, message: str):
        super().__init__(message=message, status_code=400)

class PDFExtractionError(AppException):
    """Raised when PDF text extraction fails."""
    def __init__(self, message: str):
        super().__init__(message=message, status_code=422)

class LLMIntegrationError(AppException):
    """Raised when the LLM service returns an error."""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message=message, status_code=502, details=details)
