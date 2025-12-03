from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Iterable, List

from .evaluation import EvaluatedResult


class HistoryStore:
    """Persist evaluation results to disk so trends can be tracked."""

    def __init__(self, path: str | Path = "results/history.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> List[EvaluatedResult]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as fp:
            raw = json.load(fp)
        return [EvaluatedResult(**item) for item in raw]

    def append(self, results: Iterable[EvaluatedResult]) -> None:
        existing = [asdict(result) for result in self.load()]
        existing.extend(asdict(result) for result in results)
        with self.path.open("w", encoding="utf-8") as fp:
            json.dump(existing, fp, indent=2)
