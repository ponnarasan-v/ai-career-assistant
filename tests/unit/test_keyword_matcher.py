from app.models.job_description import JobDescriptionData, JobRequirements
from app.models.resume import ResumeData, ResumeSections
from app.services.ats.keyword_matcher import KeywordMatcher


def _resume_with_skills(skills: str) -> ResumeData:
    return ResumeData(sections=ResumeSections(skills=skills))


def _job_description_with_required_skills(required_skills: list[str]) -> JobDescriptionData:
    return JobDescriptionData(
        requirements=JobRequirements(required_skills=required_skills)
    )


def test_match_keywords_perfect_match():
    resume = _resume_with_skills("Python, FastAPI, SQL")
    job_description = _job_description_with_required_skills(["Python", "FastAPI", "SQL"])

    result = KeywordMatcher().match_keywords(resume, job_description)

    assert result.matched_keywords == ["FastAPI", "Python", "SQL"]
    assert result.missing_keywords == []
    assert result.coverage_percentage == 100.0
    assert result.total_required_keywords == 3
    assert result.matched_keyword_count == 3


def test_match_keywords_partial_match():
    resume = _resume_with_skills("Python, SQL")
    job_description = _job_description_with_required_skills(["Python", "FastAPI", "SQL"])

    result = KeywordMatcher().match_keywords(resume, job_description)

    assert result.matched_keywords == ["Python", "SQL"]
    assert result.missing_keywords == ["FastAPI"]
    assert result.coverage_percentage == 66.67
    assert result.total_required_keywords == 3
    assert result.matched_keyword_count == 2


def test_match_keywords_no_match():
    resume = _resume_with_skills("Java, Spring")
    job_description = _job_description_with_required_skills(["Python", "FastAPI"])

    result = KeywordMatcher().match_keywords(resume, job_description)

    assert result.matched_keywords == []
    assert result.missing_keywords == ["FastAPI", "Python"]
    assert result.coverage_percentage == 0.0
    assert result.total_required_keywords == 2
    assert result.matched_keyword_count == 0


def test_match_keywords_ignores_duplicate_skills():
    resume = _resume_with_skills("Python, python, SQL")
    job_description = _job_description_with_required_skills(
        ["Python", "python", "SQL", "sql"]
    )

    result = KeywordMatcher().match_keywords(resume, job_description)

    assert result.matched_keywords == ["Python", "SQL"]
    assert result.missing_keywords == []
    assert result.coverage_percentage == 100.0
    assert result.total_required_keywords == 2
    assert result.matched_keyword_count == 2


def test_match_keywords_is_case_insensitive_and_preserves_output_capitalization():
    resume = _resume_with_skills("python, fastapi, sql")
    job_description = _job_description_with_required_skills(["Python", "FastAPI", "SQL"])

    result = KeywordMatcher().match_keywords(resume, job_description)

    assert result.matched_keywords == ["FastAPI", "Python", "SQL"]
    assert result.missing_keywords == []


def test_match_keywords_handles_empty_resume_skills():
    resume = _resume_with_skills("")
    job_description = _job_description_with_required_skills(["Python", "FastAPI"])

    result = KeywordMatcher().match_keywords(resume, job_description)

    assert result.matched_keywords == []
    assert result.missing_keywords == ["FastAPI", "Python"]
    assert result.coverage_percentage == 0.0
    assert result.total_required_keywords == 2
    assert result.matched_keyword_count == 0


def test_match_keywords_handles_empty_job_description_skills():
    resume = _resume_with_skills("Python, FastAPI")
    job_description = _job_description_with_required_skills([])

    result = KeywordMatcher().match_keywords(resume, job_description)

    assert result.matched_keywords == []
    assert result.missing_keywords == []
    assert result.coverage_percentage == 100.0
    assert result.total_required_keywords == 0
    assert result.matched_keyword_count == 0
