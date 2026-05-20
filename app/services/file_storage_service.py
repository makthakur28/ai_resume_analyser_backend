import os
import aiofiles
from fastapi import UploadFile
from app.core.logging import logger

class FileStorageService:
    def __init__(self, base_dir: str = "app/storage"):
        self.base_dir = base_dir
        self.upload_dir = os.path.join(self.base_dir, "uploads")
        self.generated_dir = os.path.join(self.base_dir, "generated")
        
        # Ensure directories exist
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.generated_dir, exist_ok=True)

    def get_generated_path(self, file_id: str) -> str:
        return os.path.join(self.generated_dir, f"{file_id}.pdf")

    def get_upload_path(self, file_id: str) -> str:
        return os.path.join(self.upload_dir, f"{file_id}.pdf")
