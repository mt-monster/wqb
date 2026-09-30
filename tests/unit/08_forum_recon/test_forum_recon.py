# -*- coding: utf-8 -*-
"""tools/forum_recon.py 守护（2026-09-28 论坛×流水线集成）.

覆盖设计契约：
  - 干跑零副作用（零网络、零写库）；
  - 7 天缓存回放（found / 负结果都不重复 live 查）；
  - **额度自适应**：以查出 limit 篇有效文章为标准——不足则继续扩关键词变体，
    命中即收束；扩尽/触安全上限仍无 → 负结果落库（判死证据）；
  - 有效文章判据（足量正文 + 可操作标记，滤公告/闲聊）；
  - 幽灵算子标注；KB/ledger 幂等写（by post_id）；
  - **故障 ≠ 无解**（2026-09-29 事故的回归护栏）：鉴权 / 凭据 / 依赖 / 检索 / 读帖 / 对照检索任一失败都记 `forum_recon_error_<qkey>`
    （found=None、不入缓存、退出码 1），绝不落 `forum_recon_negative_*`；旧版留下的「found=false + error」缓存条目不回放。
"""
import json
import sqlite3
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
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
    monkeypatch.setattr(fr, "_control_probe", lambda session, f: None)      # 对照检索缺省通过；专门的用例再改
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


# ---------------------------------------------------------------- 缓存回放补写 ledger（判死闸按 question_key 回 ledger 核对取证）
def _ledger_value(db, region, key):
    conn = sqlite3.connect(db)
    try:
        row = conn.execute("SELECT value FROM ledger_kv WHERE region=? AND key=?", (region, key)).fetchone()
    finally:
        conn.close()
    return json.loads(row[0]) if row else None


def _no_live(monkeypatch):
    def _boom(*a, **k):
        raise AssertionError("缓存命中不得 live 查")
    monkeypatch.setattr(fr, "live_search_round", _boom)


def test_cache_replay_mirrors_a_negative_into_this_regions_ledger_once(env, monkeypatch):
    """缓存文件不分 region：别的 region 查出的负结果，回放时本 region 的 ledger 里要有记录，否则判死闸核对不到。"""
    _no_live(monkeypatch)
    key = fr._qkey("跨区问题")
    fr._save_recon_cache({"entries": {key: {"question": "跨区问题", "question_key": key, "found": False,
                                             "status": "no_result", "searched_at": fr._now_iso()}}})
    assert _ledger_value(env["db"], "KOR", fr.RE.key_negative(key)) is None
    out = fr.recon("跨区问题", {"region": "KOR"}, "ledger", 3, 8, None, False, env["db"])
    assert out["from_cache"] is True and out["found"] is False and out["sink"] == f"KOR/{fr.RE.key_negative(key)}"
    rec = _ledger_value(env["db"], "KOR", fr.RE.key_negative(key))
    assert rec["found"] is False and rec["question_key"] == key and "from_cache" not in rec
    # 已有记录不覆盖：第二次回放是幂等的
    conn = sqlite3.connect(env["db"])
    conn.execute("UPDATE ledger_kv SET value=? WHERE key=?", (json.dumps({"found": False, "keep": 1}), fr.RE.key_negative(key)))
    conn.commit()
    conn.close()
    fr.recon("跨区问题", {"region": "KOR"}, "ledger", 3, 8, None, False, env["db"])
    assert _ledger_value(env["db"], "KOR", fr.RE.key_negative(key)) == {"found": False, "keep": 1}


def test_cache_replay_mirrors_a_hit_only_when_the_sink_is_the_ledger(env, monkeypatch):
    _no_live(monkeypatch)
    key = fr._qkey("有货问题")
    fr._save_recon_cache({"entries": {key: {"question": "有货问题", "found": True, "status": "ok",
                                             "searched_at": fr._now_iso(), "articles": [{"post_id": "p1"}]}}})
    fr.recon("有货问题", {"region": "KOR"}, "kb", 3, 8, None, False, env["db"])
    assert _ledger_value(env["db"], "KOR", fr.RE.key_found(key)) is None            # kb 落点：不写 ledger 键
    fr.recon("有货问题", {"region": "KOR"}, "ledger", 3, 8, None, False, env["db"])
    assert _ledger_value(env["db"], "KOR", fr.RE.key_found(key))["found"] is True


def test_dry_run_cache_replay_writes_nothing(env, monkeypatch):
    _no_live(monkeypatch)
    key = fr._qkey("干跑回放")
    fr._save_recon_cache({"entries": {key: {"question": "干跑回放", "found": False, "searched_at": fr._now_iso()}}})
    fr.recon("干跑回放", {"region": "KOR"}, "ledger", 3, 8, None, True, env["db"])
    assert _ledger_value(env["db"], "KOR", fr.RE.key_negative(key)) is None


