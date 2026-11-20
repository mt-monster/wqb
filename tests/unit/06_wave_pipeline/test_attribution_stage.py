# -*- coding: utf-8 -*-
"""2026-11-19：收批后**必做归因层**（PnL + 逐年 + 论坛破闸）的回归守护。

背景（用户 2026-11-19 明令）：只读聚合指标的归因会漏掉三类事实——
  ① 整年零持仓（coverage 与「数据满几年」无关）→ 违反「近十年」硬约束；
  ② 失效年定位（全期 S 低 vs 强年集中）；
  ③ 可投资性折损（原始 PnL vs investability-constrained PnL）。
实测案例：`fund_holdings_panel` 在 EUR coverage 0.84–0.92，但 2014 全年 longCount=0
（用零预热对照件验证过 ⇒ 数据集自 2015 起），聚合指标完全看不出来。

本文件守护四件事：
  1. recordsets 的行是**按 schema 顺序的数组**（不是 dict）——必须按 schema 映射列名，
     否则逐年解析恒空（这正是上一版假阴性的根因）；
  2. 任一年零持仓 ⇒ 数据层排除（不可补救，优先级高于 prod 墙）；
  3. PnL 三线对照产出可投资性折损比；
  4. 论坛破闸按墙取词，且用**确定性语料通道**（列表端点 + 本地过滤），
     不用 Playwright 抓取（实测抓取通道恒返回 0 结果，是假信号）。
"""
import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"


