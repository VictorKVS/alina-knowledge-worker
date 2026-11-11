from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ModelResponse:
    text: str
    structured: dict[str, Any] | None = None


class ModelProvider:
    def generate(self, *, system: str, user: str, schema: dict | None = None) -> ModelResponse:
        raise NotImplementedError


class NullModelProvider(ModelProvider):
    def generate(self, *, system: str, user: str, schema: dict | None = None) -> ModelResponse:
        raise RuntimeError("No model provider configured")
