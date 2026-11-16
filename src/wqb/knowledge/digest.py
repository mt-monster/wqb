# -*- coding: utf-8 -*-
"""区域经验摘要（`tracking/<REGION>/priors/experience_digest.md`，2026-11-15 P4）。

给人/Agent 的一页纸：有效骨架、统计死路（advisory）、待确认提案、最新知识版本产出率。
机器段在 `BEGIN/END` 标记内可重复刷新；标记外的人工笔记保留。
"""
from __future__ import annotations

import datetime
import os
from typing import Any, Dict, Optional

from wqb.knowledge.distill import distill_region
from wqb.knowledge.config import PROMOTE_MIN_CONFIRMATIONS
from wqb.knowledge.yield_report import compute_yield

BEGIN = "<!-- BEGIN WQB EXPERIENCE DIGEST -->"
END = "<!-- END WQB EXPERIENCE DIGEST -->"


def _table(groups, name_key: str) -> list:
    lines = ["| 名称 | n | win | near | 最高\\|S\\| | 主墙 | 占比 |",
             "|---|---:|---:|---:|---:|---|---:|"]
    for g in groups:
        name = g.get(name_key)
        if not name:
            continue
        share = g.get("dominant_wall_share")
        share_txt = f"{share:.0%}" if isinstance(share, (int, float)) else "-"
        lines.append(
            f"| `{name}` | {g.get('n')} | {g.get('n_win')} | {g.get('n_near')} | "
            f"{g.get('max_sharpe')} | {g.get('dominant_wall') or '-'} | {share_txt} |")
    return lines


def render_digest(store: Any, region: str) -> str:
    region = region.upper()
    stats = distill_region(store, region)
    proposals = store.get_ledger(region, f"experience_proposals_{region}") or {}
    yield_report = compute_yield(store, region)
    prop = (proposals.get("proposals") if isinstance(proposals, dict) else {}) or {}

    eff = [g for g in (stats.get("skeleton_stats") or [])
           if (g.get("n_win") or 0) + (g.get("n_near") or 0) > 0]
    dead = [g for g in (stats.get("skeleton_stats") or []) if g.get("dead")]
    eff.sort(key=lambda g: (-(g.get("n_win") or 0), -(g.get("n_near") or 0), -(g.get("n") or 0)))
    dead.sort(key=lambda g: (-(g.get("n") or 0), g.get("max_sharpe") or 0))

    lines = [
        BEGIN,
        f"# {region} 经验摘要（自动生成）",
        "",
        f"- generated_at: {datetime.datetime.now().isoformat(timespec='seconds')}",
        f"- 样本：{stats.get('sample_size')} 条 `attempt_knowledge`",
        f"- 知识版本（top3）：" +
        ", ".join(f"`{k}` n={v}" for k, v in
                  list((stats.get("knowledge_versions") or {}).items())[:3]),
        "",
        "## 有效骨架（win+near，top 10）",
        "",
    ]
    lines += _table(eff[:10], "skeleton") if eff else ["（暂无：需要至少一条 win/near）"]
    lines += ["", "## 统计死路（advisory，不是硬禁；top 10）", ""]
    lines += _table(dead[:10], "skeleton") if dead else ["（暂无）"]
    lines += [
        "",
        "## 待确认提案",
        "",
        f"- dead_families: {len(prop.get('dead_families') or [])}",
        f"- dead_skeletons: {len(prop.get('dead_skeletons') or [])}",
        f"- wins: {len(prop.get('wins') or [])}",
        f"- rules: {len(prop.get('rules') or [])}（proposed 不生效；满 "
        f"{PROMOTE_MIN_CONFIRMATIONS} 个独立波次确认后才转 active）",
        "",
        "## 最新知识版本产出率",
        "",
    ]
    latest = yield_report.get("latest")
    if latest:
        lines += [
            f"- knowledge_version: `{latest['knowledge_version']}` (n={latest['n']})",
            f"- win {latest['win_rate']:.1%} / near {latest['near_rate']:.1%} / "
            f"dead {latest['dead_rate']:.1%} / 最高|S| {latest['max_abs_sharpe']:.2f}",
        ]
        d = yield_report.get("delta")
        if d:
            lines.append(f"- vs 上一版：win {d['win_rate']:+.1%} / near {d['near_rate']:+.1%} / "
                         f"dead {d['dead_rate']:+.1%}")
    else:
        lines.append("（暂无知识版本样本）")
    lines += [
        "",
        "> 判死仍走 `forum_recon` + `seal_dead_end`；本摘要只提供统计与提案，不自动封存。",
        END,
    ]
    return "\n".join(lines) + "\n"


def write_digest(path: str, content: str) -> None:
    """写机器段；保留标记外的人工笔记（文件不存在则整写）。"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    prefix = suffix = ""
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                old = f.read()
            if BEGIN in old and END in old:
                prefix = old.split(BEGIN, 1)[0]
                suffix = old.split(END, 1)[1]
        except OSError:
            pass
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(prefix + content + suffix)


def write_region_digest(store: Any, region: str, path: str) -> Dict[str, Any]:
    content = render_digest(store, region)
    write_digest(path, content)
    return {"path": path, "region": region.upper(),
            "generated_at": datetime.datetime.now().isoformat(timespec="seconds")}
