# -*- coding: utf-8 -*-
"""波级默认取证的工具（`tools/forum_recon_wave.py`）与节点（`forum_recon_wave`）守护。

工具用真实 schema 的临时库（`CampaignStore`）+ 假 recon 函数：不碰网络、不碰真库。
覆盖：读库派生问题、每波 ≤ 1 次（可靠结局占额度 / 故障不占额度 / --force）、干跑零写库、不问时零副作用、
最后一行 JSON 契约与退出码、节点的 dry-run 契约与退出码 → found/status 映射（故障 ≠ 无解）。
"""
import json
import sqlite3
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "tools"))

from wqb import recon_evidence as RE  # noqa: E402
from wqb.store import CampaignStore  # noqa: E402
from wqb.workflow.nodes import forum_recon_wave as node  # noqa: E402

import forum_recon_wave as tool  # noqa: E402


# ----------------------------------------------------------------------------- 夹具
WALL_ROWS = [
    {"alpha_id": f"w{i}", "code": f"rank(f{i})", "status": "COMPLETE", "sharpe": 1.7, "fitness": 1.1,
     "ra_failed_checks": ["LOW_2Y_SHARPE"]} for i in range(3)
] + [{"alpha_id": "ok1", "code": "rank(g)", "status": "COMPLETE", "sharpe": 1.9, "fitness": 1.2, "ra_failed_checks": []}]


@pytest.fixture()
def db(tmp_path):
    path = tmp_path / "wqb.db"
    st = CampaignStore(str(path))
    st.upsert_backtest_rows("KOR", "97", WALL_ROWS, dataset="analyst4")
    st.close()
    return str(path)


def _ledger(db_path, region, key):
    conn = sqlite3.connect(db_path)
    try:
        row = conn.execute("SELECT value FROM ledger_kv WHERE region=? AND key=?", (region, key)).fetchone()
    finally:
        conn.close()
    return json.loads(row[0]) if row else None


def _ledger_count(db_path):
    conn = sqlite3.connect(db_path)
    try:
        return conn.execute("SELECT COUNT(*) FROM ledger_kv").fetchone()[0]
    finally:
        conn.close()


class FakeRecon:
    """记录调用的假 recon（签名同 `forum_recon.recon`）。"""

    def __init__(self, outcome=None, boom=None):
        self.calls = []
        self.outcome = outcome if outcome is not None else {"found": True, "n_useful": 2, "sink": "KOR/forum_recon_x"}
        self.boom = boom

    def __call__(self, question, context, out_mode, limit, max_rounds, queries, dry_run, db_path):
        self.calls.append({"question": question, "context": context, "out_mode": out_mode, "limit": limit,
                           "max_rounds": max_rounds, "queries": queries, "dry_run": dry_run})
        if self.boom:
            raise self.boom
        if dry_run:
            return {"dry_run": True, "plan": {"question": question, "queries": ["a", "b"]}}
        return dict(self.outcome)


# ----------------------------------------------------------------------------- 读库
def test_load_rows_reads_the_wave_dedupes_by_alpha_and_filters_by_dataset(db):
    rows = tool.load_rows(db, "KOR", "97")
    assert len(rows) == 4 and {r["dataset"] for r in rows} == {"analyst4"}
    assert next(r for r in rows if r["alpha_id"] == "w0")["ra_failed_checks"] in (["LOW_2Y_SHARPE"], '["LOW_2Y_SHARPE"]')
    assert tool.load_rows(db, "KOR", "97", dataset="other") == []
    assert tool.load_rows(db, "KOR", "98") == [] and tool.load_rows(db, "USA", "97") == []


def test_load_rows_takes_prod_correlation_from_alphas(db):
    conn = sqlite3.connect(db)                                       # 收批入库时 store 已为每个 alpha 建了 alphas 行；这里只补 prod 相关性
    try:
        assert conn.execute("UPDATE alphas SET prod_correlation = 0.83 WHERE alpha_id = 'w0'").rowcount == 1
        conn.commit()
    finally:
        conn.close()
    assert next(r for r in tool.load_rows(db, "KOR", "97") if r["alpha_id"] == "w0")["prod_correlation"] == 0.83