def test_a_mirror_failure_does_not_break_the_replay(env, monkeypatch, tmp_path):
    _no_live(monkeypatch)
    key = fr._qkey("写不进去")
    fr._save_recon_cache({"entries": {key: {"question": "写不进去", "found": False, "searched_at": fr._now_iso()}}})
    bare = tmp_path / "no_ledger.db"
    sqlite3.connect(str(bare)).close()                                                # 有库但没有 ledger_kv 表
    out = fr.recon("写不进去", {"region": "KOR"}, "ledger", 3, 8, None, False, str(bare))
    assert out["found"] is False and out["from_cache"] is True and out.get("sink_error")


# ---------------------------------------------------------------- 额度自适应
def _fake_live(posts_by_query):
    def _round(session, f, query, max_pages, read_top, seen, stats=None):
        posts = [dict(p, query=query) for p in posts_by_query.get(query, [])]
        if stats is not None:                                   # 模拟一轮「成功检索并读到这些帖」
            stats["searches_ok"] = stats.get("searches_ok", 0) + 1
            stats["hits"] = stats.get("hits", 0) + len(posts)
            stats["reads_ok"] = stats.get("reads_ok", 0) + len(posts)
        return posts
    return _round


def _ledger_keys(db, like):
    conn = sqlite3.connect(db)
    try:
        return [r[0] for r in conn.execute("SELECT key FROM ledger_kv WHERE key LIKE ?", (like,)).fetchall()]
    finally:
        conn.close()


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
    assert out["found"] is False and out["status"] == "no_result"
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


# ---------------------------------------------------------------- 故障 ≠ 无解（2026-09-29 事故）
def _boom_live(exc):
    def _session():
        raise exc
    return _session


@pytest.mark.parametrize("exc,code", [
    (fr.ReconToolError("auth_failed", "forum auth failed: RuntimeError: BRAIN auth failed: 401"), "auth_failed"),
    (fr.ReconToolError("credentials_missing", "缺凭据"), "credentials_missing"),
    (ImportError("No module named 'requests'"), "deps_missing"),
    (TypeError("stat: path should be string"), "unexpected"),
])
def test_session_failure_is_an_error_never_a_negative(env, monkeypatch, exc, code):
    """鉴权 / 凭据 / 依赖 / 未知异常 → found=None、status=error、落 forum_recon_error_*，**不**落 negative、**不**入缓存。"""
    monkeypatch.setattr(fr, "_live_session", _boom_live(exc))
    out = fr.recon("会话必炸", {"region": "GLB"}, "ledger", 1, 2, "a,b", False, env["db"])
    qk = fr._qkey("会话必炸")
    assert out["found"] is None and out["status"] == "error" and out["reason_code"] == code
    assert out["sink"] == f"GLB/forum_recon_error_{qk}"
    assert _ledger_keys(env["db"], "forum_recon_negative_%") == []
    assert _ledger_keys(env["db"], "forum_recon_error_%") == [f"forum_recon_error_{qk}"]
    assert not Path(fr.RECON_CACHE).exists()                    # 故障不入缓存——修好后同问题要重新 live 查
    assert fr.exit_code(out) == 1


def test_error_record_is_classified_as_error_by_the_shared_contract(env, monkeypatch):
    from wqb import recon_evidence as RE
    monkeypatch.setattr(fr, "_live_session", _boom_live(fr.ReconToolError("auth_failed", "x")))
    out = fr.recon("q", {"region": "GLB"}, "ledger", 1, 2, "a", False, env["db"])
    assert RE.classify_record(out) == "error"
    assert RE.evaluate_forum_recon(out)["allowed"] is False


def test_all_searches_failed_is_an_error_not_a_negative(env, monkeypatch):
    def _round(session, f, query, max_pages, read_top, seen, stats=None):
        stats["search_errors"] = stats.get("search_errors", 0) + 1       # 每轮都抛异常
        return []
    monkeypatch.setattr(fr, "live_search_round", _round)
    monkeypatch.setattr(fr, "_live_session", lambda: (object(), object()))
    out = fr.recon("检索全炸", {"region": "GLB"}, "ledger", 1, 2, "a,b", False, env["db"])
    assert out["status"] == "error" and out["reason_code"] == "search_failed" and out["found"] is None
    assert _ledger_keys(env["db"], "forum_recon_negative_%") == []


