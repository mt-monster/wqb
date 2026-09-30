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
    # 2026-09-29：签名跟随生产（新增 stats 归因参数），桩须与真实签名一致
    def _round(session, f, query, max_pages, read_top, seen, stats=None):
        if stats is not None:
            hits = posts_by_query.get(query, [])
            stats["hits"] = stats.get("hits", 0) + len(hits)
            stats["read_ok"] = stats.get("read_ok", 0) + len(hits)
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


# ------------------------------------------- 2026-09-29：故障 ≠ 论坛无解（假阴性修复）
def test_auth_failure_is_not_a_negative(env, monkeypatch):
    """认证/环境故障不得落 negative（否则被 SOP 当「论坛无解」判死取证 → 误判死）。

    实证：5 条 recon 记录里 2 条是故障（`load_creds` TypeError、
    `No module named 'requests'`），旧代码把它们记成 found=False 落
    `forum_recon_negative_*`，等于「工具坏了 ≡ 论坛无解」。
    """
    def _auth_fail(*a, **k):
        raise RuntimeError("No module named 'requests'")

    monkeypatch.setattr(fr, "_live_session", _auth_fail)
    q = "KOR shortinterest 卖空数据 prod correlation 撞墙 降相关"
    out = fr.recon(q, {"region": "KOR"}, "negative", 3, 8, None, False, env["db"])

    # ① found=None（未取证），严格区别于 found=False（确认无解）
    assert out["found"] is None, "故障必须返回 None（未取证），不得回落成 False"
    assert out["status"] == "error" and "requests" in out["error"]

    # ② 落 error 键，**不落** negative 键
    conn = sqlite3.connect(env["db"])
    keys = [r[0] for r in conn.execute("SELECT key FROM ledger_kv")]
    conn.close()
    qkey = fr._qkey(q)
    assert f"forum_recon_error_{qkey}" in keys
    assert f"forum_recon_negative_{qkey}" not in keys, "故障绝不得占用 negative 键名"


def test_auth_failure_is_not_cached(env, monkeypatch):
    """故障结论不进 7 天 TTL 缓存——故障应重试，不该被回放一周。"""
    def _auth_fail(*a, **k):
        raise RuntimeError("boom")

    monkeypatch.setattr(fr, "_live_session", _auth_fail)
    q = "故障不缓存验证题"
    fr.recon(q, {"region": "GLB"}, "negative", 3, 8, None, False, env["db"])

    raw = Path(fr.RECON_CACHE).read_text(encoding="utf-8") if Path(fr.RECON_CACHE).exists() else "{}"
    entries = json.loads(raw).get("entries", {})
    assert fr._qkey(q) not in entries, "故障条目不得写入缓存"

    # 二次调用必须重新尝试 live（证明没被缓存短路）
    calls = {"n": 0}

    def _count_fail(*a, **k):
        calls["n"] += 1
        raise RuntimeError("boom")

    monkeypatch.setattr(fr, "_live_session", _count_fail)
    fr.recon(q, {"region": "GLB"}, "negative", 3, 8, None, False, env["db"])
    assert calls["n"] == 1, "故障后重试必须真的再试一次（未被缓存回放）"


def test_zero_round_is_not_a_negative(env, monkeypatch):
    """一轮都没跑（关键词包为空）同样算未取证，不得记成论坛无解。"""
    monkeypatch.setattr(fr, "plan_queries", lambda *a, **k: [])
    monkeypatch.setattr(fr, "_live_session", lambda *a, **k: (_ for _ in ()).throw(
        AssertionError("零轮不得触网")))
    q = "零轮检索题"
    out = fr.recon(q, {"region": "GLB"}, "negative", 3, 8, None, False, env["db"])
    assert out["found"] is None and out["status"] == "error"
    conn = sqlite3.connect(env["db"])
    keys = [r[0] for r in conn.execute("SELECT key FROM ledger_kv")]
    conn.close()
    assert f"forum_recon_negative_{fr._qkey(q)}" not in keys


# ------------------------------------------------- 2026-09-29 命中率 0 的三处根因守护
_SNIPPET = ("实测 换手 turnover 过高会拉低 fitness，降换手的经验配方是用 ts_decay_linear 平滑权重，"
            "sharpe 与 fitness 同步改善，附具体表达式示例与回测对比。")


class _FakeFR:
    """forum_research 桩：resolve_id 按真实签名返回 **3-tuple**（回归守护的关键）。"""

    def __init__(self, is_comm=True):
        self.is_comm = is_comm
        self.read_args = []

    def search_html(self, session, query, max_pages=2):
        return [{"title": "如何降低 turnover", "click_href": "https://x/hc/zh-cn/search/click?data=abc",
                 "snippet": _SNIPPET, "votes": 12}]

    def resolve_id(self, session, href):
        return ("30927669645207", self.is_comm,
                "https://x/hc/zh-cn/community/posts/30927669645207-x")

    def read_post(self, session, pid):
        self.read_args.append(pid)
        return {"id": pid, "title": "如何降低 turnover", "body": LONG_BODY, "votes": 12}


