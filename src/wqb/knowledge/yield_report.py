# -*- coding: utf-8 -*-
"""知识版本产出率（2026-11-15 P4）。

回答一个问题：**“换了这套知识（priors + rules）之后，回测产出率有没有变好？”**

按 `attempt_knowledge.knowledge_version` 分组，计算每版的：
- 样本数 / win / near / dead / error；
- 最高 |S|、平均 |S|；
- prod-clean 比例（`prod_correlation < PRODCORR_CEILING`，仅统计**已知**相关性）；
- self-clean 比例（`self_correlation < 0.7`）。

口径提示：`win` 是“全闸 + RA 已知全过”，不是提交率；prod/self 比例的分母只含**已知值**，
`n_prod_known / n_self_known` 一并输出，避免把“没测过”当“干净”。
"""
from __future__ import annotations

import datetime
from collections import defaultdict
from typing import Any, Dict, List, Optional

from wqb.config import GATES_PLATFORM, PRODCORR_CEILING
from wqb.knowledge import config as kcfg


def _max_abs(values) -> float:
    nums = [abs(float(v)) for v in values if isinstance(v, (int, float))]
    return round(max(nums), 4) if nums else 0.0


def _avg_abs(values) -> float:
    nums = [abs(float(v)) for v in values if isinstance(v, (int, float))]
    return round(sum(nums) / len(nums), 4) if nums else 0.0


def _corr_stats(rows, key: str, ceiling: float) -> Dict[str, Any]:
    vals = []
    for r in rows:
        m = r.get("metrics_json") or {}
        v = m.get(key) if isinstance(m, dict) else None
        if isinstance(v, (int, float)):
            vals.append(float(v))
    if not vals:
        return {"n_known": 0, "clean_rate": None}
    clean = sum(1 for v in vals if v < ceiling)
    return {"n_known": len(vals), "clean_rate": round(clean / len(vals), 4)}


def compute_yield(store: Any, region: str) -> Dict[str, Any]:
    """按 knowledge_version 汇总产出率（确定性：不含生成时间戳）。"""
    region = region.upper()
    attempts = store.list_attempt_knowledge(region=region, limit=100000)
    groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for a in attempts:
        groups[str(a.get("knowledge_version") or "na")].append(a)

    versions: List[Dict[str, Any]] = []
    for ver, rows in groups.items():
        n = len(rows)
        mix: Dict[str, int] = {}
        for r in rows:
            k = str(r.get("outcome") or "unknown")
            mix[k] = mix.get(k, 0) + 1
        sharpes = [(r.get("metrics_json") or {}).get("sharpe") for r in rows
                   if isinstance(r.get("metrics_json"), dict)]
        created = [str(r.get("created_at")) for r in rows if r.get("created_at")]
        versions.append({
            "knowledge_version": ver,
            "n": n,
            "n_win": mix.get("win", 0),
            "n_near": mix.get("near", 0),
            "n_dead": mix.get("dead", 0),
            "n_error": mix.get("error", 0),
            "n_unknown": mix.get("unknown", 0),
            "win_rate": round(mix.get("win", 0) / n, 4) if n else 0.0,
            "near_rate": round(mix.get("near", 0) / n, 4) if n else 0.0,
            "dead_rate": round(mix.get("dead", 0) / n, 4) if n else 0.0,
            "max_abs_sharpe": _max_abs(sharpes),
            "avg_abs_sharpe": _avg_abs(sharpes),
            "prod": _corr_stats(rows, "prod_correlation", float(PRODCORR_CEILING)),
            "self": _corr_stats(rows, "self_correlation",
                                float(GATES_PLATFORM.get("self_corr_max", 0.7))),
            "first_at": min(created) if created else None,
            "last_at": max(created) if created else None,
        })
    versions.sort(key=lambda x: (x.get("last_at") or "", x["knowledge_version"]), reverse=True)
    latest = versions[0] if versions else None
    previous = versions[1] if len(versions) > 1 else None
    delta = None
    if latest and previous:
        delta = {
            "win_rate": round(latest["win_rate"] - previous["win_rate"], 4),
            "near_rate": round(latest["near_rate"] - previous["near_rate"], 4),
            "dead_rate": round(latest["dead_rate"] - previous["dead_rate"], 4),
            "max_abs_sharpe": round(latest["max_abs_sharpe"] - previous["max_abs_sharpe"], 4),
        }
    return {
        "region": region,
        "sample_size": len(attempts),
        "versions": versions,
        "latest": latest,
        "previous": previous,
        "delta": delta,
    }


def _fmt_rate(v: Optional[float]) -> str:
    return "-" if v is None else f"{v:.1%}"


def render_yield_markdown(report: Dict[str, Any]) -> str:
    region = report.get("region")
    lines = [
        f"# {region} 经验知识版本产出率（自动生成）",
        "",
        f"- 样本：{report.get('sample_size')} 条 `attempt_knowledge`",
        f"- 知识版本数：{len(report.get('versions') or [])}",
        "- 口径：`win` = 全闸 + RA **已知**全过；prod/self clean 率的分母只含已知相关性；不是提交率。",
        "",
        "## 按 knowledge_version",
        "",
        "| knowledge_version | n | win | near | dead | error | 最高\\|S\\| | 平均\\|S\\| | prod clean | self clean |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for v in report.get("versions") or []:
        prod = v.get("prod") or {}
        self_ = v.get("self") or {}
        prod_txt = (f"{_fmt_rate(prod.get('clean_rate'))} (n={prod.get('n_known')})"
                    if prod.get("n_known") else "-")
        self_txt = (f"{_fmt_rate(self_.get('clean_rate'))} (n={self_.get('n_known')})"
                    if self_.get("n_known") else "-")
        lines.append(
            f"| `{v['knowledge_version']}` | {v['n']} | {v['n_win']} | {v['n_near']} | "
            f"{v['n_dead']} | {v['n_error']} | {v['max_abs_sharpe']:.2f} | "
            f"{v['avg_abs_sharpe']:.2f} | {prod_txt} | {self_txt} |")
    d = report.get("delta")
    if d:
        lines += [
            "",
            "## 最新版 vs 上一版",
            "",
            f"- win_rate {d['win_rate']:+.1%} / near_rate {d['near_rate']:+.1%} / "
            f"dead_rate {d['dead_rate']:+.1%} / 最高\\|S\\| {d['max_abs_sharpe']:+.2f}",
            "",
            "> 注意：版本间样本的数据集/设置构成可能不同，这是**观察值**，不是因果结论；"
            "样本 < 30 时不要据此判定知识好坏。",
        ]
    lines.append("")
    return "\n".join(lines)


def write_yield_report(store: Any, region: str, out_dir: str) -> Dict[str, Any]:
    """写 `output_report/experience_yield_<region>_<YYYYMMDD>.md` + ledger 快照。"""
    import os

    report = compute_yield(store, region)
    generated_at = datetime.datetime.now().isoformat(timespec="seconds")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(
        out_dir, f"experience_yield_{region.lower()}_{datetime.date.today():%Y%m%d}.md")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(render_yield_markdown(report))
    store.upsert_ledger(region, f"experience_yield_{region.upper()}", {
        **report,
        "generated_at": generated_at,
        "report_path": path,
        "min_sample_note": f"样本<{kcfg.MIN_FAMILY_N} 的版本只作记录",
    })
    return {"report": report, "path": path, "generated_at": generated_at}
