# -*- coding: utf-8 -*-
"""test_operator_coverage.py - 算子全覆盖 + 语义模板驱动（_lib/operator_coverage.py）契约测试。

覆盖：
  适用性过滤 applicable_ops / 算子分类 operator_kind
  字段角色识别 field_roles / 角色池 dataset_role_pool
  语义实例化 instantiate_factor（含同字段退化修复：跨占位符去重）
  三关过滤 instantiable_operators
  语义驱动 plan_coverage_wave（签发契约 + 实例化因子落盘 + 闸6 可取）

运行（toolkit scripts 目录）：
  python -m pytest test_operator_coverage.py -q
"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import operator_coverage as oc
from _lib.common import CampaignContext
from _lib import rules as rules_mod

# 测试需定位工作区 src/wqb（VERIFIED_SAFE_OPERATORS 所在）
_WS = r"d:\coding\traeCN_project\wqb"
if os.path.isdir(os.path.join(_WS, "src", "wqb")):
    os.environ.setdefault("WQB_WORKSPACE", _WS)


# ---------------- 算子分类与适用性 ----------------

def test_operator_kind():
    assert oc.operator_kind("vec_avg") == "vec"
    assert oc.operator_kind("if_else") == "conditional"
    assert oc.operator_kind("trade_when") == "conditional"
    assert oc.operator_kind("combo_a") == "meta"
    assert oc.operator_kind("ts_rank") == "general"
    assert oc.operator_kind("group_rank") == "general"


def test_applicable_ops_filters_vec_and_meta():
    ops = {"vec_avg", "ts_rank", "if_else", "combo_a", "group_mean"}
    # 无 VECTOR：vec_* 被剔除；conditional/meta 默认剔除
    got = set(oc.applicable_ops(ops, has_vector=False))
    assert "vec_avg" not in got and "if_else" not in got and "combo_a" not in got
    assert "ts_rank" in got and "group_mean" in got
    # 有 VECTOR：vec_* 保留
    got2 = set(oc.applicable_ops(ops, has_vector=True))
    assert "vec_avg" in got2


# ---------------- 字段角色识别 ----------------

def test_field_roles():
    assert "price" in oc.field_roles("close")
    assert "volume" in oc.field_roles("volume")
    assert "valuation" in oc.field_roles("pe_ratio")
    assert "analyst" in oc.field_roles("analyst_target_price")
    assert oc.field_roles("xyzzy_unknown") == ["signal_any"]  # 兜底


# ---------------- 语义实例化（含同字段退化修复） ----------------

def _rich_pool():
    return {
        "price": ["close", "vwap"],
        "volume": ["volume", "turnover"],
        "returns": ["daily_return"],
        "signal_any": ["close", "volume"],
        "group": ["sector"],
    }


def _poor_pool():
    # price/volume 各 1 字段，回退易撞车
    return {
        "price": ["balanced_price_oscillator"],
        "volume": ["liquidity_weighted_returns_ma"],
        "signal_any": ["balanced_price_oscillator", "liquidity_weighted_returns_ma"],
    }


def test_semantics_loaded():
    sem = oc.load_semantics()
    assert len(sem) >= 100  # 102 算子全有语义模板


def test_instantiate_multi_role_distinct_fields():
    """ts_corr({price},{volume}) 两参数必须绑定不同字段（修复同字段退化）。"""
    sem = oc.load_semantics()
    expr, fields, meaning = oc.instantiate_factor("ts_corr", _rich_pool(), semantics=sem)
    assert expr == "ts_corr(close, volume, 20)"
    assert set(fields) == {"close", "volume"}
    assert meaning


def test_instantiate_poor_pool_no_collapse():
    """贫字段池：price/volume 回退也不得撞同一字段。"""
    sem = oc.load_semantics()
    expr, fields, _ = oc.instantiate_factor("ts_corr", _poor_pool(), semantics=sem)
    assert expr == "ts_corr(balanced_price_oscillator, liquidity_weighted_returns_ma, 20)"
    assert len(set(fields)) == 2  # 两字段不同


def test_instantiate_same_role_two_placeholders():
    """add({signal_any},{signal_any}) 同角色双占位符取该角色池两个不同字段。"""
    sem = oc.load_semantics()
    expr, fields, _ = oc.instantiate_factor("add", _rich_pool(), semantics=sem)
    assert expr == "add(close, volume)"
    assert len(set(fields)) == 2


def test_instantiate_group_key_fallback():
    """group_* 缺真实分组字段时退回平台内置 sector。"""
    sem = oc.load_semantics()
    pool = {"signal_any": ["mom_score"]}  # 无 group 角色
    expr, _, _ = oc.instantiate_factor("group_rank", pool, semantics=sem)
    assert expr == "group_rank(mom_score, sector)"


def test_instantiate_unknown_op_returns_none():
    expr, reason, _ = oc.instantiate_factor("no_such_op", _rich_pool(), semantics={})
    assert expr is None and reason == "no_semantics"


# ---------------- 三关过滤 + 语义驱动 plan_coverage_wave ----------------

@pytest.fixture()
def sem_ctx(tmp_path, monkeypatch):
    """最小 EUR 战役目录：settings + typed catalog（ai_equity_alpha 风格富字段）。"""
    monkeypatch.setenv("CAMPAIGN_SKIP_DIR_CHECK", "1")
    monkeypatch.setenv("WQB_WORKSPACE", _WS)
    d = tmp_path / "EUR"
    (d / "config").mkdir(parents=True)
    (d / "reference").mkdir()
    (d / "candidates").mkdir()
    (d / "config" / "settings.json").write_text(
        json.dumps({"region": "EUR", "universe": "TOP2500", "delay": 1}), encoding="utf-8")
    (d / "config" / "thresholds.json").write_text("{}", encoding="utf-8")
    # typed catalog：富字段（price/volume/returns/analyst/group 全有）
    cat = {"dataset": "ds1", "fields": [
        {"id": "close", "type": "MATRIX", "coverage": 1.0, "description": "close price"},
        {"id": "volume", "type": "MATRIX", "coverage": 0.99, "description": "daily volume"},
        {"id": "daily_return", "type": "MATRIX", "coverage": 0.98, "description": "returns"},
        {"id": "pe_ratio", "type": "MATRIX", "coverage": 0.95, "description": "pe valuation"},
        {"id": "mom_score", "type": "MATRIX", "coverage": 0.9, "description": "momentum model score"},
        {"id": "sector", "type": "MATRIX", "coverage": 1.0, "description": "sector group"},
    ]}
    (d / "reference" / "eur_ds1_fields.json").write_text(
        json.dumps(cat), encoding="utf-8")
    ctx = CampaignContext(str(d))
    # 隔离规则库（不碰真实 methodology_rules.json）
    ctx.global_path = str(tmp_path / "_no_global.json")
    return ctx


def test_instantiable_operators_three_gates(sem_ctx):
    inst = oc.instantiable_operators(sem_ctx, dataset="ds1")
    # 无 VECTOR 字段：vec_* 被关1剔除
    assert not any(op.startswith("vec_") for op in inst)
    # conditional/meta 默认不进强制池
    assert "if_else" not in inst and "combo_a" not in inst
    # 关键算子可实例化且带合法因子
    assert "ts_corr" in inst and "group_rank" in inst
    assert inst["ts_corr"]["expr"].startswith("ts_corr(")
    assert inst["group_rank"]["meaning"]


def test_plan_coverage_wave_semantic(sem_ctx):
    """语义驱动：required 全来自可实例化池，契约签发 + 因子落盘 + 闸6 可取。"""
    plan = oc.plan_coverage_wave(sem_ctx, dataset="ds1", semantic=True,
                                cover_per_wave=6, write_candidates=True)
    assert plan["issued"] and plan["semantic"]
    assert len(plan["required_operators"]) == 6
    # required 全是可实例化算子（有经济含义）
    inst = oc.instantiable_operators(sem_ctx, dataset="ds1")
    for op in plan["required_operators"]:
        assert op in inst
    # 候选文件落盘，表达式数 == required 数
    assert os.path.exists(plan["candidates_file"])
    payload = json.loads(open(plan["candidates_file"], encoding="utf-8").read())
    assert len(payload["expressions"]) == 6
    # 闸6 能取到活跃契约，且 required_operators 一致
    act = rules_mod.get_active_contract(sem_ctx, batch_type="explore")
    assert act and set(act["required_operators"]) == set(plan["required_operators"])
    # 契约 action 携带实例化因子模板（build_wave 消费）
    ft = act.get("factor_templates", {})
    assert ft and set(ft.keys()) == set(plan["required_operators"])
    for op in plan["required_operators"]:
        assert ft[op]["expr"] and ft[op]["meaning"]


def test_plan_coverage_wave_dry_run_no_side_effect(sem_ctx):
    """dry_run：不签发契约、不落盘。"""
    plan = oc.plan_coverage_wave(sem_ctx, dataset="ds1", dry_run=True, cover_per_wave=4)
    assert plan["dry_run"] and not plan["issued"]
    assert "factor_templates" in plan and len(plan["factor_templates"]) == 4
    assert not os.path.exists(sem_ctx.path("candidates", "eur_coverage_exprs.json"))
    assert rules_mod.get_active_contract(sem_ctx, batch_type="explore") is None


# ---------------- 通用化：无 catalog 自动懒建（不降级） ----------------

@pytest.fixture()
def bare_ctx(tmp_path, monkeypatch):
    """无 typed catalog 的最小战役目录（懒建触发场景）。"""
    monkeypatch.setenv("CAMPAIGN_SKIP_DIR_CHECK", "1")
    monkeypatch.setenv("WQB_WORKSPACE", _WS)
    d = tmp_path / "IND"
    (d / "config").mkdir(parents=True)
    (d / "reference").mkdir()
    (d / "candidates").mkdir()
    (d / "config" / "settings.json").write_text(
        json.dumps({"region": "IND", "universe": "TOP500", "delay": 1}), encoding="utf-8")
    (d / "config" / "thresholds.json").write_text("{}", encoding="utf-8")
    ctx = CampaignContext(str(d))
    ctx.global_path = str(tmp_path / "_no_global.json")
    return ctx


def test_lazy_build_success_goes_semantic(bare_ctx, monkeypatch):
    """无 catalog + 懒建成功 -> 走语义模式（不降级），锚点=新建的数据集。"""
    # mock ensure_catalog：建一个 ds_new catalog（写文件让 list_typed_datasets 能发现）
    def fake_ensure(ctx, top_n=3):
        cat = {"dataset": "ds_new", "fields": [
            {"id": "close", "type": "MATRIX", "coverage": 1.0, "description": "close price"},
            {"id": "volume", "type": "MATRIX", "coverage": 0.99, "description": "volume"},
            {"id": "sector", "type": "MATRIX", "coverage": 1.0, "description": "sector"},
        ]}
        (open(ctx.catalog_path("ds_new"), "w", encoding="utf-8")).write(json.dumps(cat))
        return {"built": ["ds_new"], "skipped": [], "reason": "懒建 top3"}
    monkeypatch.setattr(oc, "ensure_catalog", fake_ensure)
    plan = oc.plan_coverage_wave(bare_ctx, semantic=True, cover_per_wave=4, dry_run=True)
    assert plan["semantic"] and not plan["degraded"]
    assert plan["anchor_dataset"] == "ds_new"
    assert "懒建" in (plan["anchor_reason"] or "")


def test_lazy_build_failure_degrades(bare_ctx, monkeypatch):
    """无 catalog + 懒建失败（_CatalogBuildError）-> 退降级裸模式兜底。"""
    def fake_ensure(ctx, top_n=3):
        raise oc._CatalogBuildError("API 登录失败：401")
    monkeypatch.setattr(oc, "ensure_catalog", fake_ensure)
    plan = oc.plan_coverage_wave(bare_ctx, semantic=True, cover_per_wave=4, dry_run=True)
    assert plan["degraded"] and not plan["semantic"]
    assert "懒建 catalog 失败" in (plan["anchor_reason"] or "")
    # 降级后 pool 是裸算子池（适用性过滤后），仍能签契约
    assert plan["pool_size"] > 0 and len(plan["required_operators"]) == 4


def test_lazy_build_disabled_skips(bare_ctx, monkeypatch):
    """auto_build_catalog=False：无 catalog 直接退降级，不调 ensure_catalog。"""
    called = {"n": 0}
    def fake_ensure(ctx, top_n=3):
        called["n"] += 1
        return {"built": [], "skipped": [], "reason": "x"}
    monkeypatch.setattr(oc, "ensure_catalog", fake_ensure)
    plan = oc.plan_coverage_wave(bare_ctx, semantic=True, cover_per_wave=4,
                                dry_run=True, auto_build_catalog=False)
    assert called["n"] == 0  # 未触发懒建
    assert plan["degraded"] and not plan["semantic"]
