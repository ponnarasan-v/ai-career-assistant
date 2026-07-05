from app.models.job_description import JobDescriptionData, JobRequirements
from app.models.resume import ResumeData, ResumeSections
from app.services.ats.section_matcher import SectionMatcher


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


def test_match_sections_complete_match():
    resume = _resume(
        skills="Python, FastAPI",
        education="B.S. Computer Science",
        experience="Software Engineer",
        projects="AI Career Assistant",
    )
    job_description = _job_description(
        required_skills=["Python", "FastAPI"],
        education=["Bachelor's degree"],
        experience=["3+ years"],
        responsibilities=["Build APIs"],
    )

    result = SectionMatcher().match_sections(resume, job_description)

    assert result.skills_score == 100.0
    assert result.education_score == 100.0
    assert result.experience_score == 100.0
    assert result.projects_score == 100.0


def test_match_sections_missing_projects():
    resume = _resume(
        skills="Python, FastAPI",
        education="B.S. Computer Science",
        experience="Software Engineer",
    )
    job_description = _job_description(
        required_skills=["Python", "FastAPI"],
        education=["Bachelor's degree"],
        experience=["3+ years"],
        responsibilities=["Build APIs"],
    )

    result = SectionMatcher().match_sections(resume, job_description)

    assert result.skills_score == 100.0
    assert result.education_score == 100.0
    assert result.experience_score == 100.0
    assert result.projects_score == 0.0


def test_match_sections_missing_education():
    resume = _resume(
        skills="Python, FastAPI",
        experience="Software Engineer",
        projects="AI Career Assistant",
    )
    job_description = _job_description(
        required_skills=["Python", "FastAPI"],
        education=["Bachelor's degree"],
        experience=["3+ years"],
        responsibilities=["Build APIs"],
    )

    result = SectionMatcher().match_sections(resume, job_description)

    assert result.skills_score == 100.0
    assert result.education_score == 0.0
    assert result.experience_score == 100.0
    assert result.projects_score == 100.0


def test_match_sections_empty_resume():
    resume = _resume()
    job_description = _job_description(
        required_skills=["Python", "FastAPI"],
        education=["Bachelor's degree"],
        experience=["3+ years"],
        responsibilities=["Build APIs"],
    )

    result = SectionMatcher().match_sections(resume, job_description)

    assert result.skills_score == 0.0
    assert result.education_score == 0.0
    assert result.experience_score == 0.0
    assert result.projects_score == 0.0


def test_match_sections_empty_job_description():
    resume = _resume(
        skills="Python, FastAPI",
        education="B.S. Computer Science",
        experience="Software Engineer",
        projects="AI Career Assistant",
    )
    job_description = _job_description()

    result = SectionMatcher().match_sections(resume, job_description)

    assert result.skills_score == 100.0
    assert result.education_score == 100.0
    assert result.experience_score == 100.0
    assert result.projects_score == 100.0
