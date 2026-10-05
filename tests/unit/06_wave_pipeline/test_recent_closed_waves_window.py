# -*- coding: utf-8 -*-
"""回归测试：停止规则 B 的窗口按**波的开始时刻**取（R22 守护，2026-10-02 补）。

## 背景
`campaign._recent_closed_waves(conn, region, k)` 决定停止规则 B 的窗口 = 最近 k 个 closed 波。
2026-09-27 R22（审计 N22）修正：此前按 `COALESCE(updated_at, created_at)` 排序——
**给任何旧波补记结论 / 补写 findings 都会把它顶进「最近 k 个」**。

KOR 真实事故：按 R20 的建议给旧波 91c（早于 92–97）补记 PASS，窗口变成
`[91c PASS, 97, …]` → 区域停波被错误解除、下一波放行。

修正后：开始时刻 = 该波的 **`waves.created_at`（首次入库表达式的时间，此后不再改写）**；
没有 waves 表（最小库）时退到 `wave_results.created_at`；**绝不**用 `updated_at`。

本测试专测这条修正（此前无独立回归，仅被间接覆盖）：
  1. 富 schema（有 waves/regions）：补记旧波 → 旧波**不进**窗口；
  2. 富 schema：窗口确实按 waves.created_at 排序；
  3. 最小库（无 waves）：退到 wave_results.created_at；
  4. 最小库：补写旧波 updated_at 也不改变窗口（守护「不用 updated_at」）。
"""
import sqlite3

from wqb.workflow.nodes import campaign as C


_BASE_COLS = ("id INTEGER PRIMARY KEY, region TEXT, wave_number TEXT, verdict TEXT, "
              "status TEXT, created_at TEXT, updated_at TEXT")


