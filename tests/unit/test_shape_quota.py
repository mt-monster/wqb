# -*- coding: utf-8 -*-
"""模板形状配额（`src/wqb/shape_quota.py` + `tools/shape_quota_check.py`）守护。

准则（ra-pipeline 步 4 §4.5.1）：每波候选覆盖 ≥ 3 个形状族，`trade_when` 类条件式占比 ≤ 40%。
分类是启发式，但必须**确定**（同一条表达式恒得同一个族）、**可解释**（每个族有明确命中规则）、**不被括号 / 嵌套骗**。
"""
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "tools"))

from wqb import shape_quota as SQ  # noqa: E402
from wqb.store import CampaignStore  # noqa: E402

import shape_quota_check as tool  # noqa: E402


# ----------------------------------------------------------------------------- 分类
@pytest.mark.parametrize("expr,family", [
    ("trade_when(ts_rank(volume, 20) > 0.8, rank(ts_delta(close, 5)), -1)", "trade_when"),
    ("if_else(greater(ts_delta(x,5),0), ts_delta(x,22), multiply(-1, ts_delta(x,22)))", "if_else"),
    ("rank(ts_arg_max(close, 66))", "arg_extrema"),
    ("group_rank(ts_arg_min(eps, 252), industry)", "arg_extrema"),
    ("rank(days_from_last_change(est_eps))", "freshness"),
    ("rank(ts_corr(rank(close), rank(volume), 22))", "ts_corr"),
    ("subtract(rank(a), rank(b))", "spread"),
    ("subtract(group_rank(a, industry), ts_rank(b, 22))", "spread"),
    ("rank(a) - rank(b)", "spread"),
    ("rank(ts_delta(a,5)) - group_zscore(b, sector)", "spread"),
    ("divide(ts_delta(a, 5), ts_std_dev(a, 22))", "ratio"),
    ("rank(a / b)", "ratio"),
    ("signed_power(ts_zscore(a, 66), 0.5)", "convexity"),
    ("rank(ts_zscore(a, 66))", "ts_zscore"),
    ("winsorize(rank(a), std=4)", "truncation"),
    ("group_zscore(ts_delta(a, 22), industry)", "truncation"),
    ("rank(ts_delta(close, 5))", "plain"),
    ("group_rank(ts_mean(x, 22), sector)", "plain"),
    ("", "plain"),
])
def test_primary_family(expr, family):
    assert SQ.primary_family(expr) == family


def test_the_priority_order_decides_the_primary_family_and_all_hits_are_listed():
    e = "trade_when(x > 0, winsorize(divide(ts_zscore(a, 66), b), std=4), -1)"
    tags = SQ.shape_tags(e)
    assert tags == ["trade_when", "ratio", "ts_zscore", "truncation"] and SQ.primary_family(e) == "trade_when"
    assert SQ.shape_tags("rank(a)") == ["plain"] and SQ.shape_tags(None) == ["plain"]
    assert SQ.FAMILY_PRIORITY[-1] == SQ.PLAIN and len(set(SQ.FAMILY_PRIORITY)) == len(SQ.FAMILY_PRIORITY)


def test_a_spread_needs_two_rank_like_legs_not_just_a_subtract():
    assert SQ.primary_family("subtract(a, ts_mean(a, 20))") == "plain"                       # 去趋势不是价差几何
    assert SQ.primary_family("subtract(rank(a), b)") == "plain"
    assert SQ.primary_family("rank(a) - b") == "plain"
    assert SQ.primary_family("subtract(rank(a), rank(b))") == "spread"


def test_nesting_and_commas_inside_calls_do_not_fool_the_parser():
    e = "subtract(rank(ts_corr(a, b, 22)), group_rank(ts_delta(c, 5), industry))"
    assert SQ.primary_family(e) == "ts_corr"                                                 # ts_corr 优先级高于 spread：架构由共振定义
    assert SQ.primary_family("rank(subtract(rank(a), rank(b)))") == "spread"
    assert SQ.primary_family("rank(trade_when(unbalanced") == "plain"                        # 配不上对的括号：宁可归 plain，不抛异常
    assert SQ.primary_family("trade_when (x, y, z)") == "trade_when"                         # 函数名与括号间有空格


def test_operator_names_are_matched_whole_not_as_substrings():
    assert SQ.primary_family("rank(my_trade_when_flag)") == "plain"
    assert SQ.primary_family("rank(ts_arg_max_custom(a, 5))") == "plain"
    assert SQ.primary_family("rank(signed_power_x(a, 2))") == "plain"


