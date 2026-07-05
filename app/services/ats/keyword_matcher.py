import re

from app.models.ats import KeywordMatchResult
from app.models.job_description import JobDescriptionData
from app.models.resume import ResumeData


SKILL_SEPARATOR_PATTERN = re.compile(r"[\n,;|]+")
BULLET_PREFIX_PATTERN = re.compile(r"^\s*(?:[-*]|\d+[.)])\s*")


class KeywordMatcher:
    """Match required job description keywords against resume skills."""

    def match_keywords(
        self,
        resume: ResumeData,
        job_description: JobDescriptionData,
    ) -> KeywordMatchResult:
        """Return deterministic keyword coverage for resume skills."""
        resume_keywords = self._normalized_resume_keywords(resume.sections.skills)
        required_keywords = self._unique_required_keywords(
            job_description.requirements.required_skills
        )

        matched_keywords = []
        missing_keywords = []

        for normalized_keyword, original_keyword in required_keywords.items():
            if normalized_keyword in resume_keywords:
                matched_keywords.append(original_keyword)
            else:
                missing_keywords.append(original_keyword)

        matched_keywords = self._sort_keywords(matched_keywords)
        missing_keywords = self._sort_keywords(missing_keywords)
        total_required_keywords = len(required_keywords)
        matched_keyword_count = len(matched_keywords)
        coverage_percentage = self._coverage_percentage(
            matched_keyword_count=matched_keyword_count,
            total_required_keywords=total_required_keywords,
        )

        return KeywordMatchResult(
            matched_keywords=matched_keywords,
            missing_keywords=missing_keywords,
            coverage_percentage=coverage_percentage,
            total_required_keywords=total_required_keywords,
            matched_keyword_count=matched_keyword_count,
        )

    def _normalized_resume_keywords(self, skills_text: str) -> set[str]:
        return {
            normalized_keyword
            for skill in SKILL_SEPARATOR_PATTERN.split(skills_text)
            if (normalized_keyword := self._normalize_keyword(skill))
        }

    def _unique_required_keywords(self, required_skills: list[str]) -> dict[str, str]:
        keywords = {}
        for skill in required_skills:
            normalized_keyword = self._normalize_keyword(skill)
            if normalized_keyword and normalized_keyword not in keywords:
                keywords[normalized_keyword] = skill.strip()

        return keywords

    def _normalize_keyword(self, keyword: str) -> str:
        clean_keyword = BULLET_PREFIX_PATTERN.sub("", keyword).strip()
        clean_keyword = re.sub(r"\s+", " ", clean_keyword)
        return clean_keyword.casefold()

    def _sort_keywords(self, keywords: list[str]) -> list[str]:
        return sorted(keywords, key=lambda keyword: keyword.casefold())

    def _coverage_percentage(
        self,
        matched_keyword_count: int,
        total_required_keywords: int,
    ) -> float:
        if total_required_keywords == 0:
            return 100.0

        return round((matched_keyword_count / total_required_keywords) * 100, 2)
