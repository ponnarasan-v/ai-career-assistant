from app.models.ats import ATSScoreResult, SectionMatchResult
from app.services.ats.score_calculator import ScoreCalculator


def test_calculate_score_perfect_score():
    section_result = SectionMatchResult(
        skills_score=100.0,
        education_score=100.0,
        experience_score=100.0,
        projects_score=100.0,
    )

    result = ScoreCalculator().calculate_score(section_result)

    assert result == ATSScoreResult(
        overall_score=100.0,
        skills_score=100.0,
        education_score=100.0,
        experience_score=100.0,
        projects_score=100.0,
    )


def test_calculate_score_partial_score():
    section_result = SectionMatchResult(
        skills_score=50.0,
        education_score=100.0,
        experience_score=100.0,
        projects_score=0.0,
    )

    result = ScoreCalculator().calculate_score(section_result)

    assert result.overall_score == 60.0
    assert result.skills_score == 50.0
    assert result.education_score == 100.0
    assert result.experience_score == 100.0
    assert result.projects_score == 0.0


def test_calculate_score_zero_score():
    section_result = SectionMatchResult(
        skills_score=0.0,
        education_score=0.0,
        experience_score=0.0,
        projects_score=0.0,
    )

    result = ScoreCalculator().calculate_score(section_result)

    assert result.overall_score == 0.0
    assert result.skills_score == 0.0
    assert result.education_score == 0.0
    assert result.experience_score == 0.0
    assert result.projects_score == 0.0


def test_calculate_score_rounds_decimal_values():
    section_result = SectionMatchResult(
        skills_score=66.666,
        education_score=33.333,
        experience_score=50.555,
        projects_score=12.345,
    )

    result = ScoreCalculator().calculate_score(section_result)

    assert result.overall_score == 50.3
    assert result.skills_score == 66.67
    assert result.education_score == 33.33
    assert result.experience_score == 50.55
    assert result.projects_score == 12.35


def test_calculate_score_weighted_calculation_correctness():
    section_result = SectionMatchResult(
        skills_score=80.0,
        education_score=60.0,
        experience_score=40.0,
        projects_score=20.0,
    )

    result = ScoreCalculator().calculate_score(section_result)

    assert result.overall_score == 60.0
    assert result.model_dump() == {
        "overall_score": 60.0,
        "skills_score": 80.0,
        "education_score": 60.0,
        "experience_score": 40.0,
        "projects_score": 20.0,
    }
