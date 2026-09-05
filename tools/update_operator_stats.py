# -*- coding: utf-8 -*-
"""工具：统计区域算子使用频率并写入 region_kb（供 assemble_priors 注入 GEM）。

用法：
    python update_operator_stats.py --campaign-dir tracking/EUR
"""
import argparse
import json
import re
import sqlite3
from collections import Counter
from pathlib import Path


def extract_operators(expr: str) -> list:
    """提取表达式中所有算子（函数名）。"""
    return re.findall(r"([a-z_]+)\(", expr)


def update_operator_stats(campaign_dir: str):
    """统计区域算子使用频率并写入 region_kb。"""
    campaign_path = Path(campaign_dir)
    region = campaign_path.name
    
    # 读 region_kb
    db_path = campaign_path.parent.parent / "data" / "wqb.db"
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    
    # 统计最近 10 波的算子使用频率
    rows = conn.execute(
        "SELECT code FROM backtest_results WHERE region=? ORDER BY created_at DESC LIMIT 100",
        (region,)
    ).fetchall()
    
    op_counter = Counter()
    for r in rows:
        ops = extract_operators(r["code"])
        op_counter.update(ops)
    
    # 分类统计
    OP_CATEGORIES = {
        "Logical": {"or", "and", "not", "is_nan", "less", "equal", "greater", "if_else", "not_equal", "less_equal", "greater_equal"},
        "Group": {"group_mean", "group_rank", "group_backfill", "group_scale", "group_count", "group_zscore", "group_std_dev", "group_sum", "group_neutralize", "group_cartesian_product"},
        "Vector": {"vec_min", "vec_count", "vec_sum", "vec_max", "vec_avg", "vec_stddev", "vec_range"},
        "Time Series": {"ts_corr", "ts_zscore", "ts_returns", "ts_product", "ts_std_dev", "ts_backfill", "days_from_last_change", "last_diff_value", "ts_scale", "ts_step", "ts_sum", "ts_av_diff", "ts_kurtosis", "ts_mean", "ts_arg_max", "ts_rank", "ts_ir", "ts_delay", "ts_quantile", "ts_count_nans", "ts_covariance", "ts_decay_linear", "ts_arg_min", "ts_regression", "ts_max_diff", "kth_element", "hump", "ts_delta"},
        "Cross Sectional": {"winsorize", "rank", "zscore", "scale", "normalize", "quantile"},
        "Arithmetic": {"add", "multiply", "sign", "subtract", "pasteurize", "log", "max", "abs", "divide", "min", "signed_power", "inverse", "sqrt", "reverse", "power", "densify"},
    }
    
    category_stats = {}
    for cat, ops in OP_CATEGORIES.items():
        used = {op: op_counter[op] for op in ops if op_counter[op] > 0}
        category_stats[cat] = {
            "used_count": len(used),
            "total_count": len(ops),
            "usage_rate": len(used) / len(ops) if ops else 0,
            "top_ops": sorted(used.items(), key=lambda x: x[1], reverse=True)[:5],
        }
    
    # 过度使用/未使用清单
    overused = [op for op, count in op_counter.most_common(10)]
    all_ops = set()
    for ops in OP_CATEGORIES.values():
        all_ops.update(ops)
    unused = sorted(all_ops - set(op_counter.keys()))
    
    operator_usage_stats = {
        "total_expressions": len(rows),
        "category_stats": category_stats,
        "overused": overused,
        "unused": unused,
        "top_10": op_counter.most_common(10),
    }
    
    # 写入 region_kb
    row = conn.execute(
        "SELECT value FROM ledger_kv WHERE region=? AND key='region_kb'",
        (region,)
    ).fetchone()
    
    if row:
        kb = json.loads(row["value"])
    else:
        kb = {}
    
    kb["operator_usage_stats"] = operator_usage_stats
    
    conn.execute(
        "INSERT OR REPLACE INTO ledger_kv (region, key, value, updated_at) VALUES (?, 'region_kb', ?, datetime('now'))",
        (region, json.dumps(kb, ensure_ascii=False))
    )
    conn.commit()
    conn.close()
    
    print(f"[ok] operator_usage_stats 已写入 {region}/region_kb")
    print(f"  总表达式数: {len(rows)}")
    print(f"  过度使用 top5: {overused[:5]}")
    print(f"  未使用算子数: {len(unused)}")
    for cat, stats in category_stats.items():
        print(f"  {cat}: {stats['used_count']}/{stats['total_count']} ({stats['usage_rate']:.1%})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--campaign-dir", required=True)
    args = ap.parse_args()
    update_operator_stats(args.campaign_dir)