def test_load_helpers_never_create_or_crash_on_a_missing_db(tmp_path):
    missing = str(tmp_path / "nope.db")
    assert tool.load_rows(missing, "KOR", "97") == [] and tool.load_ledger(missing, "KOR", "k") is None
    assert not Path(missing).exists()                                 # 只读：不悄悄建空库


# ----------------------------------------------------------------------------- 主流程
def test_a_wall_wave_asks_once_and_writes_the_marker(db):
    rec = FakeRecon({"found": True, "n_useful": 2, "sink": "KOR/forum_recon_abc"})
    r = tool.run_wave("KOR", "97", db_path=db, recon_fn=rec)
    assert len(rec.calls) == 1
    c = rec.calls[0]
    assert c["question"] == "KOR analyst4 2Y 稳健性墙 破墙配方" and c["out_mode"] == "ledger" and c["dry_run"] is False
    assert c["context"] == {"region": "KOR", "dataset": "analyst4", "wall": "2Y"}
    assert (r["found"], r["status"], r["exit_code"], r["kind"], r["wall"], r["skipped"]) == (True, "ok", 0, "wall", "2Y", False)
    assert r["marker"] == "KOR/forum_recon_wave_97" and r["question_key"] == RE.question_key(c["question"])
    m = _ledger(db, "KOR", RE.key_wave(97))
    assert m["status"] == "ok" and m["question_key"] == r["question_key"] and m["sink"] == "KOR/forum_recon_abc"
    assert m["basis"]["n_blocked"] == 3 and m["dataset"] == "analyst4" and m["forced"] is False


def test_a_reliable_outcome_uses_up_the_wave_quota(db):
    rec = FakeRecon({"found": True, "sink": "KOR/forum_recon_abc"})
    tool.run_wave("KOR", "97", db_path=db, recon_fn=rec)
    r = tool.run_wave("KOR", "97", db_path=db, recon_fn=rec)
    assert len(rec.calls) == 1                                        # 第二次不再查
    assert r["skipped"] is True and r["reason"] == "already_done" and r["found"] is True and r["status"] == "ok"
    assert r["exit_code"] == 0 and r["sink"] == "KOR/forum_recon_abc" and r["previous_done_at"]


def test_a_reliable_no_result_also_uses_up_the_quota_and_replays_exit_code_2(db):
    rec = FakeRecon({"found": False, "sink": "KOR/forum_recon_negative_abc"})
    first = tool.run_wave("KOR", "97", db_path=db, recon_fn=rec)
    assert (first["found"], first["status"], first["exit_code"]) == (False, "no_result", 2)
    again = tool.run_wave("KOR", "97", db_path=db, recon_fn=rec)
    assert len(rec.calls) == 1 and again["skipped"] is True and again["found"] is False and again["exit_code"] == 2
    assert _ledger(db, "KOR", RE.key_wave(97))["status"] == "no_result"


def test_a_tool_fault_is_recorded_but_does_not_use_up_the_quota(db):
    rec = FakeRecon({"found": None, "error": "论坛鉴权失败"})
    r = tool.run_wave("KOR", "97", db_path=db, recon_fn=rec)
    assert (r["found"], r["status"], r["exit_code"]) == (None, "error", 1) and "鉴权" in r["error"]
    assert _ledger(db, "KOR", RE.key_wave(97))["status"] == "error"   # 尝试留痕
    tool.run_wave("KOR", "97", db_path=db, recon_fn=rec)
    assert len(rec.calls) == 2                                        # 故障不占额度：修好后同一波可重跑
    rec.outcome = {"found": True}
    ok = tool.run_wave("KOR", "97", db_path=db, recon_fn=rec)
    assert ok["status"] == "ok" and _ledger(db, "KOR", RE.key_wave(97))["status"] == "ok"      # 成功后覆盖故障标记
    tool.run_wave("KOR", "97", db_path=db, recon_fn=rec)
    assert len(rec.calls) == 3                                        # 成功后才占额度