def _mkdb(tmp_path, *, rich=True):
    """rich=True 时建 waves/regions（富 schema 路径）；否则只建 wave_results（最小库）。"""
    db = tmp_path / "t.db"
    conn = sqlite3.connect(str(db))
    conn.execute(f"CREATE TABLE wave_results ({_BASE_COLS})")
    if rich:
        conn.execute("CREATE TABLE regions (id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("CREATE TABLE waves (id INTEGER PRIMARY KEY, region_id INTEGER, "
                     "wave_number TEXT, created_at TEXT)")
    conn.commit()
    return db, conn


def _seed_wave(conn, wave, verdict="FAIL", *, wr_created, updated=None, start=None, rid=None):
    """写一行 wave_results；rich 时另写一行 waves（start = 波的开始时刻）。"""
    conn.execute(
        "INSERT INTO wave_results (region, wave_number, verdict, status, created_at, updated_at) "
        "VALUES ('TESTREG',?,?,'closed',?,?)",
        (str(wave), verdict, wr_created, updated or wr_created),
    )
    if rid is not None:
        conn.execute(
            "INSERT INTO waves (region_id, wave_number, created_at) VALUES (?,?,?)",
            (rid, str(wave), start),
        )


def _add_region(conn, rid=1, name="TESTREG"):
    conn.execute("INSERT INTO regions (id, name) VALUES (?,?)", (rid, name))


# ---------------- 富 schema：补记旧波不进窗口（核心守护） ----------------

def test_backfilled_old_wave_does_not_enter_window(tmp_path):
    """KOR 91c 事故复现：旧波补记 PASS 后，窗口仍是最近 3 个（不含 91c）。"""
    _db, conn = _mkdb(tmp_path, rich=True)
    _add_region(conn)
    # 92–97 是最近的波（waves.created_at 递减 = 越新越大）；91c 更早
    for i, w in enumerate(["97", "96", "95", "92"], start=0):
        _seed_wave(conn, w, "FAIL", wr_created=f"2026-09-{28 - i:02d} 00:00:00",
                   start=f"2026-09-{28 - i:02d} 00:00:00", rid=1)
    # 旧波 91c：开始时刻远早于 92，但（补记后）updated_at 最新
    _seed_wave(conn, "91c", "PASS", wr_created="2026-09-10 00:00:00",
               updated="2026-10-02 12:00:00", start="2026-09-10 00:00:00", rid=1)
    conn.commit()

    window = C._recent_closed_waves(conn, "TESTREG", 3)
    waves_in = [w for w, _v in window]
    assert "91c" not in waves_in, f"补记的旧波 91c 不应进窗口，实得 {waves_in}"
    assert waves_in == ["97", "96", "95"], waves_in


def test_window_ordered_by_wave_start_time(tmp_path):
    _db, conn = _mkdb(tmp_path, rich=True)
    _add_region(conn)
    # created_at（waves）顺序：94 < 95 < 96（波号数字与开始时刻一致）
    _seed_wave(conn, "94", "FAIL", wr_created="2026-09-24 00:00:00",
               start="2026-09-24 00:00:00", rid=1)
    _seed_wave(conn, "95", "FAIL", wr_created="2026-09-25 00:00:00",
               start="2026-09-25 00:00:00", rid=1)
    _seed_wave(conn, "96", "PASS", wr_created="2026-09-26 00:00:00",
               start="2026-09-26 00:00:00", rid=1)
    conn.commit()
    window = C._recent_closed_waves(conn, "TESTREG", 2)
    assert [w for w, _ in window] == ["96", "95"]


def test_wave_start_beats_stale_wave_results_created_at(tmp_path):
    """waves.created_at 优先于 wave_results.created_at（后者可能被旧版 REPLACE 重置）。"""
    _db, conn = _mkdb(tmp_path, rich=True)
    _add_region(conn)
    # 96 的 wave_results.created_at 被重置得很晚，但 waves.created_at 表明它是较早的波
    _seed_wave(conn, "96", "FAIL", wr_created="2026-10-01 00:00:00",
               start="2026-09-26 00:00:00", rid=1)
    _seed_wave(conn, "97", "PASS", wr_created="2026-09-27 00:00:00",
               start="2026-09-27 00:00:00", rid=1)
    conn.commit()
    window = C._recent_closed_waves(conn, "TESTREG", 2)
    # 以 waves 开始时刻为准：97（09-27）新于 96（09-26）→ [97, 96]
    assert [w for w, _ in window] == ["97", "96"]


# ---------------- 最小库（无 waves）：退到 wave_results.created_at ----------------

def test_minimal_db_falls_back_to_wave_results_created_at(tmp_path):
    _db, conn = _mkdb(tmp_path, rich=False)
    for i, (w, v) in enumerate([("97", "FAIL"), ("96", "FAIL"), ("95", "PASS")]):
        _seed_wave(conn, w, v, wr_created=f"2026-09-{27 - i:02d} 00:00:00")
    conn.commit()
    window = C._recent_closed_waves(conn, "TESTREG", 2)
    assert [w for w, _ in window] == ["97", "96"]


def test_minimal_db_ignores_updated_at(tmp_path):
    """守护「不用 updated_at」：最小库里给旧波补写很新的 updated_at，窗口不变。"""
    _db, conn = _mkdb(tmp_path, rich=False)
    _seed_wave(conn, "97", "FAIL", wr_created="2026-09-27 00:00:00")
    _seed_wave(conn, "96", "FAIL", wr_created="2026-09-26 00:00:00")
    # 95 是最旧的波，但 updated_at 最新（补记）
    _seed_wave(conn, "95", "PASS", wr_created="2026-09-25 00:00:00",
               updated="2026-10-02 12:00:00")
    conn.commit()
    window = C._recent_closed_waves(conn, "TESTREG", 2)
    assert [w for w, _ in window] == ["97", "96"], "updated_at 不得影响窗口排序"


def test_only_closed_waves_are_counted(tmp_path):
    _db, conn = _mkdb(tmp_path, rich=False)
    conn.execute("INSERT INTO wave_results (region, wave_number, verdict, status, created_at, updated_at) "
                 "VALUES ('TESTREG','98','FAIL','open','2026-09-28 00:00:00','2026-09-28 00:00:00')")
    _seed_wave(conn, "97", "FAIL", wr_created="2026-09-27 00:00:00")
    conn.commit()
    window = C._recent_closed_waves(conn, "TESTREG", 5)
    assert [w for w, _ in window] == ["97"], "open 波不进窗口"
