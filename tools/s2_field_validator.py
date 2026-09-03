# -*- coding: utf-8 -*-
"""s2_field_validator.py - S2 表达式字段强制校验器

校验表达式字段是否属于 S1 特征工程推荐的候选池（main_candidates）。
防止 wave=170 事故：构造时跳过了 S1 推荐，用了错误的字段族。

用法:
    from s2_field_validator import validate_wave_fields
    result = validate_wave_fields(region, wave, dataset, expressions, db_path)
    # result = {"pass": bool, "coverage": float, "missing": [...], "extra": [...]}
"""
from __future__ import annotations

import json
import re
import sqlite3
from typing import Dict, List, Optional, Set


def _extract_fields(expr: str) -> Set[str]:
    """从表达式中提取字段名（与 wave_gate.py 的 _extract_fields 逻辑对齐）。"""
    fields = set()
    # vec_avg/vec_sum 包裹的字段
    for m in re.finditer(r'vec_(?:avg|sum)\(([a-zA-Z_][\w]*)\)', expr):
        fields.add(m.group(1))
    # 裸字段（排除算子）
    _ops = {
        'rank', 'ts_delta', 'ts_mean', 'ts_zscore', 'ts_backfill', 'vec_avg', 'vec_sum',
        'divide', 'subtract', 'add', 'multiply', 'ts_decay_linear', 'group_neutralize',
        'ts_std_dev', 'abs', 'sign', 'log', 'max', 'min', 'if_else', 'ts_rank', 'scale',
        'group_rank', 'ts_sum', 'ts_av_diff', 'ts_delay', 'ts_corr', 'ts_covariance',
        'group_zscore', 'ts_regression', 'last_diff_value', 'kth_element', 'ts_arg_max',
        'ts_arg_min', 'ts_max', 'ts_min', 'ts_product', 'inverse', 'signed_power', 'tail',
        'trade_when', 'is_nan', 'nan_out', 'purify', 'densify', 'winsorize', 'zscore',
        'ts_count_nans', 'ts_median', 'ts_percentile', 'ts_step', 'ts_scale', 'reverse',
        'bucket', 'industry', 'sector', 'subindustry', 'market', 'country',
    }
    for tok in re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]{3,}\b', expr):
        if tok.lower() not in _ops and not tok.isdigit():
            fields.add(tok)
    return fields


def _get_s1_main_candidates(db_path: str, region: str, dataset: str) -> List[str]:
    """从 ledger_kv 读取 S1 特征工程推荐的 main_candidates。"""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # S1 ledger key 格式: s1_<dataset>_d<delay>
    # 先尝试 delay=1（KOR 默认）
    for delay in [1, 0]:
        key = f"s1_{dataset}_d{delay}"
        cur.execute(
            "SELECT value FROM ledger_kv WHERE region=? AND key=?",
            (region, key)
        )
        row = cur.fetchone()
        if row:
            try:
                data = json.loads(row[0])
                candidates = data.get("main_candidates", [])
                if candidates:
                    conn.close()
                    return candidates
            except json.JSONDecodeError:
                pass
    conn.close()
    return []


def validate_wave_fields(
    region: str,
    wave: str,
    dataset: str,
    expressions: List[str],
    db_path: str = "data/wqb.db",
) -> Dict:
    """校验 wave 表达式字段是否覆盖 S1 推荐候选池。

    Returns:
        {
            "pass": bool,           # 是否通过（coverage >= 0.5 且无 forbidden）
            "coverage": float,      # S1 候选池覆盖率
            "matched": [...],       # 匹配到的 S1 候选
            "missing": [...],       # S1 推荐但未使用的候选
            "extra": [...],         # 使用但不在 S1 推荐中的字段
            "forbidden": [...],     # 命中禁用字段（如 revise_value 族）
            "s1_key": str,          # 使用的 S1 ledger key
            "message": str,         # 人类可读摘要
        }
    """
    # 提取所有表达式字段
    all_fields: Set[str] = set()
    for expr in expressions:
        all_fields.update(_extract_fields(expr))

    # 读取 S1 推荐
    s1_candidates = _get_s1_main_candidates(db_path, region, dataset)
    s1_set = set(s1_candidates)

    # 计算覆盖
    matched = sorted(all_fields & s1_set)
    missing = sorted(s1_set - all_fields)
    extra = sorted(all_fields - s1_set)

    coverage = len(matched) / len(s1_set) if s1_set else 0.0

    # 检查禁用字段（从 S1 ledger 的 risk_notes 或显式 forbidden 读取）
    forbidden: List[str] = []
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    for delay in [1, 0]:
        key = f"s1_{dataset}_d{delay}"
        cur.execute(
            "SELECT value FROM ledger_kv WHERE region=? AND key=?",
            (region, key)
        )
        row = cur.fetchone()
        if row:
            try:
                data = json.loads(row[0])
                # 从 risk_notes 解析禁用族（如 "revise_value family dead"）
                risk_notes = data.get("risk_notes", "")
                if "revise_value" in risk_notes.lower():
                    for f in all_fields:
                        if "revise_value" in f.lower():
                            forbidden.append(f)
            except json.JSONDecodeError:
                pass
    conn.close()

    # 判定：覆盖率 >= 50% 且无禁用字段
    pass_ = coverage >= 0.5 and not forbidden

    if not s1_set:
        message = f"S1 特征工程未找到 {dataset} 的 main_candidates，跳过校验"
        pass_ = True  # 无 S1 数据时不阻塞
    elif forbidden:
        message = f"命中禁用字段: {forbidden}"
    elif coverage < 0.5:
        message = f"S1 候选池覆盖率不足: {coverage:.0%} ({len(matched)}/{len(s1_set)})，缺失: {missing[:3]}"
    else:
        message = f"S1 候选池覆盖率: {coverage:.0%} ({len(matched)}/{len(s1_set)})"

    return {
        "pass": pass_,
        "coverage": coverage,
        "matched": matched,
        "missing": missing,
        "extra": extra,
        "forbidden": forbidden,
        "s1_key": f"s1_{dataset}_d1",
        "message": message,
    }


def main():
    """CLI 入口：python tools/s2_field_validator.py --region KOR --wave 170 --dataset analyst10"""
    import argparse
    ap = argparse.ArgumentParser(description="S2 表达式字段强制校验")
    ap.add_argument("--region", required=True)
    ap.add_argument("--wave", required=True)
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--db", default="data/wqb.db")
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    cur = conn.cursor()
    cur.execute(
        "SELECT expression FROM expressions WHERE region=? AND wave=? AND dataset=?",
        (args.region, args.wave, args.dataset)
    )
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print(f"未找到 wave={args.wave} dataset={args.dataset} 的表达式")
        return 1

    expressions = [r[0] for r in rows]
    result = validate_wave_fields(args.region, args.wave, args.dataset, expressions, args.db)

    print(f"[s2-field] {result['message']}")
    if result["extra"]:
        print(f"[s2-field] 额外字段（非 S1 推荐）: {result['extra']}")
    if result["forbidden"]:
        print(f"[s2-field] 禁用字段: {result['forbidden']}")

    return 0 if result["pass"] else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
