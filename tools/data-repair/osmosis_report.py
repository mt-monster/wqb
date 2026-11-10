#!/usr/bin/env python
"""Osmosis 归因报告（只读 wqb.db，输出 markdown）。

## 定位

把三处快照拼成「能回答为什么掉」的视图：
- `osmosis_rank_history`  账户级日序列（rank / VF / WF / prod / self / subs / fields）
- `osmosis_alloc_history` 每颗的点数与 scope（vintage 序列）
- `osmosis_scope_snapshot` 每 scope 的聚合代理（颗数 / 点数 / 集中度 / 加权 IS）

## 能回答 / 不能回答（2026-11-10 平台实测边界）

能：rank 是否真的在掉（平滑后）、掉的时候是哪个 scope 的点数或质量变了、
分配改了什么（新增/剔除/加减点）、VF/WF 有没有同步恶化。

不能：per-scope 的**真实**日 PnL 与排名。平台既无 per-scope rank 端点，也无
per-alpha OS 日 PnL（recordsets/pnl 只到 IS 期末 2023-12-29）。所以 scope 质量
只能用 `wavg_is_sharpe` 代理，不等于 combo 表现。

## 用法

  python tools/data-repair/osmosis_report.py
  python tools/data-repair/osmosis_report.py --md output_report/osmosis_report.md
  python tools/data-repair/osmosis_report.py --days 60
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import date, datetime, timedelta

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, _ROOT)
sys.path.insert(0, os.path.join(_ROOT, "src"))

DB = os.path.join(_ROOT, "data", "wqb.db")
EXPECTED_SCOPE_TOTAL = 100_000
MIN_SCOPE_ALPHAS = 10
MIN_RANK_SAMPLES = 8          # 少于这个数不给趋势判断（σ≈0.15，单日不可用）


def _fmt(v, nd=4, dash="—"):
    if v is None:
        return dash
    if isinstance(v, float):
        return f"{v:.{nd}f}"
    return str(v)


def _delta(a, b, nd=4):
    if a is None or b is None:
        return "—"
    d = a - b
    return f"{d:+.{nd}f}"


def load_rank(con, days: int) -> list[dict]:
    since = (date.today() - timedelta(days=days)).isoformat()
    rows = con.execute(
        "SELECT sample_date, daily_osmosis_rank, value_factor, weight_factor, "
        "mean_prod_correlation, mean_self_correlation, submissions_count, "
        "data_fields_used, effective_from, lock_sunday, est_date, genius_level, sampled_at "
        "FROM osmosis_rank_history WHERE sample_date >= ? ORDER BY sample_date",
        (since,),
    ).fetchall()
    return [dict(r) for r in rows]


def ma(vals: list, window: int):
    """按行序的简单移动平均；样本不足返回 None。"""
    seq = [v for v in vals if v is not None]
    if len(seq) < window:
        return None
    return sum(seq[-window:]) / window


def snapshot_dates(con, table: str) -> list[str]:
    try:
        return [r[0] for r in con.execute(
            f"SELECT DISTINCT snapshot_date FROM {table} ORDER BY snapshot_date")]
    except Exception:
        return []


def load_scopes(con, day: str) -> list[dict]:
    rows = con.execute(
        "SELECT * FROM osmosis_scope_snapshot WHERE snapshot_date=? ORDER BY scope", (day,)
    ).fetchall()
    return [dict(r) for r in rows]


def load_alloc(con, day: str) -> dict[str, dict]:
    rows = con.execute(
        "SELECT * FROM osmosis_alloc_history WHERE snapshot_date=?", (day,)
    ).fetchall()
    return {r["alpha_id"]: dict(r) for r in rows}


def build_report(con, days: int) -> str:
    L: list[str] = []
    add = L.append

    rank_rows = load_rank(con, days)
    alloc_days = snapshot_dates(con, "osmosis_alloc_history")
    latest_alloc = alloc_days[-1] if alloc_days else None
    prev_alloc = alloc_days[-2] if len(alloc_days) >= 2 else None

    add(f"# Osmosis 归因报告 — {date.today().isoformat()}")
    add("")
    add(f"- 账户日样本：{len(rank_rows)} 条（窗口 {days} 天）")
    add(f"- 分配快照：{len(alloc_days)} 个日期"
        + (f"，最新 {latest_alloc}" if latest_alloc else "（尚未采集）"))
    add("")

    # ---------- 1. 账户指标 ----------
    add("## 1. 账户指标")
    add("")
    if not rank_rows:
        add("_无数据，先跑 `osmosis_rank_snapshot.py`。_")
    else:
        ranks = [r["daily_osmosis_rank"] for r in rank_rows]
        last = rank_rows[-1]
        ma5 = ma(ranks, 5)
        ma20 = ma(ranks, 20)
        ref7 = next((r for r in reversed(rank_rows)
                     if r["sample_date"] <= (date.today() - timedelta(days=7)).isoformat()),
                    None)
        add("| 指标 | 最新 | 7 天前 | Δ | 判读 |")
        add("|---|---|---|---|---|")
        add(f"| dailyOsmosisRank | {_fmt(last['daily_osmosis_rank'], 3)} | "
            f"{_fmt(ref7['daily_osmosis_rank'], 3) if ref7 else '—'} | "
            f"{_delta(last['daily_osmosis_rank'], ref7['daily_osmosis_rank'] if ref7 else None, 3)} | "
            f"MA5={_fmt(ma5, 3)} MA20={_fmt(ma20, 3)} |")
        add(f"| valueFactor | {_fmt(last['value_factor'], 3)} | "
            f"{_fmt(ref7['value_factor'], 3) if ref7 else '—'} | "
            f"{_delta(last['value_factor'], ref7['value_factor'] if ref7 else None, 3)} | "
            f"每日 base 的核心乘数 |")
        add(f"| weightFactor | {_fmt(last['weight_factor'], 3)} | "
            f"{_fmt(ref7['weight_factor'], 3) if ref7 else '—'} | "
            f"{_delta(last['weight_factor'], ref7['weight_factor'] if ref7 else None, 3)} | "
            f"季度奖 = WF × OS |")
        add(f"| meanProdCorrelation | {_fmt(last['mean_prod_correlation'], 4)} | "
            f"{_fmt(ref7['mean_prod_correlation'], 4) if ref7 else '—'} | "
            f"{_delta(last['mean_prod_correlation'], ref7['mean_prod_correlation'] if ref7 else None)} | "
            f"逼近 0.7 是全池问题 |")
        add(f"| submissionsCount | {_fmt(last['submissions_count'])} | "
            f"{_fmt(ref7['submissions_count']) if ref7 else '—'} | "
            f"{_delta(last['submissions_count'], ref7['submissions_count'] if ref7 else None, 0)} | "
            f"只涨不跌 |")
        add(f"| dataFieldsUsed | {_fmt(last['data_fields_used'])} | "
            f"{_fmt(ref7['data_fields_used']) if ref7 else '—'} | "
            f"{_delta(last['data_fields_used'], ref7['data_fields_used'] if ref7 else None, 0)} | "
            f"多样性 |")
        add("")
        add(f"- 采样时纽约日（est_date）：{_fmt(last.get('est_date'))}｜"
            f"genius_level：{_fmt(last.get('genius_level'))}｜"
            f"lock={_fmt(last.get('lock_sunday'))} → 生效 {_fmt(last.get('effective_from'))}")
        add("")

    # ---------- 2. scope 明细 ----------
    add("## 2. Scope 明细（最新分配快照）")
    add("")
    if not latest_alloc:
        add("_无分配快照，先跑 `osmosis_alloc_snapshot.py`。_")
    else:
        scopes = load_scopes(con, latest_alloc)
        prev_scopes = {s["scope"]: s for s in load_scopes(con, prev_alloc)} if prev_alloc else {}
        add(f"快照日 `{latest_alloc}`" + (f"，对比 `{prev_alloc}`" if prev_alloc else "（首次，无对比）"))
        add("")
        add("| Scope | 颗数 | 点数 | Δ点数 | 最大单颗占比 | HHI | 加权 IS Sharpe | 加权 prod |")
        add("|---|---:|---:|---:|---:|---:|---:|---:|")
        for s in scopes:
            p = prev_scopes.get(s["scope"])
            add(f"| {s['scope']} | {s['n_alphas']} | {s['total_points']} | "
                f"{_delta(s['total_points'], p['total_points'] if p else None, 0)} | "
                f"{_fmt(s['top1_share'], 3)} | {_fmt(s['hhi'], 3)} | "
                f"{_fmt(s['wavg_is_sharpe'], 3)} | {_fmt(s['wavg_prod'], 3)} |")
        add("")
        add("> `加权 IS Sharpe` / `加权 prod` 是点数加权**代理**，不是 combo 实际表现："
            "平台无 per-scope rank，也无 per-alpha OS 日 PnL（recordsets/pnl 只到 IS 期末）。")
        add("")

    # ---------- 3. 分配变动 ----------
    add("## 3. 分配变动")
    add("")
    if not latest_alloc or not prev_alloc:
        add("_需要 ≥2 个分配快照才能算变动（下次跑 `osmosis_alloc_snapshot.py` 后自动出现）。_")
        add("")
    else:
        cur = load_alloc(con, latest_alloc)
        old = load_alloc(con, prev_alloc)
        added = sorted(set(cur) - set(old))
        removed = sorted(set(old) - set(cur))
        moves = sorted(((aid, cur[aid]["points"] - old[aid]["points"])
                        for aid in set(cur) & set(old)
                        if cur[aid]["points"] != old[aid]["points"]),
                       key=lambda x: -abs(x[1]))
        add(f"- 新增 {len(added)} 颗：{', '.join(added[:10]) or '—'}")
        add(f"- 剔除 {len(removed)} 颗：{', '.join(removed[:10]) or '—'}")
        add(f"- 改点 {len(moves)} 颗" + ("：" if moves else ""))
        for aid, d in moves[:10]:
            scope = cur[aid]["scope"]
            add(f"  - `{aid}` ({scope}) {old[aid]['points']} → {cur[aid]['points']} ({d:+d})")
        add("")

    # ---------- 4. 告警 ----------
    add("## 4. 告警")
    add("")
    alerts: list[str] = []
    if latest_alloc:
        for s in load_scopes(con, latest_alloc):
            if s["total_points"] != EXPECTED_SCOPE_TOTAL:
                alerts.append(f"`{s['scope']}` 点数和 {s['total_points']} ≠ {EXPECTED_SCOPE_TOTAL}")
            if s["n_alphas"] < MIN_SCOPE_ALPHAS:
                alerts.append(f"`{s['scope']}` 只有 {s['n_alphas']} 颗（平台要求 ≥{MIN_SCOPE_ALPHAS}）")
        try:
            age = (date.today() - date.fromisoformat(latest_alloc)).days
            if age > 10:
                alerts.append(f"分配快照已 {age} 天未更新（周一/周日锁点后应重跑）")
        except ValueError:
            pass
    if len(rank_rows) < MIN_RANK_SAMPLES:
        alerts.append(f"rank 仅 {len(rank_rows)} 个样本（<{MIN_RANK_SAMPLES}）："
                      "单日 rank 是横截面排名，σ≈0.15，样本不足不得据此判优劣")
    if rank_rows:
        last = rank_rows[-1]
        wf_hist = [r["weight_factor"] for r in rank_rows if r["weight_factor"] is not None]
        if last["weight_factor"] == 0 and any(w > 0 for w in wf_hist):
            alerts.append("weightFactor 已归零（历史有非零值）⇒ 季度奖 = WF × OS 归零")
        if last["value_factor"] is not None and last["value_factor"] < 0.45:
            alerts.append(f"valueFactor={last['value_factor']}（<0.45，base 核心乘数走低）")
    if not alerts:
        alerts.append("无。")
    for a in alerts:
        add(f"- {a}")
    add("")

    # ---------- 5. 判读须知 ----------
    add("## 5. 判读须知")
    add("")
    add("- `dailyOsmosisRank` = 各**已分配** scope「当日 PnL 横截面排名」的算术平均；"
        "只作 base payment 的 quality multiplier（1–2×），不含绝对收益。")
    add("- 用的是**锁后第 8 天起生效一周**的那版分配 ⇒ 任何配置改动的效果"
        "至少 2 周后才出现在 rank 上，最小可评估窗口 5–8 周。")
    add("- 单日噪声大（实测 0.82→0.97 一天 +0.15）⇒ 只看 MA5/MA20 与同窗口对照，不看单日。")
    add("")
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description="Osmosis 归因报告（只读）")
    ap.add_argument("--days", type=int, default=90, help="账户序列窗口（默认 90 天）")
    ap.add_argument("--md", help="把 markdown 写到该路径")
    args = ap.parse_args()

    from wqb.db_conn import connect

    con = connect(DB, readonly=True, row_factory=_row_factory())
    try:
        text = build_report(con, args.days)
    finally:
        con.close()

    print(text)
    if args.md:
        os.makedirs(os.path.dirname(os.path.abspath(args.md)) or ".", exist_ok=True)
        with open(args.md, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"\n[ok] 已写 {args.md}")
    return 0


def _row_factory():
    import sqlite3
    return sqlite3.Row


if __name__ == "__main__":
    raise SystemExit(main())
