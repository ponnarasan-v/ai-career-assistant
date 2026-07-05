from app.models.ats import ATSScoreResult, SectionMatchResult


SKILLS_WEIGHT = 0.50
EDUCATION_WEIGHT = 0.15
EXPERIENCE_WEIGHT = 0.20
PROJECTS_WEIGHT = 0.15


class ScoreCalculator:
    """Calculate a weighted ATS compatibility score from section scores."""

    def calculate_score(self, section_result: SectionMatchResult) -> ATSScoreResult:
        """Return the weighted overall score while preserving section scores."""
        overall_score = (
            section_result.skills_score * SKILLS_WEIGHT
            + section_result.education_score * EDUCATION_WEIGHT
            + section_result.experience_score * EXPERIENCE_WEIGHT
            + section_result.projects_score * PROJECTS_WEIGHT
        )

        return ATSScoreResult(
            overall_score=round(overall_score, 2),
            skills_score=round(section_result.skills_score, 2),
            education_score=round(section_result.education_score, 2),
            experience_score=round(section_result.experience_score, 2),
            projects_score=round(section_result.projects_score, 2),
        )
