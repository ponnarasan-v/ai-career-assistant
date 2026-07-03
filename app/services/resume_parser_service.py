from app.models.resume import ResumeData
from app.services.document_service import DocumentService
from app.services.resume_information_extractor import ResumeInformationExtractor
from app.utils.file_validation import FileValidator
from app.utils.text_cleaning import TextCleaner


class ResumeParserService:
    """Orchestrate the complete resume parsing pipeline."""

    def __init__(
        self,
        file_validator: FileValidator | None = None,
        document_service: DocumentService | None = None,
        text_cleaner: TextCleaner | None = None,
        information_extractor: ResumeInformationExtractor | None = None,
    ) -> None:
        """Create a parser service from reusable resume processing components."""
        self.file_validator = file_validator or FileValidator()
        self.document_service = document_service or DocumentService()
        self.text_cleaner = text_cleaner or TextCleaner()
        self.information_extractor = information_extractor or ResumeInformationExtractor()

    def parse_resume(self, file_path: str) -> ResumeData:
        """Validate, extract, clean, and structure resume information."""
        self.file_validator.validate(file_path)
        extracted_text = self.document_service.extract_text(file_path)
        clean_text = self.text_cleaner.clean(extracted_text)
        return self.information_extractor.extract(clean_text)
