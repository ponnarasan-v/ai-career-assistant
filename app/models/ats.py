from pydantic import BaseModel, Field


class KeywordMatchResult(BaseModel):
    """Structured ATS keyword match result for resume and job description skills."""

    matched_keywords: list[str] = Field(default_factory=list)
    missing_keywords: list[str] = Field(default_factory=list)
    coverage_percentage: float = 100.0
    total_required_keywords: int = 0
    matched_keyword_count: int = 0


class SectionMatchResult(BaseModel):
    """Independent ATS compatibility scores for major resume sections."""

    skills_score: float = 100.0
    education_score: float = 100.0
    experience_score: float = 100.0
    projects_score: float = 100.0


class ATSScoreResult(BaseModel):
    """Weighted ATS compatibility score with preserved section scores."""

    overall_score: float = 100.0
    skills_score: float = 100.0
    education_score: float = 100.0
    experience_score: float = 100.0
    projects_score: float = 100.0
