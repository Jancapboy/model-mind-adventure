"""Unit tests for mental models definitions."""

from model_mind_game.models import MENTAL_MODELS, MODEL_MAP


def test_models_count():
    assert len(MENTAL_MODELS) == 7


def test_model_ids_unique():
    ids = [m.id for m in MENTAL_MODELS]
    assert len(ids) == len(set(ids))


def test_model_map_consistency():
    for m in MENTAL_MODELS:
        assert MODEL_MAP[m.id] == m


def test_model_attributes():
    for m in MENTAL_MODELS:
        assert m.id
        assert m.name
        assert m.name_zh
        assert m.description
        assert m.lens_prompt
        assert m.color
