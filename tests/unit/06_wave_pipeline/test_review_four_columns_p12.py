# -*- coding: utf-8 -*-
"""P1-2 / P1-5（2026-10-24）：评审 findings 固定四列 + 换手区间标注。

复盘 `reports/usa_mining_history_review_20261023.md` §8 指出旧模板三处失真：
  - 只记 best sharpe，漏反向臂（强度上限应看 max|S|）
  - 只列墙名 / FAIL 计数，不记机制方向与证伪条件（下一波无从归因）
  - 不记 prod 读数（「没测」与「测了很低」混为一谈）
本文件守四列落地：
  ① max|S| + 正负向极值 + 2Y
  ② 机制方向与证伪条件（缺登记显式标未登记，不编）
  ③ prod 读数（行内 → 本地 alphas 表；无值标「未测」）
  ④ 闸缺口按 (门槛−实测)/|门槛| 排序（不是 FAIL 行数）+ TO 越界标注
换手 [0.03, 0.70] 只标注不删行；越界行不进 prod/self 队列（P1-5）。
"""
import ast
import importlib
import json
import sqlite3
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
SRC = REPO_ROOT / "src"
TOOLKIT = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
for _p in (SRC, REPO_ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.store import CampaignStore  # noqa: E402

T = {"sharpe_min": 1.58, "fitness_min": 1.0, "two_year_sharpe_min": 1.0,
     "margin_min": 5.0, "turnover_min": 0.01, "turnover_max": 0.70}
REGION = "KOR"


@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / "wqb.db"
    CampaignStore(str(path)).close()
    return path


def _lib_modules():
    return [m for m in sys.modules if m == "_lib" or m.startswith("_lib.")]


@pytest.fixture
def wr(monkeypatch):
    """仓库那份 toolkit `_lib.wave_results`（不取安装位）。用完还原 sys.path 与模块。"""
    for m in _lib_modules():
        monkeypatch.delitem(sys.modules, m)
    monkeypatch.syspath_prepend(str(TOOLKIT))
    mod = importlib.import_module("_lib.wave_results")
    yield mod
    for m in _lib_modules():
        sys.modules.pop(m)


def _findings(db_path, wave="w1"):
    conn = sqlite3.connect(str(db_path))
    try:
        row = conn.execute("SELECT key_findings FROM wave_results WHERE region=? AND wave_number=?",
                           (REGION, wave)).fetchone()
    finally:
        conn.close()
    assert row, "wave_results 未落库"
    return json.loads(row[0])


def _seed_alpha(db_path, alpha_id, prod=None):
    """直接落 alphas 行（外键 ON：先造 region / dataset）。"""
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        conn.execute("INSERT OR IGNORE INTO regions (name) VALUES (?)", (REGION,))
        rid = conn.execute("SELECT id FROM regions WHERE name=?", (REGION,)).fetchone()[0]
        conn.execute("INSERT OR IGNORE INTO datasets (name, region_id) VALUES ('ds_test', ?)", (rid,))
        did = conn.execute("SELECT id FROM datasets WHERE name='ds_test' AND region_id=?",
                           (rid,)).fetchone()[0]
        conn.execute("INSERT INTO alphas (alpha_id, expression, region_id, dataset_id, prod_correlation) "
                     "VALUES (?, 'rank(x)', ?, ?, ?)", (alpha_id, rid, did, prod))
        conn.commit()
    finally:
        conn.close()


# ---------------------------------------------------------------- ① 强度上限

def test_strength_line_uses_max_abs_and_reports_both_directions(wr, db_path):
    rows = [
        {"id": "n5", "sharpe": -1.90, "fitness": 0.6, "two_year_sharpe": 0.4, "turnover_pct": 5.0},
        {"id": "p1", "sharpe": 1.70, "fitness": 1.1, "two_year_sharpe": 1.2, "turnover_pct": 40.0},
        {"id": "p2", "sharpe": 1.61, "fitness": 1.05, "two_year_sharpe": 1.25, "turnover_pct": 35.0},
    ]
    st = wr.WaveResultsStore(REGION, db_path=str(db_path))
    st.auto_upsert_from_review("w1", rows, [], [], thresholds=T)

    line = next(f for f in _findings(db_path) if f.startswith("① 强度上限:"))
    assert "max|S|=1.90" in line and "#n5" in line and "负向" in line   # 反向臂同样是强度上限
    assert "正向最高 1.70" in line and "负向最强 -1.90" in line
    assert "2Y 最高 1.25" in line


# ---------------------------------------------------------------- ② 机制方向与证伪条件

def test_mechanism_line_is_explicitly_unregistered_when_absent(wr, db_path):
    st = wr.WaveResultsStore(REGION, db_path=str(db_path))
    st.auto_upsert_from_review("w1", [{"id": "a1", "sharpe": 1.2}], [], [], thresholds=T)
    line = next(f for f in _findings(db_path) if f.startswith("② 机制方向与证伪条件:"))
    assert "机制=未登记" in line and "证伪=未登记" in line              # 不编机制、不留空
    assert "方向=正向" in line


def test_mechanism_line_reads_settings_then_explicit_args(wr, db_path):
    st = wr.WaveResultsStore(REGION, db_path=str(db_path))
    st.auto_upsert_from_review(
        "w1", [{"id": "a1", "sharpe": -1.1}], [], [], thresholds=T,
        settings={"mechanism": "分析师修正惯性", "falsify_if": "反向臂 3 波 |S|<0.5"})
    line = next(f for f in _findings(db_path) if f.startswith("② 机制方向与证伪条件:"))
    assert "机制=分析师修正惯性" in line and "证伪=反向臂 3 波 |S|<0.5" in line
    assert "方向=负向" in line

    # 显式入参优先于 settings（review_wave --mechanism / --falsifier）
    st.auto_upsert_from_review(
        "w2", [{"id": "a1", "sharpe": -1.1}], [], [], thresholds=T,
        settings={"mechanism": "旧", "falsifier": "旧"}, mechanism="新机制", falsifier="新证伪")
    line = next(f for f in _findings(db_path, "w2") if f.startswith("② 机制方向与证伪条件:"))
    assert "机制=新机制" in line and "证伪=新证伪" in line


# ---------------------------------------------------------------- ③ prod 读数

def test_prod_reads_row_value_then_local_db_then_marks_untested(wr, db_path):
    _seed_alpha(db_path, "a1", prod=0.42)     # DB 有实测
    _seed_alpha(db_path, "a2", prod=None)     # DB 有行但没测
    st = wr.WaveResultsStore(REGION, db_path=str(db_path))
    st.auto_upsert_from_review(
        "w1",
        [{"id": "a1", "sharpe": 1.9}, {"id": "a2", "sharpe": 1.7},
         {"id": "a3", "sharpe": 1.6, "prod_correlation": 0.31}],
        [{"id": "a1", "sharpe": 1.9}],
        [{"id": "a2", "sharpe": 1.7}, {"id": "a3", "sharpe": 1.6, "prod_correlation": 0.31}],
        thresholds=T)

    line = next(f for f in _findings(db_path) if f.startswith("③ prod 读数:"))
    assert "已测 2/3" in line and "max 0.420（#a1）" in line          # 行内 0.31 与 DB 0.42 都算已测
    assert "未测 1 条" in line and "#a2" in line                       # NULL 不算「测了 0」，显式未测
    assert "check_correlation(refresh=True)" in line


def test_prod_line_reports_when_alphas_table_unreadable(wr, tmp_path):
    # 库只有 wave_results 表 → alphas 不可读；结论要说明「未测判定不可靠」，而不是静默全未测
    db = tmp_path / "bare.db"
    conn = sqlite3.connect(str(db))
    conn.execute("CREATE TABLE wave_results (id INTEGER PRIMARY KEY AUTOINCREMENT, "
                 "region VARCHAR(50) NOT NULL, wave_number TEXT NOT NULL, focus TEXT, context TEXT, "
                 "key_findings JSON, candidates JSON, batches JSON, verdict TEXT, status VARCHAR(20), "
                 "source_file VARCHAR(500), archived INTEGER DEFAULT 0, "
                 "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
                 "full_payload JSON, UNIQUE(region, wave_number))")
    conn.commit()
    conn.close()
    st = wr.WaveResultsStore(REGION, db_path=str(db))
    st.auto_upsert_from_review("w1", [{"id": "a1", "sharpe": 1.9}], [{"id": "a1", "sharpe": 1.9}],
                               [], thresholds=T)
    line = next(f for f in _findings(db, "w1") if f.startswith("③ prod 读数:"))
    assert "未测" in line and "alphas 表不可读" in line


# ---------------------------------------------------------------- ④ 闸缺口排序（按差值）

def test_wall_ranking_orders_by_shortfall_not_fail_count(wr):
    rows = [
        {"id": "s1", "sharpe": 1.50, "walls": ["SHARPE"]},   # 差 (1.58-1.50)/1.58 ≈ 5%
        {"id": "s2", "sharpe": 1.52, "walls": ["SHARPE"]},
        {"id": "s3", "sharpe": 1.55, "walls": ["SHARPE"]},
        {"id": "f1", "fitness": 0.40, "walls": ["FITNESS"]},  # 差 60%
    ]
    ranked, worst = wr.wall_gap_ranking(rows, T)
    assert [w for w, _ in ranked][:2] == ["FITNESS", "SHARPE"]   # 行数多 ≠ 更致命
    assert worst["FITNESS"][0] == pytest.approx(0.60)
    assert worst["SHARPE"][0] == pytest.approx((1.58 - 1.50) / 1.58)   # 记最坏那条，不记均值


def test_wall_gap_supports_margin_scale_and_platform_limits(wr):
    assert wr.wall_gap({"margin_bp": 20.0}, "MARGIN", T) == pytest.approx((50000 - 20) / 50000)
    # SUB / ROBUST 用平台给的单条 limit（不同宇宙门槛不同）
    assert wr.wall_gap({"sub_universe_sharpe": 0.24, "sub_universe_limit": 1.0},
                       "LOW_SUB_UNIVERSE_SHARPE", T) == pytest.approx(0.76)
    assert wr.wall_gap({"sharpe": 1.0}, "UNKNOWN_WALL", T) is None


# ---------------------------------------------------------------- P1-5 换手区间

def test_turnover_band_marks_out_of_band_rows_without_dropping_them(wr):
    rows = [
        {"id": "t_low", "turnover_pct": 2.0},
        {"id": "t_lo_edge", "turnover_pct": 3.0},       # 闭区间
        {"id": "t_in", "turnover": 0.40},               # 比例口径自动换算
        {"id": "t_hi_edge", "turnover_pct": 70.0},
        {"id": "t_high", "turnover_pct": 70.1},
        {"id": "t_unknown"},
    ]
    bad = wr.annotate_turnover_band(rows)
    assert [r["id"] for r in bad] == ["t_low", "t_high"]
    assert [r.get("to_band") for r in rows] == ["low", "in", "in", "in", "high", "unknown"]
    assert len(rows) == 6                                # 只标注，不删行


def test_turnover_out_of_band_note_lands_in_wall_line(wr, db_path):
    rows = [
        {"id": "a1", "sharpe": 1.50, "turnover_pct": 2.0, "walls": ["SHARPE"]},
        {"id": "a2", "sharpe": 1.50, "turnover_pct": 85.0, "walls": ["SHARPE"]},
    ]
    st = wr.WaveResultsStore(REGION, db_path=str(db_path))
    st.auto_upsert_from_review("w1", rows, [], [], thresholds=T)
    line = next(f for f in _findings(db_path) if f.startswith("④ 闸缺口排序:"))
    assert "SHARPE 差 5%×2行" in line
    assert "TO 越界 low 1 条/high 1 条" in line
    assert "只标注不删行" in line and "越界行不进 prod/self 队列" in line


# ---------------------------------------------------------------- 旧模板行替换

def test_old_review_lines_are_replaced_but_foreign_lines_kept(wr, db_path):
    st = wr.WaveResultsStore(REGION, db_path=str(db_path))
    st.upsert("w1", verdict="FAIL", key_findings=[
        "RED: 6 全灭", "best sharpe=0.55 (abc)", "best 2y sharpe=0.40",
        "主墙: SHARPE×6", "[pyramid] ANALYST 2/3", "人工：换数据集"])
    st.auto_upsert_from_review("w1", [{"id": "a1", "sharpe": 0.4}], [], [], thresholds=T)

    findings = _findings(db_path)
    assert not any(f.startswith(("best sharpe=", "best 2y sharpe=", "主墙:")) for f in findings)
    assert sum(f.startswith("RED:") for f in findings) == 1              # 旧结论行不重复
    for prefix in ("① 强度上限:", "② 机制方向与证伪条件:", "③ prod 读数:", "④ 闸缺口排序:"):
        assert sum(f.startswith(prefix) for f in findings) == 1          # 四列各一条
    assert findings[-2:] == ["[pyramid] ANALYST 2/3", "人工：换数据集"]


def test_return_payload_carries_findings_for_first_screen_print(wr, db_path):
    """pipeline / review_wave 的首屏打印依赖 out["findings"]（不改 upsert 的返回契约）。"""
    st = wr.WaveResultsStore(REGION, db_path=str(db_path))
    out = st.auto_upsert_from_review("w1", [{"id": "a1", "sharpe": 1.2}], [], [], thresholds=T)

    assert out["key_findings_n"] == len(out["findings"]) == len(_findings(db_path))
    for prefix in ("① 强度上限:", "② 机制方向与证伪条件:", "③ prod 读数:", "④ 闸缺口排序:"):
        assert any(f.startswith(prefix) for f in out["findings"])


def test_skipped_upsert_has_no_findings_key(wr, db_path):
    out = wr.WaveResultsStore(REGION, db_path=str(db_path)).auto_upsert_from_review(
        "", [], [], [], thresholds=T)
    assert out.get("skipped") and "findings" not in out        # 空波号直接跳过，不编四列


# ---------------------------------------------------------------- 调用点接线（静态）

def _calls(tree, attr):
    return [n for n in ast.walk(tree)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == attr]


def test_review_wave_exposes_mechanism_args_and_passes_them_through():
    src = (TOOLKIT / "review_wave.py").read_text(encoding="utf-8")
    tree = ast.parse(src)

    flags = {n.args[0].value for n in _calls(tree, "add_argument")
             if n.args and isinstance(n.args[0], ast.Constant)}
    assert {"--mechanism", "--falsifier"} <= flags

    calls = _calls(tree, "auto_upsert_from_review")
    assert len(calls) == 1
    kw = {k.arg for k in calls[0].keywords}
    assert {"thresholds", "mechanism", "falsifier"} <= kw


def test_pipeline_review_call_sites_pass_thresholds_for_gap_ranking():
    tree = ast.parse((TOOLKIT / "pipeline.py").read_text(encoding="utf-8"))
    calls = _calls(tree, "auto_upsert_from_review")
    assert len(calls) >= 2                                  # 全灭快速通道 + 常规通道
    for c in calls:
        assert "thresholds" in {k.arg for k in c.keywords}
