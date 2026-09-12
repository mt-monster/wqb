# -*- coding: utf-8 -*-
"""s2_field_validator.py - S2 表达式字段强制校验器

校验表达式字段是否来自 S1 特征工程的字段候选池（ledger `field_whitelist` /
`candidate_field_pool`；兼容历史 `main_candidates`）。防 wave=170 事故：构造时
跳过了 S1 推荐，用了错误的字段族。

2026-09-13 修复（S1↔S2 接力）：
- 读取键从仅 `main_candidates` 改为 `field_whitelist` → `candidate_field_pool` →
  `main_candidates` 三级回退——S1 节点与 S2 回写都不再产 `main_candidates`，
  旧实现导致本闸长期静默“跳过校验”（永远 pass）。
- 判定语义修正为“池内占比”（used 中来自 S1 池的比例）：旧 `coverage` 是池检索率
  （池被用到的比例），会把“表达式完全来自池内”判成覆盖率不足——管道中 S1 池是
  绑定上限而非目标清单，成员关系才是防“用错字段族”的指标。

用法:
    from s2_field_validator import validate_wave_fields
    result = validate_wave_fields(region, wave, dataset, expressions, db_path)
    # result = {"pass": bool, "coverage": float, "missing": [...], "extra": [...]}
"""
from __future__ import annotations

import json
import re
import sqlite3
from typing import Dict, List, Set


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


#: S1 ledger 候选池键的回退顺序（2026-09-13：field_whitelist 为现行口径，
#: candidate_field_pool 为池本体，main_candidates 仅历史记录兼容）。
_POOL_KEYS = ("field_whitelist", "candidate_field_pool", "main_candidates")


def _get_s1_field_pool(db_path: str, region: str, dataset: str):
    """从 ledger_kv 读取 S1 字段候选池。

    Returns:
        (pool, s1_key, s1_record)；未命中时 (空列表, None, {})。
    """
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        cur = conn.cursor()
        # S1 ledger key 格式: s1_<dataset>_d<delay>；先尝试 delay=1（KOR 默认）
        for delay in [1, 0]:
            key = f"s1_{dataset}_d{delay}"
            cur.execute(
                "SELECT value FROM ledger_kv WHERE region=? AND key=?",
                (region, key),
            )
            row = cur.fetchone()
            if not row:
                continue
            try:
                data = json.loads(row[0])
            except json.JSONDecodeError:
                continue
            if not isinstance(data, dict):
                continue
            for pool_key in _POOL_KEYS:
                candidates = [str(x).strip() for x in (data.get(pool_key) or []) if str(x).strip()]
                if candidates:
                    return candidates, key, data
    finally:
        conn.close()
    return [], None, {}


def validate_wave_fields(
    region: str,
    wave: str,
    dataset: str,
    expressions: List[str],
    db_path: str = "data/wqb.db",
) -> Dict:
    """校验 wave 表达式字段是否来自 S1 候选池。

    pass 判据（2026-09-13 起）：
    - 无 S1 池 → 不阻塞（pass=True）；
    - 命中禁用字段（risk_notes 含 revise_value 族）→ FAIL；
    - 池内占比（used 字段中来自 S1 池的比例）< 0.5 → FAIL。
      `coverage` 即该占比（wave_gate 摘要行 "S1字段=x%" 同源）。

    Returns:
        {
            "pass": bool,           # 是否通过
            "coverage": float,      # 池内占比 = |used ∩ pool| / |used|
            "pool_recall": float,   # 池检索率 = |used ∩ pool| / |pool|（信息项）
            "matched": [...],       # 匹配到的 S1 候选
            "missing": [...],       # S1 推荐但未使用的候选
            "extra": [...],         # 使用但不在 S1 池中的字段
            "forbidden": [...],     # 命中禁用字段
            "s1_key": str,          # 实际使用的 S1 ledger key
            "message": str,         # 人类可读摘要
        }
    """
    # 提取所有表达式字段
    all_fields: Set[str] = set()
    for expr in expressions:
        all_fields.update(_extract_fields(expr))

    # 读取 S1 池（field_whitelist → candidate_field_pool → main_candidates 回退）
    s1_pool, s1_key, s1_record = _get_s1_field_pool(db_path, region, dataset)
    s1_set = set(s1_pool)

    # 计算成员关系：池内占比（主判据）+ 池检索率（信息项）
    matched = sorted(all_fields & s1_set)
    missing = sorted(s1_set - all_fields)
    extra = sorted(all_fields - s1_set)

    in_pool_ratio = len(matched) / len(all_fields) if all_fields else 1.0
    pool_recall = len(matched) / len(s1_set) if s1_set else 0.0

    # 禁用字段（沿用历史口径：从 S1 ledger risk_notes 解析 revise_value 族）
    forbidden: List[str] = []
    risk_notes = str((s1_record or {}).get("risk_notes", ""))
    if "revise_value" in risk_notes.lower():
        forbidden = [f for f in all_fields if "revise_value" in f.lower()]

    # 判定：池内占比 >= 50% 且无禁用字段（无 S1 数据时不阻塞）
    pass_ = in_pool_ratio >= 0.5 and not forbidden

    if not s1_set:
        message = (f"S1 未找到 {dataset} 的字段候选池"
                   f"（field_whitelist/candidate_field_pool），跳过校验")
        pass_ = True  # 无 S1 数据时不阻塞
    elif forbidden:
        message = f"命中禁用字段: {forbidden}"
    elif not all_fields:
        message = f"S1 池 {len(s1_set)} 字段；wave 无表达式字段可校验"
    elif in_pool_ratio < 0.5:
        message = (f"S1 字段池内占比不足: {in_pool_ratio:.0%}"
                   f"（{len(matched)}/{len(all_fields)} 在池内），池外: {extra[:3]}")
    else:
        message = (f"S1 字段池内占比: {in_pool_ratio:.0%}"
                   f"（池 {len(s1_set)} 字段，池检索率 {pool_recall:.0%}）")

    return {
        "pass": pass_,
        "coverage": in_pool_ratio,
        "pool_recall": pool_recall,
        "matched": matched,
        "missing": missing,
        "extra": extra,
        "forbidden": forbidden,
        "s1_key": s1_key or f"s1_{dataset}_d1",
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
    conn.execute("PRAGMA foreign_keys=ON")
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
