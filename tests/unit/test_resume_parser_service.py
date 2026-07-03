import shutil
from pathlib import Path

import fitz
import pytest

from app.models.resume import ResumeData
from app.services.resume_parser_service import ResumeParserService
from app.utils.file_validation import EmptyFileError, UnsupportedFileTypeError


FIXTURE_TMP_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "resume_parser_service_tmp"


@pytest.fixture
def parser_tmp_dir():
    FIXTURE_TMP_DIR.mkdir(parents=True, exist_ok=True)
    yield FIXTURE_TMP_DIR
    shutil.rmtree(FIXTURE_TMP_DIR, ignore_errors=True)


def _create_pdf(file_path: Path, text: str) -> None:
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), text)
    document.save(file_path)
    document.close()


def test_parse_resume_accepts_valid_pdf(parser_tmp_dir):
    pdf_path = parser_tmp_dir / "resume.pdf"
    _create_pdf(pdf_path, "Jane Candidate\njane@example.com")

    result = ResumeParserService().parse_resume(str(pdf_path))

    assert isinstance(result, ResumeData)
    assert result.contact.name == "Jane Candidate"
    assert result.contact.email == "jane@example.com"


def test_parse_resume_rejects_invalid_extension(parser_tmp_dir):
    text_path = parser_tmp_dir / "resume.txt"
    text_path.write_text("Jane Candidate", encoding="utf-8")

    with pytest.raises(UnsupportedFileTypeError, match="Unsupported file type"):
        ResumeParserService().parse_resume(str(text_path))


def test_parse_resume_rejects_missing_file(parser_tmp_dir):
    missing_path = parser_tmp_dir / "missing.pdf"

    with pytest.raises(FileNotFoundError, match="File not found"):
        ResumeParserService().parse_resume(str(missing_path))


def test_parse_resume_rejects_empty_file(parser_tmp_dir):
    empty_path = parser_tmp_dir / "empty.pdf"
    empty_path.touch()

    with pytest.raises(EmptyFileError, match="File is empty"):
        ResumeParserService().parse_resume(str(empty_path))


def test_parse_resume_runs_successful_end_to_end_pipeline(parser_tmp_dir):
    pdf_path = parser_tmp_dir / "complete_resume.pdf"
    _create_pdf(
        pdf_path,
        "\n".join(
            [
                "Jane Candidate",
                "jane@example.com",
                "Professional Summary",
                "Backend   developer with Python experience.",
                "",
                "Technical Skills",
                "Python,   FastAPI",
                "",
                "Projects",
                "AI Career Assistant",
            ]
        ),
    )

    result = ResumeParserService().parse_resume(str(pdf_path))

    assert result.contact.name == "Jane Candidate"
    assert result.contact.email == "jane@example.com"
    assert result.sections.summary == "Backend developer with Python experience."
    assert result.sections.skills == "Python, FastAPI"
    assert result.sections.projects == "AI Career Assistant"