def test_one_failed_round_among_successes_still_blocks_the_negative(env, monkeypatch):
    calls = {"n": 0}

    def _round(session, f, query, max_pages, read_top, seen, stats=None):
        calls["n"] += 1
        key = "search_errors" if calls["n"] == 1 else "searches_ok"
        stats[key] = stats.get(key, 0) + 1
        return []
    monkeypatch.setattr(fr, "live_search_round", _round)
    monkeypatch.setattr(fr, "_live_session", lambda: (object(), object()))
    out = fr.recon("半炸", {"region": "GLB"}, "ledger", 1, 2, "a,b", False, env["db"])
    assert out["status"] == "error" and "轮检索异常" in out["error"]
    assert _ledger_keys(env["db"], "forum_recon_negative_%") == []


def test_hits_but_nothing_readable_is_an_error(env, monkeypatch):
    def _round(session, f, query, max_pages, read_top, seen, stats=None):
        stats["searches_ok"] = stats.get("searches_ok", 0) + 1
        stats["hits"] = stats.get("hits", 0) + 3                           # 搜到 3 条
        stats["read_errors"] = stats.get("read_errors", 0) + 3             # 一篇都没读成
        return []
    monkeypatch.setattr(fr, "live_search_round", _round)
    monkeypatch.setattr(fr, "_live_session", lambda: (object(), object()))
    out = fr.recon("读不出", {"region": "GLB"}, "ledger", 1, 1, "a", False, env["db"])
    assert out["status"] == "error" and out["reason_code"] == "read_failed"


def test_control_probe_failure_turns_a_would_be_negative_into_an_error(env, monkeypatch):
    junk = [{"post_id": "j", "title": "公告：直播预告", "body": "x" * 500}]
    monkeypatch.setattr(fr, "live_search_round", _fake_live({"a": junk}))
    monkeypatch.setattr(fr, "_live_session", lambda: (object(), object()))
    monkeypatch.setattr(fr, "_control_probe", lambda s, f: ("control_probe_failed", "对照检索 0 结果"))
    out = fr.recon("会话过期", {"region": "GLB"}, "ledger", 1, 1, "a", False, env["db"])
    assert out["status"] == "error" and out["reason_code"] == "control_probe_failed"
    assert _ledger_keys(env["db"], "forum_recon_negative_%") == []
    assert not Path(fr.RECON_CACHE).exists()


def test_control_probe_is_not_run_when_articles_were_found(env, monkeypatch):
    monkeypatch.setattr(fr, "live_search_round", _fake_live({"a": [{"post_id": "a1", "title": "实盘", "body": LONG_BODY}]}))
    monkeypatch.setattr(fr, "_live_session", lambda: (object(), object()))

    def _boom(s, f):
        raise AssertionError("有货时不需要对照检索")
    monkeypatch.setattr(fr, "_control_probe", _boom)
    out = fr.recon("有货", {}, "ledger", 1, 2, "a", False, env["db"])
    assert out["found"] is True and out["status"] == "ok"


def test_partial_round_failures_are_recorded_but_do_not_undo_a_hit(env, monkeypatch):
    def _round(session, f, query, max_pages, read_top, seen, stats=None):
        stats["search_errors"] = stats.get("search_errors", 0) + 1
        stats["searches_ok"] = stats.get("searches_ok", 0) + 1
        return [{"post_id": "a1", "title": "实盘", "body": LONG_BODY, "query": query}]
    monkeypatch.setattr(fr, "live_search_round", _round)
    monkeypatch.setattr(fr, "_live_session", lambda: (object(), object()))
    out = fr.recon("有货但中途炸过", {}, "ledger", 1, 2, "a", False, env["db"])
    assert out["found"] is True and out["search_errors"] == 1


def test_a_fresh_legacy_error_shaped_cache_entry_is_not_replayed(env, monkeypatch):
    """旧版把鉴权失败缓存成 found=false + error；这种条目不能再当「论坛无解」回放 7 天。"""
    key = fr._qkey("旧故障")
    fr._save_recon_cache({"entries": {key: {
        "question": "旧故障", "found": False, "error": "forum auth failed: TypeError", "searched_at": fr._now_iso()}}})
    live = {"n": 0}

    def _session():
        live["n"] += 1
        return object(), object()
    monkeypatch.setattr(fr, "_live_session", _session)
    monkeypatch.setattr(fr, "live_search_round", _fake_live({"a": [{"post_id": "a1", "title": "实盘", "body": LONG_BODY}]}))
    out = fr.recon("旧故障", {}, "ledger", 1, 2, "a", False, env["db"])
    assert live["n"] == 1 and out["found"] is True and not out.get("from_cache")


def test_exit_code_contract():
    assert fr.exit_code({"found": True}) == 0
    assert fr.exit_code({"found": False}) == 2
    assert fr.exit_code({"found": None, "status": "error"}) == 1
    assert fr.exit_code({"dry_run": True}) == 0


