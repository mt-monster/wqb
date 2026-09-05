# -*- coding: utf-8 -*-
"""test_platform_sync.py - 平台约束同步回归测试（防 known_ops/语义模板再与平台脱节）。

背景（2026-08-19 GBR wave29 实证）：
  发现 1：gate 闸2 用 platform_constraints.json 的 known_ops（54 算子快照）识别"算子 vs 字段"，
          滞后于 operators_verified.json 的 102 verified。16 个新算子（group_scale/ts_corr 等）
          不在 known_ops 被闸2 误报"未验证字段"。
  发现 2：operator_semantics.json 的 6 个算子 template 与平台真实 definition 不符
          （group_mean 少 weight、group_backfill 少 d 等），实例化因子语法错误回测必失败。

本测试用本地权威快照做一致性断言（不依赖实时 MCP，CI 可跑）：
  1. known_ops ⊇ verified 102（防滞后）
  2. 6 个校准算子实例化参数个数匹配平台签名
  3. 语义模板引用的算子都在 known_ops（防模板引用未知算子被闸2 误杀）

运行（toolkit scripts 目录）：
  python -m pytest test_platform_sync.py -q
"""
import json
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import operator_coverage as oc
from _lib.common import load_platform_constraints

_WS = r"d:\coding\traeCN_project\wqb"
_VERIFIED_JSON = os.path.join(_WS, "data", "operators_verified.json")

# 平台真实签名的必需参数个数（get_operators 2026-08-19 快照，不含可选参数）
PLATFORM_MIN_ARITY = {
    "group_mean": 3,            # group_mean(x, weight, group)
    "group_backfill": 3,        # group_backfill(x, group, d, std=4.0)
    "group_cartesian_product": 2,  # group_cartesian_product(g1, g2)
    "ts_returns": 2,            # ts_returns(x, d, mode=1)
    "kth_element": 3,           # kth_element(x, d, k, ignore)
    "last_diff_value": 2,       # last_diff_value(x, d)
}


def _verified_ops():
    if not os.path.isfile(_VERIFIED_JSON):
        pytest.skip("operators_verified.json 不在本机（跨机跳过）")
    d = json.load(open(_VERIFIED_JSON, encoding="utf-8"))
    return set(d.get("verified", []))


def _count_args(expr, op):
    """数 expr 里 op(...) 的顶层参数个数（括号深度数逗号）。"""
    i = expr.find(op + "(")
    if i < 0:
        return -1
    j = i + len(op) + 1
    depth, args = 1, 1
    for ch in expr[j:]:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                break
        elif ch == "," and depth == 1:
            args += 1
    return args


# ---------------- 1. known_ops 覆盖 verified ----------------

def test_known_ops_covers_verified():
    """known_ops 必须覆盖 verified 102 算子（防闸2 把新算子误报为字段）。"""
    ko = set(load_platform_constraints()["known_ops"])
    verified = _verified_ops()
    missing = sorted(verified - ko)
    assert not missing, (
        f"known_ops 滞后 verified，缺 {len(missing)} 个算子（会被闸2 误报为字段）: {missing}。"
        " 用平台 get_operators 刷新 platform_constraints.json 的 known_ops。"
    )


def test_known_ops_has_new_group_ts():
    """本次缺的 16 个 group_*/ts_* 必须在 known_ops（精确回归）。"""
    ko = set(load_platform_constraints()["known_ops"])
    must = [
        "group_backfill", "group_cartesian_product", "group_count", "group_scale",
        "group_std_dev", "ts_corr", "ts_count_nans", "ts_covariance", "ts_kurtosis",
        "ts_max_diff", "ts_quantile", "ts_regression", "ts_returns", "ts_step",
        "ts_target_tvr_decay", "ts_target_tvr_hump",
    ]
    missing = [x for x in must if x not in ko]
    assert not missing, f"known_ops 仍缺: {missing}"


# ---------------- 2. 语义模板签名匹配平台 ----------------

@pytest.mark.parametrize("op,need", sorted(PLATFORM_MIN_ARITY.items()))
def test_semantic_template_arity(op, need):
    """6 个校准算子实例化后参数个数必须 >= 平台必需参数个数。"""
    role_pool = {
        "signal_any": ["field_a", "field_b", "field_c"],
        "price": ["close"],
        "group": ["sector", "industry"],
    }
    expr, used, _ = oc.instantiate_factor(op, role_pool, window=20)
    assert expr is not None, f"{op} 实例化失败: {used}"
    nargs = _count_args(expr, op)
    assert nargs >= need, (
        f"{op} 实例化 {expr} 参数 {nargs} < 平台必需 {need}。"
        " 校准 operator_semantics.json 的 template。"
    )


