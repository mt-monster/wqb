# -*- coding: utf-8 -*-
"""os_report.py — 已提交 alpha 的 OS（样本外）表现报表。

数据来源（2026-09-19 实测确认）：
  - **列表** `GET /users/self/alphas?stage=OS` 只带 `os.osISSharpeRatio` / `os.fitness`
    （`sharpe250/sharpe500/preCloseSharpe` 恒 null）。
  - **详情** `GET /alphas/{id}` 的 `os` 块才是全量：
    `{sharpe, sharpe60, sharpe125, sharpe250, sharpe500, returns, drawdown, margin,
      fitness, turnover, osISSharpeRatio, startDate}`。
    校验：`osISSharpeRatio × IS.sharpe ≈ os.sharpe`（三例误差 <0.01）。
  → 故本工具：列表拿全集 → 逐条详情取 OS 指标（本地缓存 + 断点续跑）。

用法（需 MCP venv 的 Python）：
  world-quant-brain-mcp/.venv/Scripts/python.exe tools/os_report.py
  ... --status active          # 只看 ACTIVE（默认 all）
  ... --refresh                # 忽略缓存重取
产出：`output_report/os_report_<YYYYMMDD>.md` + `logs/os_metrics.csv`
"""
import argparse
import asyncio
import csv
import json
import os
import sys
from datetime import datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MCP_DIR = os.path.join(REPO, "world-quant-brain-mcp")
sys.path.insert(0, MCP_DIR)
CACHE = os.path.join(REPO, "logs", "_os_metrics_cache.json")

#: 低门槛区（cluster 等区域差异用得到）
LOW_BAR = {"KOR", "JPS", "TWN", "HKG", "IND", "GBR", "DEU"}


async def fetch_all(refresh=False):
    from brain_api import brain_client
    await brain_client.ensure_authenticated()

    cache = {}
    if not refresh and os.path.isfile(CACHE):
        try:
            with open(CACHE, encoding="utf-8") as f:
                cache = json.load(f)
        except Exception:
            cache = {}

    # 1) 列表（分页）
    listing, off, count = [], 0, None
    while True:
        r = await brain_client.get_user_alphas(stage="OS", limit=100, offset=off)
        res = (r or {}).get("results") or []
        if count is None:
            count = (r or {}).get("count")
        listing.extend(res)
        off += len(res)
        if not res or (count and len(listing) >= count) or len(res) < 100:
            break
    print(f"OS 期 alpha 列表：{len(listing)}（平台计数 {count}）")

    # 2) 详情逐条取（缓存命中的跳过）
    rows = []
    for i, a in enumerate(listing, 1):
        aid = a["id"]
        if aid in cache:
            rows.append(cache[aid])
            continue
        try:
            d = await brain_client.get_alpha_details(aid) or {}
        except Exception as e:
            print(f"  [{i}] {aid} 取详情失败 {type(e).__name__}")
            continue
        o = d.get("os") or {}
        isd = d.get("is") or {}
        st = d.get("settings") or {}
        cls = [c.get("id") for c in (d.get("classifications") or []) if isinstance(c, dict)]
        row = {
            "alpha_id": aid,
            "status": d.get("status"),
            "region": st.get("region"),
            "delay": st.get("delay"),
            "universe": st.get("universe"),
            "neutralization": st.get("neutralization"),
            "decay": st.get("decay"),
            "date_submitted": d.get("dateSubmitted"),
            "is_sharpe": isd.get("sharpe"), "is_fitness": isd.get("fitness"),
            "is_returns": isd.get("returns"), "is_turnover": isd.get("turnover"),
            "os_start": o.get("startDate"),
            "os_sharpe": o.get("sharpe"), "os_fitness": o.get("fitness"),
            "os_returns": o.get("returns"), "os_drawdown": o.get("drawdown"),
            "os_margin": o.get("margin"), "os_turnover": o.get("turnover"),
            "os_sharpe60": o.get("sharpe60"), "os_sharpe125": o.get("sharpe125"),
            "os_sharpe250": o.get("sharpe250"), "os_sharpe500": o.get("sharpe500"),
            "os_is_ratio": o.get("osISSharpeRatio"),
            "classifications": cls,
            "is_cluster": "CLUSTER:CLUSTER" in cls,
            "is_power_pool": any(str(c).startswith("POWER_POOL") for c in cls),
            "tags": d.get("tags") or [],
        }
        rows.append(row)
        cache[aid] = row
        if i % 20 == 0:
            with open(CACHE, "w", encoding="utf-8") as f:
                json.dump(cache, f, ensure_ascii=False)
            print(f"  进度 {i}/{len(listing)}")
        await asyncio.sleep(0.12)

    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False)
    return rows


