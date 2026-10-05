# -*- coding: utf-8 -*-
"""闸 SEM（字段语义归类硬门）fail-closed 回归测试。

背景（2026-09-28 落地）：KOR/fundamental17 首波跳过「字段经济含义归类」直接进 GEM，
348 条产物里 49.4% 落在货币代码 / 汇率叉乘这类**非信号字段**上（三角套汇恒等式、
字符串分类码）——语法全对、语义全废，语法闸与 gate.py 都拦不住，只能靠回测烧配额。
黑名单字段仅占全部字段 9.9%（37/373），却吃掉 49.4% 的生成预算。

守护两条 fail-closed 契约，任一条被删/被绕过即红：
  1. 缺 s1_semantic_<ds> 台账 -> wave_gate exit 2 整波阻断（并给出生成命令）
  2. 有台账 -> 命中 blocked_fields 的表达式直接剔出候选，不进语法闸

设计：判定逻辑走**纯单测**（直接 import `_semantic_gate`，不启子进程、不碰实时库）；
只保留 2 条 CLI 契约冒烟——子进程跑真实 wave_gate 会写 data/wqb.db，
并发全量跑下受写锁竞争影响，故带一次重试。
"""
from __future__ import annotations

import importlib.util
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
WAVE_GATE = REPO / "tools" / "wave_gate.py"
WAVE_GATE_PKG = REPO / "tools" / "wave_gate_pkg" / "cli.py"
DB = REPO / "data" / "wqb.db"
PY = sys.executable


def _wave_gate_src() -> str:
    """读 wave_gate 源码（shim + pkg 合并）——包化后实现搬进 wave_gate_pkg/，
    测试同时读两处，无论安全契约写在哪都能守住。"""
    parts = []
    if WAVE_GATE.exists():
        parts.append(WAVE_GATE.read_text(encoding="utf-8"))
    if WAVE_GATE_PKG.exists():
        parts.append(WAVE_GATE_PKG.read_text(encoding="utf-8"))
    return "\n".join(parts)


