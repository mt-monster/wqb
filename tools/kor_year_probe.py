# -*- coding: utf-8 -*-
"""十年数据存在性探针（KOR / TOP600 / D1）。

按用户 2026-10-25 指令：「数据集覆盖率可动态调整，但是要求十年都要有数据」。
本脚本对候选数据集跑一次最小仿真，再用 yearly-stats 判定 2014–2023 是否逐年有数据。

判据：
  - 逐年 pnl != 0 且 (longCount + shortCount) > 0  ⇒ 该年有数据
  - 任一年缺失 ⇒ 整集出局（不接受「近几年才有效」）

用法：
  python tools/kor_year_probe.py --dataset predictive_starmine
  python tools/kor_year_probe.py --dataset ml_factor_proj --field <fid>
  python tools/kor_year_probe.py --expr "rank(ts_backfill(F,22))" --tag mytag

输出：每条一行 JSON，便于批量落盘。
"""
import argparse
import asyncio
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))

from brain_api import BrainApiClient, SimulationData, SimulationSettings  # noqa: E402

YEARS = [str(y) for y in range(2014, 2024)]


def build_expr(field_id, ftype):
    if str(ftype).upper() == "VECTOR":
        return f"rank(ts_backfill(vec_avg({field_id}), 22))"
    return f"rank(ts_backfill({field_id}, 22))"


async def pick_field(client, dataset, explicit_field):
    if explicit_field:
        return {"id": explicit_field, "type": "MATRIX", "coverage": None}, None
    resp = await client.get_datafields(
        region="KOR", universe="TOP600", delay=1,
        dataset_id=dataset, filter_sharpe=False,
    )
    fields = resp.get("results") or []
    if not fields:
        return None, resp
    # 取 coverage 最高的字段做代表
    best = max(fields, key=lambda f: (f.get("coverage") or 0))
    return best, resp


YEARLY_COLS = ["year", "pnl", "bookSize", "longCount", "shortCount", "turnover",
               "sharpe", "returns", "drawdown", "margin", "fitness", "stage"]


def normalize_yearly(ys):
    """把 yearly-stats 响应归一成 dict 列表。

    ★ 2026-10-25 修（探针 100% 假阴性的真因）：该端点 `records` 是**位置数组**，
    列序由 `schema.properties[].name` 给出，例如
      ["2014", -196476.0, 20000000, 285, 295, 0.069, -0.45, ...]
    旧代码写 `r.get("year")` ⇒ AttributeError: 'list' object has no attribute 'get'；
    加 isinstance(r, dict) 护栏后更糟——全部被静默丢弃 ⇒ n_years=0、整集误判。
    另外顶层偶尔是裸 list（无 schema），也一并处理。
    """
    if isinstance(ys, list):
        recs_list, cols = ys, None
    elif isinstance(ys, dict):
        recs_list = ys.get("records") or ys.get("yearly_stats") or []
        cols = [p.get("name") for p in ((ys.get("schema") or {}).get("properties") or [])]
    else:
        return []
    if not cols or len(cols) < len(YEARLY_COLS):
        cols = YEARLY_COLS
    out = []
    for r in recs_list:
        if isinstance(r, dict):
            out.append(r)
        elif isinstance(r, (list, tuple)):
            out.append(dict(zip(cols, r)))
    return out


async def probe(client, dataset, field, expr, tag, settings_kwargs):
    settings = SimulationSettings(
        region="KOR", universe="TOP600", delay=1,
        decay=settings_kwargs["decay"],
        neutralization=settings_kwargs["neutralization"],
        truncation=settings_kwargs["truncation"],
        nanHandling="OFF", visualization=False,
    )
    alpha = await client.create_simulation(
        SimulationData(type="REGULAR", settings=settings, regular=expr)
    )
    aid = alpha.get("id")
    if not aid:
        return {
            "tag": tag, "dataset": dataset, "field": field["id"], "expr": expr,
            "status": "SIM_FAILED", "error": str(alpha)[:400],
        }

    ys = await client.get_alpha_yearly_stats(aid)
    recs = {str(r.get("year")): r for r in normalize_yearly(ys) if r.get("year") is not None}

    empty, present = [], []
    for y in YEARS:
        r = recs.get(y)
        if not r:
            empty.append(y)
            continue
        held = (r.get("longCount") or 0) + (r.get("shortCount") or 0)
        if (r.get("pnl") or 0) == 0 or held == 0:
            empty.append(y)
        else:
            present.append(y)

    is_ = (alpha.get("is") or {})
    checks = {c.get("name"): c for c in (is_.get("checks") or [])}
    cw = checks.get("CONCENTRATED_WEIGHT") or {}

    verdict = "PASS_10Y" if len(empty) == 0 else "REJECT_MISSING_YEAR"
    # 2026-10-26 新增：稀疏数据闸。
    # `analyst11`（ESG）探针 S=0.63 排全类第一，但 5 种形态全部 CONCENTRATED_WEIGHT=1.0
    # ——持仓坍缩到单票，说明「有效覆盖」远低于名义 coverage，任何截面变换都只能
    # 区分极少数名字。CW 是同一次仿真的免费读数，是数据稀疏的唯一早期信号，
    # S 完全看不出来。故 CW 失败时直接判该集不可用，避免后续白烧结构实验。
    if cw.get("result") == "FAIL":
        verdict = "REJECT_SPARSE"

    return {
        "tag": tag,
        "dataset": dataset,
        "field": field["id"],
        "ftype": field.get("type"),
        "coverage": field.get("coverage"),
        "expr": expr,
        "alpha_id": aid,
        "sharpe": is_.get("sharpe"),
        "fitness": is_.get("fitness"),
        "turnover": is_.get("turnover"),
        "concentrated_weight": cw.get("result"),
        "cw_value": cw.get("value"),
        "drawdown": (is_.get("metrics") or is_).get("drawdown"),
        "n_years": len(present),
        "first_year": present[0] if present else None,
        "empty_years": empty,
        "verdict": verdict,
        "yearly_sharpe": {y: recs.get(y, {}).get("sharpe") for y in YEARS},
    }


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default=None)
    ap.add_argument("--field", default=None)
    ap.add_argument("--expr", default=None)
    ap.add_argument("--tag", default=None)
    ap.add_argument("--decay", type=float, default=4)
    ap.add_argument("--neutralization", default="STATISTICAL")
    ap.add_argument("--truncation", type=float, default=0.08)
    ap.add_argument("--out", default="results/kor_year_probe.jsonl")
    args = ap.parse_args()

    if not args.expr and not args.dataset:
        ap.error("需要 --dataset 或 --expr")

    client = BrainApiClient()
    await client.ensure_authenticated()

    field = {"id": args.field or "-", "type": "MATRIX", "coverage": None}
    expr = args.expr
    if expr is None:
        field, raw = await pick_field(client, args.dataset, args.field)
        if not field:
            print(json.dumps({
                "dataset": args.dataset, "verdict": "REJECT_NO_FIELDS",
                "error": str(raw)[:300],
            }, ensure_ascii=False))
            return
        expr = build_expr(field["id"], field.get("type"))

    tag = args.tag or args.dataset or "adhoc"
    out = await probe(
        client, args.dataset, field, expr, tag,
        {"decay": args.decay, "neutralization": args.neutralization, "truncation": args.truncation},
    )
    print(json.dumps(out, ensure_ascii=False))

    path = os.path.join(ROOT, args.out)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(out, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    asyncio.run(main())
