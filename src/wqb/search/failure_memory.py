"""wqb.search.failure_memory — JSONL store of failed mining arms.

Failed arms are keyed by the 4-tuple (category, dataset, universe,
paradigm) plus an optional shape bucket, so the scheduler can
deprioritize combinations that already burned budget.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import List, Tuple

DEFAULT_MEMORY_FILE = os.path.join("tracking", "mining", "failure_memory.jsonl")


@dataclass
class FailureRecord:
    category: str = ""
    dataset: str = ""
    universe: str = ""
    paradigm: str = ""
    shape_bucket: str = ""
    timestamp: str = ""
    reason: str = ""

    def signature_tuple(self) -> Tuple[str, str, str, str, str]:
        return (self.category, self.dataset, self.universe,
                self.paradigm, self.shape_bucket)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "FailureRecord":
        return cls(
            category=d.get("category", ""),
            dataset=d.get("dataset", ""),
            universe=d.get("universe", ""),
            paradigm=d.get("paradigm", ""),
            shape_bucket=d.get("shape_bucket", ""),
            timestamp=d.get("timestamp", ""),
            reason=d.get("reason", ""),
        )


def record(category: str, dataset: str, universe: str, paradigm: str,
           shape_bucket: str = "", reason: str = "",
           memory_file: str = DEFAULT_MEMORY_FILE) -> FailureRecord:
    """Append a failure record to the JSONL memory file."""
    rec = FailureRecord(
        category=category,
        dataset=dataset,
        universe=universe,
        paradigm=paradigm,
        shape_bucket=shape_bucket,
        timestamp=datetime.now(timezone.utc).isoformat(),
        reason=reason,
    )
    parent = os.path.dirname(os.path.abspath(memory_file))
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(memory_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec.to_dict(), ensure_ascii=False) + "\n")
    return rec


def get_failed_arms(memory_file: str = DEFAULT_MEMORY_FILE
                    ) -> List[FailureRecord]:
    """Return all failure records; empty list when the file is absent."""
    if not os.path.exists(memory_file):
        return []
    records: List[FailureRecord] = []
    with open(memory_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(FailureRecord.from_dict(json.loads(line)))
            except json.JSONDecodeError:
                continue
    return records


def is_deprioritized(category: str, dataset: str, universe: str,
                     paradigm: str, shape_bucket: str = "",
                     memory_file: str = DEFAULT_MEMORY_FILE) -> bool:
    """True when the arm was already recorded as failed.

    An empty ``shape_bucket`` (on either side) matches any shape.
    """
    for rec in get_failed_arms(memory_file=memory_file):
        if (rec.category, rec.dataset, rec.universe, rec.paradigm) != \
                (category, dataset, universe, paradigm):
            continue
        if shape_bucket and rec.shape_bucket and \
                rec.shape_bucket != shape_bucket:
            continue
        return True
    return False


def get_failure_count(category: str, dataset: str, universe: str,
                      paradigm: str,
                      memory_file: str = DEFAULT_MEMORY_FILE) -> int:
    """Count failures recorded for the 4-tuple arm signature."""
    return sum(
        1 for rec in get_failed_arms(memory_file=memory_file)
        if (rec.category, rec.dataset, rec.universe, rec.paradigm) ==
        (category, dataset, universe, paradigm)
    )
