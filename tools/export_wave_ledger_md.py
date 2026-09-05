# -*- coding: utf-8 -*-
"""export_wave_ledger_md.py - 从数据库生成 WAVE_LEDGER.md 快照（单轨 DB 模式）。

数据源：wave_results 表（full_payload 列存完整 wave JSON）。
输出：tracking/<REGION>/WAVE_LEDGER.md（人工可读快照，覆盖写）。

用法：
  python tools/export_wave_ledger_md.py --region MEA
  python tools/export_wave_ledger_md.py --region USA --out tracking/USA/WAVE_LEDGER.md
"""
import argparse
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "wqb.db"


def fetch_waves(region):
    """从 wave_results 表拉取某区域全部 wave（按 wave_number 排序）。"""
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(
        "SELECT * FROM wave_results WHERE region=? "
        "ORDER BY CAST(wave_number AS INTEGER)",
        (region,),
    )
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def render_wave_section(w):
    """渲染单个 wave 的 Markdown 节。"""
    wn = w["wave_number"]
    focus = w.get("focus") or f"Wave {wn}"
    context = w.get("context") or ""
    verdict = w.get("verdict") or ""
    status = w.get("status") or "open"

    # full_payload 优先（完整 JSON），否则用摘要列
    if w.get("full_payload"):
        try:
            payload = json.loads(w["full_payload"])
        except Exception:
            payload = {}
    else:
        payload = {}

    key_findings = payload.get("key_findings") or json.loads(w.get("key_findings") or "[]")
    candidates = payload.get("candidates") or json.loads(w.get("candidates") or "[]")
    batches = payload.get("batches") or json.loads(w.get("batches") or "[]")

    lines = []
    lines.append(f"## 波{wn}（{status}）— {focus}")
    if context:
        lines.append(f"\n**背景**：{context}")
    lines.append("")

    # 批次表
    if batches:
        lines.append("### 批次")
        lines.append("| 批 | multisim id | 配置摘要 |")
        lines.append("|---|---|---|")
        for b in batches:
            if isinstance(b, dict):
                tag = b.get("tag") or b.get("batch") or "?"
                msid = b.get("multisim_id") or b.get("id") or "?"
                cfg = b.get("config") or b.get("note") or ""
                lines.append(f"| {tag} | {msid} | {cfg} |")
        lines.append("")

    # 关键结论
    if key_findings:
        lines.append("### 回测结论")
        for kf in key_findings:
            lines.append(f"- {kf}")
        lines.append("")

    # 候选
    if candidates:
        lines.append("### 候选")
        lines.append("| alpha id | variant | sharpe | fitness | tvr | status |")
        lines.append("|---|---|---|---|---|---|")
        for c in candidates:
            if isinstance(c, dict):
                aid = c.get("id") or "?"
                var = c.get("variant") or c.get("code") or ""
                sh = c.get("sharpe") or ""
                fit = c.get("fitness") or c.get("fit") or ""
                tvr = c.get("turnover") or c.get("tvr") or ""
                st = c.get("status") or ""
                lines.append(f"| {aid} | {var} | {sh} | {fit} | {tvr} | {st} |")
        lines.append("")

    # 裁决
    if verdict:
        lines.append(f"### 裁决\n\n{verdict}\n")

    return "\n".join(lines)


def export_ledger_md(region, out_path=None):
    """导出 WAVE_LEDGER.md 快照。"""
    waves = fetch_waves(region)
    if not waves:
        print(f"[WARN] no waves found for region={region}")
        return

    out_path = Path(out_path) if out_path else (ROOT / "tracking" / region / "WAVE_LEDGER.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append(f"# {region} 战役波次台账（WAVE_LEDGER）")
    lines.append("")
    lines.append("> **用途**：每波回测的结论层。每波回收后追加一节；下一波开跑前**必须先读本台账「下一波决策」节**再设计批次。")
    lines.append("> **数据源**：`data/wqb.db` 的 `wave_results` 表（单轨 DB 模式，本文件为快照导出，勿手改）。")
    lines.append("> **机器伴生**：`ledger_kv` 表（判死清单/骨架登记/最佳候选，供门禁去重与脚本消费）。")
    lines.append("> **编号语义**：wave 号为本区域独立递增、仅区域内唯一；跨区域引用/对比必须带区域前缀（如 KOR-w170）。")
    lines.append("> **排序**：按数值波号升序（非字典序，波号 ≥100 后不受字符串排序干扰）。")
    lines.append("")
    lines.append("---")
    lines.append("")

    for w in waves:
        lines.append(render_wave_section(w))
        lines.append("---")
        lines.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] exported {len(waves)} waves to {out_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", required=True)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    export_ledger_md(args.region, args.out)


if __name__ == "__main__":
    main()
