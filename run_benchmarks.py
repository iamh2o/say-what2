"""Run the baseline benchmark suite against a provider."""
from __future__ import annotations

from pathlib import Path

from say_what2 import (
    EchoProvider,
    Evaluator,
    HistoryStore,
    TrendAnalyzer,
    default_benchmark_suite,
    run_suite,
)


def main() -> None:
    evaluator = Evaluator()
    suite = default_benchmark_suite(metric=evaluator.metric)
    provider = EchoProvider()
    history = HistoryStore(path=Path("results") / "history.json")

    results = run_suite(provider, suite, evaluator=evaluator, history=history)
    domain_scores = evaluator.aggregate(results)
    trend = TrendAnalyzer().summarize(history.load())

    print("Domain averages:")
    for domain, score in domain_scores.items():
        print(f" - {domain}: {score:.2f}")

    print("\nTrend summary:")
    for provider_name, metrics in trend.items():
        print(f"{provider_name} -> {metrics}")


if __name__ == "__main__":
    main()
