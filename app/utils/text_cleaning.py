import re


class TextCleaner:
    """Normalize whitespace in extracted resume text."""

    def clean(self, text: str) -> str:
        """Return deterministic plain text with normalized spacing and paragraphs."""
        normalized_text = text.replace("\r\n", "\n").replace("\r", "\n")
        normalized_text = normalized_text.replace("\t", " ")

        cleaned_lines = []
        blank_line_pending = False

        for line in normalized_text.split("\n"):
            cleaned_line = re.sub(r" {2,}", " ", line).strip()

            if not cleaned_line:
                if cleaned_lines:
                    blank_line_pending = True
                continue

            if blank_line_pending:
                cleaned_lines.append("")
                blank_line_pending = False

            cleaned_lines.append(cleaned_line)

        return "\n".join(cleaned_lines).strip()
