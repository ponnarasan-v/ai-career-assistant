import re


SECTION_KEYS = (
    "summary",
    "skills",
    "education",
    "experience",
    "projects",
    "certifications",
    "publications",
    "achievements",
)

SECTION_ALIASES = {
    "summary": "summary",
    "professional summary": "summary",
    "technical skills": "skills",
    "skills": "skills",
    "education": "education",
    "experience": "experience",
    "work experience": "experience",
    "projects": "projects",
    "certifications": "certifications",
    "publications": "publications",
    "achievements": "achievements",
}

EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_PATTERN = re.compile(
    r"(?:(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]?\d{4})"
)
URL_PATTERN = re.compile(
    r"\b(?:https?://|www\.)[^\s<>()]+",
    re.IGNORECASE,
)
LINKEDIN_PATTERN = re.compile(
    r"\b(?:https?://)?(?:www\.)?linkedin\.com/[^\s<>()]+",
    re.IGNORECASE,
)
GITHUB_PATTERN = re.compile(
    r"\b(?:https?://)?(?:www\.)?github\.com/[^\s<>()]+",
    re.IGNORECASE,
)


class ResumeInformationExtractor:
    """Extract basic contact fields and resume sections from cleaned text."""

    def extract(self, clean_text: str) -> dict[str, dict[str, str]]:
        """Return deterministic structured information from cleaned resume text."""
        text = clean_text.strip()

        return {
            "contact": self._extract_contact(text),
            "sections": self._extract_sections(text),
        }

    def _extract_contact(self, text: str) -> dict[str, str]:
        contact = {
            "name": self._extract_name(text),
            "email": self._first_match(EMAIL_PATTERN, text),
            "phone": self._first_match(PHONE_PATTERN, text),
            "linkedin": self._first_match(LINKEDIN_PATTERN, text),
            "github": self._first_match(GITHUB_PATTERN, text),
            "portfolio": self._extract_portfolio(text),
        }
        return contact

    def _extract_sections(self, text: str) -> dict[str, str]:
        sections = {key: "" for key in SECTION_KEYS}
        section_lines = {key: [] for key in SECTION_KEYS}
        current_section = ""

        for line in text.splitlines():
            heading, inline_content = self._detect_section_heading(line)
            if heading:
                current_section = heading
                if inline_content:
                    section_lines[current_section].append(inline_content)
                continue

            if current_section:
                section_lines[current_section].append(line)

        for key, lines in section_lines.items():
            sections[key] = "\n".join(lines).strip()

        return sections

    def _extract_name(self, text: str) -> str:
        for line in text.splitlines():
            candidate = line.strip()
            if not candidate:
                continue
            if self._detect_section_heading(candidate)[0]:
                return ""
            if self._looks_like_contact_line(candidate):
                continue
            return candidate

        return ""

    def _extract_portfolio(self, text: str) -> str:
        for match in URL_PATTERN.finditer(text):
            url = match.group(0).rstrip(".,;")
            normalized_url = url.lower()
            if "linkedin.com/" not in normalized_url and "github.com/" not in normalized_url:
                return url

        return ""

    def _detect_section_heading(self, line: str) -> tuple[str, str]:
        normalized_line = line.strip()
        if not normalized_line:
            return "", ""

        heading_text = normalized_line.rstrip(":").strip().lower()
        if heading_text in SECTION_ALIASES:
            return SECTION_ALIASES[heading_text], ""

        if ":" in normalized_line:
            possible_heading, inline_content = normalized_line.split(":", 1)
            canonical_heading = SECTION_ALIASES.get(possible_heading.strip().lower())
            if canonical_heading:
                return canonical_heading, inline_content.strip()

        return "", ""

    def _looks_like_contact_line(self, line: str) -> bool:
        lower_line = line.lower()
        return (
            bool(EMAIL_PATTERN.search(line))
            or bool(PHONE_PATTERN.search(line))
            or "linkedin.com/" in lower_line
            or "github.com/" in lower_line
            or lower_line.startswith(("http://", "https://", "www."))
        )

    def _first_match(self, pattern: re.Pattern[str], text: str) -> str:
        match = pattern.search(text)
        if not match:
            return ""

        return match.group(0).rstrip(".,;")
