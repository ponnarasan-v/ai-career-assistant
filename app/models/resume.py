from pydantic import BaseModel, Field


class ContactInfo(BaseModel):
    """Typed contact information extracted from a resume."""

    name: str = ""
    email: str = ""
    phone: str = ""
    linkedin: str = ""
    github: str = ""
    portfolio: str = ""


class ResumeSections(BaseModel):
    """Typed resume section content extracted from cleaned text."""

    summary: str = ""
    skills: str = ""
    education: str = ""
    experience: str = ""
    projects: str = ""
    certifications: str = ""
    publications: str = ""
    achievements: str = ""


class ResumeData(BaseModel):
    """Structured resume data returned by the resume information extractor."""

    contact: ContactInfo = Field(default_factory=ContactInfo)
    sections: ResumeSections = Field(default_factory=ResumeSections)
