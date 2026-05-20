from pydantic import BaseModel, Field
from typing import List, Optional

class ApplicationKitResponse(BaseModel):
    success: bool = True
    professional_summary: str = Field(..., description="A personalized, impactful summary")
    generic_cover_letter: str = Field(..., description="A generic reusable cover letter")
    customizable_cover_letter_template: str = Field(..., description="Template with placeholders like {{company_name}}")
    cold_apply_email: str = Field(..., description="Short, highly engaging cold email")
    linkedin_message: str = Field(..., description="Natural, non-spammy LinkedIn outreach")
    job_pitch: str = Field(..., description="Personalized job pitch")
    subject_lines: List[str] = Field(..., description="High-converting email subject lines")
    key_strengths: List[str] = Field(..., description="Strengths extracted from resume")
    highlighted_skills: List[str] = Field(..., description="Strongest technical skills")
    recommended_positioning: List[str] = Field(..., description="Strategic positioning advice")
    career_branding_keywords: List[str] = Field(..., description="Keywords for personal branding")