# ---------------- 3. 语义模板算子都在 known_ops ----------------

def test_semantic_ops_in_known_ops():
    """语义模板库引用的每个算子都必须在 known_ops（防闸2 把模板算子误报为字段）。"""
    ko = set(load_platform_constraints()["known_ops"])
    sem = oc.load_semantics()
    sem_ops = set((sem.get("operators") if isinstance(sem, dict) and "operators" in sem else sem).keys())
    # 只断言语义模板里出现的算子在 known_ops（COMBO/SELECTION-only 也应在，防误报）
    missing = sorted(o for o in sem_ops if o not in ko)
    assert not missing, (
        f"语义模板引用的算子不在 known_ops（会被闸2 误报为字段）: {missing}"
    )


def test_template_placeholders_resolvable():
    """所有语义模板的占位符都是可解析角色（signal_any/price/group/window/scalar 等）。"""
    known_roles = {
        "window", "scalar", "group", "signal_any", "price", "volume", "returns",
        "volatility", "valuation", "fundamental", "sentiment", "analyst", "model_score",
    }
    sem = oc.load_semantics()
    ops = sem.get("operators") if isinstance(sem, dict) and "operators" in sem else sem
    bad = []
    for op, s in ops.items():
        tpl = (s or {}).get("template", "")
        for ph in re.findall(r"\{([a-z_]+)\}", tpl):
            if ph not in known_roles:
                bad.append(f"{op}:{{{ph}}}")
    assert not bad, f"语义模板含未知占位符: {bad}"


# ---------------- 4. 锚点选择优先 MATRIX 强信号 ----------------

class _FakeCtx:
    """最小 ctx：提供 settings / path / ranking_path / region / prefix。"""
    def __init__(self, root, region="tst"):
        self._root = root
        self.region = region
        self.prefix = region
        self.settings = {}
        self.thresholds = {}
    def path(self, *parts):
        return os.path.join(self._root, *parts)
    def ranking_path(self):
        return os.path.join(self._root, "reference", f"{self.region}_dataset_ranking.json")


def _write_catalog(ctx, dataset, types):
    """写 typed catalog：types 是字段 type 列表（'MATRIX'/'VECTOR'）。"""
    ref = ctx.path("reference")
    os.makedirs(ref, exist_ok=True)
    cat = {
        "dataset": dataset,
        "fields": [{"id": f"{dataset}_f{i}", "type": t, "coverage": 0.9}
                   for i, t in enumerate(types)],
    }
    fp = os.path.join(ref, f"{ctx.prefix}_{dataset}_fields.json")
    json.dump(cat, open(fp, "w", encoding="utf-8"), ensure_ascii=False)


def _write_ranking(ctx, rows):
    ref = ctx.path("reference")
    os.makedirs(ref, exist_ok=True)
    json.dump({"ranking": rows}, open(ctx.ranking_path(), "w", encoding="utf-8"),
              ensure_ascii=False)


def test_dataset_field_kind(tmp_path):
    """_dataset_field_kind 正确区分 MATRIX/VECTOR/MIXED/UNKNOWN。"""
    ctx = _FakeCtx(str(tmp_path))
    _write_catalog(ctx, "mat_ds", ["MATRIX", "MATRIX", "MATRIX"])
    _write_catalog(ctx, "vec_ds", ["VECTOR", "VECTOR"])
    _write_catalog(ctx, "mix_ds", ["MATRIX", "VECTOR"])
    assert oc._dataset_field_kind(ctx, "mat_ds") == "MATRIX"
    assert oc._dataset_field_kind(ctx, "vec_ds") == "VECTOR"
    assert oc._dataset_field_kind(ctx, "mix_ds") == "MIXED"
    assert oc._dataset_field_kind(ctx, "no_catalog") == "UNKNOWN"


