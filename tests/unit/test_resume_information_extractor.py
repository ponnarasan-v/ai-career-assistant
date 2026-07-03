from app.services.resume_information_extractor import ResumeInformationExtractor


def test_extract_complete_resume():
    text = """Jane Candidate
jane@example.com | +1 555-123-4567
https://www.linkedin.com/in/janecandidate
https://github.com/janecandidate
https://janecandidate.dev

Professional Summary
Backend developer with Python experience.

Technical Skills
Python, FastAPI, PostgreSQL

Education
B.S. Computer Science

Work Experience
Software Engineer at Example Inc.

Projects
AI Career Assistant

Certifications
AWS Certified Cloud Practitioner

Publications
Resume parsing paper

Achievements
Hackathon winner"""

    result = ResumeInformationExtractor().extract(text)

    assert result["contact"] == {
        "name": "Jane Candidate",
        "email": "jane@example.com",
        "phone": "+1 555-123-4567",
        "linkedin": "https://www.linkedin.com/in/janecandidate",
        "github": "https://github.com/janecandidate",
        "portfolio": "https://janecandidate.dev",
    }
    assert result["sections"]["summary"] == "Backend developer with Python experience."
    assert result["sections"]["skills"] == "Python, FastAPI, PostgreSQL"
    assert result["sections"]["education"] == "B.S. Computer Science"
    assert result["sections"]["experience"] == "Software Engineer at Example Inc."
    assert result["sections"]["projects"] == "AI Career Assistant"
    assert result["sections"]["certifications"] == "AWS Certified Cloud Practitioner"
    assert result["sections"]["publications"] == "Resume parsing paper"
    assert result["sections"]["achievements"] == "Hackathon winner"


def test_extract_returns_empty_strings_for_missing_sections():
    text = """Jane Candidate
jane@example.com

Summary
Backend developer.

Skills
Python"""

    sections = ResumeInformationExtractor().extract(text)["sections"]

    assert sections["summary"] == "Backend developer."
    assert sections["skills"] == "Python"
    assert sections["education"] == ""
    assert sections["experience"] == ""
    assert sections["projects"] == ""
    assert sections["certifications"] == ""
    assert sections["publications"] == ""
    assert sections["achievements"] == ""


def test_extract_returns_empty_strings_for_missing_contact_fields():
    text = """Jane Candidate

Experience
Software Engineer"""

    contact = ResumeInformationExtractor().extract(text)["contact"]

    assert contact == {
        "name": "Jane Candidate",
        "email": "",
        "phone": "",
        "linkedin": "",
        "github": "",
        "portfolio": "",
    }


def test_extract_detects_mixed_case_headings():
    text = """Jane Candidate

pRoFeSsIoNaL sUmMaRy
Python developer.

tEcHnIcAl SkIlLs
Python, SQL

wOrK eXpErIeNcE
Developer at Example Inc."""

    sections = ResumeInformationExtractor().extract(text)["sections"]

    assert sections["summary"] == "Python developer."
    assert sections["skills"] == "Python, SQL"
    assert sections["experience"] == "Developer at Example Inc."


def test_extract_handles_empty_input():
    result = ResumeInformationExtractor().extract("")

    assert result["contact"] == {
        "name": "",
        "email": "",
        "phone": "",
        "linkedin": "",
        "github": "",
        "portfolio": "",
    }
    assert result["sections"] == {
        "summary": "",
        "skills": "",
        "education": "",
        "experience": "",
        "projects": "",
        "certifications": "",
        "publications": "",
        "achievements": "",
    }