def test_an_unexpected_exception_is_a_fault_not_a_no_result(db):
    rec = FakeRecon(boom=RuntimeError("socket died"))
    r = tool.run_wave("KOR", "97", db_path=db, recon_fn=rec)
    assert r["found"] is None and r["status"] == "error" and r["exit_code"] == 1 and "socket died" in r["error"]
    assert _ledger(db, "KOR", RE.key_wave(97))["status"] == "error"


def test_force_ignores_the_marker(db):
    rec = FakeRecon({"found": True})
    tool.run_wave("KOR", "97", db_path=db, recon_fn=rec)
    r = tool.run_wave("KOR", "97", db_path=db, force=True, recon_fn=rec)
    assert len(rec.calls) == 2 and r["skipped"] is False
    assert _ledger(db, "KOR", RE.key_wave(97))["forced"] is True


def test_nothing_to_ask_has_no_side_effects(db, tmp_path):
    st = CampaignStore(str(tmp_path / "quiet.db"))
    st.upsert_backtest_rows("KOR", "5", [WALL_ROWS[0], WALL_ROWS[3]], dataset="analyst4")     # 1 条卡墙 + 1 条 pass：不是共同瓶颈
    st.close()
    quiet = str(tmp_path / "quiet.db")
    before = _ledger_count(quiet)
    rec = FakeRecon()
    r = tool.run_wave("KOR", "5", db_path=quiet, recon_fn=rec)
    assert rec.calls == [] and r["skipped"] is True and r["kind"] is None and r["reason"] == "nothing_to_ask"
    assert r["exit_code"] == 0 and _ledger_count(quiet) == before      # 不查论坛、不落标记
    empty = tool.run_wave("KOR", "404", db_path=db, recon_fn=rec)
    assert empty["reason"] == "no_rows" and rec.calls == [] and empty["exit_code"] == 0


def test_dry_run_derives_the_question_and_writes_nothing(db):
    before = _ledger_count(db)
    rec = FakeRecon()
    r = tool.run_wave("KOR", "97", db_path=db, dry_run=True, recon_fn=rec)
    assert len(rec.calls) == 1 and rec.calls[0]["dry_run"] is True                       # 只取检索计划
    assert r["dry_run"] is True and r["kind"] == "wall" and r["question"] == "KOR analyst4 2Y 稳健性墙 破墙配方"
    assert r["plan"]["queries"] == ["a", "b"] and r["exit_code"] == 0
    assert _ledger_count(db) == before and _ledger(db, "KOR", RE.key_wave(97)) is None    # 零写库


def test_dry_run_still_reports_a_previously_completed_wave_without_calling_recon(db):
    rec = FakeRecon({"found": True})
    tool.run_wave("KOR", "97", db_path=db, recon_fn=rec)
    rec2 = FakeRecon()
    r = tool.run_wave("KOR", "97", db_path=db, dry_run=True, recon_fn=rec2)
    assert rec2.calls == [] and r["skipped"] is True and r["reason"] == "already_done"


def test_dataset_argument_narrows_the_rows(db):
    rec = FakeRecon()
    r = tool.run_wave("KOR", "97", "other", db_path=db, recon_fn=rec)
    assert r["skipped"] is True and r["reason"] == "no_rows" and rec.calls == []


def test_marker_write_failure_is_reported_not_raised(db, monkeypatch):
    def _boom(*a, **k):
        raise sqlite3.OperationalError("database is locked")

    monkeypatch.setattr(tool.fr, "_ledger_upsert", _boom)
    r = tool.run_wave("KOR", "97", db_path=db, recon_fn=FakeRecon({"found": True}))
    assert r["found"] is True and "locked" in r["marker_error"] and "marker" not in r


