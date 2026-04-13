"""Unit tests for scenarios."""
from model_mind_game.scenarios import SCENARIOS


def test_scenarios_exist():
    assert len(SCENARIOS) >= 1


def test_scenario_attributes():
    for s in SCENARIOS:
        assert s.title
        assert s.base_setting
        assert s.required_insights > 0
        assert s.hint
