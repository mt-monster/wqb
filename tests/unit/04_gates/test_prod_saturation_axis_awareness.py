# -*- coding: utf-8 -*-
"""prod-sat 闸：配方级（字段集 × 分组轴 × 归一化算子）判定（2026-10-21）。

起因（EUR fundamental72 实测）：
    sector 轴 CFO/TA×EBITDA>NI  → prod 0.7571 / 0.7553（撞墙）
    industry 轴 **同一字段集**  → prod 0.6747（破墙，硬闸全过）
按「字段」聚合撞墙证据 ⇒ sector 轴的墙把 industry 轴的干净配方一起染成饱和
（自我指涉误报：自家高 Sharpe alpha 把自家字段染饱和），直接拦住后续整族挖掘。

本文件守四条不变量：
  1. 同字段集、**不同分组轴** ⇒ 撞墙证据不串味（industry 不被 sector 拖下水）；
  2. 同字段集 + 同轴、**不同归一化算子** ⇒ 撞墙证据同样不串味
     （group_rank / group_neutralize 变体不被 zscore 的墙连坐）；
  3. 已确认撞墙的配方仍被拦（闸的保护意图不丢）；
  4. 报告里能看出轴分层（否则修完仍无法人工复核）。
"""
import importlib.util
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(REPO, rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class _FakeStore:
    def __init__(self, rows):
        self._rows = rows

    def search_alphas_by_sharpe(self, region, min_sharpe, limit):
        return self._rows

    def close(self):
        pass


SECTOR_EXPR = ("group_zscore(divide(vec_avg(fld_cfo), vec_avg(fld_ta)), sector)")
INDUSTRY_EXPR = ("group_zscore(divide(vec_avg(fld_cfo), vec_avg(fld_ta)), industry)")
INDUSTRY_RANK_EXPR = ("group_rank(divide(vec_avg(fld_cfo), vec_avg(fld_ta)), industry)")
INDUSTRY_NEUTRAL_EXPR = ("group_neutralize(divide(vec_avg(fld_cfo), vec_avg(fld_ta)), industry)")


def _rows():
    return [
        # sector 轴：两次独立测量都撞墙（EUR 实测 0.7571 / 0.7553）
        {"expression": SECTOR_EXPR, "sharpe": 1.75, "dataset_id": 1, "prod_correlation": 0.7571},
        {"expression": SECTOR_EXPR, "sharpe": 1.74, "dataset_id": 1, "prod_correlation": 0.7553},
        # industry 轴：同字段集，已探明破墙（EUR 实测 0.6747）
        {"expression": INDUSTRY_EXPR, "sharpe": 1.64, "dataset_id": 1, "prod_correlation": 0.6747},
    ]


def test_extract_group_axes_reads_axis_argument():
    psg = _load("prod_saturation_gate", "tools/prod_saturation_gate.py")
    assert psg.extract_group_axes(SECTOR_EXPR) == ["sector"]
    assert psg.extract_group_axes(INDUSTRY_EXPR) == ["industry"]
    # 分组轴不是数据字段（不能混进字段集）
    assert psg.extract_fields(SECTOR_EXPR) == ["fld_cfo", "fld_ta"]
    assert psg.extract_fields(
        "group_zscore(divide(vec_avg(fld_cfo), vec_avg(fld_ta)), sta1_allc5)"
    ) == ["fld_cfo", "fld_ta"]
    # 无分组算子 ⇒ 无轴
    assert psg.extract_group_axes("zscore(vec_avg(fld_cfo))") == []


def test_wall_evidence_does_not_cross_axes(monkeypatch):
    psg = _load("prod_saturation_gate", "tools/prod_saturation_gate.py")
    monkeypatch.setattr(psg, "_load_store", lambda db_path=None: _FakeStore(_rows()))
    # industry 配方已探明破墙 ⇒ 不拦
    rep = psg.check_wave([INDUSTRY_EXPR], "EUR", dataset="ds1")
    assert rep["status"] == "enforced"
    assert rep["passed"] is True and rep["violations"] == []
    # sector 配方已确认撞墙 ⇒ 仍拦（保护意图不丢）
    rep2 = psg.check_wave([SECTOR_EXPR], "EUR", dataset="ds1")
    assert rep2["passed"] is False and len(rep2["violations"]) == 1
    axes = sorted(r["axes"][0] for r in rep2["saturated_recipes"])
    assert axes == ["sector"]
    assert rep2["violations"][0]["axes"] == ["sector"]


def test_thin_wall_evidence_is_not_saturation(monkeypatch):
    """IND 教训（2026-09-19）：只有 1 条撞墙证据不得判饱和。"""
    psg = _load("prod_saturation_gate", "tools/prod_saturation_gate.py")
    rows = _rows()
    rows[1]["prod_correlation"] = 0.55
    monkeypatch.setattr(psg, "_load_store", lambda db_path=None: _FakeStore(rows))
    rep = psg.check_wave([SECTOR_EXPR], "EUR", dataset="ds1")
    assert rep["passed"] is True and rep["violations"] == []


def test_extract_group_ops_reads_normalisation_slot():
    psg = _load("prod_saturation_gate", "tools/prod_saturation_gate.py")
    assert psg.extract_group_ops(SECTOR_EXPR) == ["group_zscore"]
    assert psg.extract_group_ops(INDUSTRY_RANK_EXPR) == ["group_rank"]
    assert psg.extract_group_ops(INDUSTRY_NEUTRAL_EXPR) == ["group_neutralize"]
    # 无分组算子 ⇒ 空
    assert psg.extract_group_ops("zscore(vec_avg(fld_cfo))") == []
    # 归一化位进配方键 ⇒ 同字段同轴不同归一化 = 不同配方
    k_z = psg.recipe_key(INDUSTRY_EXPR)
    k_r = psg.recipe_key(INDUSTRY_RANK_EXPR)
    assert k_z[:2] == k_r[:2] and k_z[2] != k_r[2]


def test_wall_evidence_does_not_cross_normalisation(monkeypatch):
    """同轴同载荷换归一化位仍是不同持仓组合 ⇒ zscore 的墙不连坐 rank / neutralize。"""
    psg = _load("prod_saturation_gate", "tools/prod_saturation_gate.py")
    rows = [
        {"expression": SECTOR_EXPR, "sharpe": 1.75, "dataset_id": 1, "prod_correlation": 0.7571},
        {"expression": SECTOR_EXPR, "sharpe": 1.74, "dataset_id": 1, "prod_correlation": 0.7553},
    ]
    monkeypatch.setattr(psg, "_load_store", lambda db_path=None: _FakeStore(rows))
    # zscore 变体：撞墙 ⇒ 拦
    rep_z = psg.check_wave([SECTOR_EXPR], "EUR", dataset="ds1")
    assert rep_z["passed"] is False and len(rep_z["violations"]) == 1
    # 同轴 rank / neutralize 变体：不被连坐
    for expr in (INDUSTRY_RANK_EXPR, INDUSTRY_NEUTRAL_EXPR):
        rep = psg.check_wave([expr], "EUR", dataset="ds1")
        assert rep["passed"] is True, expr
        assert rep["violations"] == [], expr
    # 报告里能看出归一化维度
    assert rep_z["saturated_recipes"][0]["norm_ops"] == ["group_zscore"]
    assert rep_z["violations"][0]["norm_ops"] == ["group_zscore"]
