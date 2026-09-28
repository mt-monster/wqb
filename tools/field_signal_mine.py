#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""L0 零回测选基：从 backtest_results 的表达式文本挖【字段级】与【字段对】历史信号先验。

背景（2026-09-26 选基方法论）：
  传统选基在"机制表达式层"读数（GEM 406 条只换 8 次回测），字段→信号映射是间接推断。
  本工具做 L0 层——零回测、纯本地 SQL——从自家 3 万条回测史反挖每个字段的历史 max|sharpe|，
  并额外挖【字段对】（高 |S| 表达式里的字段共现对）：实证表明最强信号常在成对机制
  （如 HKG model238 screening×owner 背离对 S1.39，两条单字段探针都平庸），单字段榜会漏。

用法：
  python tools/field_signal_mine.py --region HKG --dataset model238 --top 15
  python tools/field_signal_mine.py --all --pairs --min-abs-sharpe 1.0
  python tools/field_signal_mine.py --region HKG --field mdl238_global_screening_rank

输出列：
  field / n（回测次数）/ max_abs_S（历史最大 |sharpe|）/ n_hit（|S|>=0.5 次数）/
  best_fitness / hit_rate（n_hit/n）
  --pairs 模式输出：field_a × field_b / n / max_abs_S / n_hit。

⚠ 边界：本工具产物只做**字段分诊先验**（决定 GEM/探针看哪些字段）。
  "每字段套 rank" 禁令（硬约束 7）针对提交候选池；普查探针是测量仪器，
  探针表达式本身永不进提交池、永不进 near_pool。
