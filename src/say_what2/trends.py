from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List

from .evaluation import EvaluatedResult


class TrendAnalyzer:
    """Compute rolling averages and compare performance drift."""

    def __init__(self, window: int = 5):
        self.window = window

    def _windowed_scores(self, results: Iterable[EvaluatedResult]) -> Dict[str, List[float]]:
        scores: Dict[str, List[float]] = defaultdict(list)
        for result in results:
            scores[result.provider].append(result.score)
        return scores

    def summarize(self, results: Iterable[EvaluatedResult]) -> Dict[str, Dict[str, float]]:
        provider_scores = self._windowed_scores(results)
        summaries: Dict[str, Dict[str, float]] = {}
        for provider, scores in provider_scores.items():
            if not scores:
                continue
            recent = scores[-self.window :]
            baseline = scores[: max(1, len(scores) - len(recent))]
            summaries[provider] = {
                "latest_average": sum(recent) / len(recent),
                "lifetime_average": sum(scores) / len(scores),
                "baseline_average": (sum(baseline) / len(baseline)) if baseline else scores[0],
                "delta_vs_baseline": (sum(recent) / len(recent)) - (sum(baseline) / len(baseline) if baseline else scores[0]),
            }
        return summaries
