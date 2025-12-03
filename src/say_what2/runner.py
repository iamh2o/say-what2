from __future__ import annotations

from typing import Iterable, List

from .benchmarks import BenchmarkSuite
from .evaluation import EvaluatedResult, Evaluator
from .history import HistoryStore
from .providers import BaseProvider


def run_suite(
    provider: BaseProvider,
    suite: BenchmarkSuite,
    *,
    evaluator: Evaluator | None = None,
    history: HistoryStore | None = None,
) -> List[EvaluatedResult]:
    evaluator = evaluator or Evaluator()
    results: List[EvaluatedResult] = []

    for case in suite.cases:
        response = provider.generate(case.prompt)
        result = evaluator.evaluate(
            prompt=case.prompt,
            expected=case.expected_answer,
            response=response,
            domain=case.domain,
            provider=provider.name,
        )
        results.append(result)

    if history is not None:
        history.append(results)
    return results
