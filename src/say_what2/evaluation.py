from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from difflib import SequenceMatcher
from typing import Callable, Dict


@dataclass
class EvaluatedResult:
    prompt: str
    expected: str
    response: str
    score: float
    domain: str
    provider: str
    timestamp: str


class Evaluator:
    def __init__(self, metric: Callable[[str, str], float] | None = None):
        self.metric = metric or self._similarity_metric

    @staticmethod
    def _similarity_metric(expected: str, response: str) -> float:
        """Score similarity in [0, 1] using SequenceMatcher."""
        return SequenceMatcher(None, expected.lower().strip(), response.lower().strip()).ratio()

    def evaluate(self, *, prompt: str, expected: str, response: str, domain: str, provider: str) -> EvaluatedResult:
        score = self.metric(expected, response)
        return EvaluatedResult(
            prompt=prompt,
            expected=expected,
            response=response,
            score=score,
            domain=domain,
            provider=provider,
            timestamp=datetime.utcnow().isoformat(),
        )

    def aggregate(self, results: list[EvaluatedResult]) -> Dict[str, float]:
        if not results:
            return {}
        domain_scores: Dict[str, list[float]] = {}
        for result in results:
            domain_scores.setdefault(result.domain, []).append(result.score)
        return {domain: sum(values) / len(values) for domain, values in domain_scores.items()}
