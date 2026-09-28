#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""field_pool_ab.py — 字段分类→GEM 机制 A/B 评估器（2026-09-26 落地）。

回答一个因果问题：**按数据集字段分类（s2_field_pool 候选池）约束生成的表达式，
是否比未约束的回测更出货？** 用同数据集/同波配对对比去除数据集质量混杂，并剔除
伪 alpha（riskfree/beta/基准收益）污染。

分组口径（treatment 定义）：
  - pool  组 = 表达式字段全部落在 s2_field_pool 内（消费了分类结果）
  - free  组 = 表达式字段触及池外字段（未受分类约束 / 全目录生成）
  优先用表达式 source 标注（gem_<mode>_pool / _free，生成期打标）；
  无标注明细的用"字段 ⊆ 池"启发式回溯。

评估三视图：
  1. 全局/分区 pool vs free 过闸率、avg_sharpe、avg_fitness
  2. 同数据集配对（双组各 ≥ min_group_n）——控制数据集质量的最干净对比
  3. 消费一致性报告：哪些数据集 pool 命中率低（= 字段约束未生效，Task1 诊断）

用法：
  python tools/field_pool_ab.py --region IND
  python tools/field_pool_ab.py --region GLB --wave 204 --format markdown
  python tools/field_pool_ab.py --region EUR --include-pseudo   # 含伪 alpha（对照看污染量）
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "wqb.db"
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from wqb.config import is_pseudo_alpha  # noqa: E402  单源伪 alpha 黑名单
from wqb.db_conn import connect as _db_connect  # noqa: E402  规范工厂（禁止裸 sqlite3.connect）

#: 表达式字段提取的算子/内置量白名单（不算作数据字段）
_OP_TOKENS = frozenset("""
rank ts_mean ts_std_dev ts_zscore ts_delta ts_decay_linear ts_backfill ts_rank
ts_sum ts_arg_max ts_arg_min ts_ir ts_corr ts_av_diff group_neutralize group_rank
group_zscore trade_when if_else add subtract multiply divide abs sign log power
signed_power hump winsorize quantile bucket tail zscore vec_avg vec_sum vec_max
vec_min vec_std vec_count nan returns volume close open high low vwap adv20 cap
industry subindustry sector country exchange market neutralization
""".split())


def expr_fields(expr: Optional[str]) -> Set[str]:
    """提取表达式里的数据字段 id（去算子/数字/标点）。"""
    if not expr:
        return set()
    toks = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", expr)
    return {t for t in toks if t.lower() not in _OP_TOKENS and not t.isdigit()}


def _conn() -> sqlite3.Connection:
    # 规范工厂：本工具只读（readonly=True 不改库字节）；
    # 2026-09-20 db_conn 收口，禁止白名单外裸 sqlite3.connect（守卫 test_db_write_guards）。
    return _db_connect(str(DB_PATH), readonly=True, row_factory=sqlite3.Row)


def load_pools(conn: sqlite3.Connection) -> Dict[Tuple[str, str], Dict[str, Any]]:
    """读 s2_field_pool_* 池（region, dataset) -> {fields, source, builder_version}。"""
    pools: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for r in conn.execute("SELECT region, key, value FROM ledger_kv WHERE key LIKE 's2_field_pool_%'"):
        try:
            v = json.loads(r["value"])
        except Exception:
            continue
        if not isinstance(v, dict) or not v.get("candidate_field_pool"):
            continue
        ds = r["key"].replace("s2_field_pool_", "")
        pools[(r["region"], ds)] = {
            "fields": set(v.get("candidate_field_pool") or []),
            "source": v.get("source"),
            "builder_version": v.get("builder_version"),
        }
    return pools


def classify(expr: str, pool_fields: Set[str], source: Optional[str]) -> Optional[str]:
    """判定一条表达式属 pool 组 / free 组 / None(不可判)。

    优先 source 标注（<...>_pool / <...>_free），否则用字段 ⊆ 池 启发式。
    """
    if source:
        s = str(source)
        if s.endswith("_pool"):
            return "pool"
        if s.endswith("_free"):
            return "free"
    fs = expr_fields(expr)
    if not fs:
        return None
    return "pool" if fs <= pool_fields else "free"


