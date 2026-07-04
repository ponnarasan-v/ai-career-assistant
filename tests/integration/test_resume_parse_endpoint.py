from io import BytesIO

import fitz
from docx import Document
from fastapi.testclient import TestClient

from app.api.main import app


client = TestClient(app)


def _create_pdf_bytes(text: str) -> bytes:
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), text)
    pdf_bytes = document.tobytes()
    document.close()
    return pdf_bytes


def _create_docx_bytes(paragraphs: list[str]) -> bytes:
    document = Document()
    for paragraph in paragraphs:
        document.add_paragraph(paragraph)

    output = BytesIO()
    document.save(output)
    return output.getvalue()


def test_parse_resume_endpoint_accepts_pdf_upload():
    pdf_bytes = _create_pdf_bytes(
        "\n".join(
            [
                "Jane Candidate",
                "jane@example.com",
                "Professional Summary",
                "Backend developer.",
            ]
        )
    )

    response = client.post(
        "/resume/parse",
        files={"file": ("resume.pdf", pdf_bytes, "application/pdf")},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["contact"]["name"] == "Jane Candidate"
    assert data["contact"]["email"] == "jane@example.com"
    assert data["sections"]["summary"] == "Backend developer."


def test_parse_resume_endpoint_accepts_docx_upload():
    docx_bytes = _create_docx_bytes(
        [
            "Jane Candidate",
            "jane@example.com",
            "Skills",
            "Python, FastAPI",
        ]
    )

    response = client.post(
        "/resume/parse",
        files={
            "file": (
                "resume.docx",
                docx_bytes,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["contact"]["name"] == "Jane Candidate"
    assert data["contact"]["email"] == "jane@example.com"
    assert data["sections"]["skills"] == "Python, FastAPI"


def test_parse_resume_endpoint_rejects_unsupported_file_type():
    response = client.post(
        "/resume/parse",
        files={"file": ("resume.txt", b"Jane Candidate", "text/plain")},
    )

    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]


def test_parse_resume_endpoint_rejects_empty_file():
    response = client.post(
        "/resume/parse",
        files={"file": ("resume.pdf", b"", "application/pdf")},
    )

    assert response.status_code == 400
    assert "File is empty" in response.json()["detail"]


def test_parse_resume_endpoint_handles_parsing_failure():
    response = client.post(
        "/resume/parse",
        files={"file": ("resume.pdf", b"not a real pdf", "application/pdf")},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "Unable to parse uploaded resume."
