# -*- coding: utf-8 -*-
"""S6 字段组合规律挖掘：从回测结果中提取字段组合模式。

2026-09-25 落地：解决 S6 复盘只写 wave_results/dead_end、没有提取字段组合规律的问题。
从 backtest_results 中按 sharpe/fitness 排序，找高频高效字段对/字段簇，
写入 ledger `s6_field_patterns_<region>`，供下一波 S2 生成时参考。
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional, Tuple

from ._common import _dumps, _loads, _now


def _extract_fields_from_expression(expr: str) -> List[str]:
    """从表达式中提取字段名（简单实现：匹配已知字段模式）。"""
    # 匹配常见字段名模式：小写字母+数字+下划线
    pattern = r'\b([a-z][a-z0-9_]{2,})\b'
    candidates = re.findall(pattern, expr)
    # 过滤掉算子名
    operators = {
        'rank', 'ts_delta', 'ts_mean', 'ts_zscore', 'ts_std_dev', 'ts_av_diff',
        'ts_corr', 'ts_regression', 'ts_rank', 'ts_quantile', 'ts_backfill',
        'group_rank', 'group_zscore', 'group_mean', 'group_neutralize',
        'vec_avg', 'vec_stddev', 'vec_count', 'vec_sum', 'vec_max', 'vec_min',
        'divide', 'subtract', 'add', 'multiply', 'abs', 'log', 'sqrt', 'sign',
        'max', 'min', 'if_else', 'trade_when', 'bucket', 'hump', 'scale',
        'winsorize', 'reverse', 'inverse', 'power', 'signed_power',
        'days_from_last_change', 'last_diff_value', 'ts_delay', 'ts_arg_max',
        'ts_arg_min', 'ts_max_diff', 'ts_min_diff', 'ts_ir', 'ts_kurtosis',
        'ts_skewness', 'ts_median', 'ts_percentile', 'ts_product', 'ts_sum',
        'ts_std', 'ts_variance', 'ts_zscore', 'vector_neut', 'vector_proj',
    }
    return [c for c in candidates if c not in operators and not c.isdigit()]


def extract_field_patterns(
    backtest_rows: List[Dict[str, Any]],
    min_sharpe: float = 0.5,
    top_n: int = 20,
) -> Dict[str, Any]:
    """从回测结果中提取字段组合规律。

    Args:
        backtest_rows: backtest_results 表行列表，需含 expression/sharpe/fitness
        min_sharpe: 最低 sharpe 阈值（只分析达标或接近达标的）
        top_n: 返回 top-n 高频字段组合

    Returns:
        {
            "total_analyzed": int,
            "field_frequency": {field: count},
            "field_pair_frequency": {(f1, f2): count},
            "high_sharpe_patterns": [...],
            "category_combinations": {...},
            "recommendations": [...],
        }
    """
    # 过滤达标或接近达标的
    qualified = [
        r for r in backtest_rows
        if r.get("sharpe") is not None and float(r.get("sharpe", 0)) >= min_sharpe
    ]
    if not qualified:
        qualified = backtest_rows  # 无达标时分析全部

    field_freq: Counter = Counter()
    pair_freq: Counter = Counter()
    high_sharpe_patterns: List[Dict[str, Any]] = []

    for row in qualified:
        expr = row.get("expression") or row.get("expr") or ""
        sharpe = float(row.get("sharpe", 0))
        fitness = float(row.get("fitness", 0))
        fields = _extract_fields_from_expression(expr)

        # 字段频率
        for f in fields:
            field_freq[f] += 1

        # 字段对频率
        for i, f1 in enumerate(fields):
            for f2 in fields[i + 1:]:
                pair = tuple(sorted([f1, f2]))
                pair_freq[pair] += 1

        # 高 sharpe 模式
        if sharpe >= 1.0:
            high_sharpe_patterns.append({
                "expression": expr,
                "sharpe": sharpe,
                "fitness": fitness,
                "fields": fields,
                "field_count": len(fields),
            })

    # 按 sharpe 排序
    high_sharpe_patterns.sort(key=lambda x: -x["sharpe"])

    # 生成推荐
    recommendations = []
    for fields, count in pair_freq.most_common(top_n):
        f1, f2 = fields
        recommendations.append({
            "type": "field_pair",
            "fields": [f1, f2],
            "frequency": count,
            "suggestion": f"考虑组合 {f1} 与 {f2}（共现 {count} 次）",
        })

    return {
        "total_analyzed": len(qualified),
        "field_frequency": dict(field_freq.most_common(50)),
        "field_pair_frequency": {f"{f1}|{f2}": count for (f1, f2), count in pair_freq.most_common(50)},
        "high_sharpe_patterns": high_sharpe_patterns[:20],
        "recommendations": recommendations,
        "generated_at": _now(),
    }


def build_field_combination_rules(
    patterns: Dict[str, Any],
    min_frequency: int = 3,
    min_sharpe: float = 1.0,
) -> List[Dict[str, Any]]:
    """从字段组合规律中提炼可复用的规则。

    规则形式：
    - "字段A + 字段B → 高sharpe"（共现频率高且平均sharpe高）
    - "字段C 单独使用 → 低sharpe"（频率高但sharpe低，避免）
    """
    rules: List[Dict[str, Any]] = []

    # 分析高 sharpe 模式中的字段组合
    high_patterns = patterns.get("high_sharpe_patterns", [])
    if not high_patterns:
        return rules

    # 统计字段组合的平均 sharpe
    combo_stats: Dict[Tuple[str, ...], List[float]] = defaultdict(list)
    for p in high_patterns:
        fields = tuple(sorted(p.get("fields", [])))
        if len(fields) >= 2:
            combo_stats[fields].append(p.get("sharpe", 0))

    for combo, sharpes in combo_stats.items():
        if len(sharpes) >= min_frequency:
            avg_sharpe = sum(sharpes) / len(sharpes)
            if avg_sharpe >= min_sharpe:
                rules.append({
                    "type": "high_sharpe_combo",
                    "fields": list(combo),
                    "avg_sharpe": round(avg_sharpe, 3),
                    "count": len(sharpes),
                    "rule": f"组合 {', '.join(combo)} 平均 sharpe {avg_sharpe:.2f}（{len(sharpes)} 次）",
                })

    # 按平均 sharpe 降序
    rules.sort(key=lambda x: -x["avg_sharpe"])
    return rules


def persist_field_patterns(
    store: Any,
    region: str,
    wave: str,
    patterns: Dict[str, Any],
    rules: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """把字段组合规律持久化到 ledger。"""
    payload = {
        "region": region,
        "wave": wave,
        "patterns": patterns,
        "rules": rules,
        "generated_at": _now(),
    }
    key = f"s6_field_patterns_{region}_{wave}"
    store.upsert_ledger(region, key, payload)
    return {"key": key, "region": region, "wave": wave, "rules_count": len(rules)}


def load_field_patterns(
    store: Any,
    region: str,
    wave: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """加载字段组合规律（供 S2 生成时参考）。"""
    if wave:
        key = f"s6_field_patterns_{region}_{wave}"
        return store.get_ledger(region, key)
    # 无 wave 时加载最近 N 波
    # 简化实现：返回 None，由调用方遍历
    return None


def merge_field_patterns_across_waves(
    store: Any,
    region: str,
    waves: List[str],
) -> Dict[str, Any]:
    """合并多波字段组合规律，找跨波稳定模式。"""
    all_patterns: List[Dict[str, Any]] = []
    for w in waves:
        p = load_field_patterns(store, region, w)
        if p:
            all_patterns.append(p)

    if not all_patterns:
        return {"error": "no patterns found"}

    # 合并字段频率
    merged_field_freq: Counter = Counter()
    merged_pair_freq: Counter = Counter()
    all_rules: List[Dict[str, Any]] = []

    for p in all_patterns:
        patterns = p.get("patterns", {})
        for f, count in patterns.get("field_frequency", {}).items():
            merged_field_freq[f] += count
        for pair_str, count in patterns.get("field_pair_frequency", {}).items():
            f1, f2 = pair_str.split("|")
            merged_pair_freq[(f1, f2)] += count
        all_rules.extend(p.get("rules", []))

    # 跨波稳定规则（出现 ≥2 波）
    rule_counter: Counter = Counter()
    for r in all_rules:
        rule_counter[tuple(r.get("fields", []))] += 1

    stable_rules = [
        {"fields": list(fields), "wave_count": count, "type": "stable_combo"}
        for fields, count in rule_counter.items()
        if count >= 2
    ]

    return {
        "region": region,
        "waves_merged": len(all_patterns),
        "merged_field_frequency": dict(merged_field_freq.most_common(50)),
        "merged_pair_frequency": {f"{f1}|{f2}": count for (f1, f2), count in merged_pair_freq.most_common(50)},
        "stable_rules": stable_rules,
        "generated_at": _now(),
    }
