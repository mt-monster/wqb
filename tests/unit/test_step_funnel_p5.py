# -*- coding: utf-8 -*-
"""回归测试：步级漏斗只读推导（2026-09-17）。

## 背景
`step_quality_metrics` / `step_efficiency_metrics` / `step_gain_metrics` /
`wave_summary` / `campaign_summary` 五张表自建成起恒为 0 行，评估结论是
**不接入**（理由见 `tools/step_funnel.py` 模块头）：唯一自动采集入口
`collect_from_checkpoint()` 是 TODO 空壳；9 个质量指标全可从既有表推导；
6 个增益指标是反事实估算、无客观来源。

替代方案即本工具：把"每步产出多少、哪一跳掉得最狠"从既有表**只读**推出来，
不建表、不写库。

本测试锁定：
1. 口径正确性（unconsumed 含 gem/selected；门禁表达式级计数从 report_json 提取）；
2. 单位一致性（转化链全部用表达式条数，不把"门禁次数"当表达式）；
3. 健壮性（缺表/脏 JSON 不崩，且不猜数）；
4. **只读性**（跑完 DB 文件字节不变）—— 这是本方案的核心承诺。
"""

import hashlib
import json
import os
import sqlite3
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, os.path.join(REPO, "src"))

import step_funnel  # noqa: E402


def _mkdb(tmp_path, *, with_tables=("expressions", "gate_results",
                                     "backtest_results", "wave_results", "ledger_kv")):
    """造一个最小可用的临时库。"""
    db = tmp_path / "t.db"
    conn = sqlite3.connect(str(db))
    if "expressions" in with_tables:
        conn.execute("""CREATE TABLE expressions(
            id INTEGER PRIMARY KEY, region TEXT, wave TEXT, status TEXT, created_at TEXT)""")
    if "gate_results" in with_tables:
        conn.execute("""CREATE TABLE gate_results(
            id INTEGER PRIMARY KEY, region TEXT, wave TEXT, dataset TEXT,
            all_pass INTEGER, report_json TEXT, created_at TEXT)""")
    if "backtest_results" in with_tables:
        conn.execute("""CREATE TABLE backtest_results(
            id INTEGER PRIMARY KEY, region TEXT, wave TEXT, status TEXT,
            sharpe REAL, fitness REAL, created_at TEXT)""")
    if "wave_results" in with_tables:
        conn.execute("""CREATE TABLE wave_results(
            id INTEGER PRIMARY KEY, region TEXT, wave_number TEXT, verdict TEXT)""")
    if "ledger_kv" in with_tables:
        conn.execute("""CREATE TABLE ledger_kv(
            id INTEGER PRIMARY KEY, region TEXT, key TEXT, value TEXT)""")
    conn.commit()
    return db, conn


def _seed(conn, region="TEST"):
    conn.executemany(
        "INSERT INTO expressions(region,wave,status,created_at) VALUES (?,?,?,?)",
        [(region, "w1", s, "2026-09-01T00:00:00") for s in
         # 3 gem + 2 selected + 1 pending + 1 gated + 2 backtested + 1 dropped = 10
         ["gem"] * 3 + ["selected"] * 2 + ["pending", "gated"] + ["backtested"] * 2 + ["dropped"]],
    )
    conn.execute(
        "INSERT INTO gate_results(region,wave,dataset,all_pass,report_json,created_at) "
        "VALUES (?,?,?,?,?,?)",
        (region, "w1", "ds1", 1, json.dumps({"total": 8, "passed": 6}), "2026-09-02T00:00:00"),
    )
    # 脏 JSON：不应让它崩，也不应计入表达式级
    conn.execute(
        "INSERT INTO gate_results(region,wave,dataset,all_pass,report_json,created_at) "
        "VALUES (?,?,?,?,?,?)",
        (region, "w1", "ds2", 0, "{not json", "2026-09-02T01:00:00"),
    )
    conn.executemany(
        "INSERT INTO backtest_results(region,wave,status,sharpe,fitness,created_at) "
        "VALUES (?,?,?,?,?,?)",
        [(region, "w1", "COMPLETE", 1.9, 1.2, "2026-09-03T00:00:00"),   # 过廉价闸
         (region, "w1", "COMPLETE", 1.2, 0.8, "2026-09-03T01:00:00"),   # 不过
         (region, "w1", "COMPLETE", None, None, "2026-09-03T02:00:00")],  # 无 sharpe
    )
    conn.executemany(
        "INSERT INTO wave_results(region,wave_number,verdict) VALUES (?,?,?)",
        [(region, "w1", "PASS"), (region, "w1", "FAIL"), (region, "w1", None)],
    )
    conn.execute("INSERT INTO ledger_kv(region,key,value) VALUES (?,?,?)",
                 (region, "submit_ready", json.dumps([{"id": "a"}, {"id": "b"}])))
    conn.commit()