# ----------------------------------------------------------------------------- CLI
def test_main_prints_a_final_json_line_and_returns_the_exit_code(db, monkeypatch, capsys):
    monkeypatch.setattr(tool.fr, "recon", FakeRecon({"found": False, "sink": "KOR/forum_recon_negative_z"}))
    rc = tool.main(["--region", "KOR", "--wave", "97", "--db", db])
    assert rc == 2
    last = capsys.readouterr().out.strip().splitlines()[-1]
    assert last.startswith('{"tool": "forum_recon_wave"')
    obj = json.loads(last)
    assert obj["found"] is False and obj["status"] == "no_result" and obj["wave"] == "97"


def test_main_turns_a_crash_into_exit_1_with_a_json_line(db, monkeypatch, capsys):
    def _boom(*a, **k):
        raise RuntimeError("kaput")

    monkeypatch.setattr(tool, "run_wave", _boom)
    assert tool.main(["--region", "KOR", "--wave", "97", "--db", db]) == 1
    obj = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert obj["found"] is None and obj["status"] == "error" and "kaput" in obj["error"]


# ----------------------------------------------------------------------------- 节点
def _fake_run(rc=0, timed_out=False, tail=""):
    def _run(cmd, **kw):
        return {"log_path": "L.log", "elapsed_sec": 0.1, "tail": tail, "returncode": rc, "timed_out": timed_out}
    return _run


def _tool_line(**kw):
    return "noise\n" + json.dumps({"tool": "forum_recon_wave", **kw}, ensure_ascii=False) + "\n"


def test_node_dry_run_builds_the_cmd_without_subprocess_or_db(monkeypatch):
    def _boom(*a, **k):
        raise AssertionError("dry-run 不得 subprocess")

    monkeypatch.setattr(node, "run_logged_subprocess", _boom)
    out = node.run(region="KOR", wave="97", dataset="analyst4", force=True, limit=2, max_search_rounds=5, dry_run=True)
    assert out["success"] is True and out["dry_run"] is True
    cmd = out["cmd"]
    assert "forum_recon_wave.py" in cmd[2]
    for flag, val in (("--region", "KOR"), ("--wave", "97"), ("--dataset", "analyst4"), ("--limit", "2"),
                      ("--max-search-rounds", "5")):
        assert cmd[cmd.index(flag) + 1] == val
    assert "--force" in cmd and "--dry-run" not in cmd
    assert "argv" not in out.get("error", "")                          # 真实 validate_argv 通过：工具声明了节点传的每个 flag


def test_node_dry_run_omits_optional_flags_by_default(monkeypatch):
    monkeypatch.setattr(node, "run_logged_subprocess", lambda *a, **k: (_ for _ in ()).throw(AssertionError("no")))
    cmd = node.run(region="KOR", wave="97", dry_run=True)["cmd"]
    assert "--dataset" not in cmd and "--force" not in cmd


@pytest.mark.parametrize("kw,msg", [({"region": "  ", "wave": "1"}, "region 不能为空"),
                                    ({"region": "KOR", "wave": ""}, "wave 不能为空")])
def test_node_param_validation_short_circuits(monkeypatch, kw, msg):
    monkeypatch.setattr(node, "run_logged_subprocess", lambda *a, **k: (_ for _ in ()).throw(AssertionError("no")))
    out = node.run(**kw)
    assert out["success"] is False and msg in out["error"]


def test_node_rc0_with_a_hit(monkeypatch):
    monkeypatch.setattr(node, "run_logged_subprocess", _fake_run(0, tail=_tool_line(
        found=True, status="ok", kind="wall", wall="2Y", dataset="analyst4", question="q", question_key="k1",
        skipped=False, sink="KOR/forum_recon_k1", marker="KOR/forum_recon_wave_97")))
    out = node.run(region="KOR", wave="97")
    assert out["success"] is True and out["found"] is True and out["status"] == "ok"
    assert (out["wall"], out["question_key"], out["sink"], out["marker"]) == ("2Y", "k1", "KOR/forum_recon_k1", "KOR/forum_recon_wave_97")


