import pytest
from pydantic import ValidationError

from app.models.job_description import JobDescriptionData, JobRequirements


def test_job_description_model_creation():
    requirements = JobRequirements(
        required_skills=["Python", "FastAPI"],
        preferred_skills=["Docker"],
        responsibilities=["Build APIs"],
        qualifications=["Strong communication"],
        education=["Bachelor's degree"],
        experience=["3+ years"],
        tools_and_technologies=["PostgreSQL"],
    )

    job_description = JobDescriptionData(
        job_title="Backend Engineer",
        company="Example Inc.",
        location="Remote",
        employment_type="Full-time",
        requirements=requirements,
        raw_text="Raw job description",
        clean_text="Clean job description",
    )

    assert job_description.job_title == "Backend Engineer"
    assert job_description.company == "Example Inc."
    assert job_description.requirements.required_skills == ["Python", "FastAPI"]
    assert job_description.requirements.tools_and_technologies == ["PostgreSQL"]


def test_job_description_empty_defaults_are_independent():
    first = JobDescriptionData()
    second = JobDescriptionData()

    assert first.job_title == ""
    assert first.requirements == JobRequirements()
    assert first.requirements.required_skills == []

    first.requirements.required_skills.append("Python")

    assert second.requirements.required_skills == []


def test_job_description_serialization():
    job_description = JobDescriptionData(
        job_title="Backend Engineer",
        requirements=JobRequirements(required_skills=["Python"]),
        clean_text="Backend Engineer role",
    )

    assert job_description.model_dump() == {
        "job_title": "Backend Engineer",
        "company": "",
        "location": "",
        "employment_type": "",
        "requirements": {
            "required_skills": ["Python"],
            "preferred_skills": [],
            "responsibilities": [],
            "qualifications": [],
            "education": [],
            "experience": [],
            "tools_and_technologies": [],
        },
        "raw_text": "",
        "clean_text": "Backend Engineer role",
    }


def test_job_description_nested_model_validation_from_dict():
    job_description = JobDescriptionData(
        requirements={
            "required_skills": ["Python"],
            "preferred_skills": ["AWS"],
            "responsibilities": ["Own backend services"],
        }
    )

    assert isinstance(job_description.requirements, JobRequirements)
    assert job_description.requirements.required_skills == ["Python"]
    assert job_description.requirements.preferred_skills == ["AWS"]
    assert job_description.requirements.responsibilities == ["Own backend services"]


def test_job_description_nested_model_rejects_invalid_list_value():
    with pytest.raises(ValidationError):
        JobDescriptionData(requirements={"required_skills": "Python"})
