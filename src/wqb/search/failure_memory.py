"""Failure memory: record and query failed search-arm signatures.

Records failure signatures so the scheduler can deprioritise arms that have
already failed.  Each failure is identified by the 5-tuple
``(category, dataset, universe, paradigm, shape_bucket)`` where
``shape_bucket`` comes from :func:`wqb.expression.validator._shape_signature`.

This implements the robustness Phase D write-back (robustness SKILL §D.3):
*"If REJECT, also call ``wqb.search.failure_memory.record(...)`` with the
signature ``(category, dataset, universe, paradigm, shape_bucket)`` so the
scheduler deprioritises that arm."*

Persistence format: JSONL (one JSON object per line) at
``data/failure_memory.jsonl``.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import List


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class FailureRecord:
    """A single failure record identifying a deprioritised search arm.

    Attributes
    ----------
    category : str
        Data category (e.g. ``"news"``, ``"fundamental"``).
    dataset : str
        Dataset ID (e.g. ``"news12"``).
    universe : str
        Trading universe (e.g. ``"TOP3000"``).
    paradigm : str
        Paradigm name (e.g. ``"P1_SPREAD"``).
    shape_bucket : str
        Shape signature from ``validator._shape_signature``, serialised as
        a string (e.g. ``"rank|subtract|RANK|ZSCORE|mid"``).
    timestamp : str
        ISO-8601 timestamp of when the record was created.
    reason : str
        Human-readable failure reason (e.g. ``"decay_ratio<0.30"``).
    """

    category: str
    dataset: str
    universe: str
    paradigm: str
    shape_bucket: str
    timestamp: str
    reason: str = ""

    def signature_tuple(self) -> tuple:
        """Return the 5-tuple signature ``(category, dataset, universe, paradigm, shape_bucket)``."""
        return (self.category, self.dataset, self.universe, self.paradigm, self.shape_bucket)

    def to_dict(self) -> dict:
        """Serialise to a JSON-compatible dict."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "FailureRecord":
        """Deserialise from a dict."""
        return cls(
            category=data.get("category", ""),
            dataset=data.get("dataset", ""),
            universe=data.get("universe", ""),
            paradigm=data.get("paradigm", ""),
            shape_bucket=data.get("shape_bucket", ""),
            timestamp=data.get("timestamp", ""),
            reason=data.get("reason", ""),
        )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _ensure_dir(filepath: str) -> None:
    """Ensure the parent directory of *filepath* exists."""
    parent = os.path.dirname(filepath)
    if parent:
        os.makedirs(parent, exist_ok=True)


def _read_all_records(memory_file: str) -> List[FailureRecord]:
    """Read all failure records from the JSONL file.

    Returns an empty list if the file does not exist or is empty.
    """
    if not os.path.exists(memory_file):
        return []
    records: List[FailureRecord] = []
    with open(memory_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                records.append(FailureRecord.from_dict(obj))
            except (json.JSONDecodeError, KeyError):
                continue
    return records


def _append_record(record: FailureRecord, memory_file: str) -> None:
    """Append a single record to the JSONL file."""
    _ensure_dir(memory_file)
    with open(memory_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def record(
    category: str,
    dataset: str,
    universe: str,
    paradigm: str,
    shape_bucket: str,
    reason: str = "",
    memory_file: str = "data/failure_memory.jsonl",
) -> FailureRecord:
    """Create and persist a failure record.

    Records the 5-tuple signature ``(category, dataset, universe, paradigm,
    shape_bucket)`` so the scheduler can deprioritise this arm in future
    planning cycles.

    Parameters
    ----------
    category : str
        Data category.
    dataset : str
        Dataset ID.
    universe : str
        Trading universe.
    paradigm : str
        Paradigm name.
    shape_bucket : str
        Shape signature (from ``validator._shape_signature``).
    reason : str, optional
        Human-readable failure reason.
    memory_file : str
        Path to the JSONL persistence file.

    Returns
    -------
    FailureRecord
        The created and persisted record.
    """
    record_obj = FailureRecord(
        category=category,
        dataset=dataset,
        universe=universe,
        paradigm=paradigm,
        shape_bucket=shape_bucket,
        timestamp=datetime.now(timezone.utc).isoformat(),
        reason=reason,
    )
    _append_record(record_obj, memory_file)
    return record_obj


def is_deprioritized(
    category: str,
    dataset: str,
    universe: str,
    paradigm: str,
    shape_bucket: str,
    memory_file: str = "data/failure_memory.jsonl",
) -> bool:
    """Check whether a signature has been marked as failed.

    The check matches on all five fields.  If *shape_bucket* is an empty
    string, the check matches on the first four fields only (any shape).

    Parameters
    ----------
    category : str
        Data category.
    dataset : str
        Dataset ID.
    universe : str
        Trading universe.
    paradigm : str
        Paradigm name.
    shape_bucket : str
        Shape signature.  If empty, matches any shape.
    memory_file : str
        Path to the JSONL persistence file.

    Returns
    -------
    bool
        ``True`` if the signature (or a superset match) exists in the
        failure memory.
    """
    records = _read_all_records(memory_file)
    for rec in records:
        if (
            rec.category == category
            and rec.dataset == dataset
            and rec.universe == universe
            and rec.paradigm == paradigm
        ):
            if shape_bucket == "" or rec.shape_bucket == shape_bucket:
                return True
    return False


def get_failed_arms(
    memory_file: str = "data/failure_memory.jsonl",
) -> List[FailureRecord]:
    """Return all failure records.

    Parameters
    ----------
    memory_file : str
        Path to the JSONL persistence file.

    Returns
    -------
    list[FailureRecord]
        All recorded failure records, in insertion order.
    """
    return _read_all_records(memory_file)


def get_failure_count(
    category: str,
    dataset: str,
    universe: str,
    paradigm: str,
    memory_file: str = "data/failure_memory.jsonl",
) -> int:
    """Count how many times a 4-tuple signature has failed.

    Matches on ``(category, dataset, universe, paradigm)`` regardless of
    shape_bucket.  Useful for detecting a paradigm that fails repeatedly
    across different shapes on the same dataset — a signal that the
    paradigm/dataset pairing is structurally broken.

    Parameters
    ----------
    category : str
        Data category.
    dataset : str
        Dataset ID.
    universe : str
        Trading universe.
    paradigm : str
        Paradigm name.
    memory_file : str
        Path to the JSONL persistence file.

    Returns
    -------
    int
        Number of matching failure records.
    """
    records = _read_all_records(memory_file)
    count = 0
    for rec in records:
        if (
            rec.category == category
            and rec.dataset == dataset
            and rec.universe == universe
            and rec.paradigm == paradigm
        ):
            count += 1
    return count
