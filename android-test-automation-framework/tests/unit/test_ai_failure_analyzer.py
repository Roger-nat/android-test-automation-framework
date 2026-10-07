from utils.ai_failure_analyzer import analyze_failure
from config.settings import ROOT_DIR


def test_failure_analyzer_creates_a_local_artifact_without_llm_configuration():
    path = analyze_failure(
        "tests/unit/example_failure",
        "Example assertion failed",
        "Example logcat output",
    )

    assert path.exists()
    assert path.is_relative_to(ROOT_DIR / "artifacts" / "failure_analysis")
