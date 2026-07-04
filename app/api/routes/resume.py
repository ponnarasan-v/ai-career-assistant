import logging
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.models.resume import ResumeData
from app.services.resume_parser_service import ResumeParserService
from app.utils.file_validation import EmptyFileError, FileTooLargeError, UnsupportedFileTypeError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/resume", tags=["resume"])


@router.post("/parse", response_model=ResumeData)
async def parse_resume(file: UploadFile = File(...)) -> ResumeData:
    """Parse an uploaded PDF or DOCX resume into structured resume data."""
    temp_path = _save_upload_to_temp_file(file)

    try:
        return ResumeParserService().parse_resume(str(temp_path))
    except (UnsupportedFileTypeError, EmptyFileError, FileTooLargeError, FileNotFoundError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except RuntimeError as exc:
        logger.exception("Resume parsing failed for uploaded file: %s", file.filename)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Unable to parse uploaded resume.",
        ) from exc
    except Exception as exc:
        logger.exception("Unexpected resume parsing error for uploaded file: %s", file.filename)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected resume parsing error.",
        ) from exc
    finally:
        temp_path.unlink(missing_ok=True)


def _save_upload_to_temp_file(file: UploadFile) -> Path:
    """Persist an uploaded file to a temporary path and return that path."""
    suffix = Path(file.filename or "").suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(file.file.read())
        return Path(temp_file.name)