# ----------------------------------------------------------------------------- 配额裁决
#: 每个族一个模板；`{i}` 让同族的每条互不相同（库里 (wave, expression) 唯一，重复串会被合并成一行——真实的波里表达式本来就互不相同）
_TEMPLATES = {
    "tw": "trade_when(ts_rank(volume{i}, 20) > 0.8, rank(ts_delta(close, 5)), -1)",
    "plain": "rank(ts_delta(close{i}, 5))",
    "ife": "if_else(greater(ts_delta(x{i},5),0), ts_delta(x{i},22), multiply(-1, ts_delta(x{i},22)))",
    "ratio": "divide(ts_delta(a{i}, 5), ts_std_dev(a{i}, 22))",
    "corr": "rank(ts_corr(rank(close{i}), rank(volume), 22))",
}
TW, PLAIN_E, IFE, RATIO, CORR = (_TEMPLATES[k].format(i=0) for k in ("tw", "plain", "ife", "ratio", "corr"))


def _wave(**counts):
    """按族造一波表达式：`_wave(tw=3, plain=4)` → 3 条 trade_when + 4 条基础形状。"""
    return [_TEMPLATES[fam].format(i=i) for fam, n in counts.items() for i in range(n)]


def test_a_healthy_wave_passes():
    r = SQ.check_quota(_wave(tw=3, plain=4, ife=2, ratio=1))
    assert r["verdict"] == "pass" and r["n"] == 10 and r["n_families"] == 4 and r["issues"] == []
    assert r["trade_when_share"] == 0.3 and r["families"] == {"trade_when": 3, "if_else": 2, "ratio": 1, "plain": 4}


def test_the_wave84_85_pathology_fails_on_trade_when_share():
    """实测：19 条里 trade_when 占 62%（≈12 条）。"""
    r = SQ.check_quota(_wave(tw=12, plain=4, ife=2, ratio=1))
    assert r["verdict"] == "fail" and r["n"] == 19 and r["trade_when_share"] == round(12 / 19, 4)
    assert any("trade_when 占比 63%" in i for i in r["issues"])


def test_too_few_families_fails():
    r = SQ.check_quota(_wave(tw=1, plain=9))
    assert r["verdict"] == "fail" and r["n_families"] == 2 and any("形状族只有 2 个" in i for i in r["issues"])
    assert SQ.check_quota(_wave(plain=10))["n_families"] == 1                                # plain 只占一个名额


def test_trade_when_share_boundary_is_inclusive():
    assert SQ.check_quota(_wave(tw=4, plain=3, ife=2, ratio=1))["verdict"] == "pass"        # 4/10 = 40% 恰好达标
    assert SQ.check_quota(_wave(tw=5, plain=2, ife=2, ratio=1))["verdict"] == "fail"        # 50%


def test_both_violations_are_reported_together():
    r = SQ.check_quota(_wave(tw=8, plain=2))
    assert r["verdict"] == "fail" and len(r["issues"]) == 2


def test_small_waves_are_not_judged():
    for n in (0, 1, 2):
        r = SQ.check_quota([PLAIN_E] * n)
        assert r["verdict"] == "n/a" and r["issues"] == [] and r["notes"]
    assert SQ.check_quota([PLAIN_E] * 3)["verdict"] == "fail"                                # 3 条起就要判


def test_blank_expressions_are_not_candidates():
    r = SQ.check_quota(["", "  ", None, TW, PLAIN_E, IFE])
    assert r["n"] == 3 and r["verdict"] == "pass"


def test_thresholds_are_overridable_and_reported():
    r = SQ.check_quota(_wave(tw=5, plain=2, ife=2, ratio=1), min_families=2, max_trade_when_share=0.6)
    assert r["verdict"] == "pass" and r["thresholds"] == {"min_families": 2, "max_trade_when_share": 0.6, "min_candidates": 3}


def test_a_dominant_family_is_hinted_without_changing_the_verdict():
    r = SQ.check_quota(_wave(plain=7, ife=2, ratio=1))
    assert r["verdict"] == "pass" and r["dominant_family"] == "plain" and any("plain 一族占 70%" in n for n in r["notes"])
    assert SQ.check_quota(_wave(tw=3, plain=4, ife=2, ratio=1))["notes"] == []


def test_documented_thresholds_match_the_step4_guideline():
    assert (SQ.MIN_FAMILIES, SQ.MAX_TRADE_WHEN_SHARE) == (3, 0.40)                           # 步 4 §4.5.1 准则原文
    text = (REPO / "Claude/skills/wq-brain-ra-pipeline/references/step4-generation.md").read_text(encoding="utf-8")
    assert "≥ 3 个 shape family" in text and "≤ 40%" in text


# ----------------------------------------------------------------------------- 工具（只读、退出码）
@pytest.fixture()
def db(tmp_path):
    path = tmp_path / "wqb.db"
    st = CampaignStore(str(path))
    st.upsert_expressions("KOR", "97", [{"expression": e} for e in (_wave(tw=3, plain=4, ife=2, ratio=1))],
                          dataset="analyst4", status="selected")
    st.upsert_expressions("KOR", "98", [{"expression": e} for e in (_wave(tw=12, plain=4, ife=2, ratio=1))],
                          dataset="analyst4", status="selected")
    st.upsert_expressions("KOR", "99", [{"expression": TW}, {"expression": PLAIN_E}], dataset="pv1", status="selected")
    st.close()
    return str(path)


