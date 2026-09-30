# -*- coding: utf-8 -*-
"""step_funnel.py — 步级漏斗（S2→S6）只读推导，单一事实源（2026-09-17 新增）。

## 为什么有这只工具
`step_quality_metrics` / `step_efficiency_metrics` / `step_gain_metrics` /
`wave_summary` / `campaign_summary` 五张表自建成起**恒为 0 行**。评估结论（见下）是
**不应把各步写进这五张表**，但"每步产出多少、在哪一步掉得最狠"这个真需求确实存在
—— 此前每次审计都靠手写 SQL 临时 JOIN 一次（v2/v3 审计报告里的漏斗分析就是这么来的）。

**2026-09-17 处置：该子系统已整体下线并归档**（5 张表已 DROP；9 个代码/文档文件 +
6 个 MCP 工具 + `step_metrics` workflow 节点均已移除，归档在
`attic/step_metrics_20260917/`，含 README 与复活步骤）。本工具是其替代方案。

本工具把那次手写 SQL 固化成**只读**推导：不建表、不写库、不产生任何新数据，
所有数字都来自既有 4 张表 + ledger，**单一事实源，无重复存储可漂移**。

## 评估结论（为什么不写那五张表）
| 维度 | 实测/事实 |
|---|---|
| 唯一自动采集入口 | `step_metrics_collector.py::collect_from_checkpoint()` **是 TODO 空壳**，恒返回空 dict → 无任何自动数据源 |
| 唯一写入方式 | 人工/Agent 在命令行手传 `--quality-metrics '{"accuracy":0.85}'`（即**调用方自己编数**）|
| 9 个质量指标 | **全部可从既有表实时推导**（本工具即是证明）→ 写进新表 = 重复存储、双真相源 |
| 6 个增益指标 | `avoided_backtests` / `saved_time` / `saved_tokens` / `saved_api_calls` / `reduced_invalid_simulations` / `avoided_submits` 全是**反事实估算，无客观来源** → 写入即制造不可验证数字，与「报数前必须核实」「禁止推测记账」纪律冲突 |
| `token_count` / `api_calls` | MCP 层不回传 → 同样无源 |
| 命名陷阱 | `campaign_summary` 表与**被所有战役提示词引用的** `get_campaign_summary` 工具**同名但无关**（后者读 `wave_results`，见 `reports/db_schema_audit_2026-08-26.md:59`）→ 表一旦有数据会更误导 |

→ 结论：**收益为负**；已下线该子系统，改用本工具提供同一视图。

用法：
    python tools/step_funnel.py --region KOR
    python tools/step_funnel.py --region USA --json
    python tools/step_funnel.py --region KOR --wave 101          # 只看单波
    python tools/step_funnel.py --region KOR --full              # 九步质量效能增益矩阵（方案 B）
    python tools/step_funnel.py --region KOR --full --format json|markdown|html

## 2026-09-30 方案 B：--full = 九步质量效能增益矩阵
默认输出仍是上方漏斗（S2→S6，行为不变）；`--full` 追加**九步**质量/效能/增益指标
与评分（Q/E/G/ROI），推导点在 `src/wqb/step_eval.py`（T1 只读推导 + T2 事件聚合），
评分唯一实现在 `src/wqb/step_scoring.py`。客观事件写入 `step_events` 表
（封闭词表 + source 必填 + 幂等键，见 `src/wqb/step_events.py`），本工具对两者都**只读**。
T3 反事实估算永不入库，报告估算区由渲染层标注——与上方评估结论不冲突：
那五张表死于「手传指标 + 反事实记账 + 双真相源」，本方案用「事件=事实 + 推导=单点」绕开。
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from typing import Any, Dict, List, Optional

import sys as _sys, os as _os
_sys.path.insert(0, str(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'src')))
from wqb.db_conn import connect as db_connect  # 规范工厂（2026-09-20 L1 收口）
from wqb import recon_evidence as _RE  # forum_recon 记录分类的单一实现
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(REPO_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

#: 廉价闸口径（与战役 SOP 一致；非提交层阈值）
CHEAP_SHARPE = 1.58
CHEAP_FITNESS = 1.0


def resolve_db_path() -> str:
    try:
        from wqb.workflow._common import resolve_db_path as _r
        return _r()
    except Exception:
        return os.path.join(REPO_ROOT, "data", "wqb.db")


#: 生成池里"尚未被回测消化"的状态 —— 与 backlog_gate 的 unconsumed 口径一致
_UNCONSUMED = ("gem", "selected", "pending", "gated")


def _table_exists(conn, name: str) -> bool:
    return conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)
    ).fetchone() is not None


def _scalar(conn, sql: str, params=()) -> Any:
    try:
        row = conn.execute(sql, params).fetchone()
        return row[0] if row else None
    except sqlite3.Error:
        return None


def _ledger_count(conn, region: str, key: str) -> Optional[int]:
    """读 ledger 键并尽量数出条目数；键不存在返回 None。"""
    try:
        row = conn.execute(
            "SELECT value FROM ledger_kv WHERE region=? AND key=?", (region, key)
        ).fetchone()
    except sqlite3.Error:
        return None
    if not row:
        return None
    try:
        v = json.loads(row[0])
    except Exception:
        return None
    if isinstance(v, list):
        return len(v)
    if isinstance(v, dict):
        for k in ("items", "alphas", "entries", "ready"):
            if isinstance(v.get(k), list):
                return len(v[k])
        return len(v)
    return None


def build_funnel(conn, region: str, wave: Optional[str] = None) -> Dict[str, Any]:
    """推导 S2→S6 漏斗；缺表/缺键一律记 None（不崩、不猜）。"""
    out: Dict[str, Any] = {"region": region, "wave": wave, "steps": {}}
    wexpr = ""
    wb = ""
    wp: List[Any] = [region]
    if wave:
        wexpr = " AND wave=?"
        wb = " AND wave=?"
        wp = [region, str(wave)]

    # ---- S2 生成池 ----
    s2: Dict[str, Any] = {}
    if _table_exists(conn, "expressions"):
        rows = conn.execute(
            f"SELECT status, COUNT(*) FROM expressions WHERE region=?{wexpr} GROUP BY status",
            wp,
        ).fetchall()
        by_status = {str(k): int(v) for k, v in rows}
        total = sum(by_status.values())
        unconsumed = sum(by_status.get(k, 0) for k in _UNCONSUMED)
        s2 = {
            "total": total,
            "by_status": by_status,
            "unconsumed": unconsumed,
            "unconsumed_ratio": round(unconsumed / total, 4) if total else None,
            "generated_span": _span(conn, "expressions", region, wexpr, wp),
        }
    out["steps"]["S2_generate"] = s2

    # ---- S2→S3 门禁 ----
    # 注意单位：gate_results 一律是 (region, wave, dataset) 粒度 = "一次门禁"，
    # 但 report_json 里两种 schema：① 有 passed/total（表达式级）② pipeline 式无计数。
    # 因此**同时**给"门禁次数"与"表达式级通过数"，避免把批次当表达式混进漏斗。
    s2s3: Dict[str, Any] = {}
    if _table_exists(conn, "gate_results"):
        n = _scalar(conn, f"SELECT COUNT(*) FROM gate_results WHERE region=?{wb}", wp)
        p = _scalar(conn, f"SELECT SUM(all_pass) FROM gate_results WHERE region=?{wb}", wp)
        expr_passed = expr_total = 0
        have_expr_counts = False
        for (rj,) in conn.execute(
            f"SELECT report_json FROM gate_results WHERE region=?{wb} AND report_json IS NOT NULL",
            wp,
        ):
            try:
                d = json.loads(rj)
            except Exception:
                continue
            if isinstance(d, dict) and isinstance(d.get("total"), int) \
                    and isinstance(d.get("passed"), int):
                expr_total += d["total"]
                expr_passed += d["passed"]
                have_expr_counts = True
        s2s3 = {
            "gate_checks": n,
            "gate_passed": int(p) if p is not None else None,
            "gate_pass_rate": round(int(p) / n, 4) if (n and p is not None) else None,
            "expr_total": expr_total if have_expr_counts else None,
            "expr_passed": expr_passed if have_expr_counts else None,
            "expr_pass_rate": (round(expr_passed / expr_total, 4)
                               if have_expr_counts and expr_total else None),
            "span": _span(conn, "gate_results", region, wb, wp),
        }
    out["steps"]["S2_S3_gate"] = s2s3

    # ---- S3 回测 ----
    s3: Dict[str, Any] = {}
    if _table_exists(conn, "backtest_results"):
        n = _scalar(conn, f"SELECT COUNT(*) FROM backtest_results WHERE region=?{wb}", wp)
        st = conn.execute(
            f"SELECT status, COUNT(*) FROM backtest_results WHERE region=?{wb} GROUP BY status",
            wp,
        ).fetchall()
        with_sharpe = _scalar(
            conn,
            f"SELECT COUNT(*) FROM backtest_results WHERE region=?{wb} AND sharpe IS NOT NULL",
            wp,
        )
        cheap = _scalar(
            conn,
            f"SELECT COUNT(*) FROM backtest_results WHERE region=?{wb} "
            f"AND sharpe>{CHEAP_SHARPE} AND fitness>={CHEAP_FITNESS}",
            wp,
        )
        best = _scalar(
            conn, f"SELECT MAX(sharpe) FROM backtest_results WHERE region=?{wb}", wp
        )
        s3 = {
            "rows": n,
            "by_status": {str(k): int(v) for k, v in st},
            "with_sharpe": with_sharpe,
            "cheap_gate_pass": cheap,
            "best_sharpe": round(best, 4) if isinstance(best, (int, float)) else best,
            "span": _span(conn, "backtest_results", region, wb, wp),
        }
    out["steps"]["S3_backtest"] = s3

    # ---- S4→S5 提交就绪（ledger）----
    out["steps"]["S4_S5_submit"] = {
        "submit_ready": _ledger_count(conn, region, "submit_ready"),
        "submit_ready_blocked": _ledger_count(conn, region, "submit_ready_blocked"),
    }

    # ---- S6 复盘 ----
    s6: Dict[str, Any] = {}
    if _table_exists(conn, "wave_results"):
        rows = conn.execute(
            f"SELECT COALESCE(verdict,'(空)'), COUNT(*) FROM wave_results "
            f"WHERE region=?{(' AND wave_number=' + repr(str(wave)) if wave else '')} "
            f"GROUP BY COALESCE(verdict,'(空)')",
            [region],
        ).fetchall()
        s6 = {"verdicts": {str(k): int(v) for k, v in rows}}
    out["steps"]["S6_review"] = s6

    # ---- 论坛 recon 命中率（2026-09-28 P4 闭环；只读推导自 ledger）----
    # 键形态：forum_recon_<qkey>（有货）/ forum_recon_negative_<qkey>（无解）/ forum_recon_error_<qkey>（工具故障）/
    # forum_recon_wave_<wave>（波级取证的完成标记）——分类的单一实现在 wqb.recon_evidence。
    # 命中率 = 有货 /(有货+无解)；**故障与波标记不计入**（旧版按前缀数，故障会被数成「有货」）；
    # 「进批转化」暂不可推导（KB 条目未记录入批去向）——如实标注。
    recon: Dict[str, Any] = {}
    try:
        rows = conn.execute(
            "SELECT key FROM ledger_kv WHERE (region=? OR region='GLOBAL') AND key LIKE 'forum_recon_%'",
            [region],
        ).fetchall()
        counts = _RE.summarize_keys(str(k) for (k,) in rows)
        n_found, n_neg, n_err = counts["found"], counts["negative"], counts["error"]
        total_recon = n_found + n_neg
        recon = {
            "n_recon": total_recon, "n_found": n_found, "n_negative": n_neg, "n_error": n_err,
            "hit_rate": round(n_found / total_recon, 4) if total_recon else None,
            "note": "命中率=有货/(有货+无解)；工具故障（forum_recon_error_*）不计入；进批转化未追踪（KB 条目无入批去向），暂不可推导",
        }
    except sqlite3.Error:
        recon = {}
    out["steps"]["forum_recon"] = recon

    # ---- 转化链 + 瓶颈定位 ----
    # 单位统一：全部用**表达式条数**，避免把"门禁次数"当表达式计数（见上方注释）。
    gate_expr = (s2s3 or {}).get("expr_passed")
    chain = [
        ("S2 生成", (s2 or {}).get("total")),
        ("S2→S3 门禁放行", gate_expr),
        ("S3 回测完成", (s3 or {}).get("with_sharpe")),
        ("S3 过廉价闸", (s3 or {}).get("cheap_gate_pass")),
        ("S4→S5 就绪", (out["steps"]["S4_S5_submit"] or {}).get("submit_ready")),
    ]
    out["chain"] = [{"stage": k, "count": v} for k, v in chain]
    out["chain_note"] = (
        "表达式级" if gate_expr is not None
        else "gate_results 的 report_json 未含表达式级计数（pipeline 式 schema），"
             "该跳为 n/a；请以 gate_checks/gate_passed（批次粒度）参考"
    )

    worst, worst_rate = None, None
    for (prev_name, prev_v), (name, v) in zip(chain, chain[1:]):
        if not prev_v or v is None:
            continue
        rate = v / prev_v
        if worst_rate is None or rate < worst_rate:
            worst, worst_rate = f"{prev_name} → {name}", rate
    out["bottleneck"] = {
        "stage": worst,
        "rate": round(worst_rate, 4) if worst_rate is not None else None,
    }
    return out


def _span(conn, table: str, region: str, wexpr: str, wp) -> Optional[Dict[str, str]]:
    try:
        row = conn.execute(
            f"SELECT MIN(created_at), MAX(created_at) FROM {table} "
            f"WHERE region=?{wexpr} AND created_at IS NOT NULL",
            wp,
        ).fetchone()
    except sqlite3.Error:
        return None
    if not row or not row[0]:
        return None
    return {"first": str(row[0]), "last": str(row[1])}


def _fmt(v: Any) -> str:
    if v is None:
        return "n/a"
    if isinstance(v, float):
        return f"{v:.4f}"
    return str(v)


def render(res: Dict[str, Any]) -> str:
    L: List[str] = []
    scope = f"{res['region']}" + (f" / wave={res['wave']}" if res.get("wave") else " / 全区")
    L.append("=" * 74)
    L.append(f"步级漏斗（S2→S6）· {scope}   —— 只读推导，数据源=既有表+ledger")
    L.append("=" * 74)

    s2 = res["steps"].get("S2_generate") or {}
    L.append("\n[S2 生成池] expressions")
    if not s2:
        L.append("  n/a（无 expressions 表或无数据）")
    else:
        L.append(f"  总表达式 = {s2.get('total')}")
        L.append(f"  未消化(unconsumed = gem+selected+pending+gated) = "
                 f"{s2.get('unconsumed')}  ({_fmt(s2.get('unconsumed_ratio'))})")
        L.append("  按状态：" + ", ".join(f"{k}={v}" for k, v in
                                          sorted((s2.get("by_status") or {}).items())))
        sp = s2.get("generated_span")
        if sp:
            L.append(f"  时间窗：{sp['first']} → {sp['last']}")

    s23 = res["steps"].get("S2_S3_gate") or {}
    L.append("\n[S2→S3 门禁] gate_results")
    if not s23:
        L.append("  n/a")
    else:
        L.append(f"  门禁次数(批次粒度) = {_fmt(s23.get('gate_checks'))}，"
                 f"通过 = {_fmt(s23.get('gate_passed'))}，"
                 f"通过率 = {_fmt(s23.get('gate_pass_rate'))}")
        if s23.get("expr_total") is not None:
            L.append(f"  表达式级：放行 {s23.get('expr_passed')}/{s23.get('expr_total')}"
                     f"  (通过率 {_fmt(s23.get('expr_pass_rate'))})")
        else:
            L.append("  表达式级计数：n/a（该区 gate_results 是 pipeline 式 schema，"
                     "无 passed/total）")
        if s23.get("span"):
            L.append(f"  时间窗：{s23['span']['first']} → {s23['span']['last']}")

    s3 = res["steps"].get("S3_backtest") or {}
    L.append("\n[S3 回测] backtest_results")
    if not s3:
        L.append("  n/a")
    else:
        L.append(f"  回测行 = {s3.get('rows')}，其中有 sharpe = {s3.get('with_sharpe')}")
        L.append(f"  过廉价闸(S>{CHEAP_SHARPE} & F>={CHEAP_FITNESS}) = {s3.get('cheap_gate_pass')}"
                 f"，最佳 sharpe = {_fmt(s3.get('best_sharpe'))}")
        L.append("  按状态：" + ", ".join(f"{k}={v}" for k, v in
                                          sorted((s3.get("by_status") or {}).items())))
        if s3.get("span"):
            L.append(f"  时间窗：{s3['span']['first']} → {s3['span']['last']}")

    s45 = res["steps"].get("S4_S5_submit") or {}
    L.append("\n[S4→S5 提交就绪] ledger")
    L.append(f"  submit_ready = {_fmt(s45.get('submit_ready'))}，"
             f"submit_ready_blocked = {_fmt(s45.get('submit_ready_blocked'))}")

    s6 = res["steps"].get("S6_review") or {}
    L.append("\n[S6 复盘] wave_results.verdict")
    L.append("  " + (", ".join(f"{k}={v}" for k, v in sorted((s6.get("verdicts") or {}).items()))
                     or "n/a"))

    fr = res["steps"].get("forum_recon") or {}
    if fr.get("n_recon") or fr.get("n_error"):
        L.append("\n[论坛 recon 命中率] ledger forum_recon_* / forum_recon_negative_* / forum_recon_error_*")
        L.append(f"  检索 {fr.get('n_recon', 0)} 次：有货 {fr.get('n_found', 0)} / 无解 {fr.get('n_negative', 0)}，"
                 f"命中率 = {_fmt(fr.get('hit_rate'))}；工具故障 {fr.get('n_error', 0)} 次（不计入）")
        L.append(f"  {fr.get('note', '')}")

    L.append(f"\n[漏斗转化链]  口径：{res.get('chain_note')}")
    for item in res.get("chain") or []:
        L.append(f"  {item['stage']:<16} {_fmt(item['count'])}")
    bn = res.get("bottleneck") or {}
    if bn.get("stage"):
        L.append(f"\n[瓶颈定位] 掉得最狠的一跳 = {bn['stage']}"
                 f"（保留率 {_fmt(bn['rate'])}）")
    # ⚠ 诚实标注口径局限：各步统计的是**各自表里的存量**，时间窗不完全一致，
    #   因此链上数值**不必单调递减**（例：IND 回测数 267 > 门禁放行 124，
    #   因为回测表跨更多波次累积）。别把它当严格嵌套漏斗读。
    L.append("\n[口径局限] 各步取的是各自表的存量，时间窗不一 → 链上数值可能不单调；"
             "仅用于定位'哪一跳掉得最狠'，不作精确转化率引用。")
    L.append("")
    return "\n".join(L)


def render_full(res: Dict[str, Any]) -> str:
    """九步质量效能增益矩阵 → markdown（供 --full --format markdown / 报告渲染复用）。"""
    L: List[str] = []
    scope = f"{res['region']}" + (f" / wave={res['wave']}" if res.get("wave") else " / 全区")
    L.append("=" * 74)
    L.append(f"九步质量效能增益矩阵 · {scope}   —— T1 只读推导 + T2 事件，评分=step_scoring 单点")
    L.append("=" * 74)

    for step_name, dims in (res.get("steps") or {}).items():
        L.append(f"\n[{step_name}]")
        for dim, label in (("quality", "质量"), ("efficiency", "效能"), ("gain", "增益")):
            metrics = dims.get(dim) or []
            if not metrics:
                continue
            for m in metrics:
                v = m.get("value")
                vs = "n/a" if v is None else (f"{v:.4f}" if isinstance(v, float) else str(v))
                flag = "*" if m.get("score_eligible") else " "
                note = f"  [{m['note']}]" if m.get("note") else ""
                L.append(f"  {label} {m['name']:<28} = {vs:<10} {m.get('unit', '')}"
                         f"  ({m.get('tier')}, src={m.get('source', '')[:40]}){flag}{note}")

    sc = res.get("scores") or {}
    L.append("\n[评分]  (* = 参与评分的好方向比率；原始量/计数只展示不评分)")
    for k, label in (("quality", "质量分 Q"), ("efficiency", "效能分 E"),
                     ("gain", "增益分 G"), ("roi", "ROI=达标/配额"),
                     ("unit_cost", "单位成本=配额/达标")):
        v = sc.get(k)
        L.append(f"  {label:<20} = " + ("n/a" if v is None else f"{v:.4f}"))
    L.append("\n[口径]  比率∈[0,1] 或 n/a（0 分母→n/a，禁除零）；T3 反事实估算不入库。")
    L.append("")
    return "\n".join(L)


def render_full_html(res: Dict[str, Any]) -> str:
    """九步矩阵 → html（极简表格，与 render_full 同数据）。"""
    esc = lambda s: (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    scope = f"{res['region']}" + (f" / wave={res['wave']}" if res.get("wave") else " / 全区")
    H = ["<html><head><meta charset='utf-8'><title>九步质量效能增益矩阵</title></head><body>",
         f"<h1>九步质量效能增益矩阵 · {esc(scope)}</h1>"]
    H.append("<table border='1'><tr><th>步</th><th>维度</th><th>指标</th><th>值</th>"
             "<th>单位</th><th>级别</th><th>来源</th><th>评分</th></tr>")
    for step_name, dims in (res.get("steps") or {}).items():
        for dim, label in (("quality", "质量"), ("efficiency", "效能"), ("gain", "增益")):
            for m in dims.get(dim) or []:
                v = m.get("value")
                vs = "n/a" if v is None else (f"{v:.4f}" if isinstance(v, float) else str(v))
                H.append(f"<tr><td>{esc(step_name)}</td><td>{label}</td><td>{esc(m['name'])}</td>"
                         f"<td>{vs}</td><td>{esc(m.get('unit', ''))}</td><td>{esc(m.get('tier'))}</td>"
                         f"<td>{esc(m.get('source', ''))}</td><td>{'Y' if m.get('score_eligible') else '-'}</td></tr>")
    H.append("</table>")
    sc = res.get("scores") or {}
    H.append("<h2>评分</h2><ul>")
    for k in ("quality", "efficiency", "gain", "roi", "unit_cost"):
        v = sc.get(k)
        H.append(f"<li>{esc(k)} = {'n/a' if v is None else f'{v:.4f}'}</li>")
    H.append("</ul><p>口径：比率∈[0,1] 或 n/a（0 分母→n/a）；T3 反事实估算不入库。</p>")
    H.append("</body></html>")
    return "\n".join(H)


def main() -> int:
    ap = argparse.ArgumentParser(description="步级漏斗（S2→S6）只读推导")
    ap.add_argument("--region", required=True)
    ap.add_argument("--wave", default=None, help="只统计指定波（可选）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--full", action="store_true",
                    help="九步质量效能增益矩阵（方案 B；T1 推导 + T2 事件）")
    ap.add_argument("--format", default="markdown", choices=["json", "markdown", "html"],
                    help="--full 输出格式（默认 markdown）")
    a = ap.parse_args()

    db = resolve_db_path()
    if not os.path.isfile(db):
        print(f"[step-funnel] 找不到 DB：{db}", file=sys.stderr)
        return 2

    # 只读连接：本工具契约是「跑完 DB 字节不变」（test_run_does_not_modify_db），
    # 故经工厂的 readonly=True 打开（跳过会改库头的 PRAGMA journal_mode=WAL）。
    conn = db_connect(db, readonly=True)
    try:
        if a.full:
            from wqb.step_eval import build_step_eval
            res_full = build_step_eval(conn, a.region.upper(), a.wave)
            if a.format == "json":
                print(json.dumps(res_full, ensure_ascii=False, indent=2))
            elif a.format == "html":
                print(render_full_html(res_full))
            else:
                print(render_full(res_full))
            return 0
        res = build_funnel(conn, a.region.upper(), a.wave)
    finally:
        conn.close()

    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(render(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
