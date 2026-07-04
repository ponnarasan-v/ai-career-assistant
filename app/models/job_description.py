from pydantic import BaseModel, Field


class JobRequirements(BaseModel):
    """Structured requirements extracted from a job description."""

    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    qualifications: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    tools_and_technologies: list[str] = Field(default_factory=list)


class JobDescriptionData(BaseModel):
    """Typed data model for parsed job description information."""

    job_title: str = ""
    company: str = ""
    location: str = ""
    employment_type: str = ""
    requirements: JobRequirements = Field(default_factory=JobRequirements)
    raw_text: str = ""
    clean_text: str = ""
