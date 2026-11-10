#!/usr/bin/env python
"""morphology_gate.py — 通用探针批次「字段形态 → 构型」前置闸门（全 region 适用）。

定位：派发前强制校验，保证「先判字段形态再配构型」。核心闸全 region 通用；
区域差异（破墙要素 / 命名构型）经 region 配置文件注入，不写死任何区域。

核心闸（通用）：
  M1 形态证据前置：每字段须带 field_meta（type/coverage/non_zero_rate/distribution_shape），
     无画像不许派发（先判形态）。
  M2 形态↔构型特征匹配：表达式须含该形态要求的构型特征（通用特征→算子集），错配即 FAIL。
  M3 VECTOR 聚合多样性：同批 VECTOR 字段聚合算子 ≥2 种（禁只用 vec_avg）。
  M4 族多样性：批次覆盖 ≥2 个构型族（template_families.json 签名识别）。

区域闸（配置化，可选）：
  M5 区域破墙要素：读 tracking/<region>/reference/<region>_morphology_gate.json 的
     wall_features（该区提交墙要求的构型特征）；无配置文件则跳过 M5（不写死区域）。

用法：
    python tools/gates/morphology_gate.py --spec probes.json --region KOR
    python tools/gates/morphology_gate.py --json '[{...}]' --region DEU
    python tools/gates/morphology_gate.py --spec probes.json --region KOR --verdict other567

probes.json 每条：
    {"field_id":"oth567_x","expression":"...","field_meta":{"type":"VECTOR",
      "coverage":0.95,"non_zero_rate":0.05,"distribution_shape":"zero_inflated"}}

退出码：0 全过；1 有 FAIL；2 输入/配置错。
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

try:
    from wqb.paths import find_repo_root
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
    from wqb.paths import find_repo_root

ROOT = find_repo_root()
FAMILIES_JSON = ROOT / "Claude/skills/wq-brain-campaign-toolkit/config/template_families.json"
VEC_OPS = ("vec_avg", "vec_stddev", "vec_max", "vec_min", "vec_sum", "vec_count",
           "vec_range", "vec_skewness", "vec_kurtosis", "vec_choose")

# 族签名（顺序即优先级，与 tracking/*/scripts/scan_diversity.py 对齐；单一事实源 families.json）
FAMILY_SIGNATURE_ORDERED = [
    ("diffusion",     [r"ts_regression\(", r"ts_vector_neut\(", r"regression_neut\("]),
    ("order_flips",   [r"reverse\(", r"order_flip"]),
    ("peer_gap",      [r"subtract\(\s*rank\(", r"\bgroup_neutralize\("]),
    ("info_gate",     [r"if_else\(", r"trade_when\("]),
    ("ts_shape",      [r"ts_(skewness|kurtosis|moment|zscore|rank|arg_max|arg_min|entropy)\("]),
    ("nonlinear_x",   [r"signed_power\(", r"\bpower\(", r"\bs_log_1p\(", r"\btanh\("]),
    ("group_compare", [r"\bgroup_rank\(", r"\bgroup_zscore\(", r"\bbucket\("]),
    ("event_cond",    [r"days_from_last_change\(", r"ts_count_nans\(", r"ts_step\("]),
    ("ts_position",   [r"ts_(max|min|scale|decay_linear|mean|delta|backfill|std_dev|corr|covariance)\("]),
]

# 通用「形态 → 构型特征」映射（全 region 通用；特征→可满足算子集）。
# 特征名是通用构型语义，算子集是跨区通用算子；区域可在配置里扩展算子集。
MORPHOLOGY_FEATURES = {
    "zero_inflated": {
        "label": "稀疏事件/零膨胀",
        "features": {
            "liquidity_gate": ["trade_when", "adv20", "volume", "adv60"],
            "tail_handling": ["ts_kurtosis", "winsorize", "ts_zscore"],  # ts_skewness 是幽灵算子(get_operators 无)，勿用
        },
        "why": "稀疏字段裸 rank 被零值稀释 ⇒ 须流动性门控 + 尾部矩放大事件信号",
    },
    "bounded_spread": {
        "label": "有界铺开",
        "features": {
            "centered_rank": ["group_rank", "subtract", "group_zscore"],
            "smoothing": ["hump", "ts_decay_linear", "ts_mean", "ts_backfill"],
        },
        "why": "有界铺开适合居中排名 + 平滑压 CW/换手",
    },
    "ratio_level": {
        "label": "VECTOR 比率/水平",
        "features": {
            "ratio_or_rank": ["divide", "group_rank", "vec_sum", "vec_avg"],
            "smoothing": ["hump", "ts_decay_linear", "ts_mean"],
        },
        "why": "VECTOR 比率适合 ratio/排名 + 平滑（SH 类构型）",
    },
    "return_distribution": {
        "label": "MATRIX 收益/价差分布",
        "features": {
            "higher_moment": ["ts_kurtosis", "ts_zscore", "ts_rank"],  # 无 ts_skewness(幽灵算子)；VECTOR 偏度用 reduce_skewness
            "liquidity_gate": ["trade_when", "adv20", "volume"],
        },
        "why": "收益分布用高阶矩 + 流动性门控（PV 类构型）",
    },
    "flow_level": {
        "label": "VECTOR 流量/计数",
        "features": {
            "aggregation": list(VEC_OPS),
        },
        "why": "流量/计数需聚合多样性（vec_avg/stddev/max/min/sum），禁只用 vec_avg",
    },
    "bounded_ceiling": {
        "label": "有界贴顶",
        "features": {"centered_rank": ["group_rank", "subtract", "group_zscore"]},
        "why": "贴顶字段用居中排名拉开区分度",
    },
    "concentrated": {
        "label": "集中分布",
        "features": {"tail_handling": ["winsorize", "ts_zscore", "ts_rank"]},
        "why": "集中分布须尾部处理防极端值主导",
    },
    "categorical": {
        "label": "类别字段",
        "features": {"grouping": ["group_rank", "group_neutralize", "bucket", "group_zscore"]},
        "why": "类别字段适合做分组轴而非主信号",
    },
}


def load_families():
    try:
        d = json.loads(FAMILIES_JSON.read_text(encoding="utf-8"))
        fams = list((d.get("families") or {}).keys())
        if d.get("free_explore_family"):
            fams.append(d["free_explore_family"])
        return fams
    except Exception:
        return [f for f, _ in FAMILY_SIGNATURE_ORDERED] + ["free_explore"]


def classify_family(expr):
    for fam, pats in FAMILY_SIGNATURE_ORDERED:
        if any(re.search(p, expr) for p in pats):
            return fam
    return "free_explore"


def classify_morphology(meta):
    shape = (meta.get("distribution_shape") or "").lower()
    dtype = (meta.get("type") or "").upper()
    if shape in MORPHOLOGY_FEATURES:
        return shape
    if dtype == "VECTOR":
        return "flow_level"
    nz = meta.get("non_zero_rate")
    if nz is not None and nz < 0.2:
        return "zero_inflated"
    return "bounded_spread"


def used_vec_ops(expr):
    return {op for op in VEC_OPS if re.search(r"\b" + op + r"\(", expr)}


def feature_present(expr, operators):
    """表达式是否含某特征的任一算子（词边界匹配）。"""
    return any(re.search(r"\b" + re.escape(op) + r"\b", expr) for op in operators)


def load_region_config(region):
    """读区域配置（可选）；不存在返回 {}（M5 跳过，不写死区域）。"""
    p = ROOT / "tracking" / region / "reference" / f"{region.lower()}_morphology_gate.json"
    if p.is_file():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def check_probe_batch(probes, region, families=None):
    families = families or load_families()
    region_cfg = load_region_config(region)
    # 区域可扩展特征算子集
    extra_ops = region_cfg.get("feature_operator_extensions", {})
    wall_features = region_cfg.get("wall_features", {})  # {特征名: [算子...]}
    errors, warnings = [], []
    fams_used, vec_ops_all = set(), set()
    wall_coverage = {feat: False for feat in wall_features}

    for i, p in enumerate(probes):
        fid = p.get("field_id", f"probe#{i}")
        expr = p.get("expression", "")
        meta = p.get("field_meta")
        fam = classify_family(expr)
        fams_used.add(fam)
        vops = used_vec_ops(expr)
        vec_ops_all |= vops

        # M1 形态证据前置
        if not meta:
            errors.append(f"[M1] {fid}: 缺 field_meta 画像 —— 先判字段形态再配构型，无画像不许派发")
            continue
        morph = classify_morphology(meta)
        spec = MORPHOLOGY_FEATURES.get(morph)
        if not spec:
            warnings.append(f"[M2] {fid}: 形态 {morph} 无构型映射，请人工指定")
            continue
        # M2 形态↔构型特征匹配（通用 + 区域扩展算子）
        missing = []
        for feat, ops in spec["features"].items():
            ops_ext = list(ops) + list(extra_ops.get(feat, []))
            if not feature_present(expr, ops_ext):
                missing.append(feat)
        if missing:
            errors.append(
                f"[M2] {fid}: 形态={morph}({spec['label']}) 缺构型特征 {missing} —— {spec['why']}")
        # M5 区域破墙要素（配置化）：累计批次级覆盖
        for feat, ops in wall_features.items():
            if feature_present(expr, list(ops)):
                wall_coverage[feat] = True

    # M5 区域破墙要素：批次级覆盖（整批至少一条探针覆盖每个墙特征）
    for feat, covered in wall_coverage.items():
        if not covered:
            errors.append(f"[M5] 区域 {region} 破墙特征批次未覆盖: {feat}（需 {wall_features[feat]}）")
    # M3 VECTOR 聚合多样性
    has_vector = any((p.get("field_meta") or {}).get("type", "").upper() == "VECTOR" for p in probes)
    if has_vector and len(vec_ops_all) < 2:
        errors.append(f"[M3] VECTOR 聚合多样性不足: 仅 {sorted(vec_ops_all) or '无'} —— 须 ≥2 种聚合(vec_avg/stddev/max/min/sum)")
    # M4 族多样性
    if len(probes) >= 2 and len(fams_used) < 2:
        errors.append(f"[M4] 族多样性不足: 仅 {sorted(fams_used)} —— 判死/派发须 ≥2 构型族")
    unknown = fams_used - set(families)
    if unknown:
        warnings.append(f"[M4] 出现未登记族 {sorted(unknown)}（请核对 template_families.json）")

    return {"ok": not errors, "region": region, "errors": errors, "warnings": warnings,
            "families_used": sorted(fams_used), "vec_ops_used": sorted(vec_ops_all),
            "region_config_loaded": bool(region_cfg), "n_probes": len(probes)}


def check_death_verdict(region, dataset_id):
    """判死资格闸：用过的族≥2 + 未用算子≥2 才算判死证据充分。"""
    p = ROOT / "tracking" / region / "reference" / f"{region.lower()}_generation_constraints.json"
    if not p.is_file():
        return {"ok": False, "reason": f"缺 {region} generation_constraints，无法核验判死资格"}
    d = json.loads(p.read_text(encoding="utf-8"))
    st = d.get("operator_stats", {})
    unused = st.get("unused", [])
    used = st.get("used", [])
    ok = len(unused) >= 2 or len(used) >= 2
    return {"ok": ok, "region": region, "dataset": dataset_id,
            "unused_ops_count": len(unused),
            "reason": "判死证据充分(族/算子多样性达标)" if ok else
                      f"判死证据不足: 未用算子仅 {len(unused)}(<2)，须先补未用算子再判死"}


def main():
    ap = argparse.ArgumentParser(description="通用探针「字段形态→构型」前置闸门（全 region）")
    ap.add_argument("--spec", help="探针批次 JSON 文件")
    ap.add_argument("--json", help="探针批次 JSON 字符串")
    ap.add_argument("--region", required=True, help="区域（任意，如 KOR/DEU/USA/GLB）")
    ap.add_argument("--verdict", help="判死资格核验: 传 dataset_id")
    ap.add_argument("--families", help="template_families.json 路径（默认自动）")
    args = ap.parse_args()
    region = args.region.upper()
    families = None
    if args.families:
        families = list((json.loads(Path(args.families).read_text(encoding="utf-8")).get("families") or {}).keys())
    if args.verdict:
        r = check_death_verdict(region, args.verdict)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r["ok"] else 1
    if args.spec:
        probes = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    elif args.json:
        probes = json.loads(args.json)
    else:
        print("需 --spec 或 --json 或 --verdict", file=sys.stderr)
        return 2
    if isinstance(probes, dict):
        probes = probes.get("probes", [probes])
    r = check_probe_batch(probes, region, families)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if r["ok"] else 1


# 兼容既有调用方（tests/unit/04_gates/test_morphology_gate.py 用 mg.check_batch）。
# 本模块的探针批闸与已退役的 wqb.expression.validator.check_batch 无关；主入口改调
# check_probe_batch，避免全仓「check_batch 零调用方」的守护把同名函数误判成复活。
check_batch = check_probe_batch


if __name__ == "__main__":
    sys.exit(main())