def _rows_hash(db_path):
    conn = sqlite3.connect(db_path)
    try:
        return conn.execute("SELECT COUNT(*), COALESCE(SUM(id), 0) FROM expressions").fetchone(), \
            conn.execute("SELECT COUNT(*) FROM ledger_kv").fetchone()
    finally:
        conn.close()


def test_the_tool_passes_a_healthy_wave_and_fails_the_pathological_one(db, capsys):
    assert tool.main(["--region", "KOR", "--wave", "97", "--db", db]) == 0
    out = capsys.readouterr().out
    assert "候选 10 条" in out and "[PASS]" in out and "trade_when" in out
    assert tool.main(["--region", "KOR", "--wave", "98", "--db", db]) == 1
    out = capsys.readouterr().out
    assert "[FAIL]" in out and "trade_when 占比 63%" in out and "不要靠补参数变体凑数" in out


def test_a_tiny_wave_is_not_judged_by_the_tool(db, capsys):
    assert tool.main(["--region", "KOR", "--wave", "99", "--db", db]) == 0
    assert "[N/A]" in capsys.readouterr().out


def test_json_output_and_verbose_listing(db, capsys):
    assert tool.main(["--region", "KOR", "--wave", "98", "--db", db, "--json", "--verbose"]) == 1
    obj = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert obj["verdict"] == "fail" and obj["n"] == 19 and obj["region"] == "KOR" and obj["wave"] == "98"
    assert len(obj["items"]) == 19 and obj["items"][0]["families"][0] in SQ.FAMILY_PRIORITY
    assert tool.main(["--region", "KOR", "--wave", "97", "--db", db, "--verbose"]) == 0
    assert "逐条：" in capsys.readouterr().out


def test_thresholds_can_be_overridden_on_the_command_line(db, capsys):
    assert tool.main(["--region", "KOR", "--wave", "98", "--db", db, "--max-trade-when", "0.7"]) == 0


def test_the_dataset_filter_narrows_the_wave(db, capsys):
    assert tool.main(["--region", "KOR", "--wave", "99", "--db", db, "--dataset", "analyst4"]) == 2      # 99 波没有 analyst4 的候选
    assert "没有候选" in capsys.readouterr().err


def test_the_candidate_set_matches_list_expressions_default_filter(db):
    """本工具用只读 SQL 而不是 CampaignStore（后者会建表 / 写库）——但候选口径必须与 list_expressions 缺省一致。"""
    st = CampaignStore(db)
    st.upsert_expressions("KOR", "50", [{"expression": f"rank(f{i})"} for i in range(6)], dataset="d", status="selected")
    conn = sqlite3.connect(db)
    for i, status in enumerate(("superseded", "dropped", "deferred", "gated", "selected", "backtested")):
        conn.execute("UPDATE expressions SET status=? WHERE expression=?", (status, f"rank(f{i})"))
    conn.commit()
    conn.close()
    via_store = {r["expression"] for r in st.list_expressions("KOR", "50")}
    st.close()
    via_tool = {r["expression"] for r in tool.load_candidates(db, "KOR", "50")}
    assert via_tool == via_store == {"rank(f3)", "rank(f4)", "rank(f5)"}


@pytest.mark.parametrize("argv,msg", [
    (["--region", "KOR", "--wave", "12345"], "没有候选"),
    (["--region", "USA", "--wave", "97"], "没有候选"),
])
def test_no_candidates_is_a_cannot_check_error_not_a_pass(db, capsys, argv, msg):
    assert tool.main(argv + ["--db", db]) == 2
    assert msg in capsys.readouterr().err


def test_a_missing_db_is_an_error_and_is_not_created(tmp_path, capsys):
    missing = tmp_path / "nope.db"
    assert tool.main(["--region", "KOR", "--wave", "1", "--db", str(missing)]) == 2
    assert not missing.exists() and "库不存在" in capsys.readouterr().err


def test_a_db_without_the_expressions_table_is_an_error(tmp_path, capsys):
    bare = tmp_path / "bare.db"
    sqlite3.connect(str(bare)).close()
    assert tool.main(["--region", "KOR", "--wave", "1", "--db", str(bare)]) == 2


def test_the_tool_is_read_only(db):
    before = _rows_hash(db)
    tool.main(["--region", "KOR", "--wave", "98", "--db", db, "--verbose"])
    assert _rows_hash(db) == before


def test_the_cli_runs_as_a_script(db):
    """`python tools/shape_quota_check.py …`：文档里的调用形态（含 _pyenv 解释器解析）。"""
    r = subprocess.run([sys.executable, str(REPO / "tools" / "shape_quota_check.py"), "--region", "KOR", "--wave", "98",
                        "--db", db, "--json"], capture_output=True, text=True, timeout=60,
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    assert r.returncode == 1, r.stderr
    assert json.loads(r.stdout.strip().splitlines()[-1])["verdict"] == "fail"