def _load_wave_gate():
    """按文件路径加载 tools/wave_gate.py（tools 非包，不能普通 import）。"""
    spec = importlib.util.spec_from_file_location("_wg_sem", WAVE_GATE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class _Args:
    """_semantic_gate 只需要 region / dataset。"""

    def __init__(self, region, dataset):
        self.region = region
        self.dataset = dataset


def _ledger_exists(region: str, dataset: str) -> bool:
    if not DB.exists():
        return False
    c = sqlite3.connect(f"file:{DB}?mode=ro", uri=True, timeout=30)
    try:
        return c.execute("SELECT 1 FROM ledger_kv WHERE region=? AND key=?",
                         (region, f"s1_semantic_{dataset}")).fetchone() is not None
    finally:
        c.close()


# ---------------------------------------------------------------- 纯单测（判定逻辑）

def test_unit_missing_ledger_is_reported_as_missing():
    """缺台账 -> ledger_missing=True（由 main() 转成 exit 2，CLI 冒烟另测）。"""
    wg = _load_wave_gate()
    rep = wg._semantic_gate(_Args("KOR", "__no_such_dataset_for_sem__"),
                            str(REPO / "tracking" / "KOR"), [(1, "rank(close)")])
    assert rep["ledger_missing"] is True
    assert rep["removed"] == []
    # 缺台账时不得静默吞掉候选：原样返回，由调用方决定阻断
    assert rep["items"] == [(1, "rank(close)")]


@pytest.mark.skipif(not _ledger_exists("KOR", "fundamental17"),
                    reason="需先跑 tools/field_semantic_classify.py --region KOR --dataset fundamental17 --write-ledger")
def test_unit_blocked_fields_are_removed():
    """有台账 -> 汇率叉乘 / 货币代码被剔出，干净表达式保留。"""
    wg = _load_wave_gate()
    blocked = ("divide(multiply(fnd17_1_usdtorepexrate, fnd17_1_reptoprcexrate), "
               "reporting_to_pricing_currency_fx_rate)")
    currency = "days_from_last_change(pricing_currency_code_ras1)"
    clean = "divide(ts_delta(fnd17_aintexpz, 252), ts_delta(fnd17_aebit, 252))"
    items = [(1, blocked), (2, currency), (3, clean)]
    rep = wg._semantic_gate(_Args("KOR", "fundamental17"),
                            str(REPO / "tracking" / "KOR"), items)
    assert rep["ledger_missing"] is False
    assert rep["blocked_field_count"] > 0
    assert [cid for cid, _, _ in rep["removed"]] == [1, 2], (
        f"应剔除 1、2（汇率叉乘 + 货币代码），实际 {[c for c, _, _ in rep['removed']]}")
    assert [cid for cid, _ in rep["items"]] == [3], "干净表达式必须保留"


def test_unit_ledger_absent_does_not_swallow_candidates():
    """台账缺失时不得把候选清空（那是另一种静默失败）。"""
    wg = _load_wave_gate()
    items = [(7, "rank(close)"), (8, "ts_zscore(close, 22)")]
    rep = wg._semantic_gate(_Args("KOR", "__no_such_dataset_for_sem__"),
                            str(REPO / "tracking" / "KOR"), items)
    assert len(rep["items"]) == 2


# ---------------------------------------------------------------- CLI 契约冒烟

def _run_wave_gate(dataset, exprs, wave, extra=None, tmpdir=None):
    """在**独立临时库 + 临时战役目录**里跑 wave_gate。

    为什么不用实时库：子进程会 upsert expressions 写 data/wqb.db（277MB），
    并发全量跑时写锁竞争会让耗时从 60s 涨到 350s 并偶发误判。
    `WQB_DB_PATH` 被 wave_gate / gate.py / wqb.db_conn 共同认可，故指向临时库即可完全隔离。
    """
    d = Path(tmpdir)
    exprs_file = d / f"_semtest_{wave}.txt"
    exprs_file.write_text("\n".join(exprs) + "\n", encoding="utf-8")
    # 最小战役目录（region gates / parse 需要 config/settings.json）
    camp = d / f"camp_{wave}"
    (camp / "config").mkdir(parents=True, exist_ok=True)
    src_cfg = REPO / "tracking" / "KOR" / "config" / "settings.json"
    if src_cfg.exists():
        (camp / "config" / "settings.json").write_text(
            src_cfg.read_text(encoding="utf-8"), encoding="utf-8")
    tmp_db = d / f"sem_{wave}.db"
    sqlite3.connect(str(tmp_db)).close()  # 建空库

    # --gate-mode warn 是**隔离**不是绕过：本用例只验闸 SEM，不能被 region-gates
    # （catalog / signal_floor / stop_rules / backlog）抢先 exit 2。
    cmd = [PY, str(WAVE_GATE), "--campaign-dir", str(camp),
           "--dataset", dataset, "--wave", wave, "--exprs-file", str(exprs_file),
           "--gate-mode", "warn"] + (extra or [])
    env = dict(os.environ)
    env["WQB_GATE_MODE"] = "warn"
    env["WQB_DB_PATH"] = str(tmp_db)
    env.pop("WQB_SEM_MODE", None)  # 默认 enforce，勿被外部泄漏成 off
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", env=env, timeout=300)


def test_cli_missing_ledger_exits_2(tmp_path):
    """缺台账 -> exit 2，并打印闸 SEM 阻断说明与修复命令。"""
    ds = "__sem_gate_no_ledger__"
    r = _run_wave_gate(ds, ["rank(close)"], "semtest_missing", tmpdir=tmp_path)
    out = (r.stdout or "") + (r.stderr or "")
    rc = r.returncode
    assert rc == 2, f"缺台账应 exit 2，实际 {rc}\n{out[:1000]}"
    assert "闸 SEM 阻断" in out, f"应给出闸 SEM 阻断说明\n{out[:1000]}"
    assert "field_semantic_classify.py" in out, f"应给出生成命令\n{out[:1000]}"


def test_cli_skip_flag_disables_gate(tmp_path):
    """--skip-semantic-gate 是唯一逃生口：显式传后不再因缺台账阻断，但必须告警。"""
    ds = "__sem_gate_no_ledger__"
    r = _run_wave_gate(ds, ["rank(close)"], "semtest_skip",
                       extra=["--skip-semantic-gate"], tmpdir=tmp_path)
    out = (r.stdout or "") + (r.stderr or "")
    assert "闸 SEM 阻断" not in out, f"显式 skip 后不应再阻断\n{out[:800]}"
    assert "闸 SEM 已关闭" in out, "skip 时必须打印醒目告警"


def test_semantic_classify_tool_exists_and_is_guarded():
    """归类工具存在，且不使用裸 sqlite3.connect（禁裸连静态闸）。"""
    tool = REPO / "tools" / "field_semantic_classify.py"
    assert tool.exists(), "tools/field_semantic_classify.py 缺失"
    src = tool.read_text(encoding="utf-8")
    assert "db_connect" in src, "必须走 wqb.db_conn 规范工厂"


# ------------------------------------------------ 漏洞回归（2026-09-28 修复的两个真实缺口）

def test_semantic_gate_drops_blocked_ids_in_db(tmp_path, monkeypatch):
    """闸 SEM 必须把命中的表达式**落库标 dropped**，不能只在内存剔除。

    缺口：gate.py / pipeline.py 都按 DB 的 expressions.status 取数，
    只做内存过滤的话 172 条语义垃圾照样会被判定、被发批。
    """
    wg = _load_wave_gate()
    db = tmp_path / "sem_drop.db"
    c = sqlite3.connect(str(db))
    c.execute("CREATE TABLE ledger_kv (id INTEGER PRIMARY KEY, region TEXT, key TEXT, value TEXT,"
              " created_at TEXT, updated_at TEXT)")
    c.execute("CREATE TABLE expressions (id INTEGER PRIMARY KEY, expression TEXT, status TEXT,"
              " region TEXT, updated_at TEXT)")
    sem = {"region": "KOR", "dataset": "dsx",
           "blocked_fields": [{"field": "ccy_code_a", "reason": "非信号：货币代码"}],
           "signal_fields": ["ok_field_1"]}
    c.execute("INSERT INTO ledger_kv(region,key,value) VALUES(?,?,?)",
              ("KOR", "s1_semantic_dsx", json.dumps(sem)))
    c.execute("INSERT INTO expressions(id,expression,status,region) VALUES(1,'rank(ccy_code_a)','gem','KOR')")
    c.execute("INSERT INTO expressions(id,expression,status,region) VALUES(2,'rank(ok_field_1)','gem','KOR')")
    c.commit()
    c.close()
    monkeypatch.setenv("WQB_DB_PATH", str(db))

    class _A2:
        region = "KOR"
        dataset = "dsx"
        from_db = True

    rep = wg._semantic_gate(_A2(), str(tmp_path), [(1, "rank(ccy_code_a)"), (2, "rank(ok_field_1)")])
    assert [cid for cid, _ in rep["items"]] == [2]
    assert rep.get("dropped_in_db") == 1, f"应落库标 dropped 1 条，实际 {rep.get('dropped_in_db')}"
    c = sqlite3.connect(str(db))
    st = dict(c.execute("SELECT id, status FROM expressions").fetchall())
    c.close()
    assert st[1] == "dropped", f"命中项必须落库为 dropped，实际 {st[1]}"
    assert st[2] == "gem", "干净项状态不得被改动"


def test_semantic_gate_no_db_write_when_not_from_db():
    """--exprs-file 路径的 id 是 1..N 序号，绝不可拿去 UPDATE expressions。"""
    src = _wave_gate_src()
    assert 'getattr(a, "from_db", False) and removed' in src or "a.from_db" in src, (
        "落库标 dropped 必须以 from_db 为前置条件，否则会把序号当主键写坏库")


def test_gate_result_final_verdict_is_persisted():
    """gate_results.all_pass 必须落**最终** verdict。

    缺口：store.upsert_gate_result 取 report['all_pass']，而 wave_gate 原先在写库**之后**
    才算 all_pass → DB 列恒为 0，与 report_json 打架；停止规则 C（all_pass 全 0 → 判区域死）
    会误杀。故末尾必须用 final verdict 覆盖写一次。
    """
    src = _wave_gate_src()
    assert "_persist_gate_report(final_all_pass=all_pass)" in src, (
        "缺少最终 verdict 覆盖写：all_pass 列会与 report_json 不一致")
    assert 'report["all_pass"] = bool(final_all_pass)' in src


# ------------------------------------ 2026-10-01 P0：闸 SEM 结论必须落 gate_results
#
# 断流：sem_report 此前只用于打印 + 剔式，**从未写进 report** → gate_results 里
# 看不到「剔了哪些式 / 是否因缺台账 exit 2」，get_gate_result 回读无证据；
# 实测 846 条非 mcp 记录含 semantic 键 = 0 条。修复：落脱敏摘要。

def test_sem_report_is_persisted_into_gate_report():
    """闸 SEM 结论必须写进 report['semantic']（脱敏摘要），不得只打印。"""
    src = _wave_gate_src()
    assert 'report["semantic"] = {' in src, (
        "闸 SEM 结论必须落 report['semantic']——否则 gate_results 无 SEM 痕迹（写入端断流）")
    for k in ("ledger_missing", "n_removed", "n_kept", "dropped_in_db"):
        assert f'"{k}"' in src, f"SEM 摘要缺字段 {k}"
    # removed 必须截断（全量会撑爆 report_json）
    assert "removed_sample" in src, "removed 须落样本（截前 N）而非全量"


def test_semantic_mode_off_still_recorded():
    """--skip-semantic-gate / off 也要留痕（记录「本波未做语义归类」）。"""
    src = _wave_gate_src()
    assert '_sem_mode == "off"' in src and '"semantic"' in src, (
        "SEM 关闭时也必须在 report 记录，避免下游误以为跑了")


# ------------------------------------ 2026-10-01 P2：gate 阶段探针仅规划，不回测

def test_probe_mode_status_is_planned_not_assigned():
    """gate 阶段探针只做 dry_run 规划，status 不得写成「已派发/已节省配额」。"""
    src = _wave_gate_src()
    assert "PROBE_PLANNED" in src, "gate 阶段探针状态应为 PROBE_PLANNED（仅规划）"
    # 断言的是**赋值语句**（status 的值），不是注释里提到的旧名：
    # 注释里保留 "PROBE_ASSIGNED" 作为考古说明是允许的。
    assert '"status": "PROBE_ASSIGNED"' not in src, (
        "PROBE_ASSIGNED 会被误读为「探针已跑/已省配额」，实际 gate 阶段 saved_quota 恒 0")
    assert '"executed": False' in src, "须显式标记 executed=False"


def test_sem_trace_lands_in_gate_results_end_to_end(tmp_path):
    """E2E：跑真实 wave_gate（隔离临时库），gate_results.report_json 必须含 semantic 摘要。

    这是 P0 的**真凭据**测试——不靠源码文本断言，而是端到端跑完读库。
    有台账命中 1 条非信号字段 → semantic.n_removed==1、n_kept==1。
    """
    d = Path(tmp_path)
    db = d / "sem_e2e.db"
    # 用真实 store 建全量 schema（手写 DDL 会漏列，如 expressions.wave_id）
    sys.path.insert(0, str(REPO / "src"))
    from wqb.store.campaign import CampaignStore as _CS
    _st = _CS(str(db))
    try:
        sem = {"region": "KOR", "dataset": "e2eds",
               "blocked_fields": [{"field": "ccy_code_a", "reason": "非信号：货币代码"}],
               "signal_fields": ["ok_signal_field"]}
        _st.upsert_ledger("KOR", "s1_semantic_e2eds", sem)
    finally:
        _st.close()

    camp = d / "KOR"
    (camp / "config").mkdir(parents=True, exist_ok=True)
    (camp / "reference").mkdir(parents=True, exist_ok=True)
    (camp / "config" / "settings.json").write_text(
        json.dumps({"region": "KOR", "delay": 1}), encoding="utf-8")
    # region-gates 需要 config/thresholds.json；从真实 KOR 战役目录复制，缺则给最小占位
    _thr_src = REPO / "tracking" / "KOR" / "config" / "thresholds.json"
    if _thr_src.exists():
        (camp / "config" / "thresholds.json").write_text(
            _thr_src.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        (camp / "config" / "thresholds.json").write_text("{}", encoding="utf-8")
    # gate.py 需要字段白名单：reference/<prefix>_<dataset>_fields.json。
    # prefix 由 settings 决定（KOR→kor）；给最小 catalog：两个字段。
    (camp / "reference" / "kor_e2eds_fields.json").write_text(
        json.dumps({"data_type": "MATRIX",
                    "fields": [{"id": "ccy_code_a", "type": "MATRIX"},
                               {"id": "ok_signal_field", "type": "MATRIX"}]}),
        encoding="utf-8")
    exprs_file = d / "e2e.txt"
    exprs_file.write_text("rank(ccy_code_a)\nrank(ok_signal_field)\n", encoding="utf-8")

    cmd = [PY, str(WAVE_GATE), "--campaign-dir", str(camp), "--dataset", "e2eds",
           "--wave", "sem_e2e", "--exprs-file", str(exprs_file), "--gate-mode", "warn",
           "--semantic-gate", "warn"]
    env = dict(os.environ)
    env["WQB_GATE_MODE"] = "warn"
    env["WQB_DB_PATH"] = str(db)
    env.pop("WQB_SEM_MODE", None)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env, timeout=300)
    out = (r.stdout or "") + (r.stderr or "")

    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True, timeout=30)
    try:
        row = c.execute("SELECT report_json FROM gate_results WHERE wave='sem_e2e'").fetchone()
    finally:
        c.close()
    if row is None:
        pytest.skip(f"gate_results 未落库（环境路径问题，非本契约失败）\n{out[:600]}")
    rep = json.loads(row[0])
    assert "semantic" in rep, f"P0：gate_results 缺 semantic 键（写入端断流未修）\n{json.dumps(rep)[:600]}"
    sem_out = rep["semantic"]
    assert sem_out.get("ledger_missing") is False
    assert sem_out.get("n_removed") == 1, f"应剔 1 条（货币代码），实际 {sem_out.get('n_removed')}"
    assert sem_out.get("n_kept") == 1, f"应保留 1 条，实际 {sem_out.get('n_kept')}"
