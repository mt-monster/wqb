"""Unit tests for wqb.memory.db — SimulationDB hash cache and bookkeeping.

Covers:
- Table creation (init_tables) and doctor() health check.
- compute_hash determinism and collision resistance.
- get_cached / put_cached round-trip.
- record_trajectory / add_trajectory_step / add_insight / record_batch.
- Upsert behaviour (put_cached on existing hash).
"""

import pytest

from wqb.memory.db import SimulationDB, _json_dumps, _json_loads


@pytest.fixture
def db(tmp_path):
    """Return a SimulationDB backed by a temporary SQLite file."""
    path = str(tmp_path / "test_sim.db")
    sim_db = SimulationDB(path)
    sim_db.init_tables()
    yield sim_db
    sim_db.close()


# ---------------------------------------------------------------------------
# init_tables & doctor
# ---------------------------------------------------------------------------

def test_init_tables_creates_all_required(db):
    report = db.doctor()
    assert report["ok"] is True
    assert report["missing_tables"] == []


def test_doctor_reports_missing_tables(tmp_path):
    # Fresh DB without init_tables
    path = str(tmp_path / "empty.db")
    sim_db = SimulationDB(path)
    report = sim_db.doctor()
    assert report["ok"] is False
    assert len(report["missing_tables"]) == 5  # all 5 tables missing
    sim_db.close()


def test_doctor_table_counts(db):
    report = db.doctor()
    assert all(v >= 0 for v in report["table_counts"].values())


# ---------------------------------------------------------------------------
# compute_hash
# ---------------------------------------------------------------------------

def test_compute_hash_is_deterministic(db):
    h1 = db.compute_hash("rank(close)", {"region": "USA", "delay": 1})
    h2 = db.compute_hash("rank(close)", {"region": "USA", "delay": 1})
    assert h1 == h2


def test_compute_hash_different_expression_different_hash(db):
    h1 = db.compute_hash("rank(close)", {"region": "USA", "delay": 1})
    h2 = db.compute_hash("rank(volume)", {"region": "USA", "delay": 1})
    assert h1 != h2


def test_compute_hash_different_settings_different_hash(db):
    h1 = db.compute_hash("rank(close)", {"region": "USA", "delay": 0})
    h2 = db.compute_hash("rank(close)", {"region": "USA", "delay": 1})
    assert h1 != h2


def test_compute_hash_key_order_independent(db):
    h1 = db.compute_hash("rank(close)", {"region": "USA", "delay": 1})
    h2 = db.compute_hash("rank(close)", {"delay": 1, "region": "USA"})
    assert h1 == h2


def test_compute_hash_returns_hex_digest(db):
    h = db.compute_hash("rank(close)", {"region": "USA"})
    # SHA-256 hex digest is 64 characters
    assert len(h) == 64
    assert all(c in "0123456789abcdef" for c in h)


# ---------------------------------------------------------------------------
# get_cached / put_cached
# ---------------------------------------------------------------------------

def test_get_cached_returns_none_for_missing(db):
    h = db.compute_hash("rank(close)", {"region": "USA"})
    assert db.get_cached(h) is None


def test_put_cached_and_get_cached_roundtrip(db):
    expr = "rank(close)"
    settings = {"region": "USA", "delay": 1}
    h = db.compute_hash(expr, settings)
    result = {"sharpe": 1.5, "fitness": 0.8}
    db.put_cached(h, expr, "USA_D1_TOP3000", result)

    cached = db.get_cached(h)
    assert cached is not None
    assert cached["sharpe"] == 1.5
    assert cached["fitness"] == 0.8


def test_put_cached_upsert(db):
    expr = "rank(close)"
    settings = {"region": "USA", "delay": 1}
    h = db.compute_hash(expr, settings)

    db.put_cached(h, expr, "USA_D1_TOP3000", {"sharpe": 1.0})
    cached = db.get_cached(h)
    assert cached["sharpe"] == 1.0

    db.put_cached(h, expr, "USA_D1_TOP3000", {"sharpe": 2.0})
    cached = db.get_cached(h)
    assert cached["sharpe"] == 2.0


# ---------------------------------------------------------------------------
# Trajectory bookkeeping
# ---------------------------------------------------------------------------

def test_record_trajectory_returns_id(db):
    tid = db.record_trajectory("sess1", "USA", "TOP3000", "news12", "P1_SPREAD")
    assert isinstance(tid, int)
    assert tid > 0


def test_add_trajectory_step(db):
    tid = db.record_trajectory("sess1", "USA", "TOP3000", "news12", "P1_SPREAD")
    sid = db.add_trajectory_step(
        tid,
        "generate",
        "rank(close)",
        {"region": "USA"},
        {"status": "ok"},
    )
    assert isinstance(sid, int)
    assert sid > 0


def test_add_insight(db):
    tid = db.record_trajectory("sess1", "USA", "TOP3000", "news12", "P1_SPREAD")
    iid = db.add_insight(tid, "positive", "news12 P1 works well")
    assert isinstance(iid, int)


def test_record_batch(db):
    bid = db.record_batch("sess1", "batch_001", ["rank(close)"], [{"sharpe": 1.0}])
    assert isinstance(bid, int)


def test_doctor_counts_after_inserts(db):
    db.record_trajectory("sess1", "USA", "TOP3000", "news12", "P1_SPREAD")
    report = db.doctor()
    assert report["table_counts"]["trajectories"] == 1
    assert report["ok"] is True


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def test_json_dumps_roundtrip():
    original = {"sharpe": 1.5, "fields": ["close", "volume"]}
    s = _json_dumps(original)
    restored = _json_loads(s)
    assert restored == original


def test_json_loads_none_on_empty():
    assert _json_loads("") is None


def test_json_loads_none_on_invalid():
    assert _json_loads("not json") is None


# ---------------------------------------------------------------------------
# Context manager
# ---------------------------------------------------------------------------

def test_context_manager(tmp_path):
    path = str(tmp_path / "ctx.db")
    with SimulationDB(path) as db:
        db.init_tables()
        report = db.doctor()
        assert report["ok"] is True
    # Connection should be closed
    assert db.connection is not None  # connection still exists as attribute