def test_anchor_prefers_matrix_over_vector(tmp_path):
    """锚点优先 MATRIX：即使 VECTOR 数据集字段池更丰富也不选（GBR news104 教训）。"""
    ctx = _FakeCtx(str(tmp_path))
    # VECTOR 弱信号集（字段多但需 vec_* 包裹）
    _write_catalog(ctx, "news_weak", ["VECTOR"] * 11)
    # MATRIX 强信号集（字段少但直接可用）
    _write_catalog(ctx, "starmine_strong", ["MATRIX"] * 5)
    _write_ranking(ctx, [
        {"id": "news_weak", "tier": "tier1", "valueScore": 4.0},
        {"id": "starmine_strong", "tier": "tier1", "valueScore": 4.0},
    ])
    best, reason = oc.pick_anchor_dataset(ctx)
    assert best == "starmine_strong", f"应选 MATRIX 强信号集，实际选了 {best}（{reason}）"


def test_anchor_prefers_high_value_score(tmp_path):
    """同为 MATRIX 时优先 valueScore 高的（信号强度优先）。"""
    ctx = _FakeCtx(str(tmp_path))
    _write_catalog(ctx, "low_vs", ["MATRIX"] * 8)
    _write_catalog(ctx, "high_vs", ["MATRIX"] * 3)
    _write_ranking(ctx, [
        {"id": "low_vs", "tier": "tier1", "valueScore": 4.0},
        {"id": "high_vs", "tier": "tier1", "valueScore": 7.0},
    ])
    best, reason = oc.pick_anchor_dataset(ctx)
    assert best == "high_vs", f"应选 valueScore 高的，实际选了 {best}（{reason}）"


def test_anchor_falls_back_to_vector_when_no_matrix(tmp_path):
    """候选池无 MATRIX 时退到 VECTOR（不致 None）。"""
    ctx = _FakeCtx(str(tmp_path))
    _write_catalog(ctx, "only_vec", ["VECTOR"] * 6)
    _write_ranking(ctx, [{"id": "only_vec", "tier": "tier1", "valueScore": 5.0}])
    best, reason = oc.pick_anchor_dataset(ctx)
    assert best == "only_vec", f"无 MATRIX 应退 VECTOR，实际 {best}（{reason}）"


# ---------------- 5. 字段角色分类：分组键不进 signal_any ----------------

def test_cluster_fields_classified_as_group():
    """cluster/kmeans 分组键字段必须归 group，不进 signal_any（GBR other455 unit ERROR 教训）。

    背景：other455 的 kmeans_cluster 字段不含常规 group 关键词，被兜底进 signal_any，
    导致 group_sum/ts_corr 等把分组键误当数值信号 x，报 unit ERROR
    "expected Unit[], found Unit[Group:1]"。
    """
    cluster_fields = [
        "oth455_customer_n2v_p10_q200_w1_kmeans_cluster_10",
        "oth455_competitor_n2v_p10_q200_w4_kmeans_cluster_20",
        "oth455_relation_n2v_p10_q200_w1_pca_fact1_cluster_10",
    ]
    for fid in cluster_fields:
        roles = oc.field_roles(fid)
        assert "group" in roles, f"{fid} 应归 group，实际 {roles}"
        # 归 group 后不应只被当 signal_any（signal_any 是数值信号兜底）
        assert roles != ["signal_any"], f"{fid} 不应只归 signal_any，实际 {roles}"


def test_numeric_fields_stay_signal_any():
    """连续数值字段（pca_fact_value / starmine ep_yield）应归 signal_any（数值信号）。"""
    numeric = [
        "oth455_relation_n2v_p10_q200_w1_pca_fact1_value",
        "oth455_relation_n2v_p10_q200_w1_pca_fact2_value",
        "ep_yield_pct_smest_fy1_3",
    ]
    for fid in numeric:
        roles = oc.field_roles(fid)
        assert "group" not in roles, f"{fid} 不应归 group（是数值信号），实际 {roles}"


def test_group_ops_pick_numeric_x_and_group_key():
    """group 类算子实例化：x 选数值信号，group 选分组键（不再把分组键当 x）。"""
    role_pool = {
        "signal_any": ["pca_fact1_value", "pca_fact2_value"],
        "group": ["kmeans_cluster_10", "kmeans_cluster_20"],
    }
    # group_sum(x, group)：x 必须是数值
    expr, _, _ = oc.instantiate_factor("group_sum", role_pool, window=20)
    assert "cluster" not in expr.split("(")[1].split(",")[0], \
        f"group_sum 的 x 不应是分组键: {expr}"
    assert "cluster" in expr, f"group_sum 的 group 参数应是分组键: {expr}"
    # ts_arg_min(x, d)：x 必须是数值
    expr2, _, _ = oc.instantiate_factor("ts_arg_min", role_pool, window=20)
    assert "cluster" not in expr2, f"ts_arg_min 的 x 不应是分组键: {expr2}"
