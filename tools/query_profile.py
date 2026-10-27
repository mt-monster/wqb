#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""字段画像查询接口（CLI + 可导入 API）

表：dataset_profile（数据集级）/ field_profile_full（字段级），见
    tools/load_field_profiles_to_db.py

CLI 示例：
    # 1) 数据集筛选：高覆盖 + 有 ALIVE 字段
    python tools/query_profile.py datasets --category ANALYST --min-cov 0.7 --has-alive

    # 2) 某数据集的全字段（按 best_S 排序，只看测过的）
    python tools/query_profile.py fields --dataset analyst7 --tested --min-best-s 1.5

    # 3) 跨数据集找「未测 + 高覆盖」的盲区字段
    python tools/query_profile.py fields --untested --min-cov 0.9 --family 修正与预期 --limit 100

    # 4) 关键词全文检索（字段名 + 描述）
    python tools/query_profile.py search "short interest"

    # 5) 全局统计 / TOP 榜单
    python tools/query_profile.py stats
    python tools/query_profile.py top --metric best_2y --min-cov 0.8

    # 6) JSON 输出（供程序消费）
    python tools/query_profile.py fields --dataset pv87 --limit 5 --json

可导入 API：
    from tools.query_profile import query_datasets, query_fields, stats, search
"""
import os
import sys
import json
import sqlite3          # 仅用于 sqlite3.Row（连接本身一律走 db_connect）
import argparse
from typing import Any, Dict, List, Optional

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "data", "wqb.db")

# 连接一律走规范工厂（只读：本脚本是离线查询器，永不写库）。
sys.path.insert(0, os.path.join(ROOT, "src"))
from wqb.db_conn import connect as db_connect  # noqa: E402


# ------------------------------------------------------------------ 连接
def _con():
    con = db_connect(DB, readonly=True)
    con.row_factory = sqlite3.Row
    return con


#: 选集期望值口径（与 full_template_campaign.all_datasets 的 ORDER BY 同源）：
#: value_score × 平均覆盖 × 未测占比 ÷ (1 + alphaCount/1000)。
#: 只反映「拥挤度 × 覆盖 × 未测占比」，**不反映字段信号强度**。
EV_SQL = (
    "COALESCE(value_score,0)*COALESCE(avg_field_coverage,0)"
    "*CAST(n_untested AS REAL)/NULLIF(n_fields,1)"
    "/(1.0+COALESCE(alpha_count,0)/1000.0)"
)


# ------------------------------------------------------------------ 查询 API
def query_datasets(region: str = "EUR", category: Optional[str] = None,
                   min_cov: Optional[float] = None, has_alive: bool = False,
                   max_untested_ratio: Optional[float] = None,
                   sort: str = "avg_field_coverage", desc: bool = True,
                   limit: int = 100) -> List[Dict[str, Any]]:
    """数据集级筛选。

    Args:
        category: 类别（ANALYST / PV / MODEL ...）
        min_cov: 平均字段覆盖率下限
        has_alive: 只保留历史有 ALIVE 字段的数据集
        max_untested_ratio: 未测字段占比上限（0.9 = 至少 10% 已测）
        sort: n_alive / avg_field_coverage / alpha_count / value_score / n_fields /
          best_s_in_dataset / best_2y_in_dataset / n_backtests / ev
    """
    q = [f"SELECT *, {EV_SQL} AS ev FROM dataset_profile WHERE region=?"]
    p: List[Any] = [region]
    if category:
        q.append("AND UPPER(category)=UPPER(?)")
        p.append(category)
    if min_cov is not None:
        q.append("AND avg_field_coverage>=?")
        p.append(min_cov)
    if has_alive:
        q.append("AND n_alive>0")
    if max_untested_ratio is not None:
        q.append("AND (CAST(n_untested AS REAL)/NULLIF(n_fields,0))<=?")
        p.append(max_untested_ratio)
    sort_col = sort if sort in {
        "n_alive", "avg_field_coverage", "alpha_count", "value_score",
        "n_fields", "best_s_in_dataset", "best_2y_in_dataset", "n_backtests",
        "ev"} else "avg_field_coverage"
    if sort_col == "ev":
        sort_col = EV_SQL
    q.append(f"ORDER BY {sort_col} {'DESC' if desc else 'ASC'} NULLS LAST LIMIT ?")
    p.append(limit)
    con = _con()
    try:
        return [dict(r) for r in con.execute(" ".join(q), p)]
    finally:
        con.close()


def query_fields(region: str = "EUR", dataset: Optional[str] = None,
                 family: Optional[str] = None, verdict: Optional[str] = None,
                 min_cov: Optional[float] = None, max_cov: Optional[float] = None,
                 min_best_s: Optional[float] = None, min_best_2y: Optional[float] = None,
                 keyword: Optional[str] = None, tested: bool = False,
                 untested: bool = False, alive_only: bool = False,
                 sort: str = "best_s", desc: bool = True,
                 limit: int = 50) -> List[Dict[str, Any]]:
    """字段级筛选（组合条件）。"""
    q = ["SELECT * FROM field_profile_full WHERE region=?"]
    p: List[Any] = [region]
    if dataset:
        q.append("AND dataset=?")
        p.append(dataset)
    if family:
        q.append("AND semantic_family=?")
        p.append(family)
    if verdict:
        q.append("AND UPPER(verdict)=UPPER(?)")
        p.append(verdict)
    if min_cov is not None:
        q.append("AND coverage>=?")
        p.append(min_cov)
    if max_cov is not None:
        q.append("AND coverage<=?")
        p.append(max_cov)
    if min_best_s is not None:
        q.append("AND best_s>=?")
        p.append(min_best_s)
    if min_best_2y is not None:
        q.append("AND best_2y>=?")
        p.append(min_best_2y)
    if keyword:
        q.append("AND (LOWER(field_name) LIKE ? OR LOWER(description) LIKE ?)")
        kw = f"%{keyword.lower()}%"
        p += [kw, kw]
    if tested:
        q.append("AND n_tests>0")
    if untested:
        q.append("AND is_untested=1")
    if alive_only:
        q.append("AND is_alive=1")
    sort_col = sort if sort in {
        "best_s", "best_2y", "best_sub", "coverage", "n_tests", "field_name"} else "best_s"
    q.append(f"ORDER BY {sort_col} {'DESC' if desc else 'ASC'} NULLS LAST LIMIT ?")
    p.append(limit)
    con = _con()
    try:
        return [dict(r) for r in con.execute(" ".join(q), p)]
    finally:
        con.close()


def query_dims(region: str = "EUR", category: Optional[str] = None,
               min_dim_cov: Optional[float] = None, only_bt: bool = True,
               sort: str = "dim_coverage_bt", limit: int = 40) -> List[Dict[str, Any]]:
    """维度覆盖查询。

    Args:
        min_dim_cov: 维度覆盖率下限（0~1）
        only_bt: True=按实测口径（n_tests>0）｜False=按静态判定口径
        sort: dim_coverage_bt / dim_coverage_static / n_dims / n_fields
    """
    col = "dim_coverage_bt" if only_bt else "dim_coverage_static"
    q = [f"SELECT dataset, category, n_fields, n_untested, n_dims, n_dims_bt, "
         f"n_dims_static, dim_coverage_bt, dim_coverage_static, value_score, alpha_count "
         f"FROM dataset_profile WHERE region=?"]
    p: List[Any] = [region]
    if category:
        q.append("AND UPPER(category)=UPPER(?)"); p.append(category)
    if min_dim_cov is not None:
        q.append(f"AND {col}>=?"); p.append(min_dim_cov)
    sort_col = sort if sort in {"dim_coverage_bt", "dim_coverage_static", "n_dims", "n_fields"} else col
    q.append(f"ORDER BY {sort_col} {'DESC' if only_bt else 'DESC'} NULLS LAST LIMIT ?")
    p.append(limit)
    con = _con()
    try:
        return [dict(r) for r in con.execute(" ".join(q), p)]
    finally:
        con.close()


def search(kw: str, region: str = "EUR", limit: int = 30) -> List[Dict[str, Any]]:
    """字段名 + 描述全文检索。"""
    return query_fields(region=region, keyword=kw, limit=limit)


def stats(region: str = "EUR") -> Dict[str, Any]:
    """全局统计。"""
    con = _con()
    try:
        r = con.execute(
            """SELECT COUNT(*) n_ds, SUM(n_fields) n_fl, SUM(n_alive) n_alive,
                      SUM(n_untested) n_untested, SUM(n_unusable) n_unusable,
                      SUM(n_dead) n_dead, SUM(n_axis_only) n_axis
               FROM dataset_profile WHERE region=?""", (region,)).fetchone()
        cats = [dict(x) for x in con.execute(
            """SELECT category,
                      COUNT(*) n_ds, SUM(n_fields) n_fl, SUM(n_alive) n_alive,
                      ROUND(AVG(avg_field_coverage),3) avg_cov
               FROM dataset_profile WHERE region=? GROUP BY category ORDER BY n_fl DESC""", (region,))]
        fams = [dict(x) for x in con.execute(
            """SELECT semantic_family,
                      COUNT(*) n, SUM(is_alive) n_alive, SUM(is_untested) n_untested,
                      ROUND(AVG(coverage),3) avg_cov
               FROM field_profile_full WHERE region=? GROUP BY semantic_family ORDER BY n DESC""", (region,))]
        verds = [dict(x) for x in con.execute(
            """SELECT verdict, COUNT(*) n FROM field_profile_full
               WHERE region=? GROUP BY verdict ORDER BY n DESC""", (region,))]
        overview = dict(r)
        # 空区域（如尚未跑 load_field_profiles_to_db.py 的 USA）聚合全为 NULL，
        # 直接进格式化会在 `{o['n_fl']:,}` 处抛 NoneType.__format__。
        overview["empty"] = not overview.get("n_ds")
        return {"region": region, "overview": overview,
                "by_category": cats, "by_family": fams, "by_verdict": verds}
    finally:
        con.close()


# ------------------------------------------------------------------ CLI
def _table(rows: List[Dict[str, Any]], cols: List[str], maxw: int = 42) -> str:
    if not rows:
        return "（无结果）"
    widths = []
    for c in cols:
        w = max(len(c), *(len(str(r.get(c) if r.get(c) is not None else "—")) for r in rows))
        widths.append(min(w, maxw))
    out = [" | ".join(c[:widths[i]].ljust(widths[i]) for i, c in enumerate(cols)),
           "-+-".join("-" * w for w in widths)]
    for r in rows:
        cells = []
        for i, c in enumerate(cols):
            v = r.get(c)
            v = "—" if v is None else (f"{v:.3f}" if isinstance(v, float) else str(v))
            if len(v) > widths[i]:
                v = v[: widths[i] - 1] + "…"
            cells.append(v.ljust(widths[i]))
        out.append(" | ".join(cells))
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="字段画像查询（region 默认 EUR；USA 需先建画像）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("datasets", help="数据集级筛选")
    d.add_argument("--region", default="EUR")
    d.add_argument("--category")
    d.add_argument("--min-cov", type=float)
    d.add_argument("--has-alive", action="store_true")
    d.add_argument("--max-untested", type=float)
    d.add_argument("--sort", default="avg_field_coverage")
    d.add_argument("--limit", type=int, default=30)
    d.add_argument("--json", action="store_true")

    f = sub.add_parser("fields", help="字段级筛选")
    f.add_argument("--region", default="EUR")
    f.add_argument("--dataset")
    f.add_argument("--family")
    f.add_argument("--verdict")
    f.add_argument("--min-cov", type=float)
    f.add_argument("--max-cov", type=float)
    f.add_argument("--min-best-s", type=float)
    f.add_argument("--min-best-2y", type=float)
    f.add_argument("--keyword")
    f.add_argument("--tested", action="store_true")
    f.add_argument("--untested", action="store_true")
    f.add_argument("--alive-only", action="store_true")
    f.add_argument("--sort", default="best_s")
    f.add_argument("--limit", type=int, default=30)
    f.add_argument("--json", action="store_true")

    s = sub.add_parser("search", help="关键词检索")
    s.add_argument("kw")
    s.add_argument("--region", default="EUR")
    s.add_argument("--limit", type=int, default=30)
    s.add_argument("--json", action="store_true")

    dm = sub.add_parser("dims", help="维度覆盖查询")
    dm.add_argument("--region", default="EUR")
    dm.add_argument("--category")
    dm.add_argument("--min-dim-cov", type=float)
    dm.add_argument("--static", action="store_true", help="用静态判定口径（非实测）")
    dm.add_argument("--limit", type=int, default=30)
    dm.add_argument("--json", action="store_true")

    st = sub.add_parser("stats", help="全局统计")
    st.add_argument("--region", default="EUR")
    st.add_argument("--json", action="store_true")

    tp = sub.add_parser("top", help="榜单")
    tp.add_argument("--region", default="EUR")
    tp.add_argument("--metric", default="best_s", choices=["best_s", "best_2y", "best_sub"])
    tp.add_argument("--min-cov", type=float, default=0.5)
    tp.add_argument("--limit", type=int, default=20)
    tp.add_argument("--json", action="store_true")

    a = ap.parse_args()

    if a.cmd == "datasets":
        rows = query_datasets(a.region, a.category, a.min_cov, a.has_alive,
                              a.max_untested, a.sort, True, a.limit)
        if a.json:
            print(json.dumps(rows, ensure_ascii=False, indent=1))
        else:
            print(_table(rows, ["dataset", "category", "n_fields", "avg_field_coverage",
                                "n_alive", "n_untested", "alpha_count", "value_score", "ev"]))
    elif a.cmd == "fields":
        rows = query_fields(a.region, a.dataset, a.family, a.verdict, a.min_cov, a.max_cov,
                            a.min_best_s, a.min_best_2y, a.keyword, a.tested, a.untested,
                            a.alive_only, a.sort, True, a.limit)
        if a.json:
            print(json.dumps(rows, ensure_ascii=False, indent=1))
        else:
            print(_table(rows, ["dataset", "field_name", "field_type", "coverage",
                                "semantic_family", "n_tests", "best_s", "best_2y", "verdict"]))
    elif a.cmd == "search":
        rows = search(a.kw, a.region, a.limit)
        if a.json:
            print(json.dumps(rows, ensure_ascii=False, indent=1))
        else:
            print(_table(rows, ["dataset", "field_name", "coverage", "semantic_family",
                                "best_s", "verdict"]))
    elif a.cmd == "dims":
        rows = query_dims(a.region, a.category, a.min_dim_cov, not a.static,
                          "dim_coverage_bt" if not a.static else "dim_coverage_static", a.limit)
        if a.json:
            print(json.dumps(rows, ensure_ascii=False, indent=1))
        else:
            print(_table(rows, ["dataset", "category", "n_fields", "n_dims", "n_dims_bt",
                                "dim_coverage_bt", "dim_coverage_static", "value_score"]))
    elif a.cmd == "stats":
        s2 = stats(a.region)
        if a.json:
            print(json.dumps(s2, ensure_ascii=False, indent=1))
        else:
            o = s2["overview"]
            if o.get("empty"):
                print(f"[{a.region}] 无画像行：先跑 "
                      f"`$WQ_PY tools/load_field_profiles_to_db.py --region {a.region}`")
                return
            print(f"{a.region} 画像总览：数据集 {o['n_ds']} 个｜字段 {o['n_fl']:,} 条"
                  f"｜ALIVE {o['n_alive']}｜未测 {o['n_untested']:,}"
                  f"｜UNUSABLE {o['n_unusable']:,}｜DEAD {o['n_dead']}｜仅作轴 {o['n_axis']}")
            print("\n按类别：")
            print(_table(s2["by_category"], ["category", "n_ds", "n_fl", "n_alive", "avg_cov"]))
            print("\n按语义族：")
            print(_table(s2["by_family"], ["semantic_family", "n", "n_alive", "n_untested", "avg_cov"]))
            print("\n按判定：")
            print(_table(s2["by_verdict"], ["verdict", "n"]))
    elif a.cmd == "top":
        rows = query_fields(a.region, None, None, None, a.min_cov, None, None, None,
                            None, False, False, False, a.metric, True, a.limit)
        if a.json:
            print(json.dumps(rows, ensure_ascii=False, indent=1))
        else:
            print(_table(rows, ["dataset", "field_name", "coverage", "semantic_family",
                                "best_s", "best_2y", "best_sub", "verdict"]))


if __name__ == "__main__":
    main()
