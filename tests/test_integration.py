"""Integration tests for the complete game package."""
from unittest.mock import patch

from model_mind_game.game import SCENARIO_INSIGHTS
from model_mind_game.models import MENTAL_MODELS, MODEL_MAP
from model_mind_game.scenarios import SCENARIOS


def test_all_scenarios_have_insights():
    """Every scenario must have pre-defined insights for all mental models."""
    for scenario in SCENARIOS:
        assert scenario.title in SCENARIO_INSIGHTS, f"Missing insights for {scenario.title}"
        insights = SCENARIO_INSIGHTS[scenario.title]
        for model in MENTAL_MODELS:
            assert model.id in insights, f"Missing insight for model {model.id} in {scenario.title}"
            assert insights[model.id], f"Empty insight for model {model.id} in {scenario.title}"


def test_scenario_insights_count_meets_requirement():
    """Each scenario must have at least as many insights as required."""
    for scenario in SCENARIOS:
        insights = SCENARIO_INSIGHTS[scenario.title]
        assert len(insights) >= scenario.required_insights


def test_game_imports_without_llm_client():
    """Game should be importable even when LLM client is unavailable."""
    with patch("model_mind_game.llm_client.OpenAI", None):
        from model_mind_game.llm_client import get_client
        assert get_client() is None


def test_fallback_scene_generation():
    """Scene generation must work without LLM."""
    from model_mind_game.llm_client import _fallback_scene
    model = MODEL_MAP["network"]
    text = _fallback_scene("测试场景", model)
    assert "测试场景" in text
    assert model.name_zh in text


def test_cli_entrypoint():
    """Verify the console script entrypoint target exists and is callable."""
    from model_mind_game.game import main
    assert callable(main)
