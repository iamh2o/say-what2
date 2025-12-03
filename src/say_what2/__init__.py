"""say_what2: lightweight AI benchmark framework."""

from .benchmarks import BenchmarkCase, BenchmarkSuite, default_benchmark_suite
from .providers import BaseProvider, EchoProvider, ScriptedProvider
from .evaluation import EvaluatedResult, Evaluator
from .history import HistoryStore
from .trends import TrendAnalyzer
from .runner import run_suite

__all__ = [
    "BenchmarkCase",
    "BenchmarkSuite",
    "default_benchmark_suite",
    "BaseProvider",
    "EchoProvider",
    "ScriptedProvider",
    "Evaluator",
    "EvaluatedResult",
    "HistoryStore",
    "TrendAnalyzer",
    "run_suite",
]