def test_resolve_id_tuple_is_unpacked():
    """决定性根因：resolve_id 返回 3-tuple，未解包会把 tuple 当 post_id → read_post 恒失败。

    旧代码 `pid = fr.resolve_id(...)` → URL 变成 ".../posts/(123, True, 'http...').json"
    → body 恒空 → is_useful 恒 False → 命中率结构性为 0（搜到了也读不出来）。
    """
    fake = _FakeFR()
    stats: dict = {}
    out = fr.live_search_round(None, fake, "turnover", 2, 6, set(), stats)
    assert out, "解包修复后应能真正读出文章"
    assert fake.read_args, "必须真的调用了 read_post"
    assert all(isinstance(p, str) for p in fake.read_args), (
        f"read_post 必须收到字符串 post_id，实际收到 {fake.read_args!r}")
    assert stats.get("resolved") == 1
    assert stats.get("read_ok") == 1
    assert fr.is_useful(out[0])


def test_non_community_hit_is_skipped_not_read():
    """帮助中心文章（is_community=False）不是社区帖，社区 JSON API 读不到，须跳过。"""
    fake = _FakeFR(is_comm=False)
    stats: dict = {}
    out = fr.live_search_round(None, fake, "turnover", 2, 6, set(), stats)
    assert out == []
    assert fake.read_args == [], "非社区帖不得发起 read_post"
    assert stats.get("resolve_not_community") == 1
    assert stats.get("read_ok", 0) == 0


def test_stats_attribute_zero_hits():
    """零命中必须能归因：hits>0 且 read_ok=0 = 抓取链路故障，不是论坛无解。"""
    stats: dict = {}

    class _BrokenFR(_FakeFR):
        def read_post(self, session, pid):
            self.read_args.append(pid)
            return None            # 抓取链路故障

    fr.live_search_round(None, _BrokenFR(), "turnover", 2, 6, set(), stats)
    assert stats.get("hits", 0) > 0, "确曾搜到结果"
    assert stats.get("read_ok", 0) == 0, "但一篇都没读出来"
    assert stats.get("read_failed", 0) > 0


def test_is_useful_falls_back_to_snippet():
    """正文读不到时降级用搜索摘要：把「读不了」与「没内容」分开。"""
    assert fr.is_useful({"title": "降低 turnover 的配方", "body": "", "snippet": _SNIPPET})
    # 标题噪声仍然优先否决，摘要再好也不算
    assert not fr.is_useful({"title": "公告：直播通知", "body": "", "snippet": _SNIPPET})
    # 摘要太短同样不算（不放松到「有字就算」）
    assert not fr.is_useful({"title": "降低 turnover", "body": "", "snippet": "实测 换手"})


def test_plan_queries_no_cjk_splitting():
    """旧实现按 2–6 字机械窗口把完整词劈开（"表达式骨架设" + "计灵感"），必然 0 命中。"""
    out = fr.plan_queries("表达式骨架设计灵感有哪些", {"region": "GLB"}, None)
    assert not any(("表达式骨架设" in q or "计灵感" in q) for q in out), out
    assert "表达式" in out and "骨架" in out, out


def test_plan_queries_question_terms_outrank_context():
    """问题自身术语不得被 context 实体（dataset/墙词）挤到截断层之外。"""
    ctx = {"region": "KOR", "dataset": "pv1", "wall": "LOW_SUB_UNIVERSE_SHARPE"}
    out = fr.plan_queries("short interest 卖空数据 prod correlation 撞墙", ctx, None)
    assert "short interest" in out[:5], out[:5]
    assert "correlation" in out[:12], out[:12]
    assert "卖空" in out, out          # 中文领域词仍须保留


def test_plan_queries_wall_code_maps_to_forum_terms():
    """墙码须映射成论坛真实用语，而不是把码原样丢进搜索框。"""
    out = fr.plan_queries("怎么破", {"region": "USA", "wall": "LOW_SUB_UNIVERSE_SHARPE"}, None)
    assert any(t in out for t in ("子宇宙", "sub-universe")), out
    out2 = fr.plan_queries("怎么破", {"region": "USA", "wall": "HIGH_TURNOVER"}, None)
    assert any(t in out2 for t in ("换手", "turnover")), out2


def test_plan_queries_never_empty():
    """空包 = 零轮 = 未取证（found=None），不得让判死闸拿到假的无解结论。"""
    assert fr.plan_queries("有没有人试过", {}, None)
    assert fr.plan_queries("", {}, None)
