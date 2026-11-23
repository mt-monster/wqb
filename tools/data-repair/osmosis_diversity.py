#!/usr/bin/env python
"""Osmosis 分配多样性体检 —— 数据集 / 中性化 / 换手 三条轴（点数加权）。

## 为什么需要它（2026-11-22 官方+论坛 review 结论）

官方 `Osmosis Allocation Guide` 的选品 tips 要求「Diversify across datasets and categories」
「Diversify across Operators and Neutralizations」「Spread across turnover ranges」，但分配器
只看 region / inv / margin / 相关性 —— 这三条轴**没有任何度量**，于是「已分散」永远只是
一句声称（实测 138 颗分配件里只有 2 颗带 SRC_/EXPRFAM_ 标签）。

本工具**零平台写入**，来源全部是本地库 + MCP 缓存：
- 数据集：从 alpha 表达式里的**数据字段**反查 `fields.field_name -> dataset_id`，
  并限定在**本 region 的 dataset 集合**内消歧（字段名跨区重名，不限区会串）。
  ⚠ 不能用 `alphas.dataset_id`：实测该列对整区是同一个占位值（DEU 22 颗全指向 1902），
  而按字段反查同一批得到 2–4 个不同数据集，后者才可信。
- 中性化 / 换手：`alphas.neutralization` / `alphas.turnover`。
- `datasets.category` 在本库里绝大多数为 NULL ⇒ 不出类别轴，只标注「不可得」。

多数据集 alpha 的点数**按数据集个数均分**（暴露归因口径），不是全额计入每个数据集。

## 判读

- `top1_ds` ≥ 40% ⇒ 单一数据集过重，官方口径下同涨同跌风险高。
- `top1_neut` ≥ 70% ⇒ 中性化轴单一（若候选池本身只有这一种轴，属池结构问题）。
- 换手三桶任一 >70% ⇒ 换手结构偏斜。
- `cov` < 80% ⇒ 该 scope 有较多 alpha 的字段在本地库里查不到，集中度数字要打折看。

## 用法

    PYTHONPATH=world-quant-brain-mcp python tools/data-repair/osmosis_diversity.py
    ... --plan results/osmosis_plan_v2.json --md results/osmosis_diversity.md
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from typing import Any, Dict, List

from wqb.db_conn import connect as db_connect  # noqa: E402  规范工厂（禁裸 sqlite3.connect）

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.path.join(_ROOT, "data", "wqb.db")
DEFAULT_PLAN = os.path.join(_ROOT, "results", "osmosis_plan.json")

_TOKEN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_CACHE_SQL = "select payload from api_cache where cache_key like 'user_alphas%'"


def load_codes() -> Dict[str, str]:
    """alpha_id -> 表达式（取自 user_alphas 缓存；SUPER 的组合表达式为空，跳过）。"""
    if not os.path.exists(DB_PATH):
        return {}
    con = db_connect(DB_PATH, readonly=True)
    try:
        out: Dict[str, str] = {}
        for (payload,) in con.execute(_CACHE_SQL):
            try:
                d = json.loads(payload)
            except Exception:
                continue
            for a in d.get("results") or []:
                code = ((a.get("regular") or {}).get("code") or "").strip()
                if code:
                    out[a["id"]] = code
        return out
    finally:
        con.close()


def load_db_facts() -> tuple:
    """返回 (region -> {dataset_id: label}, region -> dataset_id set,
              field -> {dataset_id}, alpha -> (neut, turnover))。"""
    con = db_connect(DB_PATH, readonly=True)
    try:
        reg_id = {name: rid for rid, name in con.execute("select id, name from regions")}
        ds_label: Dict[str, Dict[int, str]] = defaultdict(dict)
        ds_region: Dict[str, set] = defaultdict(set)
        for dsid, name, rid in con.execute("select id, coalesce(name,''), region_id from datasets"):
            rname = next((k for k, v in reg_id.items() if v == rid), None)
            if rname is None:
                continue
            ds_region[rname].add(dsid)
            ds_label[rname][dsid] = name if name and name != "_unknown" else f"ds#{dsid}"
        field_ds: Dict[str, set] = defaultdict(set)
        for fn, dsid in con.execute("select field_name, dataset_id from fields"):
            field_ds[fn].add(dsid)
        facts = {aid: (neut, to) for aid, neut, to in
                 con.execute("select alpha_id, neutralization, turnover from alphas")}
        return ds_label, ds_region, field_ds, facts
    finally:
        con.close()


def alpha_datasets(code: str, region: str, field_ds: Dict[str, set],
                   ds_region: Dict[str, set], ds_label: Dict[str, Dict[int, str]]) -> List[str]:
    scoped = ds_region.get(region, set())
    ids = set()
    for tok in set(_TOKEN.findall(code)):
        ids |= (field_ds.get(tok) or set()) & scoped
    return [ds_label.get(region, {}).get(i, f"ds#{i}") for i in sorted(ids)]


def top1(points: Dict[str, float]) -> tuple:
    if not points:
        return "—", 0.0
    k = max(points, key=lambda x: points[x])
    return k, points[k]


def analyze(plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    codes = load_codes()
    ds_label, ds_region, field_ds, facts = load_db_facts()

    by_reg: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for p in plan:
        by_reg[p["region"]].append(p)

    out: List[Dict[str, Any]] = []
    for reg in sorted(by_reg):
        rows = by_reg[reg]
        tot = sum(p["points"] for p in rows) or 1
        ra_pts_total = sum(p["points"] for p in rows if p.get("alpha_type") != "SUPER") or 1
        ds_pts: Dict[str, float] = defaultdict(float)
        neut_pts: Dict[str, float] = defaultdict(float)
        to_b: Dict[str, float] = defaultdict(float)
        covered = 0.0
        for p in rows:
            pid, pts = p["alpha_id"], p["points"]
            if p.get("alpha_type") == "SUPER":
                ds_pts["SA(组合)"] += pts
            else:
                dss = alpha_datasets(codes.get(pid, ""), reg, field_ds, ds_region, ds_label)
                if dss:
                    covered += pts
                    for d in dss:
                        ds_pts[d] += pts / len(dss)
                else:
                    ds_pts["(RA 字段不可解析)"] += pts
            neut, to = facts.get(pid, (None, None))
            neut_pts[neut or "?"] += pts
            if to is None:
                to_b["?"] += pts
            elif to < 0.10:
                to_b["<10%"] += pts
            elif to <= 0.20:
                to_b["10-20%"] += pts
            else:
                to_b[">20%"] += pts
        d1, dv = top1(ds_pts)
        n1, nv = top1(neut_pts)
        out.append({
            "scope": reg, "n": len(rows), "points": tot,
            "cov": round(100 * covered / ra_pts_total, 0),
            "n_ds": len([k for k in ds_pts if not k.startswith("(") and k != "SA(组合)"]),
            "top1_ds": d1, "top1_ds_share": round(100 * dv / tot, 1),
            "top3_ds": ", ".join(f"{k} {100 * v / tot:.0f}%" for k, v in
                                 sorted(ds_pts.items(), key=lambda kv: -kv[1])[:3]),
            "n_neut": len(neut_pts), "top1_neut": n1,
            "top1_neut_share": round(100 * nv / tot, 1),
            "to": {k: round(100 * v / tot, 1) for k, v in to_b.items()},
        })
    return out


def render(stats: List[Dict[str, Any]]) -> str:
    lines = ["| Scope | n | 数据集覆盖 | 数据集数 | top1 数据集（占比） | top3 数据集 | 中性化数 | top1 中性化（占比） | 换手 <10/10-20/>20% |",
             "|---|---:|---:|---:|---|---|---:|---|---|"]
    for s in stats:
        to = s["to"]
        lines.append(
            f"| {s['scope']} | {s['n']} | {s['cov']:.0f}% | {s['n_ds']} | "
            f"{s['top1_ds']} ({s['top1_ds_share']}%) | {s['top3_ds']} | "
            f"{s['n_neut']} | {s['top1_neut']} ({s['top1_neut_share']}%) | "
            f"{to.get('<10%', 0)} / {to.get('10-20%', 0)} / {to.get('>20%', 0)} |")
    warns = []
    for s in stats:
        tag = "" if s["cov"] >= 80 else "（覆盖率低，慎读）"
        if s["top1_ds_share"] >= 40:
            warns.append(f"- `{s['scope']}` 单一数据集占 **{s['top1_ds_share']}%**"
                         f"（{s['top1_ds']}）≥40%{tag}")
        if s["top1_neut_share"] >= 70:
            warns.append(f"- `{s['scope']}` 单一中性化占 **{s['top1_neut_share']}%**"
                         f"（{s['top1_neut']}）≥70%{tag}")
        for k, v in s["to"].items():
            if v >= 70:
                warns.append(f"- `{s['scope']}` 换手桶 {k} 占 {v}% ≥70%")
    lines.append("")
    if warns:
        lines.append("**集中度告警**")
        lines.extend(warns)
    else:
        lines.append("**无集中度告警**")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Osmosis 分配多样性体检（数据集/中性化/换手）")
    ap.add_argument("--plan", default=DEFAULT_PLAN)
    ap.add_argument("--md", default="", help="把表格追加写入该 markdown 文件")
    args = ap.parse_args()

    plan = json.load(open(args.plan, encoding="utf-8"))
    stats = analyze(plan)
    table = render(stats)
    print(f"\nOsmosis 分配多样性（{os.path.basename(args.plan)}，{len(plan)} 颗）\n")
    print(table)
    if args.md:
        with open(args.md, "a", encoding="utf-8") as f:
            f.write("\n## 多样性体检（数据集 / 中性化 / 换手）\n\n" + table + "\n")
        print(f"\n[ok] 已追加 -> {args.md}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