def test_node_rc0_skipped_is_success_without_a_found(monkeypatch):
    monkeypatch.setattr(node, "run_logged_subprocess", _fake_run(0, tail=_tool_line(
        found=None, skipped=True, reason="nothing_to_ask", kind=None, note="本波没有共同瓶颈可问")))
    out = node.run(region="KOR", wave="97")
    assert out["success"] is True and out["found"] is None and out["status"] == "skipped" and out["reason"] == "nothing_to_ask"


def test_node_rc0_without_parseable_output_is_flagged_not_guessed(monkeypatch):
    monkeypatch.setattr(node, "run_logged_subprocess", _fake_run(0, tail="garbage\n"))
    out = node.run(region="KOR", wave="97")
    assert out["success"] is True and out["found"] is None and out["status"] == "unknown" and "parse_warning" in out


def test_node_rc2_is_a_reliable_no_result_not_a_failure(monkeypatch):
    monkeypatch.setattr(node, "run_logged_subprocess", _fake_run(2, tail=_tool_line(
        found=False, status="no_result", kind="dead_end", question="KOR analyst4 有无解法", question_key="k2")))
    out = node.run(region="KOR", wave="97")
    assert out["success"] is True and out["found"] is False and out["status"] == "no_result" and out["kind"] == "dead_end"


def test_node_rc1_is_a_tool_fault_never_found_false(monkeypatch):
    monkeypatch.setattr(node, "run_logged_subprocess", _fake_run(1, tail=_tool_line(
        found=None, status="error", question_key="k3", error="鉴权失败")))
    out = node.run(region="KOR", wave="97")
    assert out["success"] is False and out["found"] is None and out["status"] == "error"
    assert "不是「论坛无解」" in out["error"] and RE.key_error("k3") in out["error"]


def test_node_timeout_is_a_tool_fault(monkeypatch):
    monkeypatch.setattr(node, "run_logged_subprocess", _fake_run(None, timed_out=True))
    out = node.run(region="KOR", wave="97", timeout_sec=1)
    assert out["success"] is False and out["found"] is None and out["status"] == "error" and out["timed_out"] is True


def test_node_parse_takes_the_last_tool_line_and_ignores_broken_json():
    assert node._parse_tool_json(_tool_line(found=True) + _tool_line(found=False))["found"] is False
    assert node._parse_tool_json('{"tool": "forum_recon_wave", broken') is None
    assert node._parse_tool_json("") is None and node._parse_tool_json(None) is None


# ----------------------------------------------------------------------------- 「收批时」的接线：pipeline.py --forum-recon 与 batch_track 默认透传
import importlib.util  # noqa: E402
import subprocess  # noqa: E402
import types  # noqa: E402

PIPELINE = REPO / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts" / "pipeline.py"


def _load_pipeline():
    spec = importlib.util.spec_from_file_location("pipeline_forum_recon_wave", str(PIPELINE))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_pipeline_declares_the_flag_and_runs_the_stage_after_review_and_prod_first():
    pl = _load_pipeline()
    assert callable(getattr(pl, "stage_forum_recon", None))
    src = PIPELINE.read_text(encoding="utf-8")
    assert '"--forum-recon"' in src and "stage_forum_recon(ctx, a)" in src
    i_review, i_prod, i_recon = (src.index("stage_review(ctx, ck, a.write_ledger"), src.index("stage_prod_first(ctx, a)"),
                                 src.index("stage_forum_recon(ctx, a)"))
    assert i_review < i_prod < i_recon                                # 评审 → prod 探针（prod 墙才看得见）→ 取证


def _stage_env(monkeypatch, result=None, boom=None):
    pl = _load_pipeline()
    seen = {}

    def _run(cmd, **kw):
        seen["cmd"], seen["kw"] = cmd, kw
        if boom:
            raise boom
        return result

    monkeypatch.setattr(subprocess, "run", _run)
    ctx = types.SimpleNamespace(region="KOR")
    a = types.SimpleNamespace(wave="97", dataset="analyst4")
    return pl, ctx, a, seen


