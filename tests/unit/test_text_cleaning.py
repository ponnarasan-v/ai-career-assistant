from app.utils.text_cleaning import TextCleaner


def test_clean_collapses_extra_spaces():
    text = "Jane   Candidate\nPython    Developer"

    assert TextCleaner().clean(text) == "Jane Candidate\nPython Developer"


def test_clean_converts_tabs_to_spaces():
    text = "Skills:\tPython\tFastAPI"

    assert TextCleaner().clean(text) == "Skills: Python FastAPI"


def test_clean_collapses_repeated_blank_lines():
    text = "Summary\n\n\nExperienced developer\n\n\n\nSkills"

    assert TextCleaner().clean(text) == "Summary\n\nExperienced developer\n\nSkills"


def test_clean_normalizes_mixed_line_endings():
    text = "Summary\r\nDeveloper\rSkills\nPython"

    assert TextCleaner().clean(text) == "Summary\nDeveloper\nSkills\nPython"


def test_clean_handles_empty_string():
    assert TextCleaner().clean("") == ""


def test_clean_preserves_already_clean_text():
    text = "Summary\n\nExperienced developer\n\nSkills\nPython"

    assert TextCleaner().clean(text) == text
