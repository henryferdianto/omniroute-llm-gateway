"""Provider adapters. Implement one class per LLM vendor."""
from abc import ABC, abstractmethod


class Provider(ABC):
    @abstractmethod
    def complete(self, model: str, prompt: str) -> str: ...

    @abstractmethod
    def healthy(self) -> bool: ...


class MockProvider(Provider):
    def complete(self, model: str, prompt: str) -> str:
        return f"[{model}] {prompt[:40]}"

    def healthy(self) -> bool:
        return True