def _done(rc=0, out="", err=""):
    return types.SimpleNamespace(returncode=rc, stdout=out, stderr=err)


def test_stage_forum_recon_calls_the_tool_with_region_wave_dataset(monkeypatch, capsys):
    line = json.dumps({"tool": "forum_recon_wave", "kind": "wall", "wall": "2Y", "found": True, "status": "ok",
                       "question": "KOR analyst4 2Y 稳健性墙 破墙配方", "sink": "KOR/forum_recon_x"}, ensure_ascii=False)
    pl, ctx, a, seen = _stage_env(monkeypatch, _done(0, "noise\n" + line + "\n"))
    pl.stage_forum_recon(ctx, a)
    cmd = seen["cmd"]
    assert cmd[0] == sys.executable and cmd[1].endswith("forum_recon_wave.py")
    assert cmd[cmd.index("--region") + 1] == "KOR" and cmd[cmd.index("--wave") + 1] == "97"
    assert cmd[cmd.index("--dataset") + 1] == "analyst4" and seen["kw"]["timeout"] == 900
    out = capsys.readouterr().out
    assert "wall/2Y found=True status=ok" in out and "KOR/forum_recon_x" in out


def test_stage_forum_recon_reports_a_skip_and_a_reliable_no_result_without_alarm(monkeypatch, capsys):
    skip = json.dumps({"tool": "forum_recon_wave", "skipped": True, "reason": "nothing_to_ask", "note": "本波没有共同瓶颈可问"},
                      ensure_ascii=False)
    pl, ctx, a, _ = _stage_env(monkeypatch, _done(0, skip + "\n"))
    pl.stage_forum_recon(ctx, a)
    assert "未查（nothing_to_ask）" in capsys.readouterr().out
    neg = json.dumps({"tool": "forum_recon_wave", "kind": "dead_end", "found": False, "status": "no_result",
                      "question": "KOR analyst4 有无解法", "marker": "KOR/forum_recon_wave_97"}, ensure_ascii=False)
    pl, ctx, a, _ = _stage_env(monkeypatch, _done(2, neg + "\n"))
    pl.stage_forum_recon(ctx, a)                                       # 退出码 2 = 可靠的「论坛无解」：不是故障，不告警
    out = capsys.readouterr().out
    assert "found=False status=no_result" in out and "工具故障" not in out


def test_stage_forum_recon_never_blocks_the_pipeline(monkeypatch, capsys):
    pl, ctx, a, _ = _stage_env(monkeypatch, _done(1, json.dumps({"tool": "forum_recon_wave", "error": "缺凭据"}, ensure_ascii=False) + "\n"))
    pl.stage_forum_recon(ctx, a)                                       # 故障：只打印，不抛
    out = capsys.readouterr().out
    assert "工具故障（退出码 1，不是「论坛无解」，不占本波额度）" in out and "缺凭据" in out
    pl, ctx, a, _ = _stage_env(monkeypatch, boom=subprocess.TimeoutExpired("x", 1))
    pl.stage_forum_recon(ctx, a)                                       # 超时 / 任何异常：同样不抛
    assert "执行异常（不阻断）" in capsys.readouterr().out


def _bt(**overrides):
    from wqb.workflow import execute
    params = {"region": "KOR", "wave": "_t", "dataset": "_t"}
    params.update(overrides)
    return (execute("batch_track", params, dry_run=True).output or {}).get("command", "")


def test_batch_track_runs_the_wave_recon_by_default_and_it_can_be_switched_off():
    cmd = _bt()
    if not cmd:
        pytest.skip("toolkit 未安装，无命令可查")
    assert "--forum-recon" in cmd and "--review" in cmd                # 取证接在评审之后，由 pipeline.py 保证顺序（见上一个用例）
    assert "--forum-recon" not in _bt(forum_recon=False)               # 离线 / 无论坛凭据的环境可关
