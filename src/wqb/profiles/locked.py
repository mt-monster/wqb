# -*- coding: utf-8 -*-
"""锁定表：任何层（类别卡 / 区域 / 区域 × 类别组合 / 学习层）都不能放宽的纪律（2026-10-04）。

冲突裁决（高 → 低）：用户显式指令（waiver；`wqb.waiver.RED_LINES` 除外）> **锁定表** > 代码 fail-closed 闸
> 组合（cells.json）> 区域（settings / thresholds / profile）> 类别卡 > 全局缺省。

数值类锁只给方向（min_only = 只许往上收；max_only = 只许往下收），具体数值读各自的单一来源
（Mode B 下限 = `mode_b_config` 的 `_floor`；平台线 = `config.PLATFORM_CHECK_LINES`），这里不抄数字。
"""
from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

LOCKED: List[Dict[str, object]] = [
    {"id": "mixed_signal_ban", "kind": "rule", "steps": ["S2", "S4"],
     "text": "两条独立信号腿不得相加（加权 / 等权 / add / 中缀 +）；第二个数据集只以条件 / 分组 / 残差入场",
     "source": "CLAUDE.md「禁止混信号调参」；methodology_rules mixed_signal_leg_ban_v1；gate.py 闸 5"},
    {"id": "mode_b_floor", "kind": "min_only", "keys": ["mode_b.sharpe_min", "mode_b.fitness_min"], "steps": ["S4"],
     "text": "Mode B 主闸只许收紧，下限 = GLOBAL 台账主闸（缺省内置值）；更低的覆盖读时钳回",
     "source": "src/wqb/workflow/mode_b_config.py（_floor / _clamped_from）"},
    {"id": "d0p_fixed", "kind": "immutable", "prefixes": ["d0p."], "steps": ["S3", "S4"],
     "text": "prod 墙处置阈值（决策表 D0-P）不接受区域 / 类别 / 组合改写",
     "source": "wq-brain-ra-pipeline SKILL.md「冲突裁决」"},
    {"id": "platform_lines", "kind": "bound", "steps": ["S4", "S5"],
     "text": "组合阈值覆盖不得比平台线更松（review.sharpe_min 不低于 LOW_SHARPE 线；换手区间不出平台范围）",
     "source": "config.PLATFORM_CHECK_LINES"},
    {"id": "user_confirm_submit", "kind": "rule", "steps": ["S5"],
     "text": "提交前必须用户明确确认；本层只出画像，不产生任何提交动作",
     "source": "wqb.waiver.RED_LINES"},
    {"id": "window_whitelist", "kind": "rule", "steps": ["S2"],
     "text": "卡片 / 组合里的窗口只用 STANDARD_WINDOWS；别的窗口必须带解释与实测证据",
     "source": "CLAUDE.md；config.STANDARD_WINDOWS"},
    {"id": "lit_tower_platform_category", "kind": "rule", "steps": ["S0"],
     "text": "点塔 / 剔已亮塔一律按平台类别；机制类别不同不能把已亮塔的数据集放回主数据集",
     "source": "用户 2026-09-19 定案（已亮塔只作组腿辅助）"},
    {"id": "no_truncation_scan", "kind": "forbid", "keys": ["mode_a.scan.truncation"], "steps": ["S4"],
     "text": "truncation 不作 Mode A 扫描维度（IND / GLB 实测零杠杆）",
     "source": "决策表 D5；optimization-v1 Mode A 扫描维度纪律"},
]

#: 生成侧全局禁止（每个类别都适用；类别卡里只写类别特有的禁止项）
GLOBAL_FORBIDDEN: List[str] = [
    "禁止两条独立信号腿相加：加权（0.4×A + 0.6×B）、等权 add(rank(A), rank(B))、中缀 + 都算；第二个数据集只以条件（trade_when / if_else）、分组（group_rank / bucket）或残差（regression_neut / vector_neut）入场",
    "禁止 ts_event_* 系列（平台没有）与幽灵算子；字段名逐一经 get_datafields 验证",
]

#: 「推荐了加权混合」的文本特征（只扫推荐类字段：原语、杠杆、骨架；禁止项里提到它不算）
_WEIGHTED_MIX = re.compile(
    r"(?:\b0\.\d+\s*[*×x]\s*(?:rank|group_rank|ts_|zscore)\b)"
    r"|(?:add\(\s*multiply\()"
    r"|(?:multiply\(\s*-?(?:rank|group_rank|ts_\w+|zscore)\((?:[^()]|\((?:[^()]|\([^()]*\))*\))*\)\s*,\s*0?\.\d+\s*\))"
    r"|(?:0\.\d+\s*/\s*0\.\d+\s*(?:加权|权重))"
    r"|(?:add\(\s*rank\([^()]*\)\s*,\s*rank\()",
    re.I)


def recommends_weighted_mix(text: str) -> bool:
    return bool(_WEIGHTED_MIX.search(text or ""))


_TS_WINDOW = re.compile(r"\b(?:ts_[a-z_]+|hump|days_from_last_change)\(([^()]*(?:\([^()]*\)[^()]*)*)\)")


def nonstandard_windows(expr: str) -> List[int]:
    """表达式里 ts_* 的窗口参数（最后一个整数实参）不在 STANDARD_WINDOWS 的值。"""
    from wqb.config import STANDARD_WINDOWS
    bad: List[int] = []
    for m in _TS_WINDOW.finditer(expr or ""):
        args = [a.strip() for a in m.group(1).split(",")]
        for a in reversed(args):
            if re.fullmatch(r"\d+", a):
                n = int(a)
                if n not in STANDARD_WINDOWS and n not in bad:
                    bad.append(n)
                break
    return bad


def platform_bounds() -> Dict[str, Tuple[str, float]]:
    """组合阈值覆盖的平台边界：key → (方向, 边界值)。方向 min = 覆盖值不得低于边界；max = 不得高于。"""
    from wqb.config import PLATFORM_CHECK_LINES as P
    lo, hi = P["turnover_range"]
    return {
        "review.sharpe_min": ("min", float(P["low_sharpe_min"]["delay1"])),
        "review.turnover_max": ("max", float(hi)),
        "review.turnover_min": ("min", float(lo)),
    }


def check_threshold_override(key: str, value: object) -> Optional[str]:
    """组合阈值覆盖是否越过锁；越过返回原因，合法返回 None。"""
    if any(key.startswith(p) for lk in LOCKED if lk["kind"] == "immutable" for p in lk.get("prefixes", [])):
        return f"{key} 属锁定项（不可覆盖）"
    b = platform_bounds().get(key)
    if b is None:
        return None
    try:
        v = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return f"{key}={value!r} 不是数值"
    direction, bound = b
    if direction == "min" and v < bound:
        return f"{key}={v} 比平台线 {bound} 更松"
    if direction == "max" and v > bound:
        return f"{key}={v} 超出平台范围上限 {bound}"
    return None
