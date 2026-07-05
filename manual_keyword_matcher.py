import json

from app.models.resume import ResumeData
from app.models.job_description import JobDescriptionData, JobRequirements
from app.services.ats.keyword_matcher import KeywordMatcher


# Create a sample ResumeData object
resume = ResumeData(
    contact={},
    sections={
        "skills": "Python\nFastAPI\nPyTorch\nSQL"
    }
)

# Create a sample JobDescriptionData object
job_description = JobDescriptionData(
    job_title="AI Engineer",
    company="OpenAI",
    location="Remote",
    employment_type="Full-time",
    requirements=JobRequirements(
        required_skills=[
            "Python",
            "Docker",
            "FastAPI",
            "AWS",
            "SQL",
        ]
    ),
    raw_text="",
    clean_text="",
)

matcher = KeywordMatcher()

result = matcher.match_keywords(
    resume=resume,
    job_description=job_description,
)

# Pydantic v2
print(json.dumps(result.model_dump(), indent=2))

# If you're using Pydantic v1 instead, replace the line above with:
# print(json.dumps(result.dict(), indent=2))