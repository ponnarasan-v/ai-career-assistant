from pathlib import Path

import fitz
from docx import Document


class DocumentService:
    """Extract plain text from supported resume document formats."""

    def extract_text(self, file_path: str) -> str:
        """Extract text from a PDF or DOCX file based on its extension."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")
        if not path.is_file():
            raise FileNotFoundError(f"Document path is not a file: {file_path}")

        extension = path.suffix.lower()
        if extension == ".pdf":
            return self._extract_pdf(str(path))
        if extension == ".docx":
            return self._extract_docx(str(path))

        raise ValueError(f"Unsupported document type: {extension or 'unknown'}")

    def _extract_pdf(self, file_path: str) -> str:
        """Extract plain text from a PDF while preserving page breaks."""
        try:
            with fitz.open(file_path) as document:
                pages = [page.get_text("text").strip() for page in document]
        except Exception as exc:
            raise RuntimeError(f"Unable to read PDF document: {file_path}") from exc

        return "\n\n".join(page for page in pages if page)

    def _extract_docx(self, file_path: str) -> str:
        """Extract plain text from a DOCX while preserving paragraph breaks."""
        try:
            document = Document(file_path)
            paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs]
        except Exception as exc:
            raise RuntimeError(f"Unable to read DOCX document: {file_path}") from exc

        return "\n\n".join(paragraph for paragraph in paragraphs if paragraph)
