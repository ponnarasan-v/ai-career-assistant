from app.models.ats import SectionMatchResult
from app.models.job_description import JobDescriptionData
from app.models.resume import ResumeData
from app.services.ats.keyword_matcher import KeywordMatcher


class SectionMatcher:
    """Compute deterministic ATS compatibility scores for resume sections."""

    def __init__(self, keyword_matcher: KeywordMatcher | None = None) -> None:
        """Create a section matcher with an optional keyword matcher dependency."""
        self.keyword_matcher = keyword_matcher or KeywordMatcher()

    def match_sections(
        self,
        resume: ResumeData,
        job_description: JobDescriptionData,
    ) -> SectionMatchResult:
        """Return independent compatibility scores for major resume sections."""
        skills_score = self.keyword_matcher.match_keywords(
            resume=resume,
            job_description=job_description,
        ).coverage_percentage

        return SectionMatchResult(
            skills_score=self._round_score(skills_score),
            education_score=self._education_score(resume, job_description),
            experience_score=self._experience_score(resume, job_description),
            projects_score=self._projects_score(resume, job_description),
        )

    def _education_score(
        self,
        resume: ResumeData,
        job_description: JobDescriptionData,
    ) -> float:
        if not job_description.requirements.education:
            return 100.0

        if resume.sections.education.strip():
            return 100.0

        return 0.0

    def _experience_score(
        self,
        resume: ResumeData,
        job_description: JobDescriptionData,
    ) -> float:
        if not job_description.requirements.experience:
            return 100.0

        if resume.sections.experience.strip():
            return 100.0

        return 0.0

    def _projects_score(
        self,
        resume: ResumeData,
        job_description: JobDescriptionData,
    ) -> float:
        if not job_description.requirements.responsibilities:
            return 100.0

        if resume.sections.projects.strip():
            return 100.0

        return 0.0

    def _round_score(self, score: float) -> float:
        return round(score, 2)