# ---------------------------------------------------------------- 凭据与依赖（live 路径旧版从未跑通过）
class _FakeFr:
    UA = "test-agent"

    def __init__(self, creds=None):
        self.creds = creds or {}
        self.paths = []

    def load_creds(self, env_path):
        self.paths.append(env_path)
        return dict(self.creds)


def _clear_creds(monkeypatch):
    for k in ("CREDENTIALS_EMAIL", "CREDENTIALS_PASSWORD"):
        monkeypatch.setenv(k, "x")
        monkeypatch.delenv(k)


def test_credentials_prefer_the_standard_env_names_and_do_not_touch_dotenv(monkeypatch):
    monkeypatch.setenv("CREDENTIALS_EMAIL", "user@example.test")
    monkeypatch.setenv("CREDENTIALS_PASSWORD", "placeholder-pw")
    f = _FakeFr()
    assert fr._load_credentials(f) == ("user@example.test", "placeholder-pw")
    assert f.paths == []                                             # 环境齐全就不读 .env


def test_credentials_fall_back_to_the_mcp_dotenv_path(monkeypatch):
    _clear_creds(monkeypatch)
    f = _FakeFr({"CREDENTIALS_EMAIL": "u@example.test", "CREDENTIALS_PASSWORD": "placeholder-pw"})
    assert fr._load_credentials(f) == ("u@example.test", "placeholder-pw")
    assert len(f.paths) == 1 and f.paths[0].replace("\\", "/").endswith("world-quant-brain-mcp/.env")


def test_missing_credentials_is_a_tool_error_that_names_variables_not_values(monkeypatch):
    _clear_creds(monkeypatch)
    with pytest.raises(fr.ReconToolError) as ei:
        fr._load_credentials(_FakeFr({}))
    assert ei.value.code == "credentials_missing" and "CREDENTIALS_EMAIL" in str(ei.value)


def test_the_old_load_creds_none_call_is_gone():
    src = (REPO_ROOT / "tools" / "forum_recon.py").read_text(encoding="utf-8")
    assert "load_creds(None)" not in src, "load_creds 要的是 .env 路径且返回 dict；传 None 会 TypeError（live 路径旧版从未跑通）"


# ---------------------------------------------------------------- 一轮检索的可靠性信号
class _SearchFr:
    def __init__(self, hits=None, search_exc=None, posts=None):
        self._hits, self._exc, self._posts = hits or [], search_exc, posts or {}

    def search_html(self, session, query, max_pages=2):
        if self._exc:
            raise self._exc
        return list(self._hits)

    def read_post(self, session, pid):
        p = self._posts.get(pid)
        if isinstance(p, Exception):
            raise p
        return p


def test_live_round_counts_search_failures_and_successes(monkeypatch):
    monkeypatch.setattr(fr.time, "sleep", lambda s: None)
    st = {}
    assert fr.live_search_round(None, _SearchFr(search_exc=RuntimeError("boom")), "q", 1, 3, set(), stats=st) == []
    assert st["search_errors"] == 1 and st["searches_ok"] == 0
    st2 = {}
    hits = [{"post_id": "p1"}, {"post_id": "p2"}, {"post_id": "p3"}]
    posts = {"p1": {"title": "t", "body": LONG_BODY}, "p2": RuntimeError("读帖炸了"), "p3": None}
    out = fr.live_search_round(None, _SearchFr(hits=hits, posts=posts), "q", 1, 3, set(), stats=st2)
    assert [p["post_id"] for p in out] == ["p1"]
    assert (st2["searches_ok"], st2["hits"], st2["reads_ok"], st2["read_errors"]) == (1, 3, 1, 2)


def test_control_probe_helper():
    assert fr._control_probe(None, _SearchFr(hits=[{"post_id": "x"}])) is None
    assert fr._control_probe(None, _SearchFr(hits=[]))[0] == "control_probe_failed"
    assert fr._control_probe(None, _SearchFr(search_exc=RuntimeError("x")))[0] == "control_probe_failed"


def test_unreliable_reason_table():
    ok = {"searches_ok": 3, "search_errors": 0, "hits": 4, "reads_ok": 2, "read_errors": 2}
    assert fr._unreliable_reason(ok) is None
    assert fr._unreliable_reason({"searches_ok": 0, "search_errors": 2})[0] == "search_failed"
    assert fr._unreliable_reason(dict(ok, search_errors=1))[0] == "search_failed"
    assert fr._unreliable_reason(dict(ok, reads_ok=0))[0] == "read_failed"
    assert fr._unreliable_reason({"searches_ok": 2, "hits": 0, "reads_ok": 0, "search_errors": 0}) is None   # 真没搜到任何结果
