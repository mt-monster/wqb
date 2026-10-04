# -*- coding: utf-8 -*-
"""区域 × 类别拆分的类别口径（2026-10-04）。

代码里有三种「类别」，本模块只管前两种，第三种不是信号类别：

1. **平台类别**（`datasets.category`，小写归一）——点塔、S0 的 `category_weights`、剔已亮塔都按它；
   组合（cell）的键也用它，保证「组合」与「塔」一一对应。
2. **类别卡**（cross-region 的生成 / 改进知识）——平台类别多数各有一张卡；没有独立卡的并到最近的卡
   （`imbalance → pv`、`socialmedia → sentiment`、`macro / equity / event / broker → other`）。
3. 算子家族（`config.OP_FAMILIES`）是表达式词汇，不是信号类别；区域差异体现在算子效应量
   （`quantile` / market 轴「禁外推」）与可用性（JPN 无 industry / sector 分组），记在组合证据里。

「Pattern」不是平台类别：`pattern_scores` / `continuation_score` 平台记 PV，`chart_cnn_alpha`
在不同区记成 PV / MODEL，所以 Pattern 是 pv / model 下的族标签（见 `FAMILY_TAGS`）。
"""
from __future__ import annotations

import os
from typing import Dict, List, Optional

#: 平台类别 → 类别卡 id（卡 id 本身也是平台类别）。并入关系只在这里写。
CARD_OF: Dict[str, str] = {
    "model": "model",
    "pv": "pv",
    "imbalance": "pv",
    "analyst": "analyst",
    "earnings": "earnings",
    "fundamental": "fundamental",
    "news": "news",
    "sentiment": "sentiment",
    "socialmedia": "sentiment",
    "insiders": "insiders",
    "institutions": "institutions",
    "shortinterest": "shortinterest",
    "risk": "risk",
    "option": "option",
    "macro": "other",
    "equity": "other",
    "event": "other",
    "broker": "other",
    "other": "other",
    "unknown": "other",
}

#: 展示用分组（用户口径的 9 组 + 补齐）。只用于汇总与目录，不参与解析。
GROUPS: Dict[str, List[str]] = {
    "MODEL": ["model"],
    "PV": ["pv", "imbalance"],
    "Analyst": ["analyst"],
    "Earnings": ["earnings"],
    "Fundamental": ["fundamental"],
    "News-Sentiment": ["news", "sentiment", "socialmedia"],
    "Insider": ["insiders"],
    "Institutions": ["institutions"],
    "ShortInterest": ["shortinterest"],
    "Risk": ["risk"],
    "Option": ["option"],
    "Other": ["other", "macro", "equity", "event", "broker", "unknown"],
}

#: 族标签（不是平台类别）：跨平台类别的信号族，挂在类别卡下面。
FAMILY_TAGS: Dict[str, Dict[str, object]] = {
    "pattern": {
        "categories": ["pv", "model"],
        "datasets": ["pattern_scores", "continuation_score", "chart_cnn_alpha"],
        "note": "图表形态族。平台类别是 PV（pattern_scores / continuation_score）或 MODEL（chart_cnn_alpha，"
                "各区记法不一），按所在平台类别进组合；KOR 三连死（chart_cnn 1.51 → continuation 0.34 → "
                "pattern_scores 0.49），GBR / DEU 亦判死。",
    },
}

#: 字段 / 数据集前缀缩写 → 平台类别（判死条目常用缩写写数据集，如 FND93 / ANL39 / RSK70）
_ABBREV: Dict[str, str] = {
    "fnd": "fundamental", "anl": "analyst", "mdl": "model", "oth": "other", "rsk": "risk",
    "nws": "news", "ern": "earnings", "snt": "sentiment", "scl": "socialmedia",
    "shrt": "shortinterest", "si": "shortinterest", "insd": "insiders", "inst": "institutions",
    "opt": "option", "imb": "imbalance", "mcr": "macro", "ipv": "pv",
}


def normalize_category(raw: Optional[object]) -> str:
    """平台类别小写归一；空 / None → ``unknown``。dict 形态（平台原始 `{"id": ...}`）取 id。"""
    if isinstance(raw, dict):
        raw = raw.get("id") or raw.get("name")
    s = str(raw or "").strip().lower()
    return s or "unknown"


def card_of(category: Optional[object]) -> str:
    """平台类别 → 类别卡 id（未登记的类别并入 other）。"""
    return CARD_OF.get(normalize_category(category), "other")


def group_of(category: Optional[object]) -> str:
    c = normalize_category(category)
    for g, members in GROUPS.items():
        if c in members:
            return g
    return "Other"


def category_from_prefix(dataset: str) -> Optional[str]:
    """数据集名前缀推断（仅作兜底，平台类别优先）。"""
    from wqb.workflow._common import _PREFIX_CATEGORY  # 单一前缀表，不在这里另写一份
    low = (dataset or "").lower()
    for key, value in _PREFIX_CATEGORY:
        if key in low:
            return value
    for abbr, cat in sorted(_ABBREV.items(), key=lambda kv: -len(kv[0])):
        if low.startswith(abbr) and low[len(abbr):len(abbr) + 1].isdigit():
            return cat
    return None


def expand_abbrev(token: str) -> Optional[str]:
    """`FND93` → `fundamental93`；`PV106` → `pv106`；认不出返回 None。"""
    low = (token or "").lower()
    for abbr, cat in sorted(_ABBREV.items(), key=lambda kv: -len(kv[0])):
        if low.startswith(abbr) and low[len(abbr):].isdigit():
            return cat + low[len(abbr):]
    return None


def dataset_category(region: str, dataset: str, db: Optional[str] = None) -> str:
    """数据集在本区的平台类别（只读查 `datasets` 表；本区无记录 → 任一区非空记录 → 前缀推断 → other）。"""
    if not dataset:
        return "unknown"
    try:
        from wqb.db_conn import connect, default_db_path
        path = db or default_db_path()
        if os.path.isfile(path):
            conn = connect(path, readonly=True, timeout=5.0)
            try:
                row = conn.execute(
                    "SELECT d.category FROM datasets d JOIN regions g ON g.id = d.region_id "
                    "WHERE g.name = ? AND d.name = ? AND d.category IS NOT NULL AND d.category != '' "
                    "ORDER BY d.id DESC LIMIT 1", (region.upper(), dataset)).fetchone()
                if not row:
                    row = conn.execute(
                        "SELECT category FROM datasets WHERE name = ? AND category IS NOT NULL "
                        "AND category != '' ORDER BY id DESC LIMIT 1", (dataset,)).fetchone()
                if row:
                    return normalize_category(row[0])
            finally:
                conn.close()
    except Exception:  # noqa: BLE001 — 类别查询失败只降级到前缀推断
        pass
    return normalize_category(category_from_prefix(dataset) or "other")
