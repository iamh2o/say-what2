from say_what2 import (
    BenchmarkCase,
    BenchmarkSuite,
    EchoProvider,
    EvaluatedResult,
    Evaluator,
    HistoryStore,
    ScriptedProvider,
    TrendAnalyzer,
    default_benchmark_suite,
    run_suite,
)


def test_evaluator_similarity_metric():
    evaluator = Evaluator()
    score = evaluator.metric("answer", "Answer with extra")
    assert 0 < score < 1


def test_run_suite_collects_results(tmp_path):
    evaluator = Evaluator()
    suite = BenchmarkSuite(
        name="demo",
        cases=[
            BenchmarkCase(prompt="1+1?", expected_answer="2", domain="math", metric=evaluator.metric),
            BenchmarkCase(prompt="Say hi", expected_answer="hi", domain="language", metric=evaluator.metric),
        ],
    )
    provider = ScriptedProvider(lambda prompt: "2" if "1+1" in prompt else "hi")
    history = HistoryStore(path=tmp_path / "history.json")

    results = run_suite(provider, suite, evaluator=evaluator, history=history)

    assert len(results) == 2
    assert all(isinstance(result.score, float) for result in results)

    loaded = history.load()
    assert len(loaded) == 2


def test_trend_analyzer_detects_delta():
    trend = TrendAnalyzer(window=2)
    results = [
        EvaluatedResult(
            prompt="",
            expected="",
            response="",
            score=score,
            domain="math",
            provider="provider-a",
            timestamp="",
        )
        for score in [0.5, 0.6, 0.9, 0.2]
    ]

    summary = trend.summarize(results)
    provider_summary = summary["provider-a"]

    assert provider_summary["latest_average"] == (0.9 + 0.2) / 2
    assert provider_summary["lifetime_average"] == sum([0.5, 0.6, 0.9, 0.2]) / 4


def test_default_suite_domains_cover_key_areas():
    evaluator = Evaluator()
    suite = default_benchmark_suite(metric=evaluator.metric)
    domains = {case.domain for case in suite.cases}
    assert {"logic", "math", "language", "coding"}.issubset(domains)
