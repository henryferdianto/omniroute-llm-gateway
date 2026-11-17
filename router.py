"""Minimal multi-provider LLM routing gateway with fallback."""
from __future__ import annotations

import time
from dataclasses import dataclass

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="OmniRoute LLM Gateway")


@dataclass
class ModelSpec:
    name: str
    cost_per_1k: float
    latency_ms: int


REGISTRY = [
    ModelSpec("small-fast", cost_per_1k=0.0002, latency_ms=300),
    ModelSpec("balanced", cost_per_1k=0.002, latency_ms=900),
    ModelSpec("frontier", cost_per_1k=0.02, latency_ms=2500),
]


class Request(BaseModel):
    prompt: str
    complexity: str = "medium"  # low | medium | high


def rank_models(complexity: str) -> list[ModelSpec]:
    if complexity == "high":
        return sorted(REGISTRY, key=lambda m: m.latency_ms)[::-1]
    if complexity == "low":
        return sorted(REGISTRY, key=lambda m: m.cost_per_1k)
    return sorted(REGISTRY, key=lambda m: m.cost_per_1k * m.latency_ms)


def call_provider(model: ModelSpec, prompt: str) -> str:
    # Replace with a real provider adapter (OpenAI, Anthropic, local, ...).
    return f"[{model.name}] response to: {prompt[:60]}"


@app.post("/route")
def route(req: Request):
    errors = []
    for model in rank_models(req.complexity):
        try:
            started = time.perf_counter()
            text = call_provider(model, req.prompt)
            return {
                "model": model.name,
                "latency_ms": model.latency_ms,
                "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
                "output": text,
            }
        except Exception as exc:  # fallback to next candidate
            errors.append({"model": model.name, "error": repr(exc)})
    return {"error": "all providers failed", "details": errors}
