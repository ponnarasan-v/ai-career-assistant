from app.models.ats import ATSScoreResult, KeywordMatchResult, SectionMatchResult
from app.services.ats.recommendation_engine import RecommendationEngine


def test_generate_recommendations_high_score():
    result = RecommendationEngine().generate_recommendations(
        keyword_result=KeywordMatchResult(),
        section_result=SectionMatchResult(),
        score_result=ATSScoreResult(overall_score=95.0),
    )

    assert result.recommendations == ["Your resume is strongly aligned with this job."]


def test_generate_recommendations_low_score():
    result = RecommendationEngine().generate_recommendations(
        keyword_result=KeywordMatchResult(),
        section_result=SectionMatchResult(),
        score_result=ATSScoreResult(overall_score=65.0),
    )

    assert result.recommendations == [
        "Tailor your resume specifically for this job description."
    ]


def test_generate_recommendations_missing_skills():
    result = RecommendationEngine().generate_recommendations(
        keyword_result=KeywordMatchResult(missing_keywords=["FastAPI", "SQL"]),
        section_result=SectionMatchResult(),
        score_result=ATSScoreResult(overall_score=85.0),
    )

    assert result.recommendations == [
        "Add the following required skills: FastAPI, SQL."
    ]


def test_generate_recommendations_missing_experience():
    result = RecommendationEngine().generate_recommendations(
        keyword_result=KeywordMatchResult(),
        section_result=SectionMatchResult(experience_score=0.0),
        score_result=ATSScoreResult(overall_score=80.0),
    )

    assert result.recommendations == [
        "Add relevant work, internship, or research experience."
    ]


def test_generate_recommendations_missing_projects():
    result = RecommendationEngine().generate_recommendations(
        keyword_result=KeywordMatchResult(),
        section_result=SectionMatchResult(projects_score=0.0),
        score_result=ATSScoreResult(overall_score=80.0),
    )

    assert result.recommendations == ["Add projects aligned with the job description."]


def test_generate_recommendations_prevents_duplicates():
    engine = RecommendationEngine()

    result = engine._deduplicate_recommendations(
        [
            "Tailor your resume specifically for this job description.",
            "Tailor your resume specifically for this job description.",
            "Add projects aligned with the job description.",
        ]
    )

    assert result == [
        "Tailor your resume specifically for this job description.",
        "Add projects aligned with the job description.",
    ]
