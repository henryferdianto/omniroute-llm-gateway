"""Provider-agnostic routing and fallback logic (no external services)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class ModelSpec:
    name: str
    cost_per_1k: float
    latency_ms: int


DEFAULT_REGISTRY = (
    ModelSpec("small-fast", cost_per_1k=0.0002, latency_ms=300),
    ModelSpec("balanced", cost_per_1k=0.002, latency_ms=900),
    ModelSpec("frontier", cost_per_1k=0.02, latency_ms=2500),
)


class AllProvidersFailed(RuntimeError):
    pass


def rank_models(complexity: str, registry=DEFAULT_REGISTRY) -> list[ModelSpec]:
    if complexity == "high":
        return sorted(registry, key=lambda m: m.latency_ms, reverse=True)
    if complexity == "low":
        return sorted(registry, key=lambda m: m.cost_per_1k)
    return sorted(registry, key=lambda m: m.cost_per_1k * m.latency_ms)


def default_caller(model: ModelSpec, prompt: str) -> str:
    return f"[{model.name}] response to: {prompt[:60]}"


def route(prompt: str, complexity: str = "medium", caller: Callable = default_caller) -> dict:
    errors = []
    for model in rank_models(complexity):
        try:
            return {"model": model.name, "output": caller(model, prompt), "errors": errors}
        except Exception as exc:  # fall back to the next candidate
            errors.append({"model": model.name, "error": repr(exc)})
    raise AllProvidersFailed(errors)
