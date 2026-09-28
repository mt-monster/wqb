# -*- coding: utf-8 -*-
"""tools/forum_recon.py 守护（2026-09-28 论坛×流水线集成）.

覆盖设计契约：
  - 干跑零副作用（零网络、零写库）；
  - 7 天缓存回放（found / 负结果都不重复 live 查）；
  - **额度自适应**：以查出 limit 篇有效文章为标准——不足则继续扩关键词变体，
    命中即收束；扩尽/触安全上限仍无 → 负结果落库（判死证据）；
  - 有效文章判据（足量正文 + 可操作标记，滤公告/闲聊）；
  - 幽灵算子标注；KB/ledger 幂等写（by post_id）。
"""
import json
import sqlite3
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools"))

import forum_recon as fr  # noqa: E402

LONG_BODY = ("实测 GLB model264 慢基本面强度墙：改用 group_zscore 自归一化后 sharpe 从 1.4 提到 1.9，"
             "换手 12%、prod 0.52，稳健性跨三年通过。配方要点是 ts_backfill(66) + ts_decay_linear。" * 2)


def _mk_db(tmp_path):
    db = tmp_path / "wqb_test.db"
    conn = sqlite3.connect(str(db))
    conn.execute("CREATE TABLE ledger_kv (id INTEGER PRIMARY KEY AUTOINCREMENT, "
                 "region VARCHAR(50) NOT NULL, key VARCHAR(200) NOT NULL, value JSON NOT NULL, "
                 "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
                 "updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, UNIQUE(region, key))")
    conn.commit()
    conn.close()
    return str(db)


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setattr(fr, "RECON_CACHE", str(tmp_path / "recon_cache.json"))
    monkeypatch.setattr(fr, "_load_ghost_names", lambda db: ["ts_entropy", "sigmoid"])
    calls = {"live": 0}

    def _no_live(*a, **k):
        calls["live"] += 1
        raise AssertionError("不应触网")

    monkeypatch.setattr(fr, "_live_session", _no_live)
    return {"db": _mk_db(tmp_path), "calls": calls, "monkeypatch": monkeypatch}


# ---------------------------------------------------------------- 干跑与缓存
def test_dry_run_zero_side_effects(env, monkeypatch):
    def _boom(*a, **k):
        raise AssertionError("dry-run 不得进入 live 检索")

    monkeypatch.setattr(fr, "live_search_round", _boom)
    out = fr.recon("GLB 慢基本面墙有无破墙配方", {"region": "GLB"}, "ledger", 3, 8,
                   None, True, env["db"])
    assert out["dry_run"] is True and out["plan"]["question_key"]
    assert not Path(fr.RECON_CACHE).exists()          # 零写库（连缓存都不落）


def test_cache_replay_found(env, monkeypatch):
    key = fr._qkey("同问题")
    fr._save_recon_cache({"entries": {key: {
        "question": "同问题", "found": True, "searched_at": fr._now_iso(),
        "articles": [{"post_id": "p1"}]}}})

    def _boom(*a, **k):
        raise AssertionError("缓存命中不得 live 查")

    monkeypatch.setattr(fr, "live_search_round", _boom)
    out = fr.recon("同问题", {}, "ledger", 3, 8, None, False, env["db"])
    assert out["from_cache"] is True and out["found"] is True


def test_negative_cache_replayed(env, monkeypatch):
    key = fr._qkey("无解问题")
    fr._save_recon_cache({"entries": {key: {
        "question": "无解问题", "found": False, "searched_at": fr._now_iso()}}})

    def _boom(*a, **k):
        raise AssertionError("负缓存命中不得 live 查")

    monkeypatch.setattr(fr, "live_search_round", _boom)
    out = fr.recon("无解问题", {}, "ledger", 3, 8, None, False, env["db"])
    assert out["found"] is False and out.get("from_cache") is True


# ---------------------------------------------------------------- 额度自适应
def _fake_live(posts_by_query):
    def _round(session, f, query, max_pages, read_top, seen):
        return [dict(p, query=query) for p in posts_by_query.get(query, [])]
    return _round


def test_quota_adaptive_stops_at_limit(env, monkeypatch):
    """每轮 1 篇有效：limit=2 → 第 2 轮命中即收束，不继续搜。"""
    useful = {"q1": [{"post_id": "a1", "title": "实盘", "body": LONG_BODY}],
              "q2": [{"post_id": "a2", "title": "实盘2", "body": LONG_BODY}]}
    monkeypatch.setattr(fr, "live_search_round", _fake_live(useful))
    monkeypatch.setattr(fr, "_live_session", lambda: (object(), object()))
    out = fr.recon("q1 q2", {}, "ledger", 2, 8, "q1,q2,q3,q4", False, env["db"])
    assert out["found"] is True and out["n_useful"] == 2
    assert out["rounds"] == 2                        # 第 3/4 轮不再跑
    assert out["queries_tried"] == ["q1", "q2"]


