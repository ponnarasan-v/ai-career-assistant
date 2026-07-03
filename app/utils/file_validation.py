from pathlib import Path


DEFAULT_MAX_FILE_SIZE = 10 * 1024 * 1024
SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


class UnsupportedFileTypeError(ValueError):
    """Raised when a file extension is not supported."""


class EmptyFileError(ValueError):
    """Raised when a file exists but has no content."""


class FileTooLargeError(ValueError):
    """Raised when a file exceeds the configured maximum size."""


class FileValidator:
    """Validate uploaded resume files before document processing."""

    def __init__(self, max_file_size: int = DEFAULT_MAX_FILE_SIZE) -> None:
        """Create a validator with a configurable maximum file size in bytes."""
        if max_file_size <= 0:
            raise ValueError("Maximum file size must be greater than zero.")

        self.max_file_size = max_file_size

    def validate(self, file_path: str) -> None:
        """Validate that a file exists, is readable, supported, and within size limits."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        if not path.is_file():
            raise FileNotFoundError(f"Path is not a file: {file_path}")

        file_size = path.stat().st_size
        if file_size == 0:
            raise EmptyFileError(f"File is empty: {file_path}")

        extension = path.suffix.lower()
        if extension not in SUPPORTED_EXTENSIONS:
            raise UnsupportedFileTypeError(f"Unsupported file type: {extension or 'unknown'}")

        if file_size > self.max_file_size:
            raise FileTooLargeError(
                f"File size {file_size} bytes exceeds maximum allowed size "
                f"of {self.max_file_size} bytes."
            )