"""
from __future__ import annotations

import argparse
import re
import sqlite3
from collections import defaultdict

# 规范工厂（2026-09-26 修复裸 connect）：本工具只读，readonly=True 不改库字节。
# 白名单外禁止裸 sqlite3.connect（守卫 test_db_write_guards::TestNoNakedSqliteConnect）。
from wqb.db_conn import connect as _db_connect
from pathlib import Path

import sys as _sys
_SRC = Path(__file__).resolve().parent.parent / "src"
if str(_SRC) not in _sys.path:
    _sys.path.insert(0, str(_SRC))

DB_DEFAULT = Path(__file__).resolve().parent.parent / "data" / "wqb.db"

# 算子/关键字/分组变量等非字段 token 停用表（保守集合；未知 token 默认当字段，宁多勿漏）
_STOPWORDS = {
    # 常见算子（快照；完整名单以 data/operators_verified.json 为准，这里只挡高频形）
    "abs", "add", "subtract", "multiply", "divide", "sign", "log", "power", "sqrt",
    "rank", "zscore", "quantile", "scale", "normalize", "winsorize", "vector_neut",
    "group_neutralize", "group_rank", "group_zscore", "group_backfill", "group_mean",
    "group_scale", "group_count", "group_sum", "bucket", "vector_avg", "vector_sum",
    "vec_avg", "vec_sum", "trade_when", "days_from_last_change", "ts_rank", "ts_zscore",
    "ts_mean", "ts_sum", "ts_std_dev", "ts_delta", "ts_delay", "ts_decay_linear",
    "ts_ir", "ts_quantile", "ts_max", "ts_min", "ts_corr", "ts_regression",
    "ts_entropy", "ts_argmax", "ts_argmin", "regression_neut", "hump", "signed_power",
    "reverse", "indneutralize", "to_nan", "replace", "is_nan", "not",
    # 字面量 / 设置
    "true", "false", "on", "off", "nan", "inf",
    # 分组变量（group_* 第二参）——不是字段
    "sector", "industry", "subindustry", "country", "market", "exchange", "subindustry",
    "stvi", "currency", "asset",
}

_TOKEN_RE = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")
_NUM_RE = re.compile(r"^[0-9.]+$")


def _extract_fields(code: str) -> set:
    """表达式文本 → 字段 token 集合（剔除算子/字面量/分组变量）。"""
    out = set()
    for tok in _TOKEN_RE.findall(code or ""):
        t = tok.lower()
        if t in _STOPWORDS or _NUM_RE.match(t):
            continue
        if t.startswith(("mdl", "anl", "fnd", "rsk", "news", "fund", "pv", "evt", "snt", "gov",
                         "ins", "est", "mrh", "cor", "ten", "short", "buy", "sell", "vpa",
                         "top", "pe", "eps", "btl", "atr", "mor", "sho", "ana", "rev")):
            out.add(tok)
        elif "_" in t and len(t) > 4:  # 形如 xxx_yyy 的长 token 大概率是字段
            out.add(tok)
    return out


def mine_fields(con, region=None, dataset=None, min_abs_sharpe=0.0):
    sql = ("SELECT region, dataset, code, sharpe, fitness FROM backtest_results "
           "WHERE code IS NOT NULL AND code != '' AND sharpe IS NOT NULL")
    args = []
    if region:
        sql += " AND region = ?"
        args.append(region)
    if dataset:
        sql += " AND dataset = ?"
        args.append(dataset)
    stats = defaultdict(lambda: {"n": 0, "max_s": 0.0, "n_hit": 0, "best_f": None, "regions": set()})
    for reg, ds, code, sharpe, fitness in con.execute(sql, args):
        if abs(sharpe) < min_abs_sharpe:
            continue
        for f in _extract_fields(code):
            s = stats[f]
            s["n"] += 1
            s["max_s"] = max(s["max_s"], abs(sharpe))
            if abs(sharpe) >= 0.5:
                s["n_hit"] += 1
            if fitness is not None:
                s["best_f"] = fitness if s["best_f"] is None else max(s["best_f"], fitness)
            s["regions"].add(reg)
    return stats


def mine_pairs(con, region=None, dataset=None, min_abs_sharpe=1.0):
    """高 |S| 表达式内的字段共现对 → 成对机制先验。"""
    sql = ("SELECT region, code, sharpe FROM backtest_results "
           "WHERE code IS NOT NULL AND code != '' AND sharpe IS NOT NULL AND abs(sharpe) >= ?")
    args = [min_abs_sharpe]
    if region:
        sql += " AND region = ?"
        args.append(region)
    if dataset:
        sql += " AND dataset = ?"
        args.append(dataset)
    stats = defaultdict(lambda: {"n": 0, "max_s": 0.0, "example": ""})
    for reg, code, sharpe in con.execute(sql, args):
        fields = sorted(_extract_fields(code))
        for i in range(len(fields)):
            for j in range(i + 1, len(fields)):
                p = (fields[i], fields[j])
                s = stats[p]
                s["n"] += 1
                if abs(sharpe) > s["max_s"]:
                    s["max_s"] = abs(sharpe)
                    s["example"] = code[:110]
    return stats


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default=str(DB_DEFAULT))
    ap.add_argument("--region")
    ap.add_argument("--dataset")
    ap.add_argument("--field", help="只看单个字段的历史战绩（含表达式样例）")
    ap.add_argument("--pairs", action="store_true", help="输出高 |S| 表达式的字段共现对")
    ap.add_argument("--min-abs-sharpe", type=float, default=0.0,
                    help="字段挖掘默认全量；pair 挖掘默认只看 |S|>=1.0 的表达式")
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--all", action="store_true", help="不限区域（默认与 --region 等价不加过滤）")
    a = ap.parse_args()
    # 规范工厂：只读（readonly=True 不改库字节）
    con = _db_connect(str(a.db), readonly=True, row_factory=sqlite3.Row)

    if a.field:
        sql = ("SELECT region, dataset, sharpe, fitness, code FROM backtest_results "
               "WHERE code LIKE ? AND sharpe IS NOT NULL ORDER BY abs(sharpe) DESC LIMIT 30")
        rows = con.execute(sql, (f"%{a.field}%",)).fetchall()
        print(f"== field {a.field}: {len(rows)} rows (top by |S|)")
        for reg, ds, s, f, code in rows:
            print(f"  [{reg}/{ds}] S={s} F={f}  {code[:100]}")
        con.close()
        return

    if a.pairs:
        stats = mine_pairs(con, a.region, a.dataset,
                           a.min_abs_sharpe if a.min_abs_sharpe > 0 else 1.0)
        rows = sorted(stats.items(), key=lambda kv: (-kv[1]["max_s"], -kv[1]["n"]))[:a.top]
        print(f"== pair priors (|S|>={a.min_abs_sharpe or 1.0}) n_pairs={len(stats)}")
        for (fa, fb), s in rows:
            print(f"  {s['max_s']:.2f}  n={s['n']}  {fa} × {fb}")
            print(f"        {s['example']}")
    else:
        stats = mine_fields(con, a.region, a.dataset, a.min_abs_sharpe)
        rows = sorted(stats.items(), key=lambda kv: (-kv[1]["max_s"], -kv[1]["n"]))[:a.top]
        print(f"== field signal priors  n_fields={len(stats)}"
              f"  (region={a.region or '*'} dataset={a.dataset or '*'})")
        print(f"{'field':46s} {'n':>4s} {'max|S|':>7s} {'hits':>5s} {'bestF':>6s} regions")
        for f, s in rows:
            hr = s["n_hit"] / s["n"] if s["n"] else 0.0
            print(f"{f:46s} {s['n']:4d} {s['max_s']:7.2f} {s['n_hit']:5d} "
                  f"{(s['best_f'] if s['best_f'] is not None else float('nan')):6.2f} "
                  f"{','.join(sorted(s['regions']))} ({hr:.0%})")
    con.close()


if __name__ == "__main__":
    main()
