"""Unit tests for wqb.search.failure_memory — deprioritisation record store.

Covers:
- ``record`` persists a FailureRecord to JSONL.
- ``is_deprioritized`` matches on 4-tuple + shape_bucket.
- ``is_deprioritized`` with empty shape_bucket matches any shape.
- ``get_failed_arms`` returns all records.
- ``get_failure_count`` counts 4-tuple matches.
- ``FailureRecord`` serialisation round-trip (to_dict / from_dict).
- File-not-found edge case returns empty list.
"""

import os

import pytest

from wqb.search.failure_memory import (
    FailureRecord,
    get_failed_arms,
    get_failure_count,
    is_deprioritized,
    record,
)


@pytest.fixture
def memory_file(tmp_path):
    return str(tmp_path / "failure_memory.jsonl")


# ---------------------------------------------------------------------------
# FailureRecord dataclass
# ---------------------------------------------------------------------------

def test_failure_record_signature_tuple():
    r = FailureRecord(
        category="news",
        dataset="news12",
        universe="TOP3000",
        paradigm="P1_SPREAD",
        shape_bucket="rank|subtract|RANK|ZSCORE|mid",
        timestamp="2026-01-01T00:00:00+00:00",
    )
    sig = r.signature_tuple()
    assert sig == ("news", "news12", "TOP3000", "P1_SPREAD", "rank|subtract|RANK|ZSCORE|mid")


def test_failure_record_to_dict_from_dict_roundtrip():
    original = FailureRecord(
        category="fundamental",
        dataset="fnd6",
        universe="TOP3000",
        paradigm="P2_RATIO",
        shape_bucket="S1",
        timestamp="2026-01-01T00:00:00+00:00",
        reason="decay_ratio<0.30",
    )
    d = original.to_dict()
    restored = FailureRecord.from_dict(d)
    assert restored.category == "fundamental"
    assert restored.reason == "decay_ratio<0.30"


def test_failure_record_from_dict_defaults():
    r = FailureRecord.from_dict({})
    assert r.category == ""
    assert r.reason == ""


# ---------------------------------------------------------------------------
# record()
# ---------------------------------------------------------------------------

def test_record_creates_file_and_writes_record(memory_file):
    assert not os.path.exists(memory_file)
    rec = record(
        category="news",
        dataset="news12",
        universe="TOP3000",
        paradigm="P1_SPREAD",
        shape_bucket="S1",
        reason="low_sharpe",
        memory_file=memory_file,
    )
    assert os.path.exists(memory_file)
    assert rec.category == "news"
    assert rec.reason == "low_sharpe"


def test_record_creates_parent_directory(tmp_path):
    path = str(tmp_path / "subdir" / "failure.jsonl")
    record(
        category="news",
        dataset="news12",
        universe="TOP3000",
        paradigm="P1_SPREAD",
        shape_bucket="S1",
        memory_file=path,
    )
    assert os.path.exists(path)


def test_record_multiple_appends(memory_file):
    record("news", "news12", "TOP3000", "P1_SPREAD", "S1", memory_file=memory_file)
    record("news", "news12", "TOP3000", "P2_RATIO", "S4", memory_file=memory_file)
    records = get_failed_arms(memory_file=memory_file)
    assert len(records) == 2


# ---------------------------------------------------------------------------
# is_deprioritized
# ---------------------------------------------------------------------------

def test_is_deprioritized_exact_match(memory_file):
    record("news", "news12", "TOP3000", "P1_SPREAD", "S1", memory_file=memory_file)
    assert is_deprioritized(
        "news", "news12", "TOP3000", "P1_SPREAD", "S1", memory_file=memory_file
    ) is True


def test_is_deprioritized_no_match(memory_file):
    record("news", "news12", "TOP3000", "P1_SPREAD", "S1", memory_file=memory_file)
    assert is_deprioritized(
        "news", "news12", "TOP3000", "P2_RATIO", "S4", memory_file=memory_file
    ) is False


def test_is_deprioritized_empty_shape_matches_any(memory_file):
    record("news", "news12", "TOP3000", "P1_SPREAD", "S1", memory_file=memory_file)
    assert is_deprioritized(
        "news", "news12", "TOP3000", "P1_SPREAD", "", memory_file=memory_file
    ) is True


def test_is_deprioritized_wrong_dataset(memory_file):
    record("news", "news12", "TOP3000", "P1_SPREAD", "S1", memory_file=memory_file)
    assert is_deprioritized(
        "news", "news29", "TOP3000", "P1_SPREAD", "S1", memory_file=memory_file
    ) is False


def test_is_deprioritized_file_not_found(tmp_path):
    path = str(tmp_path / "nonexistent.jsonl")
    assert is_deprioritized(
        "news", "news12", "TOP3000", "P1_SPREAD", "S1", memory_file=path
    ) is False


# ---------------------------------------------------------------------------
# get_failed_arms / get_failure_count
# ---------------------------------------------------------------------------

def test_get_failed_arms_empty(memory_file):
    records = get_failed_arms(memory_file=memory_file)
    assert records == []


def test_get_failed_arms_after_records(memory_file):
    record("news", "news12", "TOP3000", "P1_SPREAD", "S1", memory_file=memory_file)
    records = get_failed_arms(memory_file=memory_file)
    assert len(records) == 1
    assert records[0].dataset == "news12"


def test_get_failure_count(memory_file):
    record("news", "news12", "TOP3000", "P1_SPREAD", "S1", memory_file=memory_file)
    record("news", "news12", "TOP3000", "P1_SPREAD", "S4", memory_file=memory_file)
    record("news", "news12", "TOP3000", "P2_RATIO", "S4", memory_file=memory_file)
    # P1_SPREAD appears twice (S1 + S4)
    assert get_failure_count(
        "news", "news12", "TOP3000", "P1_SPREAD", memory_file=memory_file
    ) == 2
    assert get_failure_count(
        "news", "news12", "TOP3000", "P2_RATIO", memory_file=memory_file
    ) == 1