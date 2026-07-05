from app.models.job_description import JobDescriptionData
from app.services.job_description_information_extractor import JobDescriptionInformationExtractor


def test_extract_complete_job_description():
    text = """Job Title: Backend Engineer
Company: Example Inc.
Location: Remote
Employment Type: Full-time

Responsibilities
- Build APIs
- Maintain services

Required Skills
Python, FastAPI

Preferred Qualifications
- AWS
- Docker

Qualifications
- Strong communication

Education
- Bachelor's degree

Experience
- 3+ years backend development

Tools and Technologies
PostgreSQL, Redis"""

    result = JobDescriptionInformationExtractor().extract(text)

    assert isinstance(result, JobDescriptionData)
    assert result.job_title == "Backend Engineer"
    assert result.company == "Example Inc."
    assert result.location == "Remote"
    assert result.employment_type == "Full-time"
    assert result.requirements.responsibilities == ["Build APIs", "Maintain services"]
    assert result.requirements.required_skills == ["Python", "FastAPI"]
    assert result.requirements.preferred_skills == ["AWS", "Docker"]
    assert result.requirements.qualifications == ["Strong communication"]
    assert result.requirements.education == ["Bachelor's degree"]
    assert result.requirements.experience == ["3+ years backend development"]
    assert result.requirements.tools_and_technologies == ["PostgreSQL", "Redis"]
    assert result.raw_text == text
    assert result.clean_text == text


def test_extract_missing_sections_uses_empty_lists():
    text = """Data Analyst
Company: Example Inc.

Skills
SQL, Python"""

    result = JobDescriptionInformationExtractor().extract(text)

    assert result.job_title == "Data Analyst"
    assert result.company == "Example Inc."
    assert result.location == ""
    assert result.employment_type == ""
    assert result.requirements.required_skills == ["SQL", "Python"]
    assert result.requirements.responsibilities == []
    assert result.requirements.qualifications == []
    assert result.requirements.education == []
    assert result.requirements.experience == []
    assert result.requirements.tools_and_technologies == []


def test_extract_switches_from_required_skills_to_preferred_skills():
    text = """Required Skills
- Python
- FastAPI
- SQL

Preferred Skills
- Docker
- AWS"""

    result = JobDescriptionInformationExtractor().extract(text)

    assert result.requirements.required_skills == ["Python", "FastAPI", "SQL"]
    assert result.requirements.preferred_skills == ["Docker", "AWS"]


def test_extract_detects_mixed_case_headings():
    text = """Title: Machine Learning Engineer

rEsPoNsIbIlItIeS
- Build training pipelines

nIcE tO hAvE
- Kubernetes

tEcH sTaCk
Python | PyTorch"""

    result = JobDescriptionInformationExtractor().extract(text)

    assert result.job_title == "Machine Learning Engineer"
    assert result.requirements.responsibilities == ["Build training pipelines"]
    assert result.requirements.preferred_skills == ["Kubernetes"]
    assert result.requirements.tools_and_technologies == ["Python", "PyTorch"]


def test_extract_handles_empty_input():
    result = JobDescriptionInformationExtractor().extract("")

    assert result == JobDescriptionData()


def test_extract_serialization():
    result = JobDescriptionInformationExtractor().extract(
        """Job Title: Backend Engineer

Skills: Python, FastAPI"""
    )

    assert result.model_dump() == {
        "job_title": "Backend Engineer",
        "company": "",
        "location": "",
        "employment_type": "",
        "requirements": {
            "required_skills": ["Python", "FastAPI"],
            "preferred_skills": [],
            "responsibilities": [],
            "qualifications": [],
            "education": [],
            "experience": [],
            "tools_and_technologies": [],
        },
        "raw_text": "Job Title: Backend Engineer\n\nSkills: Python, FastAPI",
        "clean_text": "Job Title: Backend Engineer\n\nSkills: Python, FastAPI",
    }
