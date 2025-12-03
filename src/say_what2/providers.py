from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


class BaseProvider:
    """Abstract provider that interacts with an AI platform."""

    name: str

    def generate(self, prompt: str) -> str:  # pragma: no cover - interface
        raise NotImplementedError


@dataclass
class EchoProvider(BaseProvider):
    """Simple provider that echoes prompts for smoke testing."""

    name: str = "echo"

    def generate(self, prompt: str) -> str:
        return prompt


@dataclass
class ScriptedProvider(BaseProvider):
    """Provider backed by a callable so tests can supply deterministic answers."""

    responder: Callable[[str], str]
    name: str = "scripted"

    def generate(self, prompt: str) -> str:
        return self.responder(prompt)
