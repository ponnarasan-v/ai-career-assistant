import re

from app.models.job_description import JobDescriptionData, JobRequirements


SECTION_ALIASES = {
    "responsibilities": "responsibilities",
    "key responsibilities": "responsibilities",
    "requirements": "qualifications",
    "required qualifications": "qualifications",
    "qualifications": "qualifications",
    "preferred qualifications": "preferred_skills",
    "preferred skills": "preferred_skills",
    "skills": "required_skills",
    "required skills": "required_skills",
    "technical skills": "required_skills",
    "education": "education",
    "experience": "experience",
    "nice to have": "preferred_skills",
    "nice-to-have": "preferred_skills",
    "tools": "tools_and_technologies",
    "technologies": "tools_and_technologies",
    "tools and technologies": "tools_and_technologies",
    "tech stack": "tools_and_technologies",
    "benefits": "benefits",
}

METADATA_ALIASES = {
    "job title": "job_title",
    "title": "job_title",
    "company": "company",
    "organization": "company",
    "location": "location",
    "employment type": "employment_type",
    "job type": "employment_type",
}

BULLET_PATTERN = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s*")


class JobDescriptionInformationExtractor:
    """Extract structured job description data using deterministic parsing."""

    def extract(self, clean_text: str) -> JobDescriptionData:
        """Return parsed job description data from cleaned job description text."""
        text = clean_text.strip()
        metadata = self._extract_metadata(text)
        section_lines = self._extract_section_lines(text)

        requirements = JobRequirements(
            required_skills=self._split_skill_items(section_lines["required_skills"]),
            preferred_skills=self._split_skill_items(section_lines["preferred_skills"]),
            responsibilities=self._line_items(section_lines["responsibilities"]),
            qualifications=self._line_items(section_lines["qualifications"]),
            education=self._line_items(section_lines["education"]),
            experience=self._line_items(section_lines["experience"]),
            tools_and_technologies=self._split_skill_items(section_lines["tools_and_technologies"]),
        )

        return JobDescriptionData(
            job_title=metadata["job_title"],
            company=metadata["company"],
            location=metadata["location"],
            employment_type=metadata["employment_type"],
            requirements=requirements,
            raw_text=clean_text,
            clean_text=text,
        )

    def _extract_metadata(self, text: str) -> dict[str, str]:
        metadata = {
            "job_title": "",
            "company": "",
            "location": "",
            "employment_type": "",
        }

        for line in text.splitlines():
            key, value = self._split_key_value(line)
            metadata_key = METADATA_ALIASES.get(key)
            if metadata_key and value and not metadata[metadata_key]:
                metadata[metadata_key] = value

        if not metadata["job_title"]:
            metadata["job_title"] = self._first_title_candidate(text)

        return metadata

    def _extract_section_lines(self, text: str) -> dict[str, list[str]]:
        section_lines = {
            "required_skills": [],
            "preferred_skills": [],
            "responsibilities": [],
            "qualifications": [],
            "education": [],
            "experience": [],
            "tools_and_technologies": [],
            "benefits": [],
        }
        current_section = ""

        for line in text.splitlines():
            section, inline_content = self._detect_section_heading(line)
            if section:
                current_section = section
                if inline_content and section in section_lines:
                    section_lines[section].append(inline_content)
                continue

            if current_section and current_section in section_lines:
                if not self._is_metadata_line(line):
                    section_lines[current_section].append(line)

        return section_lines

    def _detect_section_heading(self, line: str) -> tuple[str, str]:
        normalized_line = line.strip()
        if not normalized_line:
            return "", ""

        heading = normalized_line.rstrip(":").strip().lower()
        if heading in SECTION_ALIASES:
            return SECTION_ALIASES[heading], ""

        if ":" in normalized_line:
            possible_heading, inline_content = normalized_line.split(":", 1)
            section = SECTION_ALIASES.get(possible_heading.strip().lower())
            if section:
                return section, inline_content.strip()

        return "", ""

    def _split_key_value(self, line: str) -> tuple[str, str]:
        if ":" not in line:
            return "", ""

        key, value = line.split(":", 1)
        return key.strip().lower(), value.strip()

    def _is_metadata_line(self, line: str) -> bool:
        key, value = self._split_key_value(line)
        return bool(value and key in METADATA_ALIASES)

    def _first_title_candidate(self, text: str) -> str:
        for line in text.splitlines():
            candidate = line.strip()
            if not candidate:
                continue
            if self._detect_section_heading(candidate)[0] or self._is_metadata_line(candidate):
                continue
            if BULLET_PATTERN.match(candidate):
                continue
            return candidate

        return ""

    def _line_items(self, lines: list[str]) -> list[str]:
        items = []
        for line in lines:
            item = BULLET_PATTERN.sub("", line).strip()
            if item:
                items.append(item)

        return items

    def _split_skill_items(self, lines: list[str]) -> list[str]:
        items = []
        for line in self._line_items(lines):
            parts = re.split(r"[,;|]", line)
            for part in parts:
                item = part.strip()
                if item:
                    items.append(item)

        return items
