from pydantic import BaseModel, Field


class KeywordMatchResult(BaseModel):
    """Structured ATS keyword match result for resume and job description skills."""

    matched_keywords: list[str] = Field(default_factory=list)
    missing_keywords: list[str] = Field(default_factory=list)
    coverage_percentage: float = 100.0
    total_required_keywords: int = 0
    matched_keyword_count: int = 0
