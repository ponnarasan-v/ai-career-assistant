from app.models.ats import ATSAnalysisResult
from app.models.job_description import JobDescriptionData, JobRequirements
from app.models.resume import ResumeData, ResumeSections
from app.services.ats.ats_analysis_service import ATSAnalysisService


def _resume(
    skills: str = "",
    education: str = "",
    experience: str = "",
    projects: str = "",
) -> ResumeData:
    return ResumeData(
        sections=ResumeSections(
            skills=skills,
            education=education,
            experience=experience,
            projects=projects,
        )
    )


def _job_description(
    required_skills: list[str] | None = None,
    education: list[str] | None = None,
    experience: list[str] | None = None,
    responsibilities: list[str] | None = None,
) -> JobDescriptionData:
    return JobDescriptionData(
        requirements=JobRequirements(
            required_skills=required_skills or [],
            education=education or [],
            experience=experience or [],
            responsibilities=responsibilities or [],
        )
    )


def test_analyze_complete_workflow():
    resume = _resume(
        skills="Python, FastAPI",
        education="B.S. Computer Science",
        experience="Software Engineer",
        projects="API project",
    )
    job_description = _job_description(
        required_skills=["Python", "FastAPI"],
        education=["Bachelor's degree"],
        experience=["2+ years"],
        responsibilities=["Build APIs"],
    )

    result = ATSAnalysisService().analyze(resume, job_description)

    assert isinstance(result, ATSAnalysisResult)
    assert result.keyword_match.coverage_percentage == 100.0
    assert result.section_scores.skills_score == 100.0
    assert result.ats_score.overall_score == 100.0
    assert result.recommendations.recommendations == [
        "Your resume is strongly aligned with this job."
    ]


def test_analyze_empty_resume():
    resume = _resume()
    job_description = _job_description(
        required_skills=["Python", "FastAPI"],
        education=["Bachelor's degree"],
        experience=["2+ years"],
        responsibilities=["Build APIs"],
    )

    result = ATSAnalysisService().analyze(resume, job_description)

    assert result.keyword_match.missing_keywords == ["FastAPI", "Python"]
    assert result.section_scores.education_score == 0.0
    assert result.section_scores.experience_score == 0.0
    assert result.section_scores.projects_score == 0.0
    assert result.ats_score.overall_score == 0.0
    assert "Tailor your resume specifically for this job description." in (
        result.recommendations.recommendations
    )


def test_analyze_empty_job_description():
    resume = _resume(
        skills="Python, FastAPI",
        education="B.S. Computer Science",
        experience="Software Engineer",
        projects="API project",
    )
    job_description = _job_description()

    result = ATSAnalysisService().analyze(resume, job_description)

    assert result.keyword_match.coverage_percentage == 100.0
    assert result.keyword_match.total_required_keywords == 0
    assert result.section_scores.skills_score == 100.0
    assert result.ats_score.overall_score == 100.0
    assert result.recommendations.recommendations == [
        "Your resume is strongly aligned with this job."
    ]


def test_analyze_missing_skills():
    resume = _resume(
        skills="Python",
        education="B.S. Computer Science",
        experience="Software Engineer",
        projects="API project",
    )
    job_description = _job_description(
        required_skills=["Python", "FastAPI", "SQL"],
        education=["Bachelor's degree"],
        experience=["2+ years"],
        responsibilities=["Build APIs"],
    )

    result = ATSAnalysisService().analyze(resume, job_description)

    assert result.keyword_match.matched_keywords == ["Python"]
    assert result.keyword_match.missing_keywords == ["FastAPI", "SQL"]
    assert result.section_scores.skills_score == 33.33
    assert result.ats_score.overall_score == 66.66
    assert result.recommendations.recommendations == [
        "Add the following required skills: FastAPI, SQL.",
        "Tailor your resume specifically for this job description.",
    ]


def test_analyze_perfect_match():
    resume = _resume(
        skills="Python, FastAPI, SQL",
        education="B.S. Computer Science",
        experience="Software Engineer",
        projects="API project",
    )
    job_description = _job_description(
        required_skills=["Python", "FastAPI", "SQL"],
        education=["Bachelor's degree"],
        experience=["2+ years"],
        responsibilities=["Build APIs"],
    )

    result = ATSAnalysisService().analyze(resume, job_description)

    assert result.keyword_match.matched_keywords == ["FastAPI", "Python", "SQL"]
    assert result.keyword_match.missing_keywords == []
    assert result.section_scores.model_dump() == {
        "skills_score": 100.0,
        "education_score": 100.0,
        "experience_score": 100.0,
        "projects_score": 100.0,
    }
    assert result.ats_score.overall_score == 100.0