def _stat(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    n = len(rows)
    if not n:
        return {"n": 0}
    npass = sum(1 for r in rows if (r["sharpe"] or 0) >= 1.58 and (r["fitness"] or 0) >= 1.0)
    return {
        "n": n,
        "passed": npass,
        "pass_rate": round(npass / n, 4),
        "avg_sharpe": round(sum(r["sharpe"] or 0 for r in rows) / n, 4),
        "avg_fitness": round(sum(r["fitness"] or 0 for r in rows) / n, 4),
    }


def run(region: str, wave: Optional[str] = None, dataset: Optional[str] = None,
        min_group_n: int = 8, include_pseudo: bool = False) -> Dict[str, Any]:
    """执行 A/B 评估，返回结构化结果。"""
    conn = _conn()
    try:
        pools = load_pools(conn)

        sql = ("SELECT b.region, b.dataset, b.wave, b.code, e.source AS source, "
               "b.sharpe, b.fitness "
               "FROM backtest_results b "
               "LEFT JOIN expressions e ON e.id = b.expression_id "
               "WHERE b.region=? AND b.sharpe IS NOT NULL AND b.code IS NOT NULL")
        params: List[Any] = [region]
        if wave:
            sql += " AND b.wave=?"
            params.append(wave)
        if dataset:
            sql += " AND b.dataset=?"
            params.append(dataset)
        rows = [dict(r) for r in conn.execute(sql, params)]
    finally:
        conn.close()

    # 伪 alpha 剔除（数据集级；include_pseudo=True 则保留用于对照污染量）
    excluded_ds: Set[str] = set()
    if not include_pseudo:
        for r in rows:
            if is_pseudo_alpha(r.get("dataset") or ""):
                excluded_ds.add(r["dataset"])
    n_pseudo = sum(1 for r in rows if is_pseudo_alpha(r.get("dataset") or ""))
    rows = [r for r in rows if r.get("dataset") not in excluded_ds]

    # 分组
    per_ds: Dict[str, Dict[str, List[Dict[str, Any]]]] = defaultdict(lambda: {"pool": [], "free": []})
    n_classified = {"pool": 0, "free": 0}
    unclassified = 0
    consume = defaultdict(lambda: [0, 0])  # (region,ds) -> [pool_n, total_n]
    for r in rows:
        key = (r["region"], r.get("dataset"))
        pool = pools.get(key)
        if not pool:
            continue  # 无池数据集不参与 A/B（无 treatment 可言）
        grp = classify(r["code"], pool["fields"], r.get("source"))
        if grp is None:
            unclassified += 1
            continue
        per_ds[r["dataset"]][grp].append(r)
        n_classified[grp] += 1
        consume[key][1] += 1
        if grp == "pool":
            consume[key][0] += 1

    # 视图1：全局/分区（同数据集池内）
    g = {"pool": [], "free": []}
    for d in per_ds.values():
        g["pool"].extend(d["pool"])
        g["free"].extend(d["free"])
    global_stat = {k: _stat(v) for k, v in g.items()}

    # 视图2：同数据集配对（双组各 ≥ min_group_n）
    pairs = []
    win = tie = lose = 0
    for ds, d in sorted(per_ds.items()):
        ps, fs = _stat(d["pool"]), _stat(d["free"])
        if ps["n"] < min_group_n or fs["n"] < min_group_n:
            continue
        pr, fr = ps["pass_rate"], fs["pass_rate"]
        tag = "pool优" if pr > fr + 0.02 else ("free优" if fr > pr + 0.02 else "持平")
        if tag == "pool优":
            win += 1
        elif tag == "free优":
            lose += 1
        else:
            tie += 1
        pairs.append({"dataset": ds, "pool": ps, "free": fs, "verdict": tag})

    # 视图3：消费一致性（pool 命中率低 = 字段约束未生效）
    low_consume = []
    for (rg, ds), (pn, tot) in sorted(consume.items()):
        if tot < 10:
            continue
        ratio = pn / tot
        if ratio < 0.5:
            low_consume.append({"region": rg, "dataset": ds, "pool_hit_ratio": round(ratio, 3),
                                "pool_n": pn, "total_n": tot})

    return {
        "region": region, "wave": wave, "dataset": dataset,
        "include_pseudo": include_pseudo,
        "excluded_pseudo_datasets": sorted(excluded_ds),
        "n_pseudo_excluded": n_pseudo if not include_pseudo else 0,
        "n_with_pool": sum(1 for r in rows if (r["region"], r.get("dataset")) in pools),
        "classified": n_classified, "unclassified": unclassified,
        "global_ab": global_stat,
        "same_dataset_pairs": pairs,
        "pair_summary": {"pool_better": win, "tie": tie, "free_better": lose},
        "low_consume_datasets": low_consume,
    }


def to_markdown(res: Dict[str, Any]) -> str:
    L = [f"# 字段分类→GEM A/B 评估（{res['region']}）", ""]
    if res.get("wave"):
        L.append(f"- 波次：{res['wave']}")
    L.append(f"- 伪 alpha 剔除：{'关（含污染）' if res['include_pseudo'] else '开'}"
             + (f"，剔除 {res['n_pseudo_excluded']} 条/集 {res['excluded_pseudo_datasets']}"
                if res["excluded_pseudo_datasets"] else ""))
    L.append(f"- 参与 A/B（有池）：{res['n_with_pool']} 条；分类 pool={res['classified']['pool']} / "
             f"free={res['classified']['free']} / 不可判={res['unclassified']}")
    L.append("")
    L.append("## 视图1：全局 pool vs free（同数据集池内）")
    L.append("")
    L.append("| 组 | n | 过闸 | 过闸率 | avg_sharpe | avg_fitness |")
    L.append("|---|---|---|---|---|---|")
    for k in ("pool", "free"):
        s = res["global_ab"][k]
        if s["n"]:
            L.append(f"| {k} | {s['n']} | {s['passed']} | {s['pass_rate']:.1%} | "
                     f"{s['avg_sharpe']} | {s['avg_fitness']} |")
    L.append("")
    L.append("## 视图2：同数据集配对（控制数据集质量，双组各≥min_n）")
    L.append("")
    L.append(f"**配对小结：pool优 {res['pair_summary']['pool_better']} / "
             f"持平 {res['pair_summary']['tie']} / free优 {res['pair_summary']['free_better']}**")
    L.append("")
    L.append("| 数据集 | pool过闸率(n) | free过闸率(n) | 判定 |")
    L.append("|---|---|---|---|")
    for p in res["same_dataset_pairs"]:
        L.append(f"| {p['dataset']} | {p['pool']['pass_rate']:.1%}({p['pool']['n']}) | "
                 f"{p['free']['pass_rate']:.1%}({p['free']['n']}) | {p['verdict']} |")
    L.append("")
    L.append("## 视图3：消费一致性（pool 命中率<50% = 字段约束疑似未生效）")
    L.append("")
    if res["low_consume_datasets"]:
        L.append("| 区域 | 数据集 | pool命中率 | pool/总 |")
        L.append("|---|---|---|---|")
        for d in res["low_consume_datasets"]:
            L.append(f"| {d['region']} | {d['dataset']} | {d['pool_hit_ratio']:.0%} | "
                     f"{d['pool_n']}/{d['total_n']} |")
    else:
        L.append("无低命中数据集。")
    L.append("")
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description="字段分类→GEM 机制 A/B 评估（同数据集对照，剔除伪 alpha）")
    ap.add_argument("--region", required=True, help="区域（如 IND/GLB）")
    ap.add_argument("--wave", help="限定波次")
    ap.add_argument("--dataset", help="限定数据集")
    ap.add_argument("--min-group-n", type=int, default=8, help="配对最小样本（双组各需≥N，默认 8）")
    ap.add_argument("--include-pseudo", action="store_true", help="不剔除伪 alpha（对照看污染量）")
    ap.add_argument("--format", choices=["json", "markdown"], default="json", help="输出格式")
    a = ap.parse_args()

    res = run(a.region, wave=a.wave, dataset=a.dataset,
              min_group_n=a.min_group_n, include_pseudo=a.include_pseudo)
    if a.format == "markdown":
        print(to_markdown(res))
    else:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
