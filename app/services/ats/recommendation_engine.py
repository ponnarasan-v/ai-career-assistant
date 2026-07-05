from app.models.ats import ATSScoreResult, KeywordMatchResult, RecommendationResult, SectionMatchResult


class RecommendationEngine:
    """Generate deterministic resume improvement recommendations from ATS results."""

    def generate_recommendations(
        self,
        keyword_result: KeywordMatchResult,
        section_result: SectionMatchResult,
        score_result: ATSScoreResult,
    ) -> RecommendationResult:
        """Return actionable recommendations based on keyword, section, and score results."""
        recommendations = []

        if keyword_result.missing_keywords:
            missing_keywords = ", ".join(keyword_result.missing_keywords)
            recommendations.append(f"Add the following required skills: {missing_keywords}.")

        if section_result.education_score < 100:
            recommendations.append("Improve education alignment with the job requirements.")

        if section_result.experience_score < 100:
            recommendations.append(
                "Add relevant work, internship, or research experience."
            )

        if section_result.projects_score < 100:
            recommendations.append("Add projects aligned with the job description.")

        if score_result.overall_score < 70:
            recommendations.append("Tailor your resume specifically for this job description.")

        if score_result.overall_score >= 90:
            recommendations.append("Your resume is strongly aligned with this job.")

        return RecommendationResult(
            recommendations=self._deduplicate_recommendations(recommendations)
        )

    def _deduplicate_recommendations(self, recommendations: list[str]) -> list[str]:
        deduplicated = []
        seen = set()

        for recommendation in recommendations:
            if recommendation in seen:
                continue
            seen.add(recommendation)
            deduplicated.append(recommendation)

        return deduplicated