def test_quota_adaptive_expands_until_found(env, monkeypatch):
    """前两轮全垃圾 → 继续扩；第 3 轮命中即停（额度以有效文章为标准，非固定小硬顶）。"""
    junk = {"body": "短", "title": "闲聊"}
    useful = {"broad 问题": [{"post_id": "b1", "title": "破墙实盘", "body": LONG_BODY}]}
    table = {"narrow1": [dict(junk, post_id="j1")], "narrow2": [dict(junk, post_id="j2")]}
    table.update(useful)
    monkeypatch.setattr(fr, "live_search_round", _fake_live(table))
    monkeypatch.setattr(fr, "_live_session", lambda: (object(), object()))
    out = fr.recon("narrow1", {"wall": "问题"}, "ledger", 1, 8,
                   "narrow1,narrow2,broad 问题", False, env["db"])
    assert out["found"] is True and out["n_useful"] == 1
    assert out["rounds"] == 3


def test_negative_result_written_when_exhausted(env, monkeypatch):
    junk = [{"post_id": "j", "title": "公告：直播预告", "body": "x" * 500}]
    monkeypatch.setattr(fr, "live_search_round", _fake_live({"a": junk, "b": junk}))
    monkeypatch.setattr(fr, "_live_session", lambda: (object(), object()))
    out = fr.recon("a b", {"region": "GLB"}, "ledger", 1, 2, "a,b", False, env["db"])
    assert out["found"] is False
    assert out["sink"].endswith(f"/forum_recon_negative_{fr._qkey('a b')}")
    # 负结果落 ledger（判死证据）
    conn = sqlite3.connect(env["db"])
    row = conn.execute("SELECT value FROM ledger_kv WHERE key LIKE 'forum_recon_negative_%'").fetchone()
    conn.close()
    assert row and json.loads(row[0])["found"] is False


# ---------------------------------------------------------------- 判据与标注
def test_is_useful_heuristic():
    assert fr.is_useful({"title": "实盘复盘", "body": LONG_BODY}) is True
    assert fr.is_useful({"title": "实盘复盘", "body": "太短"}) is False          # 正文不足
    assert fr.is_useful({"title": "公告：获奖名单", "body": LONG_BODY}) is False   # 噪声标题
    assert fr.is_useful({"title": "随便聊聊", "body": "x" * 400}) is False        # 无操作性标记


def test_ghost_scan_annotations(env, monkeypatch):
    monkeypatch.setattr(fr, "live_search_round", _fake_live({
        "g": [{"post_id": "g1", "title": "配方", "body": LONG_BODY + " 用 sigmoid(ts_entropy(x)) 平滑。"}]}))
    monkeypatch.setattr(fr, "_live_session", lambda: (object(), object()))
    out = fr.recon("g", {}, "ledger", 1, 4, "g", False, env["db"])
    assert set(out["articles"][0]["ghost_operators"]) == {"sigmoid", "ts_entropy"}


# ---------------------------------------------------------------- 入库幂等
def test_kb_merge_idempotent_by_post_id(env):
    db = env["db"]
    conn = sqlite3.connect(db)
    conn.execute("INSERT INTO ledger_kv (region, key, value) VALUES ('KB','community_tpl_kb','{}')")
    conn.commit()
    conn.close()
    ent = [{"post_id": "p1", "title": "t", "excerpt": "e"}]
    fr._kb_merge_entries(db, ent)
    fr._kb_merge_entries(db, [dict(ent[0], title="t2")])     # 同 post_id 覆盖
    conn = sqlite3.connect(db)
    raw = conn.execute("SELECT value FROM ledger_kv WHERE key='community_tpl_kb'").fetchone()[0]
    conn.close()
    kb = json.loads(raw)
    assert len(kb["forum_recon_entries"]) == 1
    assert kb["forum_recon_entries"][0]["title"] == "t2"


def test_ledger_upsert_updates_in_place(env):
    fr._ledger_upsert(env["db"], "GLB", "forum_recon_x", {"v": 1})
    fr._ledger_upsert(env["db"], "GLB", "forum_recon_x", {"v": 2})
    conn = sqlite3.connect(env["db"])
    rows = conn.execute("SELECT value FROM ledger_kv WHERE key='forum_recon_x'").fetchall()
    conn.close()
    assert len(rows) == 1 and json.loads(rows[0][0])["v"] == 2