def _load(mod_name: str):
    """按文件路径加载 toolkit scripts/_lib 下的模块（scripts/ 不是包）。"""
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location(mod_name, SCRIPTS / "_lib" / f"{mod_name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def attr_mod():
    return _load("attribution")


@pytest.fixture(scope="module")
def corpus_mod():
    return _load("forum_corpus")


# ---------------------------------------------------------------- 1. recordsets 解析

def test_records_payload_maps_schema_ordered_array_rows(attr_mod):
    """实测形态：records 的行是数组，列序由 schema.properties 决定。"""
    payload = {
        "schema": {"name": "yearly-stats", "properties": [
            {"name": "year"}, {"name": "pnl"}, {"name": "longCount"}, {"name": "shortCount"},
        ]},
        "records": [["2014", 0.0, 0, 0], ["2015", 12.5, 300, 400]],
    }
    rows = attr_mod._records_payload(payload)
    assert rows[0]["year"] == "2014"
    assert rows[0]["longCount"] == 0
    assert rows[1]["shortCount"] == 400


def test_records_payload_accepts_dict_rows(attr_mod):
    payload = {"records": [{"year": "2014", "longCount": 0, "shortCount": 0}]}
    rows = attr_mod._records_payload(payload)
    assert rows[0]["longCount"] == 0


def test_records_payload_empty_when_absent(attr_mod):
    assert attr_mod._records_payload({"records": None}) == []
    assert attr_mod._records_payload({}) == []


# ---------------------------------------------------------------- 2. 数据层排除

def _year(y, lc, sc, pnl, sharpe):
    return {"year": y, "long_count": lc, "short_count": sc, "pnl": pnl,
            "sharpe": sharpe, "returns": 0.0, "drawdown": 0.0, "turnover": 0.0}


def test_zero_position_year_triggers_data_layer_exclusion(attr_mod):
    years = [_year("2014", 0, 0, 0.0, 0.0)] + [_year(str(y), 300, 400, 1.0, 1.2) for y in range(2015, 2024)]
    defects = attr_mod.classify_defects(years, {"available": False}, {"sharpe": 1.6})
    assert attr_mod.is_data_layer_exclusion(defects)
    src = [d for d in defects if d["source"] == "数据不满十年"][0]
    assert "2014" in src["evidence"]


def test_full_ten_year_is_not_excluded(attr_mod):
    years = [_year(str(y), 300, 400, 1.0, 1.2) for y in range(2014, 2024)]
    defects = attr_mod.classify_defects(years, {"available": False}, {"sharpe": 1.6})
    assert not attr_mod.is_data_layer_exclusion(defects)


def test_missing_yearly_is_not_treated_as_pass(attr_mod):
    """逐年读数缺失 ⇒ 不得当作「满十年通过」。"""
    defects = attr_mod.classify_defects([], {"available": False}, {"sharpe": 1.6})
    assert not attr_mod.is_data_layer_exclusion(defects)  # 不是数据层排除
    assert any("不得当作通过" in d["evidence"] for d in defects)


# ---------------------------------------------------------------- 3. PnL 三线

def test_pnl_investability_drag_detected(attr_mod):
    years = [_year(str(y), 300, 400, 1.0, 1.2) for y in range(2014, 2024)]
    pnl = {"available": True, "raw_last": 5_387_719.0, "risk_neutralized_last": 3_131_170.0,
           "investability_constrained_last": 3_117_156.0,
           "investability_ratio": 0.578, "rn_ratio": 0.581}
    defects = attr_mod.classify_defects(years, pnl, {"sharpe": 1.48, "returns": 0.058, "drawdown": 0.062})
    srcs = {d["source"] for d in defects}
    assert "可投资性折损" in srcs
    assert "部分风险暴露" in srcs  # rn_ratio 0.58 不是「非风险暴露」


def test_build_attribution_flags_ten_year_ok(attr_mod):
    years = [_year(str(y), 300, 400, 1.0, 1.2) for y in range(2014, 2024)]
    a = attr_mod.build_attribution({"alpha_id": "X", "sharpe": 1.6}, years, {"available": False})
    assert a["ten_year_ok"] is True
    assert a["empty_years"] == []


# ---------------------------------------------------------------- 4. 墙识别 + 论坛

def test_wall_keywords_from_row(attr_mod):
    row = {"sharpe": 1.48, "fitness": 0.99, "two_year_sharpe": 2.10,
           "sub_universe_sharpe": 1.06, "prod_correlation": 0.7977}
    walls = attr_mod.wall_keywords_for_row(row, {"sharpe": 1.58, "fitness": 1.0, "two_year": 1.58})
    assert "S_GATE" in walls
    assert "F_GATE" in walls
    assert "PROD_WALL" in walls


def test_forum_breakthrough_uses_deterministic_corpus(attr_mod):
    class FakeCorpus:
        def __init__(self):
            self.calls = []

        def search(self, keywords, limit=5):
            self.calls.append(list(keywords))
            return [{"id": 1, "title": "t", "votes": 10, "comments": 2, "url": "u", "body": "b"}]

    fc = FakeCorpus()
    out = attr_mod.forum_breakthrough(fc, ["PROD_WALL"], per_wall=2)
    assert out[0]["wall"] == "PROD_WALL"
    assert out[0]["found"] == 1
    assert fc.calls and fc.calls[0]  # 用了墙关键词


def test_score_post_prefers_title(corpus_mod):
    post = {"title": "reduce correlation of an alpha", "body": "nothing"}
    score, matched = corpus_mod.score_post(post, ["correlation"])
    assert score == 3 and "correlation" in matched
    post2 = {"title": "unrelated", "body": "reduce correlation of an alpha"}
    score2, _ = corpus_mod.score_post(post2, ["correlation"])
    assert score2 == 1


def test_strip_html_removes_tags(corpus_mod):
    out = corpus_mod.strip_html("<p>hello <b>world</b></p>")
    assert "hello" in out and "world" in out and "<" not in out


def test_forum_corpus_uses_list_endpoint_not_playwright(corpus_mod):
    """确定性通道必须是 Zendesk 列表端点（代码里不得有 Playwright 依赖）。"""
    src = (SCRIPTS / "_lib" / "forum_corpus.py").read_text(encoding="utf-8")
    assert "/api/v2/community/posts.json" in src
    # 只查 import（文档里可以解释「为什么不用 playwright」）
    import re as _re
    assert not _re.search(r"^\s*(import|from)\s+playwright", src, _re.M)
    assert not _re.search(r"async_playwright", src)
