# -*- coding: utf-8 -*-
"""判死集合单一实现 `src/wqb/dead_datasets.py` 的守护用例。

背景（2026-11-19 审计）：判死台账的旧读取口径是 `key LIKE '%_dead'` + `key[:-5]`，
而 ledger 里的判死记录有**四种键形态**，于是：
- 聚合键 `dead_datasets`（GBR 另有 model264 / news104 / pattern_scores / pv29 / pv30
  只记在这里）与带日期/后缀的记录**一条都读不到**；
- 缩写键 `anl83_dead` 返回的名字与真数据集名（analyst83）对不上；
- 族级记录（判的是字段族，不是整集）与条件死（只禁主信号用法）会被当成整集死 ⇒ 误拦。

本用例把三档语义钉死，并保证**三个消费方同源**（MCP 工具 / pipeline 硬闸 / CLI）。
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]


@pytest.fixture(scope="module")
def dd():
    import sys
    sys.path.insert(0, str(REPO / "src"))
    from wqb import dead_datasets
    return dead_datasets


# --------------------------------------------------------------------------- 分级语义

def test_canonical_key_is_dataset_level(dd):
    rows = [("model16_dead", json.dumps({"dataset": "model16", "dead_at": "2026-09-15"}))]
    lv = dd.dead_levels(rows)
    assert lv["dataset"] == ["model16"]
    assert lv["conditional"] == [] and lv["family"] == []


def test_aggregate_key_list_form(dd):
    """EUR 形态：`dead_datasets` 值是 list[{dataset: ...}]。"""
    rows = [("dead_datasets", json.dumps([
        {"dataset": "insider_agg_matrix", "dead_at": "2026-11-02",
         "rule": "不再作为单塔主信号投入。仅可作 boost_2y 辅助腿"}]))]
    lv = dd.dead_levels(rows)
    assert lv["dataset"] == []
    assert lv["conditional"] == ["insider_agg_matrix"], "「仅可作辅助腿」⇒ 条件死（告警不拦）"


def test_aggregate_key_mapping_form(dd):
    """GBR 形态：`dead_datasets` 值是 dict{<dataset>: {...}}。"""
    rows = [("dead_datasets", json.dumps({
        "model264": {"reason": "probe 24/24 all weak"},
        "news104": {"reason": "probe 12/12 all weak"}}))]
    lv = dd.dead_levels(rows)
    assert set(lv["dataset"]) == {"model264", "news104"}


def test_family_scope_is_not_dataset_level(dd):
    """族级记录（判的是字段族）不得进数据集黑名单，否则误伤同集其他字段族。"""
    rows = [("dead_end_eur_analyst_consensus_actual", json.dumps({
        "dataset": "analyst_consensus",
        "family": "analyst_consensus_actual_fields",
        "scope": "EUR/D1/TOP2500",
        "conclusion": "actual_* 字段族 5 机制全灭"}))]
    lv = dd.dead_levels(rows)
    assert lv["dataset"] == [], "族级记录不得进硬闸"
    assert lv["family"] == ["analyst_consensus"]


def test_dataset_level_wins_when_both_records_exist(dd):
    """同一数据集既有族级又有整集级记录 ⇒ 整集级胜出（合并规则）。"""
    rows = [
        ("dead_end_event_return_model_w18",
         json.dumps({"dataset": "event_return_model", "wave": 18,
                     "reason": "IS 天花板约 0.9，无法达到 1.58 提交线"})),
        ("event_return_model_dead_end",
         json.dumps({"dataset": "event_return_model",
                     "family": "event_return_model earnings_bin",
                     "death_level": "DEAD_CONDITIONAL"})),
    ]
    lv = dd.dead_levels(rows)
    assert "event_return_model" in lv["dataset"], "整集级记录应压过族级/条件级"


def test_rule_beats_reason_for_conditional(dd):
    """判据以 `rule`（执行指令）为准：`rule` 说「不再生成」⇒ 仍是数据集级。

    2026-11-19 实测：GBR `risk88_dead` 的 rule 是「risk88 不再生成；GBR risk 域关闭」，
    reason 里却引了 02 铁律的「只可作辅助腿」⇒ 若按 reason 判会漏拦一个明令关闭的集。
    """
    rows = [("risk88_dead", json.dumps({
        "dataset": "risk88",
        "reason": "规模/市值暴露非超额来源（02 铁律：只可作辅助腿），镜像不追",
        "rule": "risk88 不再生成；GBR risk 域（60/70 跨区死、88 size tilt）关闭",
        "verdict": "DEAD"}))]
    lv = dd.dead_levels(rows)
    assert lv["dataset"] == ["risk88"], "rule 明确「不再生成」⇒ 数据集级（不得降级成条件死）"
    assert lv["conditional"] == []


def test_abbreviated_key_is_corrected_by_payload(dd):
    """`anl83_dead` 的载荷里写的是真名 `analyst83` ⇒ 以载荷为准（旧口径返回 anl83，永远匹配不上）。"""
    rows = [("anl83_dead", json.dumps({"dataset": "analyst83", "verdict": "DEAD"}))]
    lv = dd.dead_levels(rows)
    assert lv["dataset"] == ["analyst83"]
    assert "anl83" not in lv["dataset"]


def test_reopened_record_is_excluded_from_all_levels(dd):
    """撤判回写（status=reopened）⇒ 不出现在任何一档（硬闸放行）。"""
    rows = [("risk60_dead", json.dumps({
        "dataset": "risk60", "status": "reopened",
        "reason": "2026-11-10 撤判重开（DEATH_AUDIT_20261110）"}))]
    lv = dd.dead_levels(rows)
    assert lv["dataset"] == [] and lv["conditional"] == [] and lv["family"] == []


def test_dated_and_suffix_keys_are_recognised(dd):
    """带日期 / `_dead_end` 后缀的记录不再漏拦。"""
    rows = [
        ("gbr_other699_dead_20261029", json.dumps({"dataset": "other699", "verdict": "DEAD"})),
        ("tech_chart_model_dead_end", json.dumps({
            "dataset": "tech_chart_model", "family": "tech_chart_model predicted_return_quantile"})),
    ]
    lv = dd.dead_levels(rows)
    assert "other699" in lv["dataset"]
    assert "tech_chart_model" in lv["family"], "带 family 的镜像记录 ⇒ 族级"


# --------------------------------------------------------------------------- 三端同源

def test_three_consumers_share_one_implementation(dd):
    """MCP 工具 / pipeline 硬闸 / CLI 必须同源（判据只有一份）。

    - `wqb_db_mcp.get_dead_datasets` → 直接 import `wqb.dead_datasets`
    - toolkit `pipeline.dead_dataset_guard` → 经 `_lib/dead_sets.py` 委托
    - `tools/dead_sets.py` → 直接 import `wqb.dead_datasets`
    """
    mcp_src = (REPO / "wqb_db_mcp.py").read_text(encoding="utf-8")
    assert "from wqb.dead_datasets import blocking_datasets" in mcp_src, \
        "MCP 工具未走单一实现（判据漂移的源头）"

    shell_src = (REPO / "Claude" / "skills" / "wq-brain-campaign-toolkit"
                 / "scripts" / "_lib" / "dead_sets.py").read_text(encoding="utf-8")
    assert "from wqb.dead_datasets import dead_levels" in shell_src, \
        "toolkit 薄壳未委托规范实现"

    cli_src = (REPO / "tools" / "ledger" / "dead_sets.py").read_text(encoding="utf-8")
    assert "from wqb.dead_datasets import" in cli_src, "CLI 未走单一实现"

    pipe_src = (REPO / "Claude" / "skills" / "wq-brain-campaign-toolkit"
                / "scripts" / "pipeline.py").read_text(encoding="utf-8")
    assert "from _lib import dead_sets" in pipe_src, "pipeline 硬闸未走薄壳"
    assert not _guard_has_inline_sql(pipe_src), \
        "pipeline 硬闸仍内联旧口径（自己写 SQL 查判死键）"


def _guard_has_inline_sql(pipe_src: str) -> bool:
    """`dead_dataset_guard` 的**函数体**（不含 docstring）里是否还有内联判死 SQL。

    用 AST 取，避免把 docstring 里「旧实现用 `key LIKE '%_dead'`」这句说明误判成残留代码。
    """
    import ast

    tree = ast.parse(pipe_src)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "dead_dataset_guard":
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
                body = body[1:]          # 去掉 docstring
            for sub in ast.walk(ast.Module(body=body, type_ignores=[])):
                if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                    if "LIKE '%_dead'" in sub.value or "LIKE \"%_dead\"" in sub.value:
                        return True
            return False
    raise AssertionError("pipeline.py 里找不到 dead_dataset_guard（函数被改名/删除？）")


def test_degraded_mode_is_explicit_not_silent(dd):
    """仓库外安装（wqb 不可导入）⇒ 降级口径必须**显式**（少拦 + 明说），不得静默。"""
    shell = (REPO / "Claude" / "skills" / "wq-brain-campaign-toolkit"
             / "scripts" / "_lib" / "dead_sets.py").read_text(encoding="utf-8")
    assert "DEGRADED" in shell, "薄壳未暴露降级标志"
    pipe = (REPO / "Claude" / "skills" / "wq-brain-campaign-toolkit"
            / "scripts" / "pipeline.py").read_text(encoding="utf-8")
    assert "dead_sets.DEGRADED" in pipe, "pipeline 未在降级时打印 WARN"
