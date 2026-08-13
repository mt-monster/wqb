#!/usr/bin/env python3
"""从 shared_libs/operators_catalog.py 同步再生算子分类 (2026-08-13).

单一事实源: `~/.zcode/skills/shared_libs/operators_catalog.py` (8-11 平台 get_operators 拉取, 102 算子).
修复了 2026-08-05 快照的 bug: 把 41 个真算子 (abs/divide/ts_rank/hump/group_neutralize 等) 误标为 ghost。

产出:
  - data/operators_verified.json   (audit CLI 读取的运行时数据)
  - src/wqb/operators/verified.py  VERIFIED_OPERATORS = catalog 102
  - src/wqb/operators/ghost.py     GHOST_OPERATORS    = 幻觉基线 28 (不在 catalog)
  - src/wqb/operators/known_ghosts.py  KNOWN_GHOSTS    = 17 (高频误用幻觉)

平台目录更新后重跑: python tools/sync_operators_from_catalog.py
并同步更新 src/wqb/config.py 的 GHOST_OPERATORS / VERIFIED_SAFE_OPERATORS / OP_FAMILIES。
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS = Path.home() / ".zcode" / "skills" / "shared_libs"
if str(SKILLS) not in sys.path:
    sys.path.insert(0, str(SKILLS))

from operators_catalog import BY_NAME  # noqa: E402

# 幻觉基线: 旧库中确认不在平台目录的算子 (2026-08-05 分类后重新核对)
GHOST_BASELINE = sorted([
    "group_max", "group_median", "group_min", "group_normalize", "group_percentage",
    "group_vector_proj", "jump_decay", "nan_mask", "neutralize", "rank_by_side",
    "s_log_1p", "sigmoid", "tanh", "ts_co_kurtosis", "ts_co_skewness",
    "ts_decay_exp_window", "ts_delta_limit", "ts_entropy", "ts_max", "ts_median",
    "ts_min", "ts_min_max_cps", "ts_min_max_diff", "ts_partial_corr", "ts_percentage",
    "ts_skewness", "vec_choose", "vec_norm",
])
KNOWN_GHOST_BASELINE = sorted([
    "group_median", "group_normalize", "group_percentage", "group_vector_proj",
    "s_log_1p", "sigmoid", "tanh", "ts_co_kurtosis", "ts_decay_exp_window",
    "ts_delta_limit", "ts_entropy", "ts_median", "ts_min_max_cps", "ts_min_max_diff",
    "ts_partial_corr", "ts_percentage", "ts_skewness",
])


def fmt_list(name: str, items, per: int = 8) -> str:
    lines = [f"{name} = ["]
    for i, n in enumerate(items):
        lines.append(f'    "{n}",' + ("\n" if (i + 1) % per == 0 else " "))
    return "\n".join(lines).rstrip() + "\n]\n"


def main() -> int:
    verified = sorted(BY_NAME.keys())
    ghost = [g for g in GHOST_BASELINE if g not in verified]
    known = [g for g in KNOWN_GHOST_BASELINE if g in ghost]
    ts = datetime.now(timezone.utc).isoformat()
    summary = {
        "total_catalog": len(verified), "total_verified": len(verified),
        "total_ghost": len(ghost), "total_known_ghosts": len(known), "total_missing": 0,
    }
    header = (f"# AUTO-GENERATED from shared_libs/operators_catalog.py (platform pull 2026-08-11) — "
              f"do not edit by hand.\n# Regenerated: {ts}\n# Source summary: {summary}\n\n")

    (REPO / "data").mkdir(exist_ok=True)
    (REPO / "data" / "operators_verified.json").write_text(json.dumps(
        {"verified": verified, "ghost": ghost, "missing": [], "known_ghosts": known,
         "summary": summary, "timestamp": ts}, ensure_ascii=False, indent=2), encoding="utf-8")

    ops = REPO / "src" / "wqb" / "operators"
    (ops / "verified.py").write_text(
        header + '"""Operators verified live on the WQ BRAIN platform (catalog 全量)."""\n\n'
        + fmt_list("VERIFIED_OPERATORS", verified), encoding="utf-8")
    (ops / "ghost.py").write_text(
        header + '"""Ghost operators: 不在平台算子目录中 (LLM 幻觉/别名), 解析器接受但禁止使用。"""\n\n'
        + fmt_list("GHOST_OPERATORS", ghost), encoding="utf-8")
    (ops / "known_ghosts.py").write_text(
        header + '"""Subset of GHOST_OPERATORS known to be mis-used / frequently mistaken for real ops."""\n\n'
        + fmt_list("KNOWN_GHOSTS", known), encoding="utf-8")
    print(f"synced: verified={len(verified)} ghost={len(ghost)} known_ghosts={len(known)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