# ---- 1. 口径正确性 --------------------------------------------------------

def test_unconsumed_includes_gem_and_selected(tmp_path):
    """unconsumed 必须含 gem/selected（旧口径只算 pending+gated 是 bug 来源）。"""
    _db, conn = _mkdb(tmp_path)
    _seed(conn)
    res = step_funnel.build_funnel(conn, "TEST")
    s2 = res["steps"]["S2_generate"]
    assert s2["total"] == 10
    # gem3 + selected2 + pending1 + gated1 = 7
    assert s2["unconsumed"] == 7
    assert s2["unconsumed_ratio"] == pytest.approx(0.7)


def test_gate_extracts_expression_level_counts(tmp_path):
    """表达式级放行数从 report_json 的 passed/total 汇总，脏 JSON 被跳过。"""
    _db, conn = _mkdb(tmp_path)
    _seed(conn)
    g = step_funnel.build_funnel(conn, "TEST")["steps"]["S2_S3_gate"]
    assert g["gate_checks"] == 2 and g["gate_passed"] == 1     # 批次粒度
    assert g["expr_total"] == 8 and g["expr_passed"] == 6      # 表达式粒度（脏 JSON 不计）


def test_chain_uses_consistent_units(tmp_path):
    """转化链必须用表达式条数 —— 不得把'门禁次数'(2) 当成表达式数。"""
    _db, conn = _mkdb(tmp_path)
    _seed(conn)
    res = step_funnel.build_funnel(conn, "TEST")
    got = {c["stage"]: c["count"] for c in res["chain"]}
    assert got["S2 生成"] == 10
    assert got["S2→S3 门禁放行"] == 6          # 不是 gate_checks(2)
    assert got["S3 回测完成"] == 2             # 有 sharpe 的
    assert got["S3 过廉价闸"] == 1             # S>1.58 & F>=1.0
    assert got["S4→S5 就绪"] == 2              # ledger submit_ready
    assert res["chain_note"] == "表达式级"


def test_bottleneck_picks_worst_leap(tmp_path):
    _db, conn = _mkdb(tmp_path)
    _seed(conn)
    bn = step_funnel.build_funnel(conn, "TEST")["bottleneck"]
    assert bn["stage"] and bn["rate"] is not None
    assert 0.0 <= bn["rate"] <= 1.0


# ---- 2. 健壮性：缺数据不崩、不猜 ------------------------------------------

def test_missing_tables_do_not_crash(tmp_path):
    """空库（一张业务表都没有）也必须能跑出结构完整的报告。"""
    _db, conn = _mkdb(tmp_path, with_tables=())
    res = step_funnel.build_funnel(conn, "NOPE")
    assert res["region"] == "NOPE"
    assert res["steps"]["S2_generate"] == {}
    assert res["steps"]["S4_S5_submit"]["submit_ready"] is None
    assert res["bottleneck"]["stage"] is None      # 无数据 → 不硬指一个瓶颈


def test_absent_ledger_key_is_none_not_zero(tmp_path):
    """缺键必须是 None（未知），不能报 0（会被误读成'确定没有'）。"""
    _db, conn = _mkdb(tmp_path)
    _seed(conn)
    s = step_funnel.build_funnel(conn, "TEST")["steps"]["S4_S5_submit"]
    assert s["submit_ready"] == 2
    assert s["submit_ready_blocked"] is None


def test_wave_filter_scopes_counts(tmp_path):
    _db, conn = _mkdb(tmp_path)
    _seed(conn, region="T1")
    conn.execute("INSERT INTO expressions(region,wave,status,created_at) VALUES (?,?,?,?)",
                 ("OTHER", "w1", "gem", "2026-09-01T00:00:00"))
    conn.commit()
    assert step_funnel.build_funnel(conn, "T1", wave="w1")["steps"]["S2_generate"]["total"] == 10


# ---- 3. 只读性（本方案的核心承诺）----------------------------------------

def test_run_does_not_modify_db(tmp_path, monkeypatch, capsys):
    """跑完一次 CLI，DB 文件字节必须完全不变 —— 不建表、不写库。"""
    db, conn = _mkdb(tmp_path)
    _seed(conn)
    conn.close()

    before = hashlib.sha256(db.read_bytes()).hexdigest()
    tables_before = sorted(
        r[0] for r in sqlite3.connect(str(db)).execute(
            "SELECT name FROM sqlite_master WHERE type='table'")
    )

    monkeypatch.setattr(step_funnel, "resolve_db_path", lambda: str(db))
    monkeypatch.setattr(sys, "argv", ["step_funnel.py", "--region", "TEST"])
    rc = step_funnel.main()
    assert rc == 0
    assert "步级漏斗" in capsys.readouterr().out

    after = hashlib.sha256(db.read_bytes()).hexdigest()
    tables_after = sorted(
        r[0] for r in sqlite3.connect(str(db)).execute(
            "SELECT name FROM sqlite_master WHERE type='table'")
    )
    assert before == after, "本工具必须只读，DB 被改动了"
    assert tables_before == tables_after, "本工具不得建表"


