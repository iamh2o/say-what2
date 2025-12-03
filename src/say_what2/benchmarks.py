from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable, List


@dataclass
class BenchmarkCase:
    prompt: str
    expected_answer: str
    domain: str
    metric: Callable[[str, str], float]


@dataclass
class BenchmarkSuite:
    name: str
    cases: List[BenchmarkCase] = field(default_factory=list)

    def extend(self, additional_cases: Iterable[BenchmarkCase]) -> None:
        self.cases.extend(additional_cases)


def default_benchmark_suite(metric: Callable[[str, str], float]) -> BenchmarkSuite:
    """Create a baseline suite spanning logic, math, language, and coding."""
    suite = BenchmarkSuite(name="baseline")
    suite.extend(
        [
            BenchmarkCase(
                prompt="If all Bloops are Razzies and some Razzies are Lazzies, can we conclude all Bloops are Lazzies?",
                expected_answer="No, we cannot conclude that all Bloops are Lazzies.",
                domain="logic",
                metric=metric,
            ),
            BenchmarkCase(
                prompt="What is 17 * 24?",
                expected_answer="408",
                domain="math",
                metric=metric,
            ),
            BenchmarkCase(
                prompt="Rewrite the sentence in active voice: 'The ball was thrown by Maya.'",
                expected_answer="Maya threw the ball.",
                domain="language",
                metric=metric,
            ),
            BenchmarkCase(
                prompt="In Python, how do you open a file named data.txt for reading?",
                expected_answer="with open('data.txt', 'r') as f:",
                domain="coding",
                metric=metric,
            ),
        ]
    )
    return suite
