# -*- coding: utf-8 -*-
"""``wqb.prod_queue`` 落盘队列的守卫（2026-10-28 P1-2 接线时补）。

prod 相关是账号级单并发：即便是「谁先触发」这件事本身也需要排队，否则多进程只会
互相把对方顶成 ``correlation_busy``。本模块是**唯一**的队列实现（``corr_check.py``
的 ``--enqueue/--run-queue/--queue-stats`` 消费它），故语义要钉死：

1. **幂等登记**：重复 push 不重置 ``tries``；``done`` 的条目要 ``force=True`` 才会重查。
2. **租约**：取用即上 ``lease_ts``，``LEASE_SEC`` 内不会被重复取（防两头同时跑同一条）；
   租约过期可重取（防一条卡死把队列堵住）。
3. **保留期**：``done``/``error`` 超过 ``KEEP_DAYS`` 在下次写入时被清掉（防文件无限长）。

全部用例把 ``WQB_PROD_QUEUE_PATH`` 指到 tmp，**不碰仓库 cache/**。
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
for _p in (str(ROOT / "src"),):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb import prod_queue as pq  # noqa: E402


@pytest.fixture(autouse=True)
def queue_file(tmp_path, monkeypatch):
    p = tmp_path / "prod_queue.json"
    monkeypatch.setenv("WQB_PROD_QUEUE_PATH", str(p))
    return p


def _write(path: Path, items: dict) -> None:
    path.write_text(json.dumps({"items": items}, ensure_ascii=False), encoding="utf-8")


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------- 路径
class TestQueuePath:
    def test_env_override_wins(self, queue_file):
        assert pq.queue_path() == str(queue_file)

    def test_default_under_repo_cache(self, monkeypatch):
        monkeypatch.delenv("WQB_PROD_QUEUE_PATH", raising=False)
        p = pq.queue_path()
        assert os.path.isabs(p)
        assert p.endswith(os.path.join("cache", "prod_queue.json"))
        assert "src" not in Path(p).parts


# ---------------------------------------------------------------- 登记
class TestPush:
    def test_push_creates_pending(self, queue_file):
        cur = pq.push("A1", note="首批")
        assert cur["status"] == "pending" and cur["tries"] == 0
        assert pq.get("A1")["note"] == "首批"

    def test_push_is_idempotent_and_keeps_tries(self, queue_file):
        pq.push("A1")
        pq.mark("A1", status="pending_timeout")
        pq.push("A1", note="")           # 重登记不重置已尝试次数，也不清空 note
        cur = pq.get("A1")
        assert cur["status"] == "pending"
        assert cur["tries"] == 1

    def test_push_done_requires_force(self, queue_file):
        pq.push("A1")
        pq.mark("A1", max_corr=0.42, status="done")
        assert pq.push("A1")["status"] == "done"
        assert pq.get("A1")["max"] == pytest.approx(0.42)
        forced = pq.push("A1", force=True)
        assert forced["status"] == "pending"
        assert pq.get("A1")["max"] == pytest.approx(0.42)  # 旧值留着供对照

    def test_push_resets_error_without_force(self, queue_file):
        pq.push("A1")
        pq.mark("A1", status="error", error="boom")
        assert pq.push("A1")["status"] == "pending"
        assert pq.get("A1")["error"] == "boom"

    def test_get_and_items_are_copies(self, queue_file):
        pq.push("A1")
        got = pq.get("A1")
        got["status"] = "done"
        assert pq.get("A1")["status"] == "pending"
        snap = pq.items()
        snap["A1"]["status"] = "done"
        assert pq.get("A1")["status"] == "pending"
        assert pq.get("MISSING") == {}

    def test_push_many_counts_truthy(self, queue_file):
        n = pq.push_many(["A1", "", None, "A2"], note="批量")
        assert n == 2
        assert set(pq.items()) == {"A1", "A2"}
        assert pq.get("A2")["note"] == "批量"


# ---------------------------------------------------------------- 取用与租约
class TestNextPending:
    def test_picks_oldest_first(self, queue_file):
        _write(queue_file, {
            "B": {"status": "pending", "ts": 200.0},
            "A": {"status": "pending", "ts": 100.0},
        })
        assert pq.next_pending() == "A"
        assert pq.next_pending() == "B"
        assert pq.next_pending() is None

    def test_lease_blocks_repeat_pick(self, queue_file):
        _write(queue_file, {
            "A": {"status": "pending", "ts": 100.0},
            "B": {"status": "pending", "ts": 200.0},
        })
        assert pq.next_pending() == "A"
        assert _read(queue_file)["items"]["A"]["lease_ts"] > 0
        assert pq.next_pending() == "B", "A 仍在租约内，不该被重复取"

    def test_expired_lease_allows_retake(self, queue_file):
        now = time.time()
        _write(queue_file, {
            "A": {"status": "pending", "ts": now - 10, "lease_ts": now - pq.LEASE_SEC - 1},
        })
        assert pq.next_pending() == "A"

    def test_pending_timeout_is_takeable(self, queue_file):
        _write(queue_file, {"A": {"status": "pending_timeout", "ts": 1.0}})
        assert pq.next_pending() == "A"

    def test_done_and_error_are_not_takeable(self, queue_file):
        _write(queue_file, {
            "A": {"status": "done", "ts": 1.0},
            "B": {"status": "error", "ts": 2.0},
        })
        assert pq.next_pending() is None

    def test_empty_or_corrupt_file_returns_none(self, queue_file):
        assert pq.next_pending() is None
        queue_file.write_text("{not json", encoding="utf-8")
        assert pq.next_pending() is None


# ---------------------------------------------------------------- 写回
class TestMark:
    def test_mark_done_records_value_and_drops_lease(self, queue_file):
        _write(queue_file, {"A": {"status": "pending", "ts": 1.0, "lease_ts": 2.0,
                                  "tries": 2}})
        cur = pq.mark("A", max_corr="0.8125", status="done")
        assert cur["status"] == "done" and cur["tries"] == 3
        assert cur["max"] == pytest.approx(0.8125)
        assert "lease_ts" not in cur
        assert "lease_ts" not in pq.get("A")

    def test_mark_error_truncates_message(self, queue_file):
        pq.push("A")
        cur = pq.mark("A", status="error", error="x" * 500)
        assert cur["status"] == "error" and len(cur["error"]) == 200

    def test_mark_bad_max_is_ignored(self, queue_file):
        pq.push("A")
        cur = pq.mark("A", max_corr="n/a", status="done")
        assert "max" not in cur

    def test_mark_creates_entry_if_missing(self, queue_file):
        cur = pq.mark("NEW", max_corr=0.1, status="done")
        assert cur["tries"] == 1
        assert pq.get("NEW")["status"] == "done"


# ---------------------------------------------------------------- 概况与清理
class TestStatsAndClear:
    def test_stats_counts_and_pending_list(self, queue_file):
        pq.push("A")
        pq.push("B")
        pq.mark("B", max_corr=0.3, status="done")
        pq.push("C")
        pq.mark("C", status="pending_timeout")
        s = pq.stats()
        assert s["total"] == 3
        assert s["by_status"] == {"pending": 1, "done": 1, "pending_timeout": 1}
        assert s["pending"] == ["A", "C"]
        assert s["path"] == str(queue_file)
        assert s["updated"]

    def test_clear_done_only_then_all(self, queue_file):
        pq.push("A")
        pq.push("B")
        pq.mark("B", max_corr=0.3, status="done")
        assert pq.clear() == 1
        assert set(pq.items()) == {"A"}
        assert pq.clear(done_only=False) == 1
        assert pq.items() == {}

    def test_keep_days_prunes_old_done_and_error_only(self, queue_file):
        old = time.time() - (pq.KEEP_DAYS + 1) * 86400
        _write(queue_file, {
            "A": {"status": "done", "ts": old},
            "B": {"status": "error", "ts": old, "error": "x"},
            "C": {"status": "pending", "ts": old},
            "D": {"status": "done", "ts": time.time()},
        })
        pq.push("E")          # 触发一次 _save → 剪枝
        assert set(pq.items()) == {"C", "D", "E"}

    def test_save_is_atomic_no_tmp_left(self, queue_file):
        pq.push("A")
        pq.push("B")
        assert queue_file.exists()
        assert not (queue_file.parent / (queue_file.name + ".tmp")).exists()
        assert set(_read(queue_file)["items"]) == {"A", "B"}
