import pytest

from src.router_core import AllProvidersFailed, rank_models, route


def test_low_complexity_prefers_cheapest():
    assert rank_models("low")[0].name == "small-fast"


def test_high_complexity_prefers_capability():
    assert rank_models("high")[0].name == "frontier"


def test_route_returns_model():
    assert route("hello", "medium")["model"]


def test_fallback_skips_failing_provider():
    def caller(model, prompt):
        if model.name == "frontier":
            raise TimeoutError
        return "ok"

    assert route("x", "high", caller)["model"] != "frontier"


def test_all_failed_raises():
    def boom(model, prompt):
        raise RuntimeError("down")

    with pytest.raises(AllProvidersFailed):
        route("x", "medium", boom)