def test_json_mode_is_serializable(tmp_path, monkeypatch, capsys):
    db, conn = _mkdb(tmp_path)
    _seed(conn)
    conn.close()
    monkeypatch.setattr(step_funnel, "resolve_db_path", lambda: str(db))
    monkeypatch.setattr(sys, "argv", ["step_funnel.py", "--region", "TEST", "--json"])
    assert step_funnel.main() == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["steps"]["S2_generate"]["total"] == 10


def test_missing_db_returns_nonzero(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(step_funnel, "resolve_db_path",
                        lambda: str(tmp_path / "nope.db"))
    monkeypatch.setattr(sys, "argv", ["step_funnel.py", "--region", "X"])
    assert step_funnel.main() == 2
    assert "找不到 DB" in capsys.readouterr().err


# ---- 4. 下线决策必须留痕（防止"空表又长回来"）--------------------------

def test_tool_documents_the_no_wiring_verdict():
    """工具头部必须记录'为何不写那五张表'的证据，否则下次容易被重新接入。"""
    src = open(os.path.join(REPO, "tools", "step_funnel.py"), encoding="utf-8").read()
    for need in ["collect_from_checkpoint", "空壳", "反事实", "campaign_summary",
                 "同名但无关"]:
        assert need in src, f"缺少评估依据：{need}"


def test_subsystem_is_archived_not_live():
    """子系统必须处于'已归档'状态：决策留痕 README 存在，且原位源码已清空。

    注：最早的版本曾断言 8 个源码文件归档进 attic/step_metrics_20260917/。
    事后核验那些文件从未纳入本仓库版本控制（git ls-files / git log --all 均无记录），
    是已弃用宿主（.box-agent/.qoder-cn/.zcode）的实验性产物，已在弃用宿主清理时移除。
    故本测试只锁定"决策已留痕 + 原位已清空"这一可验证终态，不在归档里编造无法溯源的快照。
    详见 attic/step_metrics_20260917/README.md。
    """
    attic = os.path.join(REPO, "attic", "step_metrics_20260917")
    assert os.path.isdir(attic), "归档目录不存在"
    assert os.path.isfile(os.path.join(attic, "README.md")), "归档缺少 README（决策留痕）"

    # 原位必须已清空（否则会被 import / 收集到）
    for gone in ("tools/step_metrics_collector.py", "tools/step_gain_reporter.py",
                 "tools/wave_summary_computer.py", "tools/campaign_summary_computer.py",
                 "tools/migrate_step_metrics.py",
                 "src/wqb/workflow/nodes/step_metrics.py",
                 "tests/unit/test_step_metrics.py"):
        assert not os.path.exists(os.path.join(REPO, gone)), f"原位仍有残留：{gone}"


def test_archived_readme_records_the_revival_precondition():
    """README 必须写明复活前提（若 collect_from_checkpoint 仍是空壳，重接线只会再造空表）。"""
    txt = open(os.path.join(REPO, "attic", "step_metrics_20260917", "README.md"),
               encoding="utf-8").read()
    assert "collect_from_checkpoint" in txt
    assert "空壳" in txt
    assert "step_funnel" in txt, "README 未指向替代方案"


def test_five_tables_are_dropped_and_node_unregistered():
    """终态断言：5 张表已 DROP；节点已从 registry 解除注册。"""
    import sqlite3
    sys.path.insert(0, os.path.join(REPO, "src"))
    try:
        from wqb.workflow._common import resolve_db_path
        from wqb.workflow.registry import get_registry
    except Exception:  # pragma: no cover
        pytest.skip("依赖不可用")

    db = resolve_db_path()
    if os.path.isfile(db):
        conn = sqlite3.connect(db)
        try:
            left = [r[0] for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name IN "
                "('step_quality_metrics','step_efficiency_metrics','step_gain_metrics',"
                "'wave_summary','campaign_summary')")]
        finally:
            conn.close()
        assert not left, f"以下表仍存在：{left}"

    reg = get_registry()
    names = set(reg.list_nodes()) if hasattr(reg, "list_nodes") else set(reg._nodes)
    assert "step_metrics" not in names, "step_metrics 节点仍在注册表里"