def _fmt(v, nd=3):
    if v is None:
        return "—"
    if isinstance(v, float):
        return f"{v:.{nd}f}"
    return str(v)


def build_report(rows, status_filter):
    sel = [r for r in rows if status_filter == "all" or (r["status"] or "").lower() == status_filter]
    act = [r for r in sel if (r["status"] or "").upper() == "ACTIVE"]
    neg = sorted([r for r in act if (r["os_sharpe"] or 0) < 0], key=lambda r: r["os_sharpe"])
    weak60 = sorted([r for r in act if r["os_sharpe60"] is not None],
                    key=lambda r: r["os_sharpe60"])[:20]
    ratio = [r["os_is_ratio"] for r in act if r["os_is_ratio"] is not None]
    osh = [r["os_sharpe"] for r in act if r["os_sharpe"] is not None]
    import statistics as S

    L = []
    L.append(f"# 已提交 alpha 的 OS（样本外）表现报表")
    L.append("")
    L.append(f"生成时间：{datetime.now():%Y-%m-%d %H:%M}｜数据源：`GET /users/self/alphas?stage=OS` + 逐条 `GET /alphas/{{id}}` 的 `os` 块")
    L.append(f"（列表端点只带 `osISSharpeRatio`，OS 全量指标只在详情端点 —— 已校验 `osISSharpeRatio × IS.sharpe = os.sharpe`，误差 <0.01）")
    L.append("")
    L.append(f"## 0. 总览（OS 期 = 平台样本外窗口，startDate 多为 2023-01-21 / 2024-01-01）")
    L.append("")
    L.append(f"| 项 | 数量 |")
    L.append(f"|---|---|")
    L.append(f"| OS 期 alpha（本报表范围）| {len(sel)} |")
    L.append(f"| 其中 **ACTIVE**（在实盘书里）| {len(act)} |")
    L.append(f"| 其中 DECOMMISSIONED（已退出）| {len([r for r in sel if (r['status'] or '').upper()=='DECOMMISSIONED'])} |")
    L.append(f"| **ACTIVE 且 OS Sharpe < 0** | **{len(neg)}** |")
    if osh:
        L.append(f"| ACTIVE 的 OS Sharpe 均值 / 中位 | {S.mean(osh):.3f} / {S.median(osh):.3f} |")
    if ratio:
        L.append(f"| ACTIVE 的 OS/IS Sharpe 比 均值 / 中位 | {S.mean(ratio):.3f} / {S.median(ratio):.3f} |")
    L.append("")
    # 区域分布
    import collections
    L.append("## 1. ACTIVE 按区域")
    L.append("")
    L.append("| 区域 | 数量 | OS Sharpe 均值 | OS<0 数 |")
    L.append("|---|---|---|---|")
    by_reg = collections.defaultdict(list)
    for r in act:
        by_reg[r["region"] or "?"].append(r)
    for reg, rs in sorted(by_reg.items(), key=lambda kv: -len(kv[1])):
        vals = [x["os_sharpe"] for x in rs if x["os_sharpe"] is not None]
        n2 = len([x for x in rs if (x["os_sharpe"] or 0) < 0])
        L.append(f"| {reg} | {len(rs)} | {(S.mean(vals) if vals else float('nan')):.3f} | {n2} |")
    L.append("")
    L.append(f"## 2. ACTIVE 且 OS Sharpe < 0（共 {len(neg)} 颗）—— 首要处置对象")
    L.append("")
    L.append("> 依据本仓既有杠杆排序：**退役负 OS alpha > 降 meanProdCorr > 跨区分散 > 提数量**。")
    L.append("> ⚠ 研究 API **无法退役**（PATCH status 静默忽略）——只能控制台操作或用标签标记。")
    L.append("")
    L.append("| alpha_id | 区域 | OS Sharpe | OS 近60日 | OS 近125日 | IS Sharpe | OS/IS 比 | OS 收益 | OS 回撤 | 提交日 | 标签 |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in neg:
        L.append(f"| `{r['alpha_id']}` | {r['region']} | **{_fmt(r['os_sharpe'])}** | {_fmt(r['os_sharpe60'],2)} | "
                 f"{_fmt(r['os_sharpe125'],2)} | {_fmt(r['is_sharpe'],2)} | {_fmt(r['os_is_ratio'],2)} | "
                 f"{_fmt(r['os_returns'],4)} | {_fmt(r['os_drawdown'],4)} | {(r['date_submitted'] or '')[:10]} | "
                 f"{','.join(r['tags'][:2]) or '—'} |")
    L.append("")
    L.append("## 3. 近 60 日 OS Sharpe 最差（含正值恶化者）")
    L.append("")
    L.append("| alpha_id | 区域 | OS 近60日 | OS 近125日 | OS Sharpe | IS Sharpe |")
    L.append("|---|---|---|---|---|---|")
    for r in weak60:
        L.append(f"| `{r['alpha_id']}` | {r['region']} | **{_fmt(r['os_sharpe60'],2)}** | {_fmt(r['os_sharpe125'],2)} | "
                 f"{_fmt(r['os_sharpe'],2)} | {_fmt(r['is_sharpe'],2)} |")
    L.append("")
    # cluster / power pool 交叉
    cl = [r for r in act if r["is_cluster"]]
    pp = [r for r in act if r["is_power_pool"]]
    L.append("## 4. 分类交叉（ACTIVE）")
    L.append("")
    L.append(f"- **Cluster Alpha**：{len(cl)} 颗；其中 OS<0 的 {len([r for r in cl if (r['os_sharpe'] or 0)<0])} 颗")
    L.append(f"- **Power Pool eligible**：{len(pp)} 颗")
    L.append("")
    L.append("## 5. ACTIVE 全量明细（按 OS Sharpe 升序）")
    L.append("")
    L.append("| alpha_id | 区域 | 状态 | OS Sharpe | 60日 | IS Sharpe | OS/IS | OS 收益 | OS 回撤 | 换手 | 中性化 | Cluster |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in sorted(act, key=lambda x: (x["os_sharpe"] is None, x["os_sharpe"] if x["os_sharpe"] is not None else 0)):
        L.append(f"| `{r['alpha_id']}` | {r['region']} | {r['status']} | {_fmt(r['os_sharpe'])} | "
                 f"{_fmt(r['os_sharpe60'],2)} | {_fmt(r['is_sharpe'],2)} | {_fmt(r['os_is_ratio'],2)} | "
                 f"{_fmt(r['os_returns'],4)} | {_fmt(r['os_drawdown'],4)} | {_fmt(r['os_turnover'],3)} | "
                 f"{r['neutralization'] or '—'} | {'✓' if r['is_cluster'] else ''} |")
    return "\n".join(L)


async def main():
    ap = argparse.ArgumentParser(description="已提交 alpha 的 OS 表现报表")
    ap.add_argument("--status", default="all", choices=("all", "active", "decommissioned"))
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--out-md", default=None)
    ap.add_argument("--out-csv", default=os.path.join(REPO, "logs", "os_metrics.csv"))
    a = ap.parse_args()

    rows = await fetch_all(refresh=a.refresh)
    md = build_report(rows, a.status)
    out_md = a.out_md or os.path.join(REPO, "output_report", f"os_report_{datetime.now():%Y%m%d}.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(md + "\n")
    cols = [k for k in rows[0].keys() if k != "classifications"]
    with open(a.out_csv, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    act = [r for r in rows if (r["status"] or "").upper() == "ACTIVE"]
    neg = [r for r in act if (r["os_sharpe"] or 0) < 0]
    print(f"\nOS 期 {len(rows)} 颗｜ACTIVE {len(act)}｜**ACTIVE 且 OS<0 = {len(neg)}**")
    print(f"报表 → {out_md}\n明细 → {a.out_csv}")


asyncio.run(main())
