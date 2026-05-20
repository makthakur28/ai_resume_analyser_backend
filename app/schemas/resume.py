from pydantic import BaseModel, Field
from typing import List, Optional

class ResumeAnalysisResponse(BaseModel):
    ats_score: int = Field(..., description="The overall ATS compatibility score from 0 to 100")
    strengths: List[str] = Field(..., description="Key strengths identified in the resume")
    weaknesses: List[str] = Field(..., description="Areas of weakness or poor formatting")
    missing_skills: List[str] = Field(..., description="Important skills that are missing based on typical industry standards")
    improvement_suggestions: List[str] = Field(..., description="Actionable suggestions to improve the resume")
    improved_professional_summary: str = Field(..., description="A rewritten, highly professional summary tailored for ATS")
    recommended_projects: List[str] = Field(..., description="Ideas for projects to build that would enhance the candidate's profile")
    recommended_tech_stack: List[str] = Field(..., description="Technologies the candidate should learn to stay competitive")
class PersonalInfo(BaseModel):
    name: Optional[str] = ""
    email: Optional[str] = ""
    phone: Optional[str] = ""
    linkedin: Optional[str] = ""
    github: Optional[str] = ""
    portfolio: Optional[str] = ""

class Experience(BaseModel):
    company: str
    role: str
    start_date: str
    end_date: str
    location: Optional[str] = ""
    bullets: List[str]

class Project(BaseModel):
    name: str
    technologies: List[str]
    description: str
    bullets: List[str]
    link: Optional[str] = ""

class Education(BaseModel):
    institution: str
    degree: str
    graduation_date: str
    gpa: Optional[str] = ""
    location: Optional[str] = ""

class StructuredResume(BaseModel):
    personal_info: PersonalInfo = Field(default_factory=PersonalInfo)
    summary: Optional[str] = ""
    skills: List[str] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)

class OptimizeResumeResponse(BaseModel):
    success: bool
    file_id: str
    download_url: str
    preview_url: str
    ats_score: int
    optimized_sections: List[str]
    recommendations: List[str]
