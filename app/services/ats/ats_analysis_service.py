from app.models.ats import ATSAnalysisResult
from app.models.job_description import JobDescriptionData
from app.models.resume import ResumeData
from app.services.ats.keyword_matcher import KeywordMatcher
from app.services.ats.recommendation_engine import RecommendationEngine
from app.services.ats.score_calculator import ScoreCalculator
from app.services.ats.section_matcher import SectionMatcher


class ATSAnalysisService:
    """Orchestrate the complete deterministic ATS analysis pipeline."""

    def __init__(
        self,
        keyword_matcher: KeywordMatcher | None = None,
        section_matcher: SectionMatcher | None = None,
        score_calculator: ScoreCalculator | None = None,
        recommendation_engine: RecommendationEngine | None = None,
    ) -> None:
        """Create an ATS analysis service from reusable ATS components."""
        self.keyword_matcher = keyword_matcher or KeywordMatcher()
        self.section_matcher = section_matcher or SectionMatcher()
        self.score_calculator = score_calculator or ScoreCalculator()
        self.recommendation_engine = recommendation_engine or RecommendationEngine()

    def analyze(
        self,
        resume: ResumeData,
        job_description: JobDescriptionData,
    ) -> ATSAnalysisResult:
        """Return keyword, section, score, and recommendation analysis results."""
        keyword_match = self.keyword_matcher.match_keywords(resume, job_description)
        section_scores = self.section_matcher.match_sections(resume, job_description)
        ats_score = self.score_calculator.calculate_score(section_scores)
        recommendations = self.recommendation_engine.generate_recommendations(
            keyword_result=keyword_match,
            section_result=section_scores,
            score_result=ats_score,
        )

        return ATSAnalysisResult(
            keyword_match=keyword_match,
            section_scores=section_scores,
            ats_score=ats_score,
            recommendations=recommendations,
        )
