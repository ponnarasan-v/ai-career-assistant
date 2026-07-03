import shutil
from pathlib import Path

import pytest

from app.utils.file_validation import (
    EmptyFileError,
    FileTooLargeError,
    FileValidator,
    UnsupportedFileTypeError,
)


FIXTURE_TMP_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "file_validation_tmp"


@pytest.fixture
def validation_tmp_dir():
    FIXTURE_TMP_DIR.mkdir(parents=True, exist_ok=True)
    yield FIXTURE_TMP_DIR
    shutil.rmtree(FIXTURE_TMP_DIR, ignore_errors=True)


def test_validate_accepts_valid_pdf(validation_tmp_dir):
    pdf_path = validation_tmp_dir / "resume.pdf"
    pdf_path.write_bytes(b"%PDF-1.7\nresume")

    assert FileValidator().validate(str(pdf_path)) is None


def test_validate_accepts_valid_docx(validation_tmp_dir):
    docx_path = validation_tmp_dir / "resume.docx"
    docx_path.write_bytes(b"docx content")

    assert FileValidator().validate(str(docx_path)) is None


def test_validate_rejects_unsupported_extension(validation_tmp_dir):
    text_path = validation_tmp_dir / "resume.txt"
    text_path.write_text("resume", encoding="utf-8")

    with pytest.raises(UnsupportedFileTypeError, match="Unsupported file type"):
        FileValidator().validate(str(text_path))


def test_validate_rejects_empty_file(validation_tmp_dir):
    pdf_path = validation_tmp_dir / "empty.pdf"
    pdf_path.touch()

    with pytest.raises(EmptyFileError, match="File is empty"):
        FileValidator().validate(str(pdf_path))


def test_validate_rejects_oversized_file(validation_tmp_dir):
    pdf_path = validation_tmp_dir / "large.pdf"
    pdf_path.write_bytes(b"0" * 11)

    with pytest.raises(FileTooLargeError, match="exceeds maximum allowed size"):
        FileValidator(max_file_size=10).validate(str(pdf_path))


def test_validate_rejects_missing_file(validation_tmp_dir):
    missing_path = validation_tmp_dir / "missing.pdf"

    with pytest.raises(FileNotFoundError, match="File not found"):
        FileValidator().validate(str(missing_path))
