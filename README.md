# Say What 2

A lightweight Python framework for probing and assessing AI platforms (Claude, ChatGPT, Grok, etc.) to detect whether their intelligence has been dialed down over time. The toolkit standardizes benchmarking, automates scoring, and stores historical runs so you can track trend lines and detect performance degradation.

## Features
- **Standardized benchmark suite** spanning logic, math, language, and coding prompts.
- **Provider abstraction** so you can plug in multiple AI platforms while reusing the same suite.
- **Automated scoring** with similarity-based metrics and domain averages.
- **Trend analysis** to compare recent performance against historical baselines.
- **Historical result tracking** persisted to JSON for long-term audits.

## Quick start
Run the bundled smoke-test provider against the baseline suite:

```bash
python run_benchmarks.py
```

The script will:
1. Execute the baseline tests against the `EchoProvider`.
2. Score each response and print domain averages.
3. Persist results to `results/history.json`.
4. Print rolling trend summaries for each provider recorded in history.

## Extending
- Implement `BaseProvider.generate` to integrate with your AI endpoint.
- Add `BenchmarkCase` items to the default suite or create new `BenchmarkSuite` collections.
- Swap the scoring metric by passing a custom callable to `default_benchmark_suite` or directly into `Evaluator`.

## Tests
Run the unit tests with:

```bash
python -m pytest
```